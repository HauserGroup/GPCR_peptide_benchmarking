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
import glob
import json

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
chai1_runtime_path = f"{repo_dir}/structure_benchmark/Chai-1"
af3_runtime_path = f"{repo_dir}/structure_benchmark/AF3"
af3_runtime_no_templates_path = f"{repo_dir}/structure_benchmark/AF3_no_templates"
af2_runtime_path = f"{repo_dir}/structure_benchmark/AF2"
af2_runtime_no_templates_path = f"{repo_dir}/structure_benchmark/AF2_no_templates"
neuralplexer_runtime_path = f"{repo_dir}/structure_benchmark/NeuralPLexer/NeuralPLexer_runtimes.txt"
neuralplexer_folder_path = f"{repo_dir}/structure_benchmark/NeuralPLexer"

def get_neuralplexer_runtimes(filepath, folderpath, avg = True):
    runtime_dict = {}
    pattern = re.compile(r"Processed (.+?) in (\d+) seconds")

    # List pdb files in folderpath
    pdb_files = [f for f in os.listdir(folderpath) if f.endswith(".pdb")]

    # Open file
    with open(filepath, "r") as f:
        lines = f.readlines()
        
    for line in lines:
        match = pattern.search(line)
        if match and match.group(1) + ".pdb" in pdb_files:
            pdb_code = match.group(1)
            runtime = float(match.group(2))
            runtime_dict[pdb_code] = runtime
            if avg:
                runtime_dict[pdb_code] /= 16
    
    return runtime_dict

def get_af2_total_runtime(timings_json, avg = True):

    with open(timings_json, "r") as f:
        timings = json.load(f)

    total_time = 0
    c = 0
    for key in timings:
        if "predict_and_compile_model" in key:
            c += 1
            total_time += timings[key]
    
    # Get average
    if c > 0 and avg:
        total_time /= c

    return total_time

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
            if not os.path.exists(f"{model_dir}/{file_name}.pdb"):
                print(f"{model_dir}/{file_name}.pdb does not exist")
                continue
            runtime_dict[file_name] = runtime
    
    return runtime_dict


def parse_chai_runtime(folder_path, avg = True):
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
                        if avg:
                            runtime_dict[file_name] /= 5
    
    return runtime_dict


def parse_alphafold3_runtime(folder_path, avg = True):
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
                        if avg:
                            runtime_dict[model_name.upper().split("_")[0]] /= 5
    
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


# List timings.json files in the subdirectories of the above two folders and parse them
# to get the runtimes for each model
af2_timings = glob.glob(f"{af2_runtime_path}/*/timings.json")
af2_no_templates_timings = glob.glob(f"{af2_runtime_no_templates_path}/*/timings.json")

# List AF2 models run on A100
af2_a100 = {}
dir_path = f"{repo_dir}/structure_benchmark/AF2/*/AF_pred*.txt"
log_files = glob.glob(dir_path)
log_files.sort(key=lambda x: int(x.split("/")[-2].split("_")[1]))
for file in log_files:
    pdb_code = file.split("/")[-2].split("_")[0]
    with open(file, 'r') as f:
        lines = f.readlines()
        if "node263.cluster" in lines[4] and pdb_code not in af2_a100:
            af2_a100[pdb_code] = file.split("/")[-2] 

# List AF2 models run on A100
af2_no_templates_a100 = {}
dir_path = f"{repo_dir}/structure_benchmark/AF2_no_templates/*/AF_pred*.txt"
log_files = glob.glob(dir_path)
log_files.sort(key=lambda x: int(x.split("/")[-2].split("_")[1]))
for file in log_files:
    pdb_code = file.split("/")[-2].split("_")[0]
    with open(file, 'r') as f:
        lines = f.readlines()
        if "node263.cluster" in lines[4] and pdb_code not in af2_no_templates_a100:
            af2_no_templates_a100[pdb_code] = file.split("/")[-2] 

# Keep only af2_timings that were run on A100
af2_timings = [timings for timings in af2_timings if timings.split("/")[-2] in af2_a100.values()]
af2_no_templates_timings = [timings for timings in af2_no_templates_timings if timings.split("/")[-2] in af2_no_templates_a100.values()]

