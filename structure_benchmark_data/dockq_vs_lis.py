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
    plot_dir = f"{file_dir}/plots"
    repo_dir = file_dir.split("GPRC_peptide_benchmarking")[0] + "GPRC_peptide_benchmarking"

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

    af3_lis_df["pdb"] = [i.split("_")[-1].upper() for i in af3_lis_df["folder_name"]]
    af2_lis_df["pdb"] = [i.split("/")[-1].upper() for i in af2_lis_df["saved folder"]]

    # For af2, make a new column from saved folder if it contains "no_templates"
    af2_lis_df["MODEL_NAME"] = af2_lis_df["saved folder"].apply(lambda x: "AF2_no_templates" if "no_templates" in x else "AF2")
    af3_lis_df["MODEL_NAME"] = "AF3"

    # Make column names uppercase
    af2_lis_df.columns = af2_lis_df.columns.str.upper()
    af3_lis_df.columns = af3_lis_df.columns.str.upper()

    # Keep only model number 0 for AF3
    af3_lis_df = af3_lis_df[af3_lis_df["MODEL_NUMBER"] == "0"]
    
    # Drop PROTEIN_1 and PROTEIN_2 columns
    af2_lis_df.drop(columns = ["PROTEIN_1", "PROTEIN_2", "PKL", "RECYCLE", "MODEL", "CONFIDENCE", "PTM", "PLDDT", "SAVED FOLDER"], inplace = True)
    af3_lis_df.drop(columns = ["PROTEIN_1", "PROTEIN_2", "MODEL_NUMBER", "CLIS", "CLIA", "CLIR", "LIR", "FOLDER_NAME"], inplace = True)

    # Concatenate the two dataframes
    lis_df = pd.concat([af2_lis_df, af3_lis_df])

    # Keep only the highest lis score for each model
    lis_df = lis_df.groupby(["PDB", "MODEL_NAME"]).max().reset_index()

    # Merge lis_df with dockq_df
    lis_dockq_df = pd.merge(dockq_df, lis_df, on = ["PDB", "MODEL_NAME"], how = "inner")
    # Save the merged dataframe
    lis_dockq_df.to_csv(f"{file_dir}/lis_dockq_merged.csv", index = False)

    # Prepare the data for plotting
    x = lis_dockq_df['LIS']
    y = lis_dockq_df['DOCKQ']
    model_names = lis_dockq_df['MODEL_NAME']

    # Create a larger figure for better visibility
    plt.figure(figsize=(12, 8))

    # Custom color and marker mapping for each model
    custom_color_mapping = {
        'AF2': COLOR["AF2"],
        'AF2_no_templates': COLOR["AF2 (no templates)"],
        'AF3': COLOR["AF3"]
    }

    custom_marker_mapping = {
        'AF2': 'o',  # Circle
        'AF2_no_templates': 's',  # Square
        'AF3': '^'  # Triangle
    }

    # Specify the path to the Aptos font file
    font_path = f'{repo_dir}/Aptos.ttf'

    # Adjust the font properties
    font_prop_title = fm.FontProperties(fname=font_path, size=25, weight='bold')
    font_prop_labels = fm.FontProperties(fname=font_path, size=20)
    font_prop_legend = fm.FontProperties(fname=font_path, size=16)
    font_prop_legend_title = fm.FontProperties(fname=font_path, size=20, weight='bold')
    font_prop = fm.FontProperties(fname=font_path, size=15, weight='bold')

    # Plot each model separately with its own color and shape
    for model in custom_color_mapping.keys():
        model_data = lis_dockq_df[model_names == model]
        plt.scatter(
            model_data['LIS'], 
            model_data['DOCKQ'], 
            c=custom_color_mapping[model], 
            marker=custom_marker_mapping[model], 
            s=20, alpha=0.8, label=model
        )

        # Add regression lines with confidence intervals
        sns.regplot(
            x=model_data['LIS'], 
            y=model_data['DOCKQ'], 
            scatter=False,  # Scatter is already plotted
            color=custom_color_mapping[model], 
            ci=95,  # Confidence interval (95%)
            line_kws={"linewidth": 2}  # Customize the regression line
        )

    # Add grid
    plt.grid(color='gray', linestyle='--', linewidth=0.5)

    # Add labels and title using the font properties object
    plt.title('DockQ score vs AFM-LIS', fontproperties=font_prop_title)
    plt.xlabel('LIS (Local Interface Score)', fontproperties=font_prop_labels)
    plt.ylabel('DockQ score', fontproperties=font_prop_labels)

    # Set x and y limits
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    # Add horizontal line and text annotation
    plt.axhline(0.23, color='grey', linestyle='-', alpha=0.5)
    padding = -0.01
    plt.text(0.02, 0.23-padding, 'Incorrect (DockQ < 0.23)', color='black', alpha=0.5, fontproperties=font_prop)

    # Customize legend
    legend = plt.legend(title="Model", loc="lower right", prop=font_prop_legend)
    legend.get_title().set_fontproperties(font_prop_legend_title)

    # Save the plot
    plt.savefig(f"{plot_dir}/DockQ_vs_LIS.png", dpi=300)

    import scipy.stats as stats
    # Loop through each model and calculate the Pearson correlation between LIS and DockQ
    for model in lis_dockq_df["MODEL_NAME"].unique():
        model_data = lis_dockq_df[lis_dockq_df['MODEL_NAME'] == model]
        correlation, p_value = stats.pearsonr(model_data['LIS'], model_data['DOCKQ'])
        
        print(f"Model: {model}")
        print(f"Pearson correlation: {correlation}")
        print(f"P-value: {p_value}")
        print("-" * 30)