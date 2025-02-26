# Function to make fasta files for the Chai benchmark dataset
import os 
import pandas as pd
import json

# Get the directory of the current file and build the path to the repository directory
file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Output path for the fasta files
fasta_path = f"{repo_dir}/classifier_benchmark/models/Chai-1/fastas"
os.makedirs(fasta_path, exist_ok=True)

# Load the classifier benchmark dataset
decoy_df = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv")

for index, row in decoy_df.iterrows():
    # Parse id and sequences
    ligand_sequence = row["Ligand Sequence"]
    gpcr_sequence = row["GPCR Sequence"]
    identifier = row["Identifier"]
    gpcr_name = identifier.split("___")[0]
    peptide_name = identifier.split("___")[1]

    # Parse identifier and fasta output path
    output_fasta_path = f"{fasta_path}/{identifier}.fasta"

    # Make fasta for the complex - parse the GPCR and peptide sequences
    with open(output_fasta_path, "w") as f:
        f.write(f">protein|name={gpcr_name}\n{gpcr_sequence}\n")
        f.write(f">protein|name={peptide_name}\n{ligand_sequence}\n")