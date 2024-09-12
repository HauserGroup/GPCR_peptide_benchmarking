# Script to visualize the correlation between DockQ and LIS scores for the benchmark dataset
#
# Usage: python dockq_vs_lis.py
#

import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import sys

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(top_level_dir)
from colors import *


if __name__ == "__main__":
    # Get the file directory
    file_dir = os.path.dirname(__file__)

    # Path to the DockQ results file
    dockq_path = f"{file_dir}/DockQ_results.csv"
    dockq_df = pd.read_csv(dockq_path)

    # Keep only AF2 and AF3 models
    dockq_df = dockq_df[dockq_df["model"].isin(["AF2", "AF3", "AF2_no_templates"])]
    print(dockq_df.columns)
    # Rename model to model_name
    dockq_df.rename(columns = {"model": "MODEL_NAME"}, inplace = True)
    # Make column names uppercase
    dockq_df.columns = dockq_df.columns.str.upper()

    # Load AF LIS data
    af2_lis_df = pd.read_csv(f"{file_dir}/AF_LIS_results/AF2_LIS_results.csv", sep = ",")
    af3_lis_df = pd.read_csv(f"{file_dir}/AF_LIS_results/AF3_LIS_results.csv", sep = ",")

    print(af2_lis_df.columns)
    print(af3_lis_df.columns)

    af3_lis_df["pdb"] = [i.split("_")[-1].upper() for i in af3_lis_df["folder_name"]]
    af2_lis_df["pdb"] = [i.split("/")[-1].upper() for i in af2_lis_df["saved folder"]]

    # For af2, make a new column from saved folder if it contains "no_templates"
    af2_lis_df["MODEL_NAME"] = af2_lis_df["saved folder"].apply(lambda x: "AF2_no_templates" if "no_templates" in x else "AF2")
    af3_lis_df["MODEL_NAME"] = "AF3"


    # Make column names uppercase
    af2_lis_df.columns = af2_lis_df.columns.str.upper()
    af3_lis_df.columns = af3_lis_df.columns.str.upper()

    # Drop PROTEIN_1 and PROTEIN_2 columns
    af2_lis_df.drop(columns = ["PROTEIN_1", "PROTEIN_2", "PKL", "RECYCLE", "MODEL", "CONFIDENCE", "PTM", "PLDDT", "SAVED FOLDER"], inplace = True)
    af3_lis_df.drop(columns = ["PROTEIN_1", "PROTEIN_2", "MODEL_NUMBER", "CLIS", "CLIA", "CLIR", "LIR", "FOLDER_NAME"], inplace = True)

    # Concatenate the two dataframes
    lis_df = pd.concat([af2_lis_df, af3_lis_df])

    # Keep only the highest lis score for each model
    lis_df = lis_df.groupby(["PDB", "MODEL_NAME"]).max().reset_index()

    # Merge lis_df with dockq_df
    lis_dockq_df = pd.merge(dockq_df, lis_df, on = ["PDB", "MODEL_NAME"], how = "inner")

    # Prepare the data for plotting
    x = lis_dockq_df['LIS']
    y = lis_dockq_df['DOCKQ']
    model_names = lis_dockq_df['MODEL_NAME']

    # Create a larger figure for better visibility
    plt.figure(figsize=(12, 8))

    # Use unique model names and assign each a distinct color using a colormap
    unique_models = pd.Categorical(model_names).categories
    colors = pd.Categorical(model_names).codes

    # Scatter plot with proper color coding by model name
    scatter = plt.scatter(x, y, c=colors, cmap='tab10', s=100, alpha=0.8)

    # Add grid for better readability
    plt.grid(True)

    # Add labels and title
    plt.title('DOCKQ vs LIS by MODEL_NAME', fontsize=16, weight='bold')
    plt.xlabel('LIS (Local Interface Score)', fontsize=14)
    plt.ylabel('DOCKQ (Docking Quality)', fontsize=14)

    # Manually create the legend using unique model names
    handles, _ = scatter.legend_elements()
    legend_labels = unique_models
    plt.legend(handles, legend_labels, title="MODEL_NAME", loc="upper right", fontsize=12)

    # Show the improved scatter plot
    plt.show()
            