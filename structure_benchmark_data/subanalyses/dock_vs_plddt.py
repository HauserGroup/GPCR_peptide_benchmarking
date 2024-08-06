import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import numpy as np
import scipy.stats as stats
import torch

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]

repo_name = "GPRC_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Output path for plots 
plot_dir = f'{file_dir}/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

sys.path.append(repo_dir)
from colors import * 

def read_rosetta_score_file(score_file_path, metric = "mean_pae"):
    score_file = torch.load(score_file_path, map_location=torch.device('cpu'))
    return score_file[metric]

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

def scatter_plot(model, dockq_path, repo_dir):
    data = pd.read_csv(dockq_path)
    data = data[data['model'] == model]

    plot_path = f"{repo_dir}/structure_benchmark_data/subanalyses/plots"

    # X and Y 
    y = "DockQ"
    x = "average_plddt"

    # Get average pLDDT scores for predictions
    for pdb in data['pdb']:
        model_extension = ""
        if "RFAA" in model:
            model_name = "RFAA_chain"
            if "no_templates" in model:
                model_name += "_no_templates"
                model_extension = "_no_templates"
        else:
            model_name = model
        pdb_file_path = f"{repo_dir}/structure_benchmark/{model_name}/{pdb}{model_extension}.pdb"
        average_plddt = calculate_average_plddt(pdb_file_path)
        if "RFAA" in model:
            average_plddt = average_plddt * 100
        data.loc[data['pdb'] == pdb, 'average_plddt'] = average_plddt

    # Make a scatter plot of DockQ vs e-value
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot path 
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    output_path = os.path.join(plot_path, f"{model}_{x}_vs_{y}.svg")

    # Specify the path to the Aptos font file
    font_path = f'{repo_dir}/Aptos.ttf'  
    font_prop = fm.FontProperties(fname=font_path)

    # Calculate the linear regression line and 95% confidence interval
    slope, intercept = np.polyfit(data[x], data[y], 1)
    y_model = np.polyval([slope, intercept], data[x])
    x_mean = np.mean(data[x])
    y_mean = np.mean(data[y])
    n = data[x].size
    m = 2
    dof = n - m
    t = stats.t.ppf(0.975, dof)
    residual = data[y] - y_model
    std_error = (np.sum(residual**2) / dof)**.5   # Standard deviation of the error
    numerator = np.sum((data[x] - x_mean)*(data[y] - y_mean))
    denominator = ( np.sum((data[x] - x_mean)**2) * np.sum((data[y] - y_mean)**2) )**.5
    correlation_coef = numerator / denominator
    r2 = correlation_coef**2
    MSE = 1/n * np.sum( (data[y] - y_model)**2 )
    x_line = np.linspace(np.min(data[x]), np.max(data[x]), 100)
    y_line = np.polyval([slope, intercept], x_line)
    ci = t * std_error * (1/n + (x_line - x_mean)**2 / np.sum((data[x] - x_mean)**2))**.5

    # Create new figure
    fig, ax = plt.subplots()

    # Make the scatterplot
    sc = ax.scatter(x=data[x], y=data[y], s=15)
    ax.plot(x_line, y_line, color = COLOR["Receptor"])
    ax.fill_between(x_line, y_line + ci, y_line - ci, color = COLOR["Receptor"], label = '95% confidence interval', alpha = 0.1)
    ax.text(3.5, 0.85, 'y = ' + str(np.round(intercept, 2)) + ' + ' + str(np.round(slope,2)) + 'x\n' + 'r$^2$ = ' + str(np.round(r2,3)) + '\nMSE = ' + str(np.round(MSE,3)), font_properties=font_prop, fontsize=12)

    # Update fonts and labels
    plt.xlabel(x, fontproperties=font_prop, fontsize=14)
    plt.ylabel(y, fontproperties=font_prop, fontsize=14)

    # Update fonts and labels
    plt.xlabel(x, fontproperties=font_prop, fontsize=14)
    plt.ylabel(y, fontproperties=font_prop, fontsize=14)

    # Modify the title
    model_title = model.split("_")[0]
    if "no_templates" in model:
        model_title += " (no templates)"
    plt.title(f"{model_title}", fontproperties=font_prop, fontsize=16)

    # Set the font properties for the ticks
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(font_prop)
        label.set_fontsize(12)

    # Modift ticks and set axis limits
    plt.tick_params(axis="y", direction="in")
    plt.tick_params(axis="x", direction="in")
    plt.ylim(0, 1)
    plt.xlim(0, 100)

    # Save the figure
    plt.savefig(output_path, dpi=600)

if __name__ == "__main__":
    # Path to the DockQ scores file
    dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"

    # Model name
    model = "AF2"

    # X and Y variables
    x = "DockQ"
    y = "average_plddt"

    scatter_plot(model, dockq_path, repo_dir)