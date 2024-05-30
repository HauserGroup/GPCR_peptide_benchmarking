import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve
import matplotlib.font_manager as fm

def get_closest_training_structures(input_path):
    # List files in the input directory
    files = os.listdir(input_path)
    results_per_pdb = {}

    # Loop through the files
    for file in files:
        # Check if the file is a .msa file
        if file.endswith(".m8"):
            # Define the full path to the file
            full_path = os.path.join(input_path, file)
            # Print the full path
            print(full_path)

        # Read first line of the file
        with open(full_path, "r") as f:
            line = f.readline()
            print(line)
            # Split the line by whitespace
            parts = line.split("\t")
            # Extract the e-value
            e_value = float(parts[10])
            identity = float(parts[2])
            # Print the e-value
            print(f"Closest training structure for {file} is {parts[1]} with e-value of {e_value}." ) 

            # Extract the PDB code from the filename
            pdb_code = file.split(".")[0]
            pdb_code = pdb_code.split("_")[0]
            # Store the e-value in the dictionary
            results_per_pdb[pdb_code] = [e_value, identity]

    # Make dictionary into dataframe with columns pdb, e_value, and identity
    df = pd.DataFrame.from_dict(results_per_pdb, orient='index', columns=['e_value', 'identity'])
    df.reset_index(inplace=True)
    df.columns = ['pdb', 'e_value', 'identity']

    return df

def calculate_average_plddt(pdb_file_path):
    """
    Calculate the average plddt score from a PDB file.

    Parameters:
    - pdb_file_path (str): Path to the PDB file.

    Returns:
    - float: Average plddt score.
    """

    try:
        # Open the PDB file and extract plddt scores (adjust as needed)
        with open(pdb_file_path, 'r') as pdb_file:
            plddt_scores = []
            for line in pdb_file:
                if line.startswith("ATOM") and line[12:16].strip() == "CA":
                    plddt_score = float(line[60:66].strip())
                    plddt_scores.append(plddt_score)

        # Calculate the average plddt score
        if plddt_scores:
            average_plddt = sum(plddt_scores) / len(plddt_scores)
            return average_plddt
        else:
            print("No plddt scores found in the PDB file.")
            return None

    except FileNotFoundError:
        print(f"Error: File '{pdb_file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Input paths to the search results
rfaa_input_path = "/projects/ilfgrid/people/pqh443/rfaa_training_db/search_results"
af_input_path="/projects/ilfgrid/people/pqh443/alphafold_training_db/search_results"

# Get the closest training structures
af_training_struct = get_closest_training_structures(af_input_path)
rfaa_training_struct = get_closest_training_structures(rfaa_input_path)

# Path to the DockQ results file
dockq_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results_new.csv"
data = pd.read_csv(dockq_path)

# Get only AF2, AF3 and RFAA models
#for model in ['AF2', 'AF2_no_templates' 'AF3', 'RFAA', 'RFAA_no_templates']:
model = "AF2"

data = data[data['model'] == model]

if "AF" in model:
    data = data.merge(af_training_struct, left_on='pdb', right_on='pdb', how='left')
elif "RFAA" in model:
    data = data.merge(rfaa_training_struct, left_on='pdb', right_on='pdb', how='left')
else:
    print("Model not recognized.")

for pdb in data['pdb']:
    if model == "RFAA":
        model_name = "RFAA_chain"
    else:
        model_name = model
    pdb_file_path = f"/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/{model_name}/{pdb}.pdb"
    average_plddt = calculate_average_plddt(pdb_file_path)
    data.loc[data['pdb'] == pdb, 'average_plddt'] = average_plddt

# Make a scatter plot of DockQ vs e-value
fig, ax = plt.subplots(figsize=(8, 5))
x = "identity"
y = "DockQ"

# Plot path 
plot_path = "./plots"
if not os.path.exists(plot_path):
    os.makedirs(plot_path)
output_path = os.path.join(plot_path, f"{model}_{x}_vs_{y}.png")

# Specify the path to the Aptos font file
font_path = '/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/Aptos.ttf'  
font_prop = fm.FontProperties(fname=font_path)
sns.scatterplot(x=x, y=y, data=data, ax=ax)

# Color the points based on model plddt
sns.scatterplot(x=x, y=y, data=data, ax=ax, hue='average_plddt')



# Update fonts
plt.xlabel(x, fontproperties=font_prop)
plt.ylabel(y, fontproperties=font_prop)
plt.title(f"{model} {x} vs {y}", fontproperties=font_prop)
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontproperties(font_prop)
    label.set_fontsize(12)
plt.tick_params(axis="y",direction="in")
plt.tick_params(axis="x",direction="in")
plt.ylim(0, 1)
plt.savefig(output_path, dpi=600)


       