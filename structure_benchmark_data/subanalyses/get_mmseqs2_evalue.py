import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
sys.path.append(repo_dir)
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
    df = pd.DataFrame.from_dict(
        results_per_pdb, orient="index", columns=["e_value", "Identity"]
    )
    df.reset_index(inplace=True)
    df.columns = ["pdb", "e_value", "Identity"]

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
        with open(pdb_file_path, "r") as pdb_file:
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


def identity_vs_dockq_plot(model, dockq_path, training_struct_df, plot_path="", x="Identity", y="DockQ"):
    data = pd.read_csv(dockq_path)
    data = data[data["model"] == model]
    data = data.merge(training_struct_df, left_on="pdb", right_on="pdb", how="left")

    # Get the top-level directory and build the path to the plot directory
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if plot_path == "":
        plot_path = f"{repo_dir}/structure_benchmark_data/subanalysis/plots"

    # Get average pLDDT scores for predictions
    for pdb in data["pdb"]:
        model_extension = ""
        if "RFAA" in model:
            model_name = "RFAA_chain"
            if "no_templates" in model:
                model_name += "_no_templates"
                model_extension = "_no_templates"
        else:
            model_name = model
        pdb_file_path = (
            f"{repo_dir}/structure_benchmark/{model_name}/{pdb}{model_extension}.pdb"
        )
        average_plddt = calculate_average_plddt(pdb_file_path)
        if "RFAA" in model:
            average_plddt = average_plddt * 100
        data.loc[data["pdb"] == pdb, "average_plddt"] = average_plddt

    # Use Spearman's rank correlation to calculate the correlation between the two variables
    statistic, corr_p_val = stats.spearmanr(data[[x, y]], axis=0, nan_policy='propagate', alternative='two-sided')
    statistic = np.round(statistic, 3)
    corr_p_val = np.round(corr_p_val, 3)
    n = len(data[x])

    # Calculate the regression statistics
    slope, intercept, r_value, p_value, std_err = stats.linregress(data[x], data[y])

    # Make the plot using Seaborn
    plt.figure(figsize=(8, 5))

    # Create the scatterplot using plt.scatter with fixed colormap scale
    points = plt.scatter(
        data[x],
        data[y],
        c=data["average_plddt"],  # Set color based on average pLDDT
        cmap=get_good_bad_cmap(),  # Use a consistent colormap
        s=100,  # Set point size
        linewidth=0,  # Set edge width
        vmin=0,  # Fix the minimum value at 0
        vmax=100  # Fix the maximum value at 100
    )

    # Add colorbar for the scatter plot
    cbar = plt.colorbar(points)
    cbar.set_label("Average pLDDT", fontsize=14)

    # Create the scatterplot with regression line and confidence intervals using sns.regplot()
    scatter_plot = sns.regplot(
        x=data[x],
        y=data[y],
        scatter_kws={"s": 0},
        line_kws={"color": "#0b3d91", "alpha": 0.9},
        ci=95
    )

    # Set axis labels and title
    plt.xlabel(x, fontsize=14)
    plt.ylabel(y, fontsize=14)
    model_title = model.split("_")[0]
    if "no_templates" in model:
        model_title += " (no templates)"
    plt.title(f"{model_title}, r({n}) = {statistic}, p = {corr_p_val}", fontsize=16)

    # Set axis limits
    plt.ylim(-0.025, 1.025)
    plt.xlim(-0.025, 1.025)

    # Annotate the plot with the regression statistics
    plt.text(
        0.05,
        0.85,
        f"y = {intercept:.2f} + {slope:.2f}x\nr² = {r_value:.3f}",
        fontsize=12,
        transform=scatter_plot.transAxes
    )

    # Hide grid and legend
    plt.grid(False)

    # Make frame around the plot grey
    for spine in plt.gca().spines.values():
        spine.set_edgecolor("#d0d0d0")

    # Make tickmarks go inward
    plt.tick_params(direction="in", length=2)

    # Remove tickmarks from colorbar
    cbar.ax.tick_params(direction="in", length=0)

    # Save the plot
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt.rcParams["svg.fonttype"] = "none"
    output_path = os.path.join(plot_path, f"{model}_{x}_vs_{y}.svg")
    plt.tight_layout()
    plt.savefig(output_path, dpi=600)
    plt.close()

if __name__ == "__main__":
    # Get the file directory
    file_dir = os.path.dirname(__file__)
    known_structs = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/3f_known_structures.csv")
    pdb_to_protein = dict(zip(known_structs["pdb_code"], known_structs["protein"]))

    # Input paths to the search results
    rfaa_input_path = f"{file_dir}/mmseqs2_results/RFAA/search_results"
    af_input_path = f"{file_dir}/mmseqs2_results/AF/search_results"

    # Get the closest training structures
    af_training_struct = get_closest_training_structures(af_input_path)
    af_training_struct["gpcr"] = af_training_struct["pdb"].map(pdb_to_protein)
    af_training_struct.to_csv(
        f"{file_dir}/mmseqs2_results/mmseq2_af_training_structures.csv", index=False
    )
    rfaa_training_struct = get_closest_training_structures(rfaa_input_path)
    rfaa_training_struct["gpcr"] = rfaa_training_struct["pdb"].map(pdb_to_protein)
    rfaa_training_struct.to_csv(
        f"{file_dir}/mmseqs2_results/mmseq2_rfaa_training_structures.csv", index=False
    )

    # Path to the DockQ results file
    dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"

    # Get only AF2, AF3 and RFAA models
    input_models = ["AF2", "AF2_no_templates", "AF3", "RFAA", "RFAA_no_templates"]
    for model in input_models:
        if "AF" in model:
            training_struct_df = af_training_struct
        else:
            training_struct_df = rfaa_training_struct
        identity_vs_dockq_plot(model, dockq_path, training_struct_df)
