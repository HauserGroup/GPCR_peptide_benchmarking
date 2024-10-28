import os 
import pandas as pd
import requests 
import re

def get_peptide_gpcr_structures():
    # Get a list of peptide ligands and their corresponding structures from GPCRdb API
    url = "https://gpcrdb.org/services/ligands/peptides/"
    response = requests.get(url)
    peptides = response.json()

    # Empty list to store the peptide ligands
    peptide_list = []
    for peptide in peptides:
        name = peptide["Peptide name"]
        seq = peptide["Sequence"]
        pdb = peptide["PDB"]
        family = peptide["Family"]
        gpcr_class = peptide["GPCR Class"]
        receptor = peptide["Receptor"]
        if receptor and "human" in receptor:
            peptide_list.append([name, seq, family, gpcr_class, receptor, pdb])

    # Make a dataframe from the list
    return pd.DataFrame(peptide_list, columns=['peptide', 'sequence', 'family', 'class', 'receptor', 'pdb_code'])

def get_interactions_from_gpcrdb(peptide_df):
    # List to store all interactions
    interactions_df = []

    for index, row in peptide_df.iterrows():
        # Get peptide interactions from GPCRdb
        pdb_code = row["pdb_code"]
        ligand = row["peptide"]
        response = requests.get(f'https://gpcrdb.org/services/structure/{pdb_code}/interaction/')
        interactions = response.json()
        keys_to_extract = [
            "pdb_code",
            "ligand_name",
            "amino_acid",
            "sequence_number",
            "interaction_type",
            "display_generic_number"
        ]

        # Get only those interactions that have a generic residue number and the correct ligand name
        interactions = [i for i in interactions if 'display_generic_number' in i.keys() and i["ligand_name"] == ligand]

        # Remove interactions with label "accessible"
        interactions = [i for i in interactions if i["interaction_type"] != "accessible"]

        # Extract data from required keys
        interactions = [[i[key] for key in keys_to_extract] for i in interactions]

        # Append interactions to interactions_df
        interactions_df.extend(interactions)

    interactions_df = pd.DataFrame(interactions_df, columns=keys_to_extract)
    interactions_df["residue"] = interactions_df["amino_acid"] + interactions_df["sequence_number"].astype(str)

    response = requests.get(f'https://gpcrdb.org/services/structure/')
    structures = response.json()
    structures = pd.DataFrame.from_dict(structures)

    interactions_df = pd.merge(interactions_df, structures, on = "pdb_code")
    return interactions_df

def map_gpcrdb_b_to_a(mapping_file_path):
    # Table containing mapping from GPCRdb A to B general residue numbering
    # Source: https://github.com/protwis/gpcrdb_data/blob/master/residue_data/generic_numbers/mapping_gpcrdbb.txt
    gpcrdb_a_to_b_mapping = []

    # Read text file line by line
    with open(mapping_file_path) as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        line = line.split(" ")
        line = [i for i in line if i != ""]
        if len(line) == 2:
            line = [line[0], line[1]]
            gpcrdb_a_to_b_mapping.append(line)

    gpcrdb_a_to_b_mapping = pd.DataFrame(gpcrdb_a_to_b_mapping)
    gpcrdb_a_to_b_mapping.columns = ["gpcrdb_a", "gpcrdb_b"]

    # Convert to dictionary 
    return dict(zip(gpcrdb_a_to_b_mapping["gpcrdb_b"], gpcrdb_a_to_b_mapping["gpcrdb_a"]))

