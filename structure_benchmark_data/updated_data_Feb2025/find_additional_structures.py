# Check which structures are missing from the updated data
import pandas as pd
import os
import requests

file_dir = os.getcwd()
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
old = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30.csv"
updated = f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/3f_known_structures_benchmark_2021-09-30_updated.csv"

old_df = pd.read_csv(old)
updated_df = pd.read_csv(updated)

# Check which structures are missing from the updated data
missing = old_df[~old_df["pdb"].isin(updated_df["pdb"])]

training_structures = pd.read_csv("/Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/classifier_benchmark_data/output/3f_known_structures_summary_2021-09-30.csv")
training_structures = training_structures[training_structures["has_peptide_complex_before_cutoff"] == True]


for receptor in old_df["receptor"].unique():
    if receptor in training_structures["Target GPCRdb ID"].unique():
        print(receptor)




