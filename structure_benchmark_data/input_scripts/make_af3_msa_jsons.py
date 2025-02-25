# Script to make complex .json files for AF3 classifier benchmark dataset
# NOTE: Run this script on ILFGRID as it requires access to the MSA data
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

# Paths to the json output folder
json_path = "/projects/ilfgrid/people/pqh443/AF3/structural_benchmark_jsons/msa_inputs/"
os.makedirs(json_path, exist_ok=True)

# Loop over the dataframe and make the complex jsons
for index, row in structural_benchmark_df.iterrows():

    # Parse identifier and json output path
    identifier = row["pdb"].lower()
    output_json_path = f"{json_path}/{identifier}.json"

    # Make json for the complex - parse the GPCR and peptide MSA data from the dictionaries
    complex_dict = {}
    complex_dict["name"] = identifier
    complex_dict["sequences"] = []
    complex_dict["sequences"].append({"protein": {"id": "A", "sequence": row["receptor_pdb_seq"]}})
    complex_dict["sequences"].append({"protein": {"id": "B", "sequence": row["ligand_pdb_seq"]}})
    complex_dict["modelSeeds"] = [1]
    complex_dict["dialect"] = "alphafold3"
    complex_dict["version"] = 1
    if not os.path.exists(output_json_path):
        with open(output_json_path, "w") as f:
            json.dump(complex_dict, f, indent=2)