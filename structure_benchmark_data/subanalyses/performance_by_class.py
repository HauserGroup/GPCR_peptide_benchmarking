import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

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

# Read in DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2", "AF2")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (no templates)")

# Read GPCR class datafrom UniProt
gpcr_class_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30.csv"
gpcr_class_data = pd.read_csv(gpcr_class_path)

# Merge DockQ data with GPCR class data
full_data = data.merge(gpcr_class_data, on='pdb').copy()

for gpcr_class in full_data['class'].unique():

    # Filter data based on GPCR class
    data = full_data[full_data['class'] == gpcr_class]

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 5))

    # Color the points based on model
    colors = {
        'NeuralPLexer' : COLOR["NeuralPLexer"],
        'ESMFold': COLOR["ESMFold"],
        'RF-AA': COLOR["RF-AA"], 
        'RF-AA (no templates)': COLOR["RF-AA (no templates)"], 
        'AF2': COLOR["AF2"], 
        'AF2 (no templates)': COLOR["AF2 (no templates)"],
        'AF3': COLOR["AF3"],
    }  
    data = data.sort_values(by='model', key=lambda x: pd.Categorical(x, categories=list(colors.keys()), ordered=True))
    data = data.reset_index(drop=True)

    # Specify the path to the Aptos font file
    font_path = f'{repo_dir}/Aptos.ttf'  
    font_prop = fm.FontProperties(fname=font_path)

    # Creating a swarm plot
    sns.swarmplot(x='model', y='DockQ', data=data, ax=ax, size = 3, alpha=0.6, palette=colors.values(), order = list(colors.keys()))

    for i, model in enumerate(list(colors.keys())):
        ax.get_children()[i].set_color(colors[model])

    # Calculate the mean and standard error of the mean (SEM) for each category
    means = data.groupby('model')['DockQ'].mean()
    sems = data.groupby('model')['DockQ'].sem()

    # Add error bars and mean points
    for i, model in enumerate(list(colors.keys())):
        ax.errorbar(i, means[model], yerr=sems[model], fmt='none', color=colors[model], capsize=20, label='Mean ± SEM' if i == 0 else "")
        ax.hlines(means[model], i-0.025, i+0.025, color=colors[model], lw=1, label='Mean' if i == 0 else "")

    # Add horizontal lines showing prediction quality
    ax.axhline(0.23, color='grey', linestyle='-', alpha = 0.5)
    ax.axhline(0.49, color='grey', linestyle='-', alpha = 0.5)
    ax.axhline(0.80, color='grey', linestyle='-', alpha = 0.5)

    # Add text annotations using axes fraction coordinates
    text_size = 12
    padding = 0.05
    ax.text(0.02, 0.23-padding, 'Incorrect (DockQ < 0.23)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5, fontproperties=font_prop)
    ax.text(0.02, 0.49-padding, 'Acceptable (0.23 ≤ DockQ < 0.49)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5, fontproperties=font_prop)
    ax.text(0.02, 0.80-padding, 'Medium (0.49 ≤ DockQ < 0.80)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5, fontproperties=font_prop)
    ax.text(0.02, 1.0-padding, 'High (DockQ ≥ 0.80)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5, fontproperties=font_prop)

    # Set y-axis limit
    ax.set_ylim(0, 1)

    # Set labels and title
    ax.set_xlabel('', fontsize=0)
    ax.set_ylabel('DockQ Score', fontsize=14, fontproperties=font_prop)
    ax.set_xticklabels(list(colors.keys()), rotation=0, ha="center", fontsize=12, fontproperties=font_prop)
    ax.set_title(gpcr_class, fontsize=18, fontproperties=font_prop)
    ax.tick_params(axis="y",direction="in")

    plt.tight_layout()
    plt.savefig(f"{plot_dir}/DockQ_scores_{gpcr_class}.png", dpi=600)
