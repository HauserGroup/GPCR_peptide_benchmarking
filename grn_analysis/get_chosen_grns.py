import os 
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt
import sys

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'
grn_freq_path = f'{file_dir}/grn_frequencies.csv'

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(file_dir, '..'))
sys.path.append(top_level_dir)
from colors import * 

# Font path
font_path = f'{repo_dir}/Aptos.ttf'
font_prop = fm.FontProperties(fname=font_path)

def get_chosen_grns(grn_freq_path, interaction_csv_path):

    # List to store the PDBs that are covered by the generic residue numbers
    pdbs_covered = []
    pdbs_covered_p = []

    # List to store chosen generic residue numbers for the classifier
    chosen_grns = []
    chosen_grns_per_round = []

    # Read in the grn frequencies
    grn_frequencies = pd.read_csv(grn_freq_path, index_col=0)

    # Read in the interactions data
    interactions_df = pd.read_csv(interaction_csv_path)

    # Get the generic residues required to cover all receptor-ligand interactions
    for generic_residue_number in grn_frequencies.index:
        grn_subset = interactions_df[interactions_df["generic_residue_number_a"] == generic_residue_number]
        pdbs = grn_subset["pdb_code"].unique()

        # Print pdbs not in pdbs_covered but in pdbs
        pdbs_not_covered = [pdb for pdb in pdbs if pdb not in pdbs_covered]
        if len(pdbs_not_covered) > 0:
            pdbs_covered.extend(pdbs)
            pdbs_covered = list(set(pdbs_covered))
            pdbs_covered_p.append(len(pdbs_covered)/len(interactions_df["pdb_code"].unique())*100)

            # Add generic residue number to chosen_grns
            chosen_grns.append(generic_residue_number)
            chosen_grns_per_round.append([chosen_grns.copy()])
            
            if len(pdbs_covered) == len(interactions_df["pdb_code"].unique()):
                break

    return chosen_grns, chosen_grns_per_round, pdbs_covered_p

# Get chosen GRNs
chosen_grns, chosen_grns_per_round, pdbs_covered_p = get_chosen_grns(grn_freq_path, interaction_csv_path)

# Print the chosen GRNs
print(f"Chosen {len(chosen_grns)} GRNs:")
print(chosen_grns)

# Parse the chosen GRNs labels
chosen_grns_labels = ["+ " + str(i[0][-1]) for i in chosen_grns_per_round]
chosen_grns_labels[0] = chosen_grns_labels[0].replace("+ ", " ")

# Cumulative plot of number of PDBs covered by the generic residue numbers
fig, ax = plt.subplots()
fig.set_figwidth(10) 
fig.set_figheight(5) 

labels = []
labels = chosen_grns_labels
y_pos = np.arange(len(labels))

ax.barh(y_pos, pdbs_covered_p, align='center', color = COLOR["Receptor"])
ax.set_yticks(y_pos, labels=labels, size = 16, weight = "bold", fontproperties=font_prop)
ax.invert_yaxis() 

# Display percentage on top of each bar
for i, v in enumerate(pdbs_covered_p):
    ax.text(v - 10, i, str(round(v, 2)) + "%", color='white', fontweight='bold', size = 14, fontproperties=font_prop)

ax.set_xlabel('Percentage (%)', fontproperties=font_prop, size = 16)
ax.set_title("Percentage of PDBs covered by the generic residue numbers", size = 20, fontproperties=font_prop)
ax.set_xlim(0,100)

plt.yticks(fontsize = 12)
plt.xticks(fontsize = 12)
plt.tick_params(axis="x",direction="in")
plt.tick_params(axis="y",length=0)
plt.savefig(f"{plot_dir}/pdbs_covered.png", bbox_inches='tight', dpi = 300)