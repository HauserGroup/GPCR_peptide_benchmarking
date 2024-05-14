import pandas as pd
import requests 
import ast
import os

def get_sequence_from_pdb_fasta(pdb_id, chain_id):
    '''
    Helper function to get a fasta sequence from RCSB PDB using the PDB identifier and the chain ID
    '''
    from Bio import SeqIO
    import requests
    from io import StringIO

    # Link to the fasta file on RCSB PDB
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}/display"
    fasta = requests.get(url).text

    # If chain_id is not provided, return None
    if chain_id.strip() == "":
        print(f"Chain ID not provided for PDB {pdb_id}.")
        return None

    # Return the requested sequence - try first the author chain ID, then the PDB chain ID
    fasta_iterator = SeqIO.parse(StringIO(fasta), "fasta")
    for seq in fasta_iterator:
        if f"[auth {chain_id}]" in seq.description:
            return str(seq.seq)

    fasta_iterator = SeqIO.parse(StringIO(fasta), "fasta")
    for seq in fasta_iterator:
        if f"Chain {chain_id}" in seq.description:
            return str(seq.seq)

    # If the sequence is not found, return None
    return None

def download_pdb(pdb_id, output_folder, overwrite = False):
    '''
    Function to download PDB files using the RCSB PDB API given a PDB identifier 
    and output folder name. If the PDB file already exists in the output folder,
    the function will not download it again unless overwrite is set to True.
    Returns the path of the downloaded PDB file.
    '''

    # Check if the PDB file already exists in the output folder
    if os.path.exists(f"{output_folder}/{pdb_id}.pdb") and not overwrite:
        print(f"PDB file {pdb_id}.pdb already exists in the output folder.")
        return f"{output_folder}/{pdb_id}.pdb"

    # Make sure output folder exists and create it if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # URL for the PDB file
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    # Send an HTTP GET request to the PDB URL
    response = requests.get(pdb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(f"{output_folder}/{pdb_id}.pdb", "wb") as pdb_file:
            pdb_file.write(response.content)
        print(f"PDB file {pdb_id}.pdb downloaded successfully.")
        return f"{output_folder}/{pdb_id}.pdb"
    else:
        print(f"Failed to download PDB file {pdb_id}. Status code: {response.status_code}")
        return ""

def sequence_similarity(seq1, seq2):
    from Bio import pairwise2
    """Calculate the sequence similarity by finding the best alignment and considering the number of identical matches."""
    alignments = pairwise2.align.globalxx(seq1, seq2)
    # Best alignment is taken as the first alignment returned by Biopython, which has the highest score
    best_alignment = alignments[0]
    max_length = max(len(seq1), len(seq2))
    similarity = best_alignment.score / max_length
    return similarity

def get_receptor_sequence(uniprot_id):
    '''
    Function to get fasta sequence of the receptor without its signal peptide using UniProt API.
    Returns the fasta sequence and the description of the entry given a UniProt ID.
    '''

    # Get features of the receptor from UniProt
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.json"   
    response = requests.get(url)

    if response.status_code == 200:

        # Parse the JSON response
        data = response.json()

        try:
            # Get the full sequence
            sequence = data["sequence"]["value"]
        except KeyError:
            return None, None

        try:
            # Extract feature information
            features = data["features"]
        except KeyError:
            return None, None

        # Get the start and end positions of the chain and signal peptide
        for feature in features:
            if feature["type"] == "Chain":
                chain_start = feature["location"]["start"]["value"]
                chain_end = feature["location"]["end"]["value"]
                return feature["description"], sequence[chain_start-1:chain_end]
    else:
        print(f"Error: Unable to retrieve data from UniProt using ID {uniprot_id}. Status code {response.status_code}")
        return None, None
    
def get_receptor_list(receptors = []):
    """
    Helper function to get a list of GPCRdb receptors with their UniProt accession numbers.
    """
    # Add UniProt accession numbers of the receptors to the dataframe
    response = requests.get("https://gpcrdb.org/services/receptorlist/")
    receptor_list = response.json()
    receptor_list = pd.DataFrame.from_dict(receptor_list)
    if len(receptors) != 0:
        receptor_list = receptor_list[receptor_list["entry_name"].isin(receptors)]
    receptor_list = receptor_list[["entry_name", "accession"]]
    receptor_list.columns = ["protein", "accession"]
    receptor_list.reset_index(inplace=True, drop=True)
    return receptor_list

def get_peptide_ligands(pdb_codes = []):
    """
    Helper function to get a dataframe of peptide ligands with PDB structures from GPCRdb
    """

    # Get peptide ligands for the pdb files that have been found
    response = requests.get("https://gpcrdb.org/services/ligands/peptides/")
    peptide_ligands = response.json()
    peptide_ligands = pd.DataFrame.from_dict(peptide_ligands)
    if len(pdb_codes) != 0:
        peptide_ligands = peptide_ligands[peptide_ligands["PDB"].isin(pdb_codes)]
    peptide_ligands.drop(columns=["Sequence length", "Family", "GPCR Class"], inplace=True)
    peptide_ligands.columns = ["name", "sequence", "pdb_code", "chain", "protein"]

    return peptide_ligands

def get_structure_list(species = "Homo sapiens"):
    """
    Helper function to get a list of PDB structures from GPCRdb
    """
    # Get structure information from GPCRdb for the pdb files included
    response = requests.get('https://gpcrdb.org/services/structure/')
    structures = response.json()
    structures = [structure for structure in structures if structure["species"] == species]
    return structures

def parse_dataset(filepath):
    # Get receptors that have peptide complexes with more recent structures
    filepath = "3f_known_structures_summary_2021-09-30.csv"
    df = pd.read_csv(filepath)
    df = df[df["has_peptide_complex_before_cutoff"] == False]
    df = df[df["has_peptide_complex"] == True]

    # Get the pdb codes for each receptor and make a dictionary
    pdbs = {}
    for i, row in df.iterrows():
        pdb_codes = ast.literal_eval(row["Peptide complex PDBs after"])
        pdb_codes = [x[0] for x in pdb_codes]
        pdbs[row["Target GPCRdb ID"]] = pdb_codes

    # Make a dataframe from dict and make multiple rows for each key if there are multiple values
    pdb_code_df = pd.DataFrame.from_dict(pdbs, orient="index")
    pdb_code_df = pdb_code_df.stack().reset_index()
    pdb_code_df = pdb_code_df.drop(columns=["level_1"])
    pdb_code_df.columns = ["Target GPCRdb ID", "PDB code"]
    pdb_code_df = pdb_code_df.merge(df[["Target GPCRdb ID", "family"]], on="Target GPCRdb ID", how="left")

    # Get unique pdb codes
    pdb_codes = pdb_code_df["PDB code"].unique()

    # Get peptide ligands and list of structures from GPCRdb
    peptide_ligands = get_peptide_ligands(pdb_codes)
    structures = get_structure_list()

    # Filter out the structures whose ligand is not a peptide
    receptors = []
    for structure in structures:
        for ligand in structure["ligands"]:
            if ligand["type"] in ["peptide", "protein"] and structure["pdb_code"] in pdb_codes:
                keys = [k for k in structure.keys() if k not in ["ligands", "signalling_protein"]]
                line = [structure[k] for k in keys]
                line.extend([ligand["name"], ligand["function"]])
                receptors.append(line)

    # Create a dataframe from the list of peptide receptors and set column names
    keys.extend(["name", "function"])
    receptors = pd.DataFrame(receptors)
    receptors.columns = keys

    # Merge peptide_ligands and receptors dataframes
    benchmark_set = pd.merge(receptors, peptide_ligands, on = ["pdb_code", "protein", "name"], how="left")
    benchmark_set.rename(
        columns={
            'preferred_chain': 'receptor_chain',
            'sequence': 'peptide_sequence'
        }, inplace=True
    )

    # Get the UniProt accession numbers of the receptors from GPCRdb
    receptor_list = get_receptor_list(receptors["protein"].unique())

    # Merge with receptors dataframe to add UniProt accession numbers
    benchmark_set = pd.merge(benchmark_set, receptor_list, on = ["protein"], how="left")

    # Rename accession column to uniprot_id, and sort by protein and name
    benchmark_set = benchmark_set.rename(columns={"accession": "receptor_uniprot_id"})
    benchmark_set = benchmark_set.sort_values(by=["protein", "name"])
    benchmark_set.reset_index(drop=True, inplace=True)
    benchmark_set = benchmark_set.rename(columns={"chain": "ligand_chain"})
    benchmark_set.drop(columns=["family"], inplace=True)

    # Merge pdb_code_df with benchmark_set
    pdb_code_df.rename(columns={"PDB code": "pdb_code"}, inplace=True)
    benchmark_set = benchmark_set.merge(pdb_code_df, on="pdb_code")
    benchmark_set["receptor_pdb_seq"] = None
    benchmark_set["ligand_pdb_seq"] = None

    # Manual fixes to the ligand chains – unannotated on GPCRdb
    benchmark_set.loc[benchmark_set['pdb_code'] == '7XMS', 'ligand_chain'] = 'L'
    benchmark_set.loc[benchmark_set['pdb_code'] == '8HCQ', 'ligand_chain'] = 'L'
    benchmark_set.loc[benchmark_set['pdb_code'] == '8IC0', 'ligand_chain'] = 'F'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7XJK', 'ligand_chain'] = 'A'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7T10', 'ligand_chain'] = 'P'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7WIC', 'ligand_chain'] = 'L'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7XAT', 'ligand_chain'] = 'F'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7XMR', 'ligand_chain'] = 'L'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7Y27', 'ligand_chain'] = 'C'
    benchmark_set.loc[benchmark_set['pdb_code'] == '7WJ5', 'ligand_chain'] = 'S'

    # Get the amino acid sequences from PDB files
    for index, row in benchmark_set.iterrows():
        receptor_pdb_seq = get_sequence_from_pdb_fasta(row["pdb_code"], row["receptor_chain"])
        ligand_pdb_seq = get_sequence_from_pdb_fasta(row["pdb_code"], row["ligand_chain"])
        benchmark_set.at[index, "receptor_pdb_seq"] = receptor_pdb_seq
        benchmark_set.at[index, "ligand_pdb_seq"] = ligand_pdb_seq

    # Reorder and drop unnecessary columns
    col_order = {
        'pdb_code': 'pdb',
        'protein': 'receptor', 
        'receptor_uniprot_id': 'uniprot_id',
        'class': 'class',
        'family': 'family',
        'resolution': 'resolution',
        'type': 'type',
        'state': 'state',
        'name': 'ligand_name',
        'ligand_chain': 'ligand_chain',
        'ligand_pdb_seq': 'ligand_pdb_seq',
        'receptor_chain': 'receptor_chain',
        'receptor_pdb_seq': 'receptor_pdb_seq',
        'publication': 'publication', 
        'publication_date': 'publication_date',
    }
    benchmark_set = benchmark_set[col_order.keys()]
    benchmark_set = benchmark_set.rename(columns=col_order)
    benchmark_set = benchmark_set[col_order.values()]

    # Drop the following PDB codes:
    # - 7XBX has ligand and receptor in the same chain.
    # - 8I2G has two ligands in one complex.
    # - 7X0X has been marked obsolete
    # - 7VUZ, 7VUY, and 7VV3: ligand chain missing
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "7XBX"]
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "8I2G"]
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "7XOX"]
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "7VUZ"]
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "7VUY"]
    benchmark_set = benchmark_set[benchmark_set["pdb"] != "7VV3"]

    # Drop rows where ligand_chain and receptor_chain are the same
    benchmark_set = benchmark_set[benchmark_set["ligand_chain"] != benchmark_set["receptor_chain"]]

    # Remove rows where ligand_pdb_sequence is not at least 4 amino acids long
    benchmark_set = benchmark_set[benchmark_set["ligand_pdb_seq"].str.len() >= 4]

    # Drop duplicates based on ligand_pdb_seq and receptor_pdb_seq
    benchmark_set = benchmark_set.sort_values(by=["receptor", "resolution"])
    pdbs_before = benchmark_set["pdb"]
    benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_pdb_seq", "receptor_pdb_seq"])
    pdbs_after = benchmark_set["pdb"]

    # Check if any pdb codes were removed
    removed_pdbs = set(pdbs_before) - set(pdbs_after)
    if removed_pdbs:
        print(f"Removed the following PDB codes: {removed_pdbs}")

    # Removed the following PDB codes: 
    # '7X1U', '7F8V', '7XBD', '7SK5', '8F2A', 
    # '7VDL', '7SK8', '8DWC', '7FIY', '7SK3', '7SK6', '7TYL', '7TZF', '7TYX', 
    # '7P02', '7TYI', '7RMH', '8F0J', '7TYH'   

    # If ligand_pdb_seq ends with X, remove it (C-terminal amidation)
    benchmark_set["ligand_pdb_seq"] = benchmark_set["ligand_pdb_seq"].str.rstrip("X")

    # Replace X with A for 7W40 ligand_pdb_seq
    benchmark_set.loc[benchmark_set["pdb"] == "7W40", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7W40", "ligand_pdb_seq"].str.replace("X", "A")

    # Remove the first letter from ligand_pdb_seq for 7Y66 and 7XAV - hetatm lines in PDB
    benchmark_set.loc[benchmark_set["pdb"] == "7Y66", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7Y66", "ligand_pdb_seq"].str[1:]
    benchmark_set.loc[benchmark_set["pdb"] == "7XAV", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7XAV", "ligand_pdb_seq"].str[1:]

    # Drop duplicates based on ligand_pdb_seq + name and receptor
    benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_pdb_seq", "receptor"])
    benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_name", "receptor"])

    # Filter out nearly identical ligands per each receptor
    filtered_ligands = {}
    for receptor, group in benchmark_set.groupby('receptor'):
        unique_ligands = []
        for _, row in group.iterrows():
            add_ligand = True
            for unique in unique_ligands:
                # Calculate similarity between current row's ligand sequence and already added unique ligand sequences
                sim = sequence_similarity(row['ligand_pdb_seq'], unique['ligand_pdb_seq'])
                if sim > 0.80:
                    add_ligand = False
                    break
            if add_ligand:
                unique_ligands.append(row)
        filtered_ligands[receptor] = unique_ligands

    # Save the benchmark set to a CSV file
    benchmark_set = pd.concat([pd.DataFrame.from_records([ligand]) for ligands in filtered_ligands.values() for ligand in ligands])
    benchmark_set.reset_index(drop=True, inplace=True)
    benchmark_set.to_csv("3f_known_structures_benchmark_2021-09-30.csv", index=False)

    # Save fastas to separate folders
    os.makedirs("fastas", exist_ok=True)
    os.makedirs("fastas/receptors", exist_ok=True)
    os.makedirs("fastas/ligands", exist_ok=True)
    os.makedirs("fastas/pairs", exist_ok=True)
    os.makedirs("pdbs", exist_ok=True)

    for index, row in benchmark_set.iterrows():
        with open(f"fastas/receptors/{row['pdb']}_receptor.fasta", "w") as f:
            f.write(f">{row['pdb']}_receptor\n{row['receptor_pdb_seq']}")
        with open(f"fastas/ligands/{row['pdb']}_ligand.fasta", "w") as f:
            f.write(f">{row['pdb']}_ligand\n{row['ligand_pdb_seq']}")
        with open(f"fastas/pairs/{row['pdb']}.fasta", "w") as f:
            f.write(f">{row['pdb']}_receptor\n{row['receptor_pdb_seq']}\n")
            f.write(f">{row['pdb']}_ligand\n{row['ligand_pdb_seq']}\n")
        
        # Dowload PDB files
        download_pdb(row["pdb"], "pdbs")


if __name__ == "__main__":
    parse_dataset("3f_known_structures_summary_2021-09-30.csv")