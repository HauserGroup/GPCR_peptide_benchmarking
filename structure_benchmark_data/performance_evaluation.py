# Script to make plots of DockQ performance metrics

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve

# Load DockQ data
dockq_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results_new.csv"
data = pd.read_csv(dockq_path)

# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA\n(without templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA\n(with templates)")
data["model"] = data["model"].replace("AF2", "AF2\n(with templates)")
data["model"] = data["model"].replace("AF2_no_templates", "AF2\n(without templates)")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Color the points based on model
colors = {
    'NeuralPLexer' : "#dc8c03",
    'ESMFold': "#478347",
    'RF-AA\n(with templates)': '#a676d6', 
    'RF-AA\n(without templates)': '#7352bf', 
    'AF2\n(with templates)': '#115185', 
    'AF2\n(without templates)': '#008fd7',
    'AF3': '#008fd7',
} 

data = data.sort_values(by='model', key=lambda x: pd.Categorical(x, categories=list(colors.keys()), ordered=True))
print(data.head())

# Reset index
data = data.reset_index(drop=True)

# Creating a swarm plot
sns.swarmplot(x='model', y='DockQ', data=data, ax=ax, size=4, alpha=0.9, palette=colors.values(), order = list(colors.keys()))

for i, model in enumerate(list(colors.keys())):
    ax.get_children()[i].set_color(colors[model])

# Add horizontal lines showing prediction quality
ax.axhline(0.23, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.49, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.80, color='grey', linestyle='-', alpha = 0.5)

# Add text annotations using axes fraction coordinates
text_size = 12
ax.text(0.01, 0.10, 'Incorrect (DockQ < 0.23)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.01, 0.30, 'Acceptable (0.23 ≤ DockQ < 0.49)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.01, 0.60, 'Medium (0.49 ≤ DockQ < 0.80)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)
ax.text(0.01, 0.85, 'High (DockQ ≥ 0.80)', color='black', fontsize=text_size, transform=ax.transAxes, alpha = 0.5)

# Set y-axis limit
ax.set_ylim(0, 1)

# Set labels and title
ax.set_xlabel('', fontsize=0)
ax.set_ylabel('DockQ Score', fontsize=16)
ax.set_title('DockQ Scores for Predicted Peptide-GPCR Complexes\n', fontsize=18)
ax.set_xticklabels(list(colors.keys()), rotation=45, ha="center", fontsize=12)

plt.tight_layout()
plt.savefig("DockQ_scores_swarm_new.png")