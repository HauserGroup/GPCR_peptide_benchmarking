import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt
from get_chosen_grns import get_chosen_grns

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

# Read in the grn frequencies
grn_freq_path = f"{file_dir}/grn_frequencies.csv"
grn_frequencies = pd.read_csv(grn_freq_path, index_col=0)

# Get chosen GRNs
chosen_grns, _, _  = get_chosen_grns(grn_freq_path, interaction_csv_path)

# Subset to generic residue numbers that cover more than 10% of the PDBs
grn_subset = grn_frequencies[grn_frequencies["percentage"] > 10]

# Make bar plot
fig = plt.figure(figsize=(13, 5))
plt.bar(grn_subset.index, grn_subset["percentage"], color=COLOR["Receptor"], width=0.7)
plt.xlabel("Generic residue number", fontsize=16)
plt.ylabel("PDBs covered (%)", fontsize=16)
plt.title("Coverage of PDBs per generic residue number", fontsize=16)
plt.xticks(rotation=90, fontsize=12)
plt.tight_layout()

# Bold the x-axis labels if they appear in chosen_grns
ax = plt.gca()
# Set x-axis labels to the Aptos font
labels = ax.get_xticklabels()
for label in labels:
    if label.get_text() in chosen_grns:
        label.set_fontweight('bold')

plt.tick_params(axis="x", length=0)
plt.tick_params(axis="y", direction="in", length=2)
plt.ylim(0, 100)

# Save the plot
plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()
plt.savefig(f"{plot_dir}/interacting_residues_percentage.svg", dpi = 600)