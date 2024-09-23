import os 
import sys
import pandas as pd
import requests

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
fasta_dir = f'{file_dir}/fastas'
os.makedirs(fasta_dir, exist_ok = True)
decoy_df = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv")

# Keep only rows where Decoy Rank is 0.0, 4.0 or empty
decoy_df = decoy_df[(decoy_df["Decoy Rank"].isin([0.0, 4.0])) | (decoy_df["Decoy Rank"].isnull())]

# Sort dataframe first based on Target ID and then "Target Similarity to Original Target" in descending order 
decoy_df = decoy_df.sort_values(by = ["Target ID", "Target Similarity to Original Target"], ascending = [True, False])

receptors_with_wrong_seq = [
    "mchr1_human", 
    "ednrb_human", 
    "g37l1_human",
    "gpr37_human",
    "lgr6_human",
    "lgr5_human", 
    "ccr8_human", 
    "cx3c1_human", 
    "ackr2_human",
    "fzd1_human",
    "par4_human",
    "glr_human",
    "glp1r_human",
    "ednra_human",
    "calrl_human",
    "sctr_human",
    "fzd6_human",
    "ccr4_human",
    "gpr39_human",
    "fzd2_human",
    "gp107_human",
    "ccr7_human",
    "xcr1_human",
    "ccr6_human",
    "lgr4_human"
]

seq_856 = "QHHGVTKCNITCSKMTSKIPVALLIHYQQNQASCGKRAIILETRQHRLFCADPKEQWVKDAMQHLDRQAAALTRN"

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

def get_gene_name(uniprot_id, verbose = False):
    # UniProt API endpoint for retrieving UniProt entry in JSON format
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.json"

    # Make GET request to retrieve UniProt entry
    response = requests.get(url)

    # Check if request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        
        # Extract gene name from the entry
        gene_name = data['genes']
        
        return gene_name[0]["geneName"]["value"]
    else:
        if verbose:
            print(f"Failed to retrieve UniProt entry for {uniprot_id}. Status code: {response.status_code}")
        return None
    
def get_uniprot_id(receptor_id):
    '''
    Function to get the UniProt ID of a receptor given its ID in the GPCRdb.
    '''
    url = f"https://gpcrdb.org/services/protein/{receptor_id}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["accession"]
    else:
        print(f"Error: Unable to retrieve data from GPCRdb using ID {receptor_id}. Status code {response.status_code}")
        return None

# Loop over receptors and make fasta files with all ligands
for receptor in decoy_df["Target ID"].unique():
    receptor_df = decoy_df[decoy_df["Target ID"] == receptor]
    receptor_id = get_uniprot_id(receptor)
    receptor_sequence = get_receptor_sequence(receptor_id)[1]
    if receptor_sequence is None or receptor in receptors_with_wrong_seq:
        receptor_sequence = receptor_df["GPCR Sequence"].values[0]

    ligands = receptor_df["Decoy ID"].unique()
    with open(f"{fasta_dir}/{receptor.split('_')[0]}_tournament.fasta", "w") as f:
        f.write(f">{receptor}\n")
        f.write(f"{receptor_sequence}\n")
        for ligand in ligands:
            ligand_seq = receptor_df[receptor_df["Decoy ID"] == ligand]['Ligand Sequence'].values[0]
            if str(ligand) == "856":
                ligand_seq = seq_856

            f.write(f">{ligand}\n")
            f.write(f"{ligand_seq}\n")
