# Script to make .json files for AF3 dataset.
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

# Make a directory for the jsons
os.makedirs(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons", exist_ok=True)
os.makedirs(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/receptors", exist_ok=True)
os.makedirs(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/peptides", exist_ok=True)

# json name: Identifier + .json
for index, row in decoy_df.iterrows():
    # Parse id and sequences
    ligand_sequence = row["Ligand Sequence"]
    gpcr_sequence = row["GPCR Sequence"]
    identifier = row["Identifier"]
    
    gpcr_name = identifier.split("___")[0]
    peptide_name = identifier.split("___")[1]

    gpcr_msa_path = f"/projects/ilfgrid/people/pqh443/AF3/MSAs/{gpcr_name}/"
    peptide_msa_path = f"/projects/ilfgrid/people/pqh443/AF3/MSAs/{peptide_name}/"

    # Make json for the receptor only
    receptor_dict = {}
    receptor_dict["name"] = identifier.split("___")[0]
    receptor_dict["sequences"] = []
    receptor_dict["sequences"].append({"protein": {"id": "A", "sequence": gpcr_sequence}})
    receptor_dict["modelSeeds"] = [1]
    receptor_dict["dialect"] = "alphafold3"
    receptor_dict["version"] = 1
    if not os.path.exists(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/receptors/{receptor_dict['name']}.json"):
        with open(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/receptors/{receptor_dict['name']}.json", "w") as f:
            json.dump(receptor_dict, f, indent=2)

    # Make json for the peptide only
    peptide_dict = {}
    peptide_dict["name"] = identifier.split("___")[1]
    peptide_dict["sequences"] = []
    peptide_dict["sequences"].append({"protein": {"id": "B", "sequence": ligand_sequence}})
    peptide_dict["modelSeeds"] = [1]
    peptide_dict["dialect"] = "alphafold3"
    peptide_dict["version"] = 1
    if not os.path.exists(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/peptides/{peptide_dict['name']}.json"):
        with open(f"{repo_dir}/classifier_benchmark/models/AF3/classifier_jsons/peptides/{peptide_dict['name']}.json", "w") as f:
            json.dump(peptide_dict, f, indent=2)