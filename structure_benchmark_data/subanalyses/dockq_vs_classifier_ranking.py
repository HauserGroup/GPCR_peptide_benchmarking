import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]

repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Output path for plots 
plot_dir = f'{file_dir}/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

sys.path.append(repo_dir)
from colors import * 
 
from Bio import pairwise2
from Bio.Seq import Seq

def get_seq_similarity(seq1, seq2):
    """
    Align two sequences and calculate the sequence identity.
    """
    seq1 = Seq(seq1)
    seq2 = Seq(seq2)

    alignments = pairwise2.align.globalxx(seq1, seq2)
    alignment = alignments[0]

    # Calculate similarity
    alignment_score = alignment[2]
    alignment_length = alignment[4]
    similarity_percentage = (alignment_score / alignment_length) * 100
    return similarity_percentage


# Read in DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Read GPCR class datafrom UniProt
gpcr_class_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30.csv"
gpcr_class_data = pd.read_csv(gpcr_class_path)

# Merge DockQ data with GPCR class data
data = data.merge(gpcr_class_data, on='pdb')

principal_agonists_path = f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv"
principal_agonists = pd.read_csv(principal_agonists_path)
principal_agonists = principal_agonists[principal_agonists["Decoy Type"] == "Principal Agonist"]

# Rename Identifier column to receptor
renaming_dict = {
    "Target ID": "receptor",
    "Ligand Sequence": "ligand_gtp_seq",
    "GPCR Sequence": "receptor_gtp_seq",
    "Decoy ID": "peptide_gtp_id",
    "Identifier": "classifier_id"
}

principal_agonists = principal_agonists[renaming_dict.keys()]
principal_agonists = principal_agonists.rename(columns=renaming_dict)

# Merge the two dataframes
data = data.merge(principal_agonists, on='receptor')
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (no templates)")
data.reset_index(drop=True, inplace=True)
rows_to_keep = []

failed_receptors = ['cml1_human', 'galr2_human', 'npy4r_human', 'vipr2_human', 'ccr1_human', 'fpr1_human', 'gasr_human', 'gipr_human']

for index, row in data.iterrows():

    # Calculate sequence identity
    seq1 = row["ligand_pdb_seq"]
    seq2 = row["ligand_gtp_seq"]
    similarity = get_seq_similarity(seq1, seq2)
    if similarity >= 80:
        rows_to_keep.append(index)
    elif seq1 in seq2:
        rows_to_keep.append(index)
    else:
        if row["receptor"] in failed_receptors:
            print(f"Classifier id: {row['classifier_id']} – PDB reference: {row['pdb']}")
            print(f"Similarity: {similarity:.2f}")
            print(f"PDB ligand: {seq1}")
            print(f"Classifier ligand: {seq2}")
            print("")

# Drop rows
data = data.loc[rows_to_keep].copy()

# Read ranking data
ranking_data = f"{repo_dir}/classifier_subanalysis/agonist_rankings.csv"
ranking_data = pd.read_csv(ranking_data)

# Rename GPCR column to receptor 
ranking_data = ranking_data.rename(columns={
    "GPCR": "receptor", 
    "Model": "model",
    "AgonistRank": "classifier_rank"
})
ranking_data = ranking_data.drop(columns=["class"])

# Merge ranking_data with data
data = data.merge(ranking_data, on=["receptor", "model"])

# Merge the two dataframes
data.to_csv(f"{file_dir}/classifier_dockq.csv")

# Extract unique models and create a color palette
unique_models = data['model'].unique()
palette = sns.color_palette("husl", len(unique_models))
color_mapping = dict(zip(unique_models, palette))

color_mapping = {
    "RF-AA": COLOR["RF-AA"],
    "RF-AA (no templates)": COLOR["RF-AA (no templates)"],
    "AF2": COLOR["AF2"],
    "AF2 (no templates)": COLOR["AF2 (no templates)"],
    "AF2 LIS": COLOR["AF2 LIS"],
}

receptors_after = data["receptor"].unique()

# Map the colors to the models
colors = data['model'].map(color_mapping)

fig, ax = plt.subplots()
sns.lmplot(
    x='classifier_rank', 
    y='DockQ', 
    hue='model', 
    data=data, 
    palette=color_mapping, 
    aspect=1.5, 
    markers='o', 
    scatter_kws={'alpha':0.8, 's': 5}, 
    legend=False, 
    seed=42,
    line_kws={'alpha':0.5},
)

plt.rcParams['svg.fonttype'] = 'none'
plt.xlabel('Classifier Rank', fontsize=14)
plt.ylabel('DockQ Score', fontsize=14)
plt.title('DockQ Score vs Classifier Rank', fontsize=16)
plt.legend(loc='upper right', frameon=False, markerscale=2)
plt.tick_params(axis='both', which='both', direction='in')
plt.xticks(range(1, 11))
plt.axhline(y=0, color='black', linewidth=0.5, alpha=0.5, linestyle = "--")
plt.ylim(-0.025, 1)
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.tight_layout()
plt.savefig(f"{plot_dir}/dockq_vs_classifier_ranking.svg")

# Create a dataframe to store the regression results
results = []
for model in unique_models:
    subset = data[data['model'] == model]
    # Calculate Spearman rank correlation
    spearman_corr, p_value = spearmanr(subset['classifier_rank'], subset['DockQ'])

    print(f"Spearman rank correlation: {spearman_corr:.3f}, p-value: {p_value:.3f}")
    results.append((model, spearman_corr, p_value))

results_df = pd.DataFrame(results, columns=['Model', 'Spearmann_corr' , 'P-value'])
