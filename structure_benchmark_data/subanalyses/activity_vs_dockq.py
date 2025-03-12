import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import scipy.stats as stats
import sys
import requests 
import json
import numpy as np
from statsmodels.stats.multitest import multipletests


def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)

def get_ligand_data(receptor_name):
    url = f"https://gpcrdb.org/services/ligands/{receptor_name}/"
    response = requests.get(url)
    ligand_data = json.loads(response.text)
    if len(ligand_data) == 0:
        return pd.DataFrame()
    ligand_data = pd.DataFrame(ligand_data)
    ligand_data["receptor"] = receptor_name
    ligand_data = ligand_data[["receptor","Ligand name", "Activity value (Standard)", "Activity value (P)", "Value type"]]
    ligand_data.rename(columns={"Ligand name": "ligand_name"}, inplace=True)
    return ligand_data

def get_pki_data(dataset, save_path):
    if os.path.exists(save_path):
        return pd.read_csv(save_path)
    ligand_data = []
    for receptor_name in dataset["receptor"].unique():
        print("Getting ligands for: ", receptor_name)
        ligand_data.append(get_ligand_data(receptor_name))

    ligand_df = pd.concat(ligand_data)

    # Merge ligand data with DockQ data
    activity_df = pd.merge(dataset, ligand_df, on=["receptor", "ligand_name"], how="inner")

    # Keep only "Value type" == "pKi"
    activity_df = activity_df[(activity_df["Value type"] == "pKi") | (activity_df["Value type"] == "Ki")]

    # Replace "Ki" with "pKi" in "Value type" column
    activity_df["Value type"] = activity_df["Value type"].replace("Ki", "pKi")
    # Drop Activity value (Standard) column
    activity_df.drop(columns="Activity value (Standard)", inplace=True)

    # Sort data by "pdb" and "pKi" and keep only first row for each pdb
    activity_df = activity_df.sort_values(["model", "pdb", "Activity value (P)"], ascending=[True, True, False])
    activity_df = activity_df.drop_duplicates(subset=["model","pdb"], keep="first").reset_index(drop=True)
    activity_df.to_csv(save_path, index=False)

    return activity_df

# Script to analyse Dock correlations against peptide length and activity values
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
plot_dir = f"{repo_dir}/structure_benchmark_data/subanalyses/plots"
sys.path.append(repo_dir)
from colors import * 

# Read DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
dockq_df = pd.read_csv(dockq_path)
dockq_df = dockq_df[dockq_df["seed"] == 1]
dockq_df = dockq_df[["model","pdb","DockQ"]]

# Get receptor name for each pdb code
receptor_info_path = f"{repo_dir}/structure_benchmark_data/structural_benchmark_dataset.csv"
receptor_info_df = pd.read_csv(receptor_info_path)
receptor_info_df["Peptide length"] = [len(x) for x in list(receptor_info_df["ligand_pdb_seq"])]
receptor_info_df = receptor_info_df[["pdb", "receptor", "uniprot_id", "ligand_name", "Peptide length"]]

# Print how many unique receptors are in the dataset
print(f"Unique receptors: {len(receptor_info_df['receptor'].unique())}")
print(f"Unique ligands: {len(receptor_info_df['ligand_name'].unique())}")

# Merge DockQ data with receptor info
dockq_df = pd.merge(dockq_df, receptor_info_df, on="pdb", how="inner")

