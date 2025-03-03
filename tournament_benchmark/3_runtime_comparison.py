# Script to read timings.json files from different run setups and plot them
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pandas as pd
import seaborn as sns
from scipy.stats import wilcoxon

def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)
    
def get_total_time(timings):
    total_time = 0
    c = 0
    for key in timings:
        if "predict_and_compile_model" in key:
            c += 1
            total_time += timings[key]
    
    # Get average
    if c > 0:
        total_time /= c

    return total_time

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
json_dir = f"{repo_dir}/tournament_benchmark/"

# Add the repository directory to the path
sys.path.append(repo_dir)
from colors import *

# Make a directory to save the plots
plot_dir = f'{file_dir}/plots'
os.makedirs(plot_dir, exist_ok=True)

# Setup names for the different runs
setups = ["one_to_two", "one_to_four", "one_to_eight", "one_to_ten"]

# Read the timings.json files from the different setups
timings = {}
results = []
for setup in setups:
    setup_folder = f"{json_dir}/{setup}"
    subfolders = [f.path for f in os.scandir(setup_folder) if f.is_dir()]

    # Calculate runtime for each subfolder
    for subfolder in subfolders:
        receptor = subfolder.split("/")[-1].split("_")[0]
        with open(f"{subfolder}/timings.json", "r") as f:
            timings[subfolder] = json.load(f)

        with open(f"{subfolder}/msas/chain_id_map.json", "r") as f:
            chains = json.load(f)
            ligands = []
            for chain in chains:
                if "_" in chains[chain]["description"]:
                    continue
                else:
                    ligands.append(chains[chain]["description"])

        results.append([setup, receptor, ligands, get_total_time(timings[subfolder]), True])

# Create a pandas dataframe from the runtime results
df = pd.DataFrame(results, columns=["Setup", "Receptor", "Ligands", "Time", "Tournament"])

# Read the timings.json files from the baseline setup
results_baseline = []
for index, row in df.iterrows():
    baseline_time = 0
    for ligand in row["Ligands"]:
        baseline_model = f"{json_dir}/baseline/{row['Receptor']}_human___{ligand}/timings.json"
        with open(baseline_model, "r") as f:
            baseline_time += get_total_time(json.load(f))

    results_baseline.append([row["Setup"], row["Receptor"], row["Ligands"], baseline_time, False])

df_baseline = pd.DataFrame(results_baseline, columns=["Setup", "Receptor", "Ligands", "Time", "Tournament"])
df_merged = pd.concat([df, df_baseline])

# Replace the setup names with more descriptive names
df_merged["Setup"] = df_merged["Setup"].replace({
    "one_to_two": "1:2",
    "one_to_four": "1:4",
    "one_to_eight": "1:8",
    "one_to_ten": "1:10"
})

# Make time into minutes
df_merged["Time_min"] = df_merged["Time"] / 60

# Calculate the means and standard deviations for error bars by setup and tournament
grouped_stats = df_merged.groupby(["Setup", "Tournament"])["Time_min"].agg(["mean", "std"]).reset_index()

# Make a swarm plot to show the timings for each setup
fig, ax = plt.subplots()
ax = sns.swarmplot(
    data=df_merged,
    x="Setup",
    y="Time_min",
    hue="Tournament",
    dodge=True,
    ax=ax,
    size=1.5,
    palette=["#0b3d91", "#f9aa43"]
)

sns.barplot(
    x="Setup",
    y="Time_min",
    hue="Tournament",
    data=df_merged,
    capsize=0.5,
    alpha=0.0,
    ax=ax,
    err_kws={'linewidth': 1.0},
    legend=False
)

plt.rcParams['svg.fonttype'] = 'none'
plt.ylim(0, 50)
plt.title("Runtime comparison between tournament and one-to-zero setups\n")
plt.xlabel("Principal agonist-to-decoy peptides ratio")
plt.ylabel("Average runtime per prediction (min)", fontsize="large")
plt.savefig(f"{plot_dir}/timings.svg", format="svg")
plt.close()

# Use paired Wilcoxon signed-rank test to compare the tournament and baseline timings
wilcoxon_results = []
for setup in df_merged["Setup"].unique():
    df_merged = df_merged.sort_values(by=["Receptor"])
    tournament_times = df_merged[(df_merged["Setup"] == setup) & (df_merged["Tournament"] == True)]["Time"]
    baseline_times = df_merged[(df_merged["Setup"] == setup) & (df_merged["Tournament"] == False)]["Time"]
    stat, p_val = wilcoxon(tournament_times, baseline_times)
    wilcoxon_results.append([setup, tournament_times.mean(), baseline_times.mean(), stat, p_val])

# Create a pandas dataframe from the Wilcoxon results and save to csv
wilcoxon_df = pd.DataFrame(wilcoxon_results, columns=["Setup", "Tournament time (s)", "Baseline time (s)", "Statistic", "p-value"])
wilcoxon_df["Setup"] = pd.Categorical(wilcoxon_df["Setup"], ["1:2", "1:4", "1:8", "1:10"])
wilcoxon_df = wilcoxon_df.sort_values("Setup")
for col in wilcoxon_df.columns:
    wilcoxon_df[col] = wilcoxon_df[col].apply(lambda x: round_to_significant_digits(x, 6) if pd.to_numeric(x, errors='coerce') is not None else x)
wilcoxon_df.to_csv(f"{json_dir}/tournament_runtime_wilcoxon.csv", index=False)