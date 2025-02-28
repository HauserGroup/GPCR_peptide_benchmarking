# Analysing and plotting the runtimes of different models in the benchmark dataset
import pandas as pd
import os
import re
import sys 

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

print(all_runtimes)

# Plot the runtimes
import seaborn as sns
import matplotlib.pyplot as plt

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
plt.title("Runtime comparison between different models\n")
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
