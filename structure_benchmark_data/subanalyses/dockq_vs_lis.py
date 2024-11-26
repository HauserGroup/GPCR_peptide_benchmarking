import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import scipy.stats as stats
import sys

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
plot_dir = f"{file_dir}/plots"

repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
sys.path.append(repo_dir)
from colors import * 

if __name__ == "__main__":
    # Read in DockQ data
    dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
    dockq_df = pd.read_csv(dockq_path)
    dockq_df = dockq_df[dockq_df["model"].isin(["AF2", "AF3", "AF2_no_templates"])]
    dockq_df.rename(columns = {"model": "MODEL_NAME"}, inplace = True)
    dockq_df.columns = dockq_df.columns.str.upper()

    # Load AF LIS data
    af2_lis_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/AF_LIS_results/AF2_LIS_results.csv", sep = ",")
    af3_lis_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/AF_LIS_results/AF3_LIS_results.csv", sep = ",")
    af3_lis_df["pdb"] = [i.split("_")[-1].upper() for i in af3_lis_df["folder_name"]]
    af2_lis_df["pdb"] = [i.split("/")[-1].upper() for i in af2_lis_df["saved folder"]]
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

    # Concatenate the two dataframes and keep only the highest lis score for each model
    lis_df = pd.concat([af2_lis_df, af3_lis_df])
    lis_df = lis_df.groupby(["PDB", "MODEL_NAME"]).max().reset_index()

    # Merge lis_df with dockq_df
    lis_dockq_df = pd.merge(dockq_df, lis_df, on = ["PDB", "MODEL_NAME"], how = "inner")
    lis_dockq_df["MODEL_NAME"] = lis_dockq_df["MODEL_NAME"].replace("AF2_no_templates", "AF2 (no templates)")

    # Prepare the data for plotting
    x = lis_dockq_df['LIS']
    y = lis_dockq_df['DOCKQ']
    model_names = lis_dockq_df['MODEL_NAME']

    # Create a figure
    fig, ax = plt.subplots(figsize=(7, 5))

    # Custom color and marker mapping for each model
    custom_color_mapping = {
        'AF2': COLOR["AF2"],
        'AF2 (no templates)': COLOR["AF2 (no templates)"],
        'AF3': COLOR["AF3"]
    }

    custom_marker_mapping = {
        'AF2': 'o',  # Circle
        'AF2 (no templates)': 's',  # Square
        'AF3': '^'  # Triangle
    }

    # Plot each model separately with its own color and shape
    for model in custom_color_mapping.keys():
        model_data = lis_dockq_df[model_names == model]
        ax.scatter(
            model_data['LIS'], 
            model_data['DOCKQ'], 
            c=custom_color_mapping[model], 
            marker=custom_marker_mapping[model], 
            s=20, 
            alpha=0.8, 
            label=model
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
    ax.grid(color='gray', linestyle='-', linewidth=0.25)

    # Add labels and title using the font properties object
    ax.set_xlabel('AFM-LIS', fontsize = 14)
    ax.set_ylabel('DockQ score', fontsize = 14)

    # Set x and y limits and edit ticks
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")

    # Customize legend
    legend = ax.legend(
        title="Model", 
        facecolor="white", 
        fontsize=16, 
        framealpha=1, 
        loc = "lower right", 
        handletextpad=0.0, 
        borderaxespad = 0.1,
        borderpad = 0.1,
        labelspacing = 0.2
    )
    legend.get_title().set_fontproperties(fm.FontProperties(size=0))
    frame = legend.get_frame()
    frame.set_linewidth(0.25)  

    # Save the plot
    plt.rcParams['svg.fonttype'] = 'none'
    plt.tight_layout()
    plt.savefig(f"{plot_dir}/DockQ_vs_LIS.svg", dpi=600)

    # Loop through each model and calculate the Pearson correlation between LIS and DockQ
    for model in lis_dockq_df["MODEL_NAME"].unique():
        model_data = lis_dockq_df[lis_dockq_df['MODEL_NAME'] == model]
        correlation, p_value = stats.pearsonr(model_data['LIS'], model_data['DOCKQ'])
        print(f"Model: {model}")
        print(f"Degrees of freedom: {len(model_data) - 2}")
        print(f"Pearson correlation: {correlation}")
        print(f"P-value: {p_value}")
        print("-" * 30)