# Rename RFAA_no_templates to RF-AA (without templates)
dockq_df["model"] = dockq_df["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
dockq_df["model"] = dockq_df["model"].replace("RFAA", "RF-AA")
dockq_df["model"] = dockq_df["model"].replace("AF2_no_templates", "AF2 (no templates)")
dockq_df["model"] = dockq_df["model"].replace("AF3_no_templates", "AF3 (no templates)")
dockq_df["model"] = dockq_df["model"].replace("AF3_server", "AF3 (server)")

# Count how many times RF-AA DockQ score is under 0.23
print(dockq_df[(dockq_df["model"] == "RF-AA") & (dockq_df["DockQ"] < 0.23)].shape[0])
print(dockq_df[(dockq_df["model"] == "RF-AA (no templates)") & (dockq_df["DockQ"] < 0.23)].shape[0])

print("Failed AF3 models:")
print("AF3 with templates: ",dockq_df[(dockq_df["model"] == "AF3") & (dockq_df["DockQ"] < 0.23)].shape[0])
print("AF3 without templates: ",dockq_df[(dockq_df["model"] == "AF3 (no templates)") & (dockq_df["DockQ"] < 0.23)].shape[0])
print("AF3 server: ", dockq_df[(dockq_df["model"] == "AF3 (server)") & (dockq_df["DockQ"] < 0.23)].shape[0])

# Print failed AF2 models
print("Failed AF2 models:")
print("AF2 with templates: ",dockq_df[(dockq_df["model"] == "AF2") & (dockq_df["DockQ"] < 0.23)].shape[0])
print(dockq_df[(dockq_df["model"] == "AF2") & (dockq_df["DockQ"] < 0.23)]["pdb"].values)
print("AF2 without templates: ",dockq_df[(dockq_df["model"] == "AF2 (no templates)") & (dockq_df["DockQ"] < 0.23)].shape[0])
print(dockq_df[(dockq_df["model"] == "AF2 (no templates)") & (dockq_df["DockQ"] < 0.23)]["pdb"].values)

# Get activity data from GPCRdb
activity_df = get_pki_data(dockq_df, f"{repo_dir}/structure_benchmark_data/subanalyses/activity_data.csv")

###############################
### PEPTIDE LENGTH VS DOCKQ ###
###############################

# Create a figure
fig, ax = plt.subplots(figsize=(13, 7))

# Color the points based on model
custom_color_mapping = {
    'NeuralPLexer' : COLOR["NeuralPLexer"],
    'ESMFold': COLOR["ESMFold"],
    'RF-AA': COLOR["RF-AA"], 
    'RF-AA (no templates)': COLOR["RF-AA (no templates)"], 
    'Chai-1': COLOR["Chai-1"],
    'AF2': COLOR["AF2"], 
    'AF2 (no templates)': COLOR["AF2 (no templates)"],
    'AF3': COLOR["AF3"],
    'AF3 (no templates)': COLOR["AF3 (no templates)"],
    'AF3 (server)': COLOR["AF3 (server)"]
} 

model_names = list(dockq_df["model"].keys())

# Plot each model separately with its own color and shape
for model in custom_color_mapping.keys():
    model_data = dockq_df[dockq_df["model"] == model]
    ax.scatter(
        model_data['Peptide length'], 
        model_data['DockQ'], 
        c=custom_color_mapping[model], 
        s=10, 
        alpha=0.8, 
        label=model
    )

    # Add regression lines with confidence intervals
    sns.regplot(
        x=model_data['Peptide length'], 
        y=model_data['DockQ'], 
        scatter=False,  # Scatter is already plotted
        color=custom_color_mapping[model], 
        ci=95,  # Confidence interval (95%)
        line_kws={"linewidth": 2}  # Customize the regression line
    )

# Add grid
ax.grid(color='gray', linestyle='-', linewidth=0.25)

# Add labels and title using the font properties object
ax.set_xlabel('Peptide length', fontsize = 14)
ax.set_ylabel('DockQ score', fontsize = 14)

# Edit ticks
ax.tick_params(axis="y",direction="in")
ax.tick_params(axis="x",direction="in")

# Customize legend
legend = ax.legend(
    title="Model", 
    facecolor="white", 
    fontsize=16, 
    framealpha=1, 
    loc="center left", 
    bbox_to_anchor=(1, 0.5), 
    handletextpad=0.0, 
    borderaxespad=0.1,
    borderpad=0.1,
    labelspacing=0.2
)
legend.get_title().set_fontproperties(fm.FontProperties(size=0))
frame = legend.get_frame()
frame.set_linewidth(0.0)  

ax.title.set_text(f"DockQ vs Peptide Length (n={dockq_df['pdb'].nunique()})")
ax.title.set_fontsize(16)

# Save the plot
plt.ylim(0, 1)
plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()
plt.savefig(f"{plot_dir}/DockQ_vs_PeptideLength.png", dpi=600)

# Loop through each model and calculate the Pearson correlation between LIS and DockQ
results = []
for model in dockq_df["model"].unique():
    model_data = dockq_df[dockq_df['model'] == model]
    correlation, p_value = stats.pearsonr(model_data['Peptide length'], model_data['DockQ'])
    results.append([model, correlation, p_value])

results_df = pd.DataFrame(results, columns=["Model", "Pearson correlation", "P-value"])
_, corrected_p_values, _, _ = multipletests(results_df['P-value'], method='fdr_bh')
results_df['Corrected P-value'] = corrected_p_values

for col in results_df.columns:
    results_df[col] = results_df[col].apply(lambda x: round_to_significant_digits(x, 4) if pd.to_numeric(x, errors='coerce') is not None else x)

results_df.to_csv(f"{repo_dir}/structure_benchmark_data/subanalyses/peptide_length_vs_dockq.csv", index=False)

###############################
###    ACTIVTIY VS DOCKQ    ###
###############################

# Rename Activity value (P) to pKi
activity_df.rename(columns={"Activity value (P)": "pKi"}, inplace=True)
activity_df["pKi"] = activity_df["pKi"].astype(float)

# Create a figure
fig, ax = plt.subplots(figsize=(13, 7))

# Color the points based on model
custom_color_mapping = {
    'NeuralPLexer' : COLOR["NeuralPLexer"],
    'ESMFold': COLOR["ESMFold"],
    'RF-AA': COLOR["RF-AA"], 
    'RF-AA (no templates)': COLOR["RF-AA (no templates)"], 
    'Chai-1': COLOR["Chai-1"],
    'AF2': COLOR["AF2"], 
    'AF2 (no templates)': COLOR["AF2 (no templates)"],
    'AF3': COLOR["AF3"],
    'AF3 (no templates)': COLOR["AF3 (no templates)"],
    'AF3 (server)': COLOR["AF3 (server)"]
} 

model_names = list(activity_df["model"].keys())

# Plot each model separately with its own color and shape
for model in custom_color_mapping.keys():
    model_data = activity_df[activity_df["model"] == model]
    ax.scatter(
        model_data['pKi'], 
        model_data['DockQ'], 
        c=custom_color_mapping[model], 
        s=10, 
        alpha=0.8, 
        label=model
    )

    # Add regression lines with confidence intervals
    sns.regplot(
        x=model_data['pKi'], 
        y=model_data['DockQ'], 
        scatter=False,  # Scatter is already plotted
        color=custom_color_mapping[model], 
        ci=95,  # Confidence interval (95%)
        line_kws={"linewidth": 2}  # Customize the regression line
    )

# Add grid
ax.grid(color='gray', linestyle='-', linewidth=0.25)

# Add labels and title using the font properties object
ax.set_xlabel('pKi', fontsize = 14)
ax.set_ylabel('DockQ score', fontsize = 14)

# Edit ticks
ax.tick_params(axis="y",direction="in")
ax.tick_params(axis="x",direction="in")

# Customize legend
legend = ax.legend(
    title="Model", 
    facecolor="white", 
    fontsize=16, 
    framealpha=1, 
    loc="center left", 
    bbox_to_anchor=(1, 0.5), 
    handletextpad=0.0, 
    borderaxespad=0.1,
    borderpad=0.1,
    labelspacing=0.2
)
legend.get_title().set_fontproperties(fm.FontProperties(size=0))
frame = legend.get_frame()
frame.set_linewidth(0.0)  

ax.title.set_text(f"DockQ vs pKi (n={activity_df['pdb'].nunique()})")
ax.title.set_fontsize(16)

# Save the plot
plt.ylim(0, 1)
plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()
plt.savefig(f"{plot_dir}/DockQ_vs_pKi.png", dpi=600)

# Loop through each model and calculate the Pearson correlation between LIS and DockQ
results = []
for model in activity_df["model"].unique():
    model_data = activity_df[activity_df['model'] == model]
    correlation, p_value = stats.pearsonr(model_data['pKi'], model_data['DockQ'])
    results.append([model, correlation, p_value])

results_df = pd.DataFrame(results, columns=["Model", "Pearson correlation", "P-value"])
_, corrected_p_values, _, _ = multipletests(results_df['P-value'], method='fdr_bh')
results_df['Corrected P-value'] = corrected_p_values

for col in results_df.columns:
    results_df[col] = results_df[col].apply(lambda x: round_to_significant_digits(x, 4) if pd.to_numeric(x, errors='coerce') is not None else x)

results_df.to_csv(f"{repo_dir}/structure_benchmark_data/subanalyses/activity_vs_dockq.csv", index=False)