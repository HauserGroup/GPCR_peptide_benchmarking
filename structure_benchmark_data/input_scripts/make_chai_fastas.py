# Function to make fasta files for the Chai benchmark dataset
import os 
import pandas as pd
import json

# Get the directory of the current file and build the path to the repository directory
file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Load the classifier benchmark dataset
structural_benchmark_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/structural_benchmark_dataset.csv")

# Output path for the fasta files
fasta_path = f"{repo_dir}/structure_benchmark_data/fastas/chai"
os.makedirs(fasta_path, exist_ok=True)

# Loop over the dataframe and make the fasta files
for index, row in structural_benchmark_df.iterrows():

    # Parse identifier and fasta output path
    identifier = row["pdb"]
    output_fasta_path = f"{fasta_path}/{identifier}.fasta"

    # Make fasta for the complex - parse the GPCR and peptide sequences
    with open(output_fasta_path, "w") as f:
        f.write(f">protein|name={identifier}_receptor\n{row['receptor_pdb_seq']}\n")
        f.write(f">protein|name={identifier}_ligand\n{row['ligand_pdb_seq']}\n")