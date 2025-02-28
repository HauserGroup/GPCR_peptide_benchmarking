# Analysing and plotting the runtimes of different models in the benchmark dataset
import pandas as pd
import os
import re
import sys 
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
import itertools
from statsmodels.stats.multitest import multipletests
import numpy as np

file_dir = os.getcwd()
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

sys.path.append(repo_dir)
from colors import * 

# Paths to the runtime files and models
rfaa_runtime_path = f"{repo_dir}/structure_benchmark/RFAA_runtimes.txt"
rfaa_model_path = f"{repo_dir}/structure_benchmark/"
rfaa_model_no_templates_path = f"{repo_dir}/structure_benchmark/RFAA_no_templates"
esm_runtime_path = f"{repo_dir}/structure_benchmark/ESMFold/ESMfold_241608_out.txt"
esm_model_path = f"{repo_dir}/structure_benchmark/ESMFold"
af3_runtime_path = f"{repo_dir}/structure_benchmark/AF3"
af3_runtime_no_templates_path = f"{repo_dir}/structure_benchmark/AF3_no_templates"

af2_runtime_path = f"{repo_dir}/structure_benchmark/AF2"
af2_runtime_no_templates_path = f"{repo_dir}/structure_benchmark/AF2_no_templates"

chai1_runtime_path = f"{repo_dir}/structure_benchmark/Chai-1"

# ADD NEURALPLEXER RUNTIMES
# ADD AF2 RUNTIMES

def parse_esm_rfaa_runtimes(filepath, model_dir):
    runtime_dict = {}
    pattern_yaml = re.compile(r"Runtime for (.+?): (\d+) seconds")
    pattern_fasta = re.compile(r"Processed (.+?) with seed \d+ in (\d+) seconds")
    
    with open(filepath, "r") as f:
        lines = f.readlines()

    for line in lines:
        match_yaml = pattern_yaml.search(line)
        match_fasta = pattern_fasta.search(line)
        
        if match_yaml:
            file_path = match_yaml.group(1)
            runtime = float(match_yaml.group(2))
            file_name = file_path.split('/')[-1].split('.')[0]  # Extract filename without extension
            if "no_templates" in file_name:
                model_subdir = "RFAA_no_templates"
            else:
                model_subdir = "RFAA"
            if file_name + ".pdb" not in os.listdir(model_dir + "/" + model_subdir):
                continue
            runtime_dict[file_name] = runtime
        elif match_fasta:
            file_path = match_fasta.group(1)
            runtime = float(match_fasta.group(2))
            file_name = file_path.split('/')[-1].split('.')[0]  # Extract filename without extension
            if not os.path.exists(f"{model_dir}/{file_name}/{file_name}.pdb"):
                print(f"{model_dir}/{file_name}/{file_name}.pdb does not exist")
                continue
            runtime_dict[file_name] = runtime
    
    return runtime_dict


def parse_chai_runtime(folder_path):
    runtime_dict = {}
    pattern = re.compile(r"Done running inference for (.+?) in (\d+) seconds")
    
    for root, _, files in os.walk(folder_path):
        if "pred.model_idx_4.cif" not in files:
            continue  # Skip folders without the required file
        
        for filename in files:
            if filename.endswith("_out.txt") and "_1_" in filename:
                with open(os.path.join(root, filename), "r") as f:
                    lines = f.readlines()
                    
                for line in lines:
                    match = pattern.search(line)
                    if match:
                        file_path = match.group(1)
                        runtime = float(match.group(2))
                        file_name = file_path.split('/')[-1].split('.')[0]  # Extract filename without extension
                        runtime_dict[file_name] = runtime
    
    return runtime_dict


def parse_alphafold3_runtime(folder_path):
    runtime_dict = {}
    pattern = re.compile(r"Running model inference and extracting output structures for seeds .* took\s+(\d+\.\d+) seconds")
    
    for root, _, files in os.walk(folder_path):
        if not any(file.endswith("_model.cif") for file in files):
            continue  # Skip folders without a "*_model.cif" file
        
        for filename in files:
            if filename.endswith("_log.txt"):
                model_name = os.path.basename(root)
                if not model_name.endswith("_1"):
                    continue

                with open(os.path.join(root, filename), "r") as f:
                    lines = f.readlines()
                    
                for line in lines:
                    match = pattern.search(line)
                    if match:
                        runtime = float(match.group(1))
                        runtime_dict[model_name.upper().split("_")[0]] = runtime
    
    return runtime_dict

def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)

def significance_stars(p):
    if p < 0.0001:
        return '****'
    elif p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'ns'

