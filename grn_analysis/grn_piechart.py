import os
import pandas 
import json
import requests
import matplotlib.pyplot as plt
import sys

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'
interactions_df = pandas.read_csv(interaction_csv_path)

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(file_dir, '..'))
sys.path.append(top_level_dir)
from colors import *

# Count unique PDBs
unique_receptors = interactions_df["protein"].nunique()
print(f"Unique receptors: {unique_receptors}")
print(interactions_df.columns)

# Count unique GPCRs
structures_per_gpcr = interactions_df.drop_duplicates(subset = ["protein", "class"], keep = "first")

# Make a piechart of the GPCR classes
x = structures_per_gpcr["class"].value_counts()
colors = [COLOR["Class A (Rhodopsin)"], COLOR["Class B1 (Secretin)"]]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
    
# Plot pie chart
plt.figure(figsize=(6, 6))
plt.pie(x, labels=x.index, autopct='%1.1f%%', startangle=90, counterclock=False, colors=colors)
plt.title('GPCR class distribution of experimental GPCR–peptide interactions')
plt.rcParams['svg.fonttype'] = 'none'
plt.savefig(f"{plot_dir}/gpcr_class_distribution.svg", dpi = 600)