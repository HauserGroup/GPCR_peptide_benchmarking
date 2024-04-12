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
dockq_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (without templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA (with templates)")
data["model"] = data["model"].replace("AF2", "AF2 (with templates)")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (without templates)")

# Calculating the means and standard deviations again to ensure clarity in this step
means = data.groupby('model')['DockQ'].mean()
stds = data.groupby('model')['DockQ'].std()
models = means.index

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(models, means, yerr=stds, capsize=4)
ax.set_xlabel('Model')
ax.set_ylabel('DockQ Score (Mean ± SD)')
ax.set_title('DockQ Scores for GPCR-Peptide Complexes')

# Add horizontal lines showing prediction quality
ax.axhline(0.23, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.49, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.80, color='grey', linestyle='-', alpha = 0.5)

text_size = 8
ax.text(0.01, 0.10, 'Incorrect (DockQ < 0.23)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.30, 'Acceptable (0.23 ≤ DockQ < 0.49)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.60, 'Medium (0.49 ≤ DockQ < 0.80)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.85, 'High (DockQ ≥ 0.80)', color='grey', fontsize=text_size, transform=ax.transAxes)

# Set limit from 0,1 to y axis
ax.set_ylim(0, 1)
ax.set_xticklabels(models, rotation=0, ha="center")

plt.tight_layout()
plt.savefig("DockQ_scores.png")


# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Creating a swarm plot
sns.swarmplot(x='model', y='DockQ', data=data, ax=ax)

# Add horizontal lines showing prediction quality
ax.axhline(0.23, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.49, color='grey', linestyle='-', alpha = 0.5)
ax.axhline(0.80, color='grey', linestyle='-', alpha = 0.5)

# Add text annotations using axes fraction coordinates
text_size = 8
ax.text(0.01, 0.10, 'Incorrect (DockQ < 0.23)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.30, 'Acceptable (0.23 ≤ DockQ < 0.49)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.60, 'Medium (0.49 ≤ DockQ < 0.80)', color='grey', fontsize=text_size, transform=ax.transAxes)
ax.text(0.01, 0.85, 'High (DockQ ≥ 0.80)', color='grey', fontsize=text_size, transform=ax.transAxes)

# Set y-axis limit
ax.set_ylim(0, 1)

# Set labels and title
ax.set_xlabel('Model')
ax.set_ylabel('DockQ Score')
ax.set_title('DockQ Scores for GPCR-Peptide Complexes')
plt.xticks(rotation=0, ha="center")

plt.tight_layout()
plt.savefig("DockQ_scores_swarm.png")