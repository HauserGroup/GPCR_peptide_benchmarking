# Script to make complex .json files for AF3 structural benchmark dataset for the AF3 server
import os 
import pandas as pd
import json

# Get the directory of the current file and build the path to the repository directory
file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Load the structural benchmark dataset
structural_benchmark_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/structural_benchmark_dataset.csv")

# Paths to the json output folder
json_path = f"{repo_dir}/structure_benchmark_data/fastas/AF3_server_jsons/"
os.makedirs(json_path, exist_ok=True)

json_list = []
c = 0

# Loop over the dataframe and make the complex jsons
for index, row in structural_benchmark_df.iterrows():

    # Parse identifier and json output path
    identifier = row["pdb"].lower()

    # Make json for the complex - parse the GPCR and peptide MSA data from the dictionaries
    complex_dict = {}
    complex_dict["name"] = identifier
    complex_dict["sequences"] = []
    complex_dict["sequences"].append({"proteinChain": {"sequence": row["receptor_pdb_seq"], "count": 1, "maxTemplateDate": "2021-09-30"}})
    complex_dict["sequences"].append({"proteinChain": {"sequence": row["ligand_pdb_seq"], "count": 1, "maxTemplateDate": "2021-09-30"}})
    complex_dict["modelSeeds"] = []
    complex_dict["dialect"] = "alphafold3"
    complex_dict["version"] = 1

    json_list.append(complex_dict)
    if len(json_list) == 20 or index == len(structural_benchmark_df) - 1:
        c+=1
        output_json_path = f"{json_path}/batch_{c}.json"
        with open(output_json_path, "w") as f:
            json.dump(json_list, f, indent=2)
        json_list = []
