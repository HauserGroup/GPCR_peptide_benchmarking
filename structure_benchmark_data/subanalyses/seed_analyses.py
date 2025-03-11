# Script to analyse whether extra seeds produce significantly different models
import os 
import pandas as pd
from scipy.stats import friedmanchisquare
import sys
import numpy as np
from statsmodels.stats.multitest import multipletests

def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)
    
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
    friedman_results[model] = [friedman_stat, p_value_friedman]

# Save Friedman test results
friedman_results_df = pd.DataFrame(friedman_results.items(), columns=["model", "p_value"])
friedman_results_df["chisq"] = friedman_results_df["p_value"].apply(lambda x: x[0])
friedman_results_df["p_value"] = friedman_results_df["p_value"].apply(lambda x: x[1])

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

friedman_results_df = pd.merge(friedman_results_df, sd_summary, on="model")
friedman_results_df = friedman_results_df[["model",  "DockQ_sd", "chisq", "p_value"]]

_, corrected_p_values, _, _ = multipletests(friedman_results_df['p_value'], method='fdr_bh')
friedman_results_df['P-value'] = friedman_results_df['p_value']
friedman_results_df = friedman_results_df.drop(columns=["p_value"])
friedman_results_df['Corrected P-value'] = corrected_p_values

# Apply function to all numeric columns in the DataFrame
for col in friedman_results_df.columns:
    friedman_results_df[col] = friedman_results_df[col].apply(lambda x: round_to_significant_digits(x, 4) if pd.to_numeric(x, errors='coerce') is not None else x)

friedman_results_df.to_csv(f"{repo_dir}/structure_benchmark_data/subanalyses/seed_analyses_friedman.csv", index=False)