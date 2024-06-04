import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(file_dir, '..'))
sys.path.append(top_level_dir)
from colors import * 

# Font path
font_path = f'{repo_dir}/Aptos.ttf'
font_prop = fm.FontProperties(fname=font_path)

# Remove duplicated rows in the subset – make sure that each interacting residue site is only counted once per PDB
interactions_df = pd.read_csv(interaction_csv_path)
interactions_df_subset = interactions_df[["pdb_code", "protein", "ligand_name", "class", "sequence_number", "display_generic_number", "generic_residue_number_a", "region"]].copy()
interactions_df_subset = interactions_df_subset.drop_duplicates()

# Get number of interactions per receptor
interactions_df_subset["count"] = 1
interactions_df_subset = interactions_df_subset.groupby(["pdb_code", "protein", "ligand_name", "class"]).sum()
interactions_df_subset = interactions_df_subset.reset_index()
interactions_df_subset = interactions_df_subset[["pdb_code", "protein", "ligand_name", "class", "count"]]
interactions_df_subset = interactions_df_subset.sort_values(by=["count"], ascending=False)

# Sort by protein
interactions_df_subset = interactions_df_subset.sort_values(by=["protein", "count"], ascending=True)

# Calculate average number of interactions per receptor
proteins = list(interactions_df_subset["protein"].unique())
avg_interactions_per_receptor = {}
for protein in proteins:
    average_interactions = interactions_df_subset[interactions_df_subset["protein"] == protein]["count"].mean()
    avg_interactions_per_receptor[protein] = average_interactions

# Sort dictionary by value
avg_interactions_per_receptor = dict(sorted(avg_interactions_per_receptor.items(), key=lambda item: item[1], reverse=True))

# Plot the average number of interactions per receptor
x = avg_interactions_per_receptor.keys()
x = [i.split("_")[0].upper() for i in x]
y = avg_interactions_per_receptor.values()
avg_to_plot = np.mean(list(avg_interactions_per_receptor.values()))

# Use the Aptos font
font_prop = fm.FontProperties(fname=font_path)

# Bar color from the colors dictionary
bar_color = COLOR["Receptor"]

# Make barplot
fig = plt.figure(figsize = (15, 5))
plt.bar(x, y, color =bar_color, width = 0.5)
plt.xlabel("Receptor", fontproperties=font_prop, fontsize=16)
plt.ylabel("Count", fontproperties=font_prop, fontsize=16)
plt.title("Number of interacting generic residue numbers per receptor", fontsize = 20, fontproperties=font_prop)
plt.xticks(rotation=90, fontproperties=font_prop)
plt.tick_params(axis="y",direction="in")
plt.tick_params(axis="x",direction="in", length=0)

# Add horizontal line
plt.axhline(y=avg_to_plot, color='k', linestyle='--')
plt.text(45, avg_to_plot + 0.8, f'Average number of interactions per receptor = {round(avg_to_plot, 2)}', fontsize=14, fontproperties=font_prop)
plt.tight_layout()
plt.ylim(0, 30)
plt.savefig(f"{plot_dir}/interacting_generic_residue_numbers_per_receptor.png", dpi = 600)