af2 = {}
af2_no_templates = {}

for timings_file in af2_timings:
    model = os.path.basename(os.path.dirname(timings_file)).split("_1")[0].upper()
    af2[model] = get_af2_total_runtime(timings_file)

for timings_file in af2_no_templates_timings:
    model = os.path.basename(os.path.dirname(timings_file)).split("_1")[0].upper()
    af2_no_templates[model] = get_af2_total_runtime(timings_file)

# Get neuralplexer runtimes
neuralplexer_runtimes = get_neuralplexer_runtimes(neuralplexer_runtime_path, neuralplexer_folder_path)
    

# Make a dataframe from the runtimes
rfaa_df = pd.DataFrame(rfaa_with_templates.items(), columns=["Model", "Runtime"])
rfaa_no_templates_df = pd.DataFrame(rfaa_no_templates.items(), columns=["Model", "Runtime"])
esm_df = pd.DataFrame(esmfold.items(), columns=["Model", "Runtime"])
chai_df = pd.DataFrame(chai1.items(), columns=["Model", "Runtime"])
af3_df = pd.DataFrame(af3.items(), columns=["Model", "Runtime"])
af3_no_templates_df = pd.DataFrame(af3_no_templates.items(), columns=["Model", "Runtime"])
af2_df = pd.DataFrame(af2.items(), columns=["Model", "Runtime"])
af2_no_templates_df = pd.DataFrame(af2_no_templates.items(), columns=["Model", "Runtime"])
neuralplexer_df = pd.DataFrame(neuralplexer_runtimes.items(), columns=["Model", "Runtime"])

# Add the model type to the dataframes
rfaa_df["Model Type"] = "RF-AA"
rfaa_no_templates_df["Model Type"] = "RF-AA\n(no templates)"
esm_df["Model Type"] = "ESMFold"
chai_df["Model Type"] = "Chai-1"
af3_df["Model Type"] = "AF3"
af3_no_templates_df["Model Type"] = "AF3\n(no templates)"
af2_df["Model Type"] = "AF2"
af2_no_templates_df["Model Type"] = "AF2\n(no templates)"
neuralplexer_df["Model Type"] = "NeuralPLexer"

colors = {
    'NeuralPLexer' : COLOR["NeuralPLexer"],
    'ESMFold': COLOR["ESMFold"],
    'RF-AA': COLOR["RF-AA"], 
    'RF-AA\n(no templates)': COLOR["RF-AA (no templates)"], 
    'Chai-1': COLOR["Chai-1"],
    'AF2': COLOR["AF2"], 
    'AF2\n(no templates)': COLOR["AF2 (no templates)"],
    'AF3': COLOR["AF3"],
    'AF3\n(no templates)': COLOR["AF3 (no templates)"],
} 

# Concatenate the dataframes
all_runtimes = pd.concat([neuralplexer_df, esm_df, rfaa_df, rfaa_no_templates_df, chai_df, af2_df, af2_no_templates_df, af3_df, af3_no_templates_df])

### Plot the runtimes

# Get consistent order
model_order = all_runtimes["Model Type"].unique()

# Create figure
fig, ax = plt.subplots()

# Swarm plot (dots)
sns.swarmplot(
    data=all_runtimes,
    x="Model Type",
    y="Runtime",
    hue="Model Type",
    dodge=False,  # Prevent offset
    ax=ax,
    size=1.5,
    palette=colors,
    order=model_order, 
    hue_order=model_order,
    zorder=3  # Ensure dots appear above error bars
)

# Bar plot (invisible bars, just for error bars)
sns.barplot(
    x="Model Type",
    y="Runtime",
    hue="Model Type",
    data=all_runtimes,
    capsize=0.5,
    alpha=0.2,  # Make bars invisible
    ax=ax,
    err_kws={'linewidth': 1.0},
    legend=False,
    palette=colors,
    order=model_order, 
    hue_order=model_order
)

plt.rcParams['svg.fonttype'] = 'none'
plt.ylim(0, 200)
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