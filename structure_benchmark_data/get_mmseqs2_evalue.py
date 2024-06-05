import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from scipy import stats
import numpy as np
from sklearn.metrics import r2_score 


# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(top_level_dir)
from colors import * 

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

        # Read first line of the file
        with open(full_path, "r") as f:
            line = f.readline()
            # Split the line by whitespace
            parts = line.split("\t")
            # Extract the e-value
            e_value = float(parts[10])
            identity = float(parts[2])

            # Extract the PDB code from the filename
            pdb_code = file.split(".")[0]
            pdb_code = pdb_code.split("_")[0]
            # Store the e-value in the dictionary
            results_per_pdb[pdb_code] = [e_value, identity]

    # Make dictionary into dataframe with columns pdb, e_value, and identity
    df = pd.DataFrame.from_dict(results_per_pdb, orient='index', columns=['e_value', 'Identity'])
    df.reset_index(inplace=True)
    df.columns = ['pdb', 'e_value', 'Identity']

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


def identity_vs_dockq_plot(model, dockq_path, training_struct_df, plot_path=""):
    data = pd.read_csv(dockq_path)
    data = data[data['model'] == model]
    data = data.merge(training_struct_df, left_on='pdb', right_on='pdb', how='left')

    # Get the top-level directory
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    if plot_path == "":
        plot_path = f"{repo_dir}/structure_benchmark_data/plots"

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
    x = "Identity"
    y = "DockQ"

    # Plot path 
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    output_path = os.path.join(plot_path, f"{model}_{x}_vs_{y}.png")

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

    # Set the normalization range for the colormap from 0 to 100
    norm = mcolors.Normalize(vmin=0, vmax=100)

    # Make the scatterplot
    sc = ax.scatter(x=data[x], y=data[y], c=data['average_plddt'], cmap=get_good_bad_cmap(), norm=norm, s=15)
    ax.plot(x_line, y_line, color = COLOR["Receptor"])
    ax.fill_between(x_line, y_line + ci, y_line - ci, color = COLOR["Receptor"], label = '95% confidence interval', alpha = 0.1)
    ax.text(0.0025, 0.90, '$r^2$ = ' + str(np.round(r2,3)) + '\nMSE = ' + str(np.round(MSE,3)), font_properties=font_prop, fontsize=12)

    # Add colorbar
    cbar = plt.colorbar(sc, ax=ax, orientation='vertical')
    cbar.set_label('Average pLDDT', fontproperties=font_prop, fontsize=14)

    # Optionally, set custom ticks and labels for the colorbar
    cbar.set_ticks([0, 20, 40, 60, 80, 100])  # Customize the ticks if needed
    cbar.set_ticklabels([0, 20, 40, 60, 80, 100])  # Customize the tick labels if needed

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
    plt.ylim(-0.025, 1.025)
    plt.xlim(-0.025, 1.025)

    # Save the figure
    plt.savefig(output_path, dpi=600)


if __name__ == "__main__":

    # Get the file directory
    file_dir = os.path.dirname(__file__)

    # Input paths to the search results
    rfaa_input_path = f"{file_dir}/mmseqs2_results/RFAA/search_results"
    af_input_path=f"{file_dir}/mmseqs2_results/AF/search_results"

    # Get the closest training structures
    af_training_struct = get_closest_training_structures(af_input_path)
    rfaa_training_struct = get_closest_training_structures(rfaa_input_path)

    # Path to the DockQ results file
    dockq_path = f"{file_dir}/DockQ_results.csv"

    # Get only AF2, AF3 and RFAA models
    input_models = ['AF2', 'AF2_no_templates', 'AF3', 'RFAA', 'RFAA_no_templates']
    for model in input_models:
        if "AF" in model:
            training_struct_df = af_training_struct
        else:
            training_struct_df = rfaa_training_struct
        identity_vs_dockq_plot(model, dockq_path, training_struct_df)