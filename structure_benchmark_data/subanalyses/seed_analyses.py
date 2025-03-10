# Script to analyse whether extra seeds produce significantly different models
import os 
import pandas as pd
from scipy.stats import friedmanchisquare
import sys

# Script to analyse Dock correlations against peptide length and activity values
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
plot_dir = f"{repo_dir}/structure_benchmark_data/plots"
sys.path.append(repo_dir)
from colors import * 

# Read DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
dockq_df = pd.read_csv(dockq_path)
dockq_df = dockq_df[["model","pdb","seed","DockQ"]]
dockq_df = dockq_df[dockq_df["model"].isin(["AF2", "AF3", "AF2_no_templates", "AF3_no_templates", "Chai-1"])]

# Use Friedman test to compare models with different seeds
friedman_results = {}

for model in dockq_df["model"].unique():
    model_df = dockq_df[dockq_df["model"] == model]
    
    # Pivot data: Rows = pdb structures, Columns = seeds, Values = DockQ scores
    pivot_df = model_df.pivot(index="pdb", columns="seed", values="DockQ")
    
    # Friedman test (non-parametric alternative)
    friedman_stat, p_value_friedman = friedmanchisquare(*pivot_df.T.values)
    friedman_results[model] = p_value_friedman

print("\nFriedman test results:")
for model, p_value in friedman_results.items():
    print(f"{model}: {p_value}")

# Make a summary table that computes average DockQ for each model and input
summary_results = []
for model in dockq_df["model"].unique():
    for pdb in dockq_df["pdb"].unique():
        model_df = dockq_df[(dockq_df["model"] == model) & (dockq_df["pdb"] == pdb)]
        avg_seed = model_df["DockQ"].mean()
        sd_seed = model_df["DockQ"].std()
        min_seed = model_df["DockQ"].min()
        max_seed = model_df["DockQ"].max()
        summary_results.append([model, pdb, avg_seed, sd_seed, min_seed, max_seed])

# Save summary of DockQ scores
summary_df = pd.DataFrame(summary_results, columns=["model", "pdb", "DockQ_avg", "DockQ_sd", "DockQ_min", "DockQ_max"])
summary_df.to_csv(f"{repo_dir}/structure_benchmark_data/subanalyses/seed_analyses_summary.csv", index=False)

# Save summary of DockQ score SDs per model
sd_summary = summary_df.groupby("model")["DockQ_sd"].mean()
sd_summary = sd_summary.round(6)
sd_summary.to_csv(f"{repo_dir}/structure_benchmark_data/subanalyses/seed_analyses_sds.csv")