def parse_dataset(interaction_csv_path, grn_frequencies_path, mapping_file_path):
    """
    Parse the interactions from GPCRdb and save them to a csv file
    """
    peptide_df = get_peptide_gpcr_structures()
    interactions_df = get_interactions_from_gpcrdb(peptide_df)
    gpcrdb_b_to_a_mapping = map_gpcrdb_b_to_a(mapping_file_path)

    # Column to store generic residue number in class A
    interactions_df["generic_residue_number_a"] = ""

    for index, row in interactions_df.iterrows():

        # Parse generic residue number from GPCRdb
        # Remove the string between a dot and x
        # e.g. 3.29x29 -> 3x29
        receptor_grn = row["display_generic_number"]
        receptor_grn = re.sub(r'\.\d+', '', receptor_grn)

        # In case the last part of the GRN is three digits, remove the last digit
        # These residues represent helix bulges at a given position. 
        # For example, 5x501 is a bulge following position 5x50
        if len(receptor_grn.split("x")[-1]) == 3:
            receptor_grn = receptor_grn[:-1]

        # If the class is B1, convert the generic residue number from B to A
        if row["class"] == "Class B1 (Secretin)":
            try: 
                interactions_df.at[index, "generic_residue_number_a"] = gpcrdb_b_to_a_mapping[receptor_grn]
            except:
                print("Failed to map generic residue number ", receptor_grn, " from class B to A")
        else:
            interactions_df.at[index, "generic_residue_number_a"] = receptor_grn

    # Add region labels
    interactions_df["region"] = interactions_df["generic_residue_number_a"].str.split("x").str[0]
    regions = {
        "1" : "TM1",
        "12" : "ICL1",
        "2" : "TM2",
        "23" : "ECL1",
        "3" : "TM3",
        "34" : "ICL2",
        "4" : "TM4",
        "45" : "ECL2",
        "5" : "TM5",
        "56" : "ICL3",
        "6" : "TM6",
        "67" : "ECL3",
        "7" : "TM7"
    }
    interactions_df["region"] = [regions[i] for i in interactions_df["region"]]

    # Sort by protein, ligand_name, and resolution
    interactions_df = interactions_df.sort_values(["protein", "ligand_name", "resolution"])

    # Merge with peptide_df so that we can have peptide sequence in the dataframe
    interactions_df = pd.merge(interactions_df, peptide_df[["sequence", "pdb_code"]], on="pdb_code")

    # Get the best quality pdb for each protein-ligand pair - first based on sequence and then based on ligand name
    pdbs_to_keep = interactions_df.drop_duplicates(["protein", "sequence"], keep="first")["pdb_code"]
    interactions_df = interactions_df[interactions_df["pdb_code"].isin(pdbs_to_keep)]
    interactions_df["ligand_name"] = interactions_df["ligand_name"].str.upper()
    pdbs_to_keep = interactions_df.drop_duplicates(["protein", "ligand_name"], keep="first")["pdb_code"]
    interactions_df = interactions_df[interactions_df["pdb_code"].isin(pdbs_to_keep)]

    # Save to csv
    interactions_df.to_csv(interaction_csv_path, index=False)

    # Remove duplicated rows in the subset – make sure that each interacting residue site is only counted once per PDB
    interactions_df_subset = interactions_df[["pdb_code", "protein", "ligand_name", "class", "sequence_number", "display_generic_number", "generic_residue_number_a", "region"]].copy()
    interactions_df_subset = interactions_df_subset.drop_duplicates()

    # Print number of unique pdbs
    print("Number of unique PDBs: ", len(interactions_df["pdb_code"].unique()))
    print("Number of unique receptors: ", len(interactions_df["protein"].unique()))

    # Print nunmber of Class A and Class B interactions
    class_df = interactions_df[["protein", "class"]].drop_duplicates()
    print(class_df["class"].value_counts())

    # Count frequency table of generic residue numbers
    grn_frequencies = interactions_df_subset["generic_residue_number_a"].value_counts()
    grn_frequencies = pd.DataFrame(grn_frequencies)
    grn_frequencies.columns = ["count"]
    grn_frequencies["percentage"] = grn_frequencies["count"] / len(interactions_df["pdb_code"].unique()) * 100
    grn_frequencies.to_csv(grn_frequencies_path)

if __name__ == "__main__":
    file_dir = os.path.dirname(__file__)
    folder_name = file_dir.split('/')[-1]
    repo_dir = file_dir.replace(f'/{folder_name}', '')
    interaction_csv_path = f'{file_dir}/interactions.csv'
    grn_frequencies_path = f'{file_dir}/grn_frequencies.csv'
    mapping_file_path = f'{file_dir}/mapping_gpcrdbb.txt'
    parse_dataset(interaction_csv_path, grn_frequencies_path, mapping_file_path)