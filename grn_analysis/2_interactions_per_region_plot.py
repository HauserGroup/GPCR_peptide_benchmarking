import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from get_chosen_grns import get_chosen_grns

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'
grn_freq_path = f'{file_dir}/grn_frequencies.csv'

sys.path.append(repo_dir)
from colors import * 

# Dict of regions
regions = {
    "1" : "TM1",
    "12" : "ICL1",
    "2" : "TM2",
    "23" : "ECL1",
    "3" : "TM3",
    "34" : "ICL2",
    "4" : "TM4",
    "45" : "ECL2",
    "5" : "TM5",
    "56" : "ICL3",
    "6" : "TM6",
    "67" : "ECL3",
    "7" : "TM7"
}

# Read in interaction data and get chosen generic residue numbers
interactions_df = pd.read_csv(interaction_csv_path)
# Print unique pdb codes
chosen_grns, _, _ = get_chosen_grns(f"{file_dir}/grn_frequencies.csv", interaction_csv_path)
interactions_chosen_grns = interactions_df[interactions_df["generic_residue_number_a"].isin(chosen_grns)]

# Subset dataframe to include unique GRN interactions for each PDB
interactions_df_subset = interactions_df[["pdb_code", "protein", "ligand_name", "class", "sequence_number", "display_generic_number", "generic_residue_number_a", "region"]].copy()
interactions_df_subset = interactions_df_subset.drop_duplicates(subset=["pdb_code", "generic_residue_number_a"])

# Calculate frequency of interactions per GPCR domain - all GRNs
region_frequencies = interactions_df_subset["region"].value_counts()
region_frequencies = pd.DataFrame(region_frequencies)
region_frequencies.reset_index(inplace=True)
region_frequencies.columns = ["region","count"]
region_frequencies_dict = {}
for region in list(regions.values()):
    if region in list(region_frequencies["region"]):
        region_frequencies_dict[region] = region_frequencies[region_frequencies["region"] == region]["count"].values[0]
    else: 
        region_frequencies_dict[region] = 0

x_all = list(region_frequencies_dict.keys())
y_all = list(region_frequencies_dict.values())

# Calculate frequency of interactions per GPCR domain - only chosen GRNs
interactions_chosen_grns = interactions_df_subset[interactions_df_subset["generic_residue_number_a"].isin(chosen_grns)]
region_frequencies = interactions_chosen_grns["region"].value_counts()
region_frequencies = pd.DataFrame(region_frequencies)
region_frequencies.reset_index(inplace=True)
region_frequencies.columns = ["region","count"]
region_frequencies_dict = {}
for region in list(regions.values()):
    if region in list(region_frequencies["region"]):
        region_frequencies_dict[region] = region_frequencies[region_frequencies["region"] == region]["count"].values[0]
    else: 
        region_frequencies_dict[region] = 0

x = list(region_frequencies_dict.keys())
y = list(region_frequencies_dict.values())

# Make barplot
fig = plt.figure(figsize = (10, 5))
plt.bar(x_all, y_all, color =COLOR["Receptor"], width = 0.4, label = "All interactions")
plt.bar(x, y, color =COLOR["Ligand"], width = 0.4, label = "Chosen GRNs")
plt.xlabel("Domain", fontsize=16)
plt.ylabel("Count", fontsize=16)
plt.title("Number of interacting residues per receptor domain", fontsize = 20)
plt.xticks(fontsize = 12)
plt.tick_params(axis="x",direction="in", length=0)
plt.tick_params(axis="y",direction="in")
plt.ylim(0, max(y_all) + 10)
plt.legend(loc='upper left', prop=fm.FontProperties(size=16), frameon=False)
plt.rcParams['svg.fonttype'] = 'none'
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(f"{plot_dir}/interacting_residues_per_domain_chosen_residues.svg", dpi = 600)