def get_significance(data, variable, model_col='model', pdb_col='pdb'):
    # Order dataframe by model and then by PDB code
    data = data.sort_values(by=[model_col, pdb_col])

    # Perform pairwise Wilcoxon signed-rank tests between all models
    results = []
    for model1, model2 in itertools.combinations(data[model_col].unique(), 2):
        # Get subset of data for each model
        var1 = data[data[model_col] == model1][[variable, pdb_col, model_col]].dropna()
        var2 = data[data[model_col] == model2][[variable, pdb_col, model_col]].dropna()

        # Merge the two subsets on PDB code
        merged = var1.merge(var2, on=pdb_col, suffixes=(f'_{model1}', f'_{model2}'))

        if merged.shape[0] < 2:
            # Skip if there are not enough data points for the test
            continue

        try:
            stat, p_value = wilcoxon(merged[f'{variable}_{model1}'], merged[f'{variable}_{model2}'])
        except ValueError:
            # Skip this pair if Wilcoxon test fails
            continue

        # Calculate averages and standard errors
        avg_1 = var1[variable].mean()
        se_1 = var1[variable].sem()
        avg_2 = var2[variable].mean()
        se_2 = var2[variable].sem()

        results.append((model1, model2, avg_1, se_1, avg_2, se_2, stat, p_value))

    # Create a DataFrame from the results
    results_df = pd.DataFrame(results, columns=[
        'Model1', 'Model2', f'Model1_Avg_{variable}', f'Model1_SE_{variable}', 
        f'Model2_Avg_{variable}', f'Model2_SE_{variable}', 'Statistic', 'P-value'
    ])

    # Apply Benjamini-Hochberg correction and add corrected p-values to the DataFrame
    if not results_df.empty:
        _, corrected_p_values, _, _ = multipletests(results_df['P-value'], method='fdr_bh')
        results_df['Corrected P-value'] = corrected_p_values

        # Round the p-values and apply the function to create a new column with significance stars
        results_df['P-value'] = results_df['P-value'].apply(lambda x: round(x, 10))
        results_df['Corrected P-value'] = results_df['Corrected P-value'].apply(lambda x: round(x, 10))
        results_df['Significance'] = results_df['Corrected P-value'].apply(significance_stars)

        # Apply function to all numeric columns in the DataFrame
        for col in results_df.columns:
            results_df[col] = results_df[col].apply(lambda x: round_to_significant_digits(x, 4) if pd.to_numeric(x, errors='coerce') is not None else x)

        # Save the results to a CSV file
        results_df.to_csv(f'{repo_dir}/structure_benchmark_data/wilcoxon_results_{variable}.csv', index=False)
    else:
        print(f"No valid comparisons for {variable}")

rfaa_runtimes = parse_esm_rfaa_runtimes(rfaa_runtime_path, rfaa_model_path)
rfaa_no_templates = {k: v for k, v in rfaa_runtimes.items() if "no_templates" in k}
rfaa_with_templates = {k: v for k, v in rfaa_runtimes.items() if "no_templates" not in k}
esmfold = parse_esm_rfaa_runtimes(esm_runtime_path, esm_model_path)
chai1 = parse_chai_runtime(chai1_runtime_path)
af3 = parse_alphafold3_runtime(af3_runtime_path)
af3_no_templates = parse_alphafold3_runtime(af3_runtime_no_templates_path)

# Make a dataframe from the runtimes
rfaa_df = pd.DataFrame(rfaa_with_templates.items(), columns=["Model", "Runtime"])
rfaa_no_templates_df = pd.DataFrame(rfaa_no_templates.items(), columns=["Model", "Runtime"])
esm_df = pd.DataFrame(esmfold.items(), columns=["Model", "Runtime"])
chai_df = pd.DataFrame(chai1.items(), columns=["Model", "Runtime"])
af3_df = pd.DataFrame(af3.items(), columns=["Model", "Runtime"])
af3_no_templates_df = pd.DataFrame(af3_no_templates.items(), columns=["Model", "Runtime"])

# Add the model type to the dataframes
rfaa_df["Model Type"] = "RF-AA"
rfaa_no_templates_df["Model Type"] = "RF-AA (no templates)"
esm_df["Model Type"] = "ESMFold"
chai_df["Model Type"] = "Chai-1"
af3_df["Model Type"] = "AF3"
af3_no_templates_df["Model Type"] = "AF3 (no templates)"

# Concatenate the dataframes
all_runtimes = pd.concat([rfaa_df, rfaa_no_templates_df, esm_df, chai_df, af3_df, af3_no_templates_df])

### Plot the runtimes

# Get consistent order
model_order = all_runtimes["Model Type"].unique()

# Create figure
fig, ax = plt.subplots()

# Bar plot (invisible bars, just for error bars)
sns.barplot(
    x="Model Type",
    y="Runtime",
    hue="Model Type",
    data=all_runtimes,
    capsize=0.5,
    alpha=0.0,  # Make bars invisible
    ax=ax,
    err_kws={'linewidth': 1.0},
    legend=False,
    palette=COLOR,
    order=model_order, 
    hue_order=model_order
)

# Swarm plot (dots)
sns.swarmplot(
    data=all_runtimes,
    x="Model Type",
    y="Runtime",
    hue="Model Type",
    dodge=False,  # Prevent offset
    ax=ax,
    size=1.5,
    palette=COLOR,
    order=model_order, 
    hue_order=model_order,
    zorder=3  # Ensure dots appear above error bars
)

plt.rcParams['svg.fonttype'] = 'none'
plt.ylim(0, 500)
plt.title("Runtime comparison between different models")
ax.set_xlabel("")
plt.ylabel("Runtime (seconds)", fontsize="large")
plt.xticks(rotation=90)

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Make ticks go inwards
ax.tick_params(axis='x', direction='in')
ax.tick_params(axis='y', direction='in')
plt.tight_layout()
plt.savefig(f"{repo_dir}/structure_benchmark_data/plots/runtime_comparison.svg", format="svg")
plt.close()

# Statistical analysis of the runtimes
all_runtimes["Model"] = all_runtimes["Model"].str.upper()
all_runtimes["Model"] = [i.split("_")[0] for i in all_runtimes["Model"]]
all_runtimes.to_csv(f'{repo_dir}/structure_benchmark_data/model_runtimes.csv', index=False)

# Perform Wilcoxon signed-rank tests for DockQ scores
all_runtimes = all_runtimes.rename(columns={"Model": "pdb", "Model Type": "model", "Runtime": "Runtime"})
get_significance(all_runtimes, 'Runtime')