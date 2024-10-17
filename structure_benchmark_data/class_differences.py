# Script to analyse Class A and B1 differences in DockQ performance
import os
import sys

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

import numpy as np
def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)


# Load DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Load receptor RMSD data
receptor_rmsd_path = f"{repo_dir}/structure_benchmark_data/subanalyses/receptor_rmsds.csv"
receptor_rmsd = pd.read_csv(receptor_rmsd_path)

# Merge with data
data = data.merge(receptor_rmsd, on=["pdb", "model"])

# Get class A and B1 data 
class_data_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30_cleaned.csv"
class_data = pd.read_csv(class_data_path)
class_data = class_data[["pdb","receptor","uniprot_id","class","family","resolution","ligand_name"]]

# Merge with class data
data = data.merge(class_data, on="pdb", how = "inner")

# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA\n(no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2", "AF2")
data["model"] = data["model"].replace("AF2_no_templates", "AF2\n(no templates)")
data["model"] = data["model"].replace("Chai-1_no_MSAs", "Chai-1\n(no MSAs)")

def plot_dockq_class_comparison(data, variable, plot_dir, y_label = None):
    # Define the custom colors for the models based on the provided dictionary
    colors = {
        'NeuralPLexer': COLOR["NeuralPLexer"],
        'ESMFold': COLOR["ESMFold"],
        'RF-AA': COLOR["RF-AA"], 
        'RF-AA\n(no templates)': COLOR["RF-AA (no templates)"], 
        'Chai-1': COLOR["Chai-1"],
        'Chai-1\n(no MSAs)': COLOR["Chai-1 (no MSAs)"],
        'AF2': COLOR["AF2"], 
        'AF2\n(no templates)': COLOR["AF2 (no templates)"],
        'AF3': COLOR["AF3"]
    }
    # Order data by model
    data = data.sort_values(
        by='model',
        key=lambda x: pd.Categorical(x, categories=list(colors.keys()),ordered=True)
    )

    if y_label is None:
        y_label = variable

    # Create a figure with subplots, one for each model
    num_models = len(colors.keys())
    fig, axes = plt.subplots(nrows=(num_models // 2) + 1, ncols=2, figsize=(8, 14))

    # Flatten axes for easier iteration
    axes = axes.flatten()

    class_a_color = COLOR["Class A (Rhodopsin)"]
    class_b1_color = COLOR["Class B1 (Secretin)"]
    class_colors = [class_a_color, class_b1_color]

    # Plot each model separately using swarmplots
    for i, (model, color) in enumerate(colors.items()):
        ax = axes[i]
        
        # Filter the data for the current model
        model_data = data[data['model'] == model]
        
        # Create the swarmplot for this model
        sns.swarmplot(x='class', y=variable, data=model_data, ax=ax, palette=class_colors, s=2.5)

        # Calculate the mean and SEM for each class
        means = model_data.groupby('class')[variable].mean()
        sems = model_data.groupby('class')[variable].sem()
        
        # Add mean and SEM as error bars
        for j, class_type in enumerate(means.index):
            ax.errorbar(j, means[class_type], yerr=sems[class_type], fmt='', color=class_colors[j], lw=1.25, capsize=30, capthick=1.25)

        # Set plot labels
        ax.set_title(model)
        ax.set_ylabel(y_label)
        ax.set_xlabel('')
        if variable == "DockQ":
            ax.set_ylim(0, 1)
        elif variable == "rmsd":
            ax.set_ylim(0, max(model_data[variable])+0.5)
        ax.set_xlim(-0.5, 1.5)

    # Remove any empty subplots if there are fewer than the grid allows
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Adjust layout
    plt.tight_layout()
    plt.rcParams["svg.fonttype"] = "none"
    plt.savefig(f"{plot_dir}/{variable}_class_comparison.svg", dpi=300)

# Plot DockQ scores for Class A and Class B1
plot_dockq_class_comparison(data, 'DockQ', f"{plot_dir}", y_label = "DockQ Score")
plot_dockq_class_comparison(data, 'rmsd', f"{plot_dir}", y_label = "RMSD (Å)")

def stat_results(data, variable, data_dir):
    from scipy.stats import mannwhitneyu
    # Define the custom colors for the models based on the provided dictionary
    colors = {
        'NeuralPLexer': COLOR["NeuralPLexer"],
        'ESMFold': COLOR["ESMFold"],
        'RF-AA': COLOR["RF-AA"], 
        'RF-AA\n(no templates)': COLOR["RF-AA (no templates)"], 
        'Chai-1': COLOR["Chai-1"],
        'Chai-1\n(no MSAs)': COLOR["Chai-1 (no MSAs)"],
        'AF2': COLOR["AF2"], 
        'AF2\n(no templates)': COLOR["AF2 (no templates)"],
        'AF3': COLOR["AF3"]
    }

    # Initialize a dictionary to store the results
    stat_results = {}

    # Loop through each model to perform the statistical test between Class A and Class B1
    for model in colors.keys():
        # Filter the data for the current model
        model_data = data[data['model'] == model]
        
        # Get DockQ scores for Class A and Class B1
        class_a_data = model_data[model_data['class'] == 'Class A (Rhodopsin)'][variable]
        class_b1_data = model_data[model_data['class'] == 'Class B1 (Secretin)'][variable]
        
        # If data is not normally distributed, use Mann-Whitney U test
        stat, p_value = mannwhitneyu(class_a_data, class_b1_data)
        
        # Store the results for the current model
        stat_results[model] = {
            'Model': model.replace("\n", " "),
            'N (Class A)': len(class_a_data),
            'N (Class B1)': len(class_b1_data),
            f'{variable} Mean (Class A)': class_a_data.mean(),
            'SEM (Class A)': class_a_data.sem(),
            f'{variable} Mean (Class B1)': class_b1_data.mean(),
            'SEM (Class B1)': class_b1_data.sem(),
            'Statistic': stat,
            'P-value': p_value
        }

    # Convert the results to a DataFrame and display
    results_df = pd.DataFrame(stat_results).T
    results_df.reset_index(drop=True, inplace=True)

    # Make sure columns are numerical if they only contain numbers
    results_df = results_df.apply(pd.to_numeric, errors='ignore')
    
    # Apply function to all numeric columns in the DataFrame
    for col in results_df.columns:
        results_df[col] = results_df[col].apply(lambda x: round_to_significant_digits(x, 3) if pd.to_numeric(x, errors='coerce') is not None else x)

    
    results_df.to_csv(f"{data_dir}/subanalyses/class_{variable}_comparison_results.csv", index=False)

# Perform statistical tests for DockQ scores
stat_results(data, 'DockQ', f"{file_dir}")
stat_results(data, 'rmsd', f"{file_dir}")