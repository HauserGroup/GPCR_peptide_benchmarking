import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

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


# Loop over receptors and make fasta files with all ligands
for receptor in decoy_df["Target ID"].unique():
    receptor_df = decoy_df[decoy_df["Target ID"] == receptor]
    receptor_sequence = receptor_df["GPCR Sequence"].values[0]
    ligands = receptor_df["Decoy ID"].unique()
    with open(f"{fasta_dir}/{receptor.split('_')[0]}_tournament.fasta", "w") as f:
        f.write(f">{receptor}\n")
        f.write(f"{receptor_sequence}\n")
        for ligand in ligands:
            f.write(f">{ligand}\n")
            f.write(f"{receptor_df[receptor_df['Decoy ID'] == ligand]['Ligand Sequence'].values[0]}\n")