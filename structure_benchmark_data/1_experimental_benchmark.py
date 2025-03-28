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

def download_structure(pdb_id, output_folder, overwrite = False, type = "pdb"):
    '''
    Function to download PDB/CIF files using the RCSB PDB API given a PDB identifier 
    and output folder name. If the PDB/CIF file already exists in the output folder,
    the function will not download it again unless overwrite is set to True.
    Returns the path of the downloaded PDB/CIF file.
    '''

    # Check if the PDB file already exists in the output folder
    if os.path.exists(f"{output_folder}/{pdb_id}.pdb") and not overwrite:
        print(f"PDB file {pdb_id}.pdb already exists in the output folder.")
        return f"{output_folder}/{pdb_id}.pdb"

    # Make sure output folder exists and create it if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # URL for the PDB file
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.{type}"

    # Send an HTTP GET request to the PDB URL
    response = requests.get(pdb_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open(f"{output_folder}/{pdb_id}.{type}", "wb") as pdb_file:
            pdb_file.write(response.content)
        print(f"{type} file {pdb_id}.pdb downloaded successfully.")
        return f"{output_folder}/{pdb_id}.{type}"
    else:
        print(f"Failed to download {type} file {pdb_id}. Status code: {response.status_code}")
        return ""

def sequence_similarity(seq1, seq2):
    from Bio import pairwise2
    """Calculate the sequence similarity by finding the best alignment and considering the number of identical matches."""
    alignments = pairwise2.align.globalxx(seq1, seq2)
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

def get_peptide_interaction(pdb_code):
    """
    Helper function to get peptide interaction data of a PDB structure from GPCRdb
    """
    # Get structure information from GPCRdb for the pdb files included
    response = requests.get(f'https://gpcrdb.org/services/structure/{pdb_code}/peptideinteraction/')
    response = response.json()
    # Make into a dataframe
    response_df = pd.DataFrame.from_dict(response)
    return response_df

file_dir = os.getcwd()
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
filepath = f"{repo_dir}/classifier_benchmark_data/output/3f_known_structures_summary_2021-09-30.csv"
outfile = "structural_benchmark_dataset.csv"
outdir = f"{repo_dir}/structure_benchmark_data/"
os.makedirs(f"{outdir}", exist_ok=True)

# Get receptors that have peptide complexes with more recent structures
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

peptide_interactions = []
for pdb_code in benchmark_set["pdb_code"].unique():
    peptide_interaction = get_peptide_interaction(pdb_code)
    peptide_interactions.append(peptide_interaction)

# Drop duplicates based on pdb_code and ligand_chain
peptide_interactions_df = pd.concat(peptide_interactions)
peptide_interactions_df = peptide_interactions_df[["pdb_code", "ligand_chain"]].drop_duplicates()

# If "chain" is NaN, replace it with the value from "peptide_interactions_df"
benchmark_set = benchmark_set.merge(peptide_interactions_df, on="pdb_code", how="left")
benchmark_set["chain"] = benchmark_set["chain"].fillna(benchmark_set["ligand_chain"])
benchmark_set.drop(columns=["ligand_chain"], inplace=True)

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

# Drop rows where ligand_chain is NaN
benchmark_set = benchmark_set[~benchmark_set["ligand_chain"].isna()]

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

# Drop rows where ligand_pdb_seq is none
benchmark_set = benchmark_set[~benchmark_set["ligand_pdb_seq"].isna()]

# Remove pdb codes that have multiple ligands
duplicated_pdbs = benchmark_set[benchmark_set.duplicated(subset=["pdb"])]
benchmark_set = benchmark_set[~benchmark_set["pdb"].isin(duplicated_pdbs["pdb"])]

# Remove 7SK7 and 7SK8 from the benchmark set - there is another structure without an additional small molecule ligand
benchmark_set = benchmark_set[benchmark_set["pdb"] != "7SK7"]
benchmark_set = benchmark_set[benchmark_set["pdb"] != "7SK8"]

# Drop rows where ligand_chain and receptor_chain are the same
benchmark_set = benchmark_set[benchmark_set["ligand_chain"] != benchmark_set["receptor_chain"]]

# If ligand_pdb_seq ends with X, remove it (C-terminal amidation)
benchmark_set["ligand_pdb_seq"] = benchmark_set["ligand_pdb_seq"].str.rstrip("X")

# Drop sequences that contain non-standard amino acids (i.e. X)
benchmark_set = benchmark_set[~benchmark_set["ligand_pdb_seq"].str.contains("X")]

# Replace X with A for 7W40 ligand_pdb_seq
benchmark_set.loc[benchmark_set["pdb"] == "7W40", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7W40", "ligand_pdb_seq"].str.replace("X", "A")

# Remove the first letter from ligand_pdb_seq for 7Y66 and 7XAV - hetatm lines in PDB
benchmark_set.loc[benchmark_set["pdb"] == "7Y66", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7Y66", "ligand_pdb_seq"].str[1:]
benchmark_set.loc[benchmark_set["pdb"] == "7XAV", "ligand_pdb_seq"] = benchmark_set.loc[benchmark_set["pdb"] == "7XAV", "ligand_pdb_seq"].str[1:]

# Drop duplicates based on ligand_pdb_seq and receptor_pdb_seq
benchmark_set = benchmark_set.sort_values(by=["receptor", "resolution"])
pdbs_before = benchmark_set["pdb"]
benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_pdb_seq", "receptor_pdb_seq"])
pdbs_after = benchmark_set["pdb"]

# Check if any pdb codes were removed
removed_pdbs = set(pdbs_before) - set(pdbs_after)
if removed_pdbs:
    print(f"Removed the following PDB codes: {removed_pdbs}")

# Drop duplicates based on ligand_pdb_seq + name and receptor
benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_pdb_seq", "receptor"])
benchmark_set = benchmark_set.drop_duplicates(subset=["ligand_name", "receptor"])

# Remove rows where ligand_pdb_sequence is not at least 4 amino acids long
benchmark_set = benchmark_set[benchmark_set["ligand_pdb_seq"].str.len() >= 4]

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

# Drop rows where receptor_pdb_seq or receptor_pdb_seq is None or empty
benchmark_set = benchmark_set[~benchmark_set["receptor_pdb_seq"].isna()]
benchmark_set = benchmark_set[~benchmark_set["receptor_pdb_seq"].str.strip().eq("")]
benchmark_set = benchmark_set[~benchmark_set["receptor_pdb_seq"].str.strip().eq("None")]
benchmark_set = benchmark_set[~benchmark_set["ligand_pdb_seq"].isna()]
benchmark_set = benchmark_set[~benchmark_set["ligand_pdb_seq"].str.strip().eq("")]
benchmark_set = benchmark_set[~benchmark_set["ligand_pdb_seq"].str.strip().eq("None")]

# Drop 8JBG, 8JBF, 8JBH from the benchmark set - the receptor sequence contains BRIL fusion protein
benchmark_set = benchmark_set[benchmark_set["pdb"] != "8JBG"]
benchmark_set = benchmark_set[benchmark_set["pdb"] != "8JBH"]
benchmark_set.to_csv(f"{outdir}/{outfile}", index=False)

# Save fastas to separate folders
os.makedirs(f"{outdir}/fastas", exist_ok=True)
os.makedirs(f"{outdir}/fastas/receptors", exist_ok=True)
os.makedirs(f"{outdir}/fastas/ligands", exist_ok=True)
os.makedirs(f"{outdir}/fastas/pairs", exist_ok=True)
os.makedirs(f"{outdir}/pdbs", exist_ok=True)
os.makedirs(f"{outdir}/cifs", exist_ok=True)

for index, row in benchmark_set.iterrows():
    with open(f"{outdir}/fastas/receptors/{row['pdb']}_receptor.fasta", "w") as f:
        f.write(f">{row['pdb']}_receptor\n{row['receptor_pdb_seq']}")
    with open(f"{outdir}/fastas/ligands/{row['pdb']}_ligand.fasta", "w") as f:
        f.write(f">{row['pdb']}_ligand\n{row['ligand_pdb_seq']}")
    with open(f"{outdir}/fastas/pairs/{row['pdb']}.fasta", "w") as f:
        f.write(f">{row['pdb']}_receptor\n{row['receptor_pdb_seq']}\n")
        f.write(f">{row['pdb']}_ligand\n{row['ligand_pdb_seq']}\n")
     
    # Dowload PDB files
    download_structure(row["pdb"], f"{outdir}/pdbs")
    download_structure(row["pdb"], f"{outdir}/cifs", type="cif")