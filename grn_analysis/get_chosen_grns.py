import os 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'
grn_freq_path = f'{file_dir}/grn_frequencies.csv'

sys.path.append(repo_dir)
from colors import * 

def get_chosen_grns(grn_freq_path, interaction_csv_path):

    # List to store the PDBs that are covered by the generic residue numbers
    pdbs_covered = []
    pdbs_covered_p = []

    # List to store chosen generic residue numbers for the classifier
    chosen_grns = []
    chosen_grns_per_round = []

    # Read in the grn frequencies and interactions data
    grn_frequencies = pd.read_csv(grn_freq_path, index_col=0)
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

# Parse the chosen GRNs labels and save them to a file
chosen_grns_labels = ["+ " + str(i[0][-1]) for i in chosen_grns_per_round]
chosen_grns_labels[0] = chosen_grns_labels[0].replace("+ ", " ")
with open(f"{file_dir}/chosen_grns.txt", "w") as f:
    for grn in chosen_grns:
        f.write(f"{grn}\n")

# Make a cumulative plot of number of PDBs covered by the generic residue numbers
fig, ax = plt.subplots()
fig.set_figwidth(7) 
fig.set_figheight(6) 
labels = []
labels = chosen_grns_labels
y_pos = np.arange(len(labels))

ax.barh(y_pos, pdbs_covered_p, align='center', color = COLOR["Receptor"])
ax.set_yticks(y_pos, labels=labels, size = 16, weight = "bold")
ax.invert_yaxis() 

# Add the percentage values to the bars
for i, v in enumerate(pdbs_covered_p):
    ax.text(v - 10, i, str(round(v, 2)) + "%", color='white', fontweight='bold', size = 14)
ax.set_xlabel('Percentage (%)', size = 16)
ax.set_title("Percentage of PDBs covered by the generic residue numbers", size = 20)
ax.set_xlim(70,100)

# Adjust ticks and labels
plt.yticks(fontsize = 12)
plt.xticks(fontsize = 12)
plt.tick_params(axis="x",direction="in")
plt.tick_params(axis="y",length=0)
plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()

# Remove the plot frame lines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

# Save the plot
plt.savefig(f"{plot_dir}/pdbs_covered.svg", bbox_inches='tight', dpi = 300)