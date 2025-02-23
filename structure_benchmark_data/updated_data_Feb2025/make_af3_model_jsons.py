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
structural_benchmark_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/3f_known_structures_benchmark_2021-09-30_updated.csv")

# Paths to the json output folder
json_path = "/projects/ilfgrid/people/pqh443/AF3/structural_benchmark_jsons/with_templates/"
msa_path = "/projects/ilfgrid/people/pqh443/AF3/MSAs/"
os.makedirs(json_path, exist_ok=True)

# Loop over the dataframe and make the complex jsons
for index, row in structural_benchmark_df.iterrows():

    # Parse identifier and json output path
    identifier = row["pdb"].lower()
    msa_path = f"{msa_path}/{identifier}/{identifier}_data.json"
    output_json_path = f"{json_path}/{identifier}.json"

    # Load the MSA data for the GPCR and peptide
    with open(msa_path, "r") as f:
        msa_dict = json.load(f)

    # Make json for the complex - parse the GPCR and peptide MSA data from the dictionaries
    complex_dict = {}
    complex_dict["name"] = identifier
    complex_dict["sequences"] = msa_dict["sequences"]
    complex_dict["modelSeeds"] = [1]
    complex_dict["dialect"] = "alphafold3"
    complex_dict["version"] = 1
    if not os.path.exists(output_json_path):
        with open(output_json_path, "w") as f:
            json.dump(complex_dict, f, indent=2)

    # Parse identifier and json output path
    identifier = row["pdb"].lower()
    msa_path = f"{msa_path}/{identifier}/{identifier}_data.json"
    output_json_path = f"{json_path}/{identifier}_no_templates.json"

    # Load the MSA data for the GPCR and peptide and remove templates
    with open(msa_path, "r") as f:
        msa_dict = json.load(f)
        msa_dict["sequences"][0]["protein"]["templates"] = []
        msa_dict["sequences"][1]["protein"]["templates"] = []

    # Make json for the complex - parse the GPCR and peptide MSA data from the dictionaries
    complex_dict = {}
    complex_dict["name"] = identifier + "_no_templates"
    complex_dict["sequences"] = msa_dict["sequences"]
    complex_dict["modelSeeds"] = [1]
    complex_dict["dialect"] = "alphafold3"
    complex_dict["version"] = 1
    if not os.path.exists(output_json_path):
        with open(output_json_path, "w") as f:
            json.dump(complex_dict, f, indent=2)