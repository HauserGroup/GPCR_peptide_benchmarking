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
decoy_df = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv")

# Paths to the MSA data and json output folder
msa_folder = "/projects/ilfgrid/people/pqh443/AF3/MSAs/"
json_path = "/projects/ilfgrid/people/pqh443/AF3/classifier_jsons/complexes/"
os.makedirs(json_path, exist_ok=True)

# Loop over the dataframe and make the complex jsons
for index, row in decoy_df.iterrows():

    # Parse identifier, GPCR and peptide names
    identifier = row["Identifier"]
    gpcr_name = identifier.split("___")[0]
    peptide_name = identifier.split("___")[1]

    # Load GPCR and peptide MSA data
    receptor_json_path = f"{msa_folder}/{gpcr_name}/{gpcr_name}_data.json"
    peptide_json_path = f"{msa_folder}/{peptide_name}/{peptide_name}_data.json"

    # Check if the MSA data exists for both GPCR and peptide
    if not os.path.exists(receptor_json_path) or not os.path.exists(peptide_json_path):
        continue

    # Load the MSA data for the GPCR and peptide
    with open(receptor_json_path, "r") as f:
        receptor_dict = json.load(f)
        receptor_dict = receptor_dict["sequences"][0]
    with open(peptide_json_path, "r") as f:
        peptide_dict = json.load(f)
        peptide_dict = peptide_dict["sequences"][0]

    # Make json for the complex - parse the GPCR and peptide MSA data from the dictionaries
    complex_dict = {}
    complex_dict["name"] = identifier
    complex_dict["sequences"] = []
    complex_dict["sequences"].append(receptor_dict)
    complex_dict["sequences"].append(peptide_dict)
    complex_dict["modelSeeds"] = [1]
    complex_dict["dialect"] = "alphafold3"
    complex_dict["version"] = 1

    # Save output json
    output_path = f"{json_path}/{identifier}.json"
    print("Saving", output_path)
    if not os.path.exists(output_path):
        with open(output_path, "w") as f:
            json.dump(complex_dict, f, indent=2)
