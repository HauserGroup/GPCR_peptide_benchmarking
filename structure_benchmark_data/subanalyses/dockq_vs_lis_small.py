import os 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import scipy.stats as stats
import sys
import pathlib as pl

file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = pl.Path(__file__).parent.parent.parent
plot_dir = f"{repo_dir}/structure_benchmark_data/plots"
sys.path.append(repo_dir)
sys.path.append(str(repo_dir))
sys.path.append(str(repo_dir.parent.parent))
from colors import * 


if __name__ == "__main__":
    # Read in DockQ data
    script_dir = pl.Path(__file__)
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
    fig, ax = plt.subplots(figsize=(3.5, 2))

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

    colors = {'IPTM': custom_color_mapping['AF2 (no templates)'],
              'LIS' : 'black'}
    fontsize = 10
    # Plot each model separately with its own color and shape
    for model in custom_color_mapping.keys():
        for score_col in ['IPTM', 'LIS']:
            # only allow AF2 (no templates)
            if model != 'AF2 (no templates)':
                continue
            model_data = lis_dockq_df[model_names == model]
            ax.scatter(
                model_data[score_col], 
                model_data['DOCKQ'], 
                c=colors[score_col],
                marker='.',
                s=fontsize//3, 
                alpha=1.0, 
                label=f'{score_col}',
            )

            # Add regression lines with confidence intervals
            sns.regplot(
                x=model_data[score_col], 
                y=model_data['DOCKQ'], 
                scatter=False,  # Scatter is already plotted
                color=colors[score_col],
                ci=95,  # Confidence interval (95%)
                line_kws={"linewidth": 1.5,
                          }  # Customize the regression line
            )

    # Add grid
    ax.grid(color='gray', linestyle='-', linewidth=0.25,
            alpha=0.5)

    # Add labels and title using the font properties object
    ax.set_xlabel('Predicted score', fontsize=fontsize)
    ax.set_ylabel('DockQ score', fontsize=fontsize)


    ax.tick_params(axis="y",direction="in")
    ax.tick_params(axis="x",direction="in")
    for item in ax.get_xticklabels() + ax.get_yticklabels():
        item.set_fontsize(fontsize-1)

    # Customize legend
    legend = ax.legend(
        title="Model", 
        facecolor="white", 
        fontsize=fontsize, 
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

    # add dockq labels
    dockq_labels = {
     'perfect': 1.0,
     'high':0.80,
     'medium':0.49,
     'acceptable':0.23,
     'incorrect':0,
    }
    ygridlines = []
    for dockq_label, score in dockq_labels.items():
        ygridlines.append(score)
    ax.set_yticks(ygridlines)
    # Set x and y limits and edit ticks
    plt.xlim(-0.2, 1)
    plt.ylim(0, 1)

    # Save the plot
    plt.rcParams['svg.fonttype'] = 'none'
    plt.tight_layout()
    plot_p = f"{plot_dir}/DockQ_vs_LIS_small.svg"
    plt.savefig(plot_p, dpi=600)
    plt.savefig(plot_p.replace('.svg', '.png'), dpi=600)
    # Loop through each model and calculate the Pearson correlation between LIS and DockQ
    for model in lis_dockq_df["MODEL_NAME"].unique():
        model_data = lis_dockq_df[lis_dockq_df['MODEL_NAME'] == model]
        # print(model_data.columns)
        correlation, p_value = stats.pearsonr(model_data['LIS'], model_data['DOCKQ'])
        print(f"Model: {model}")
        print(f"Degrees of freedom: {len(model_data) - 2}")
        print(f"Pearson correlation: {correlation}")
        print(f"P-value: {p_value}")
        print("-" * 30)