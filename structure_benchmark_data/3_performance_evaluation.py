import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

# Output path for plots 
plot_dir = f'{file_dir}/plots'
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

sys.path.append(repo_dir)
from colors import * 

# Load DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Load receptor RMSD data
receptor_rmsd_path = f"{repo_dir}/structure_benchmark_data/subanalyses/receptor_rmsds.csv"
receptor_rmsd = pd.read_csv(receptor_rmsd_path)
receptor_rmsd = receptor_rmsd[receptor_rmsd["seed"] == 1]
receptor_rmsd = receptor_rmsd.drop(columns=["seed"])

# Merge with data
data = data.merge(receptor_rmsd, on=["pdb", "model"])

# Drop rows where "seed" is not 1
data = data[data["seed"] == 1]

# Output path for plots 
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA\n(no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2_no_templates", "AF2\n(no templates)")
data["model"] = data["model"].replace("AF3_no_templates", "AF3\n(no templates)")
data["model"] = data["model"].replace("AF3_server", "AF3 (server)")

# Color the points based on model
colors = {
    'NeuralPLexer' : COLOR["NeuralPLexer"],
    'ESMFold': COLOR["ESMFold"],
    'RF-AA': COLOR["RF-AA"], 
    'RF-AA\n(no templates)': COLOR["RF-AA (no templates)"], 
    'Chai-1': COLOR["Chai-1"],
    'AF2': COLOR["AF2"], 
    'AF2\n(no templates)': COLOR["AF2 (no templates)"],
    'AF3': COLOR["AF3"],
    'AF3\n(no templates)': COLOR["AF3 (no templates)"],
    'AF3 (server)': "#02bfe7"
} 
data = data.sort_values(by='model', key=lambda x: pd.Categorical(x, categories=list(colors.keys()), ordered=True))
data = data.reset_index(drop=True)

# Print most and least accurate AF2 models
af2_models = data[data["model"] == "AF2"]
af2_models = af2_models.sort_values(by='DockQ', ascending=False)
print("Most accurate AF2 model:")
print(af2_models.iloc[0])
print("\nLeast accurate AF2 model:")
print(af2_models.iloc[-1])

# DockQ plot
# Creating a swarm plot
fig, ax = plt.subplots(figsize=(8, 6))
sns.swarmplot(
    x='model', 
    y='DockQ', 
    data=data,
    ax=ax, 
    size = 3, 
    alpha=0.6, 
    palette=colors.values(), 
    order = list(colors.keys())
)
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
ax.axhline(0.23, color='grey', linestyle='-', alpha = 0.5, linewidth=0.5)
ax.axhline(0.49, color='grey', linestyle='-', alpha = 0.5, linewidth=0.5)
ax.axhline(0.80, color='grey', linestyle='-', alpha = 0.5, linewidth=0.5)

# Add text annotations using axes fraction coordinates
text_size = 12
padding = 0.1
ax.text(0.02, 0.23-padding, 'Incorrect\nDockQ < 0.23', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.02, 0.49-padding, 'Acceptable\n0.23 ≤ DockQ < 0.49', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.02, 0.80-padding, 'Medium\n0.49 ≤ DockQ < 0.80', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.02, 1.0-padding, 'High\nDockQ ≥ 0.80', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)

# Set y-axis limit and remove x-axis ticks
ax.set_ylim(0, 1)
ax.xaxis.set_ticks_position('none')

# Set labels and title
ax.set_xlabel('', fontsize=0)
ax.set_ylabel('DockQ Score')
ax.set_xticklabels(list(colors.keys()), rotation=90, ha="center")
ax.tick_params(axis="y",direction="in")

plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()
plt.savefig(f"{plot_dir}/DockQ_scores.svg", dpi=600)
plt.close()

# RMSD plot
# Calculate the mean and standard error of the mean (SEM) for each category
means = data.groupby('model')['rmsd'].mean()
sems = data.groupby('model')['rmsd'].sem()

# Creating a bar plot
fig, ax = plt.subplots(figsize=(8, 6))

sns.swarmplot(
    x='model', 
    y='rmsd', 
    data=data,
    ax=ax, 
    size = 3.0, 
    alpha=0.6, 
    palette=colors.values(), 
    order = list(colors.keys())
)
for i, model in enumerate(list(colors.keys())):
    ax.get_children()[i].set_color(colors[model])

# Add error bars
for i, model in enumerate(list(colors.keys())):
    ax.errorbar(
        i, 
        means[model], 
        yerr=sems[model], 
        fmt='none', 
        color=colors[model], 
        capsize=5, 
        label='Mean ± SEM' if i == 0 else ""
    )

# Customize the bar colors according to the `colors` dictionary
for bar, model in zip(ax.patches, list(colors.keys())):
    bar.set_facecolor(colors[model])

# Set labels and title
ax.set_xlabel('', fontsize=0)
ax.set_ylabel('Receptor RMSD (Å)', fontsize=18)
ax.set_xticklabels(list(colors.keys()), rotation=90, ha="center", fontsize=18)
ax.tick_params(axis="y", direction="in")
plt.title('Receptor RMSD of predicted complexes', fontsize=20)

ax.set_ylim(0, max(data['rmsd'])/2)

# Remove the x-axis ticks
ax.xaxis.set_ticks_position('none')

plt.rcParams['svg.fonttype'] = 'none'
plt.tight_layout()
plt.savefig(f"{plot_dir}/receptor_rmsd.svg", dpi=600)