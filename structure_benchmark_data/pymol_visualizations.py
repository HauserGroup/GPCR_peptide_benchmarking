# Script to make pymol visualizations of best and worst structures according to DockQ score
import sys
import os 
import pandas as pd

# Get the top-level directory
repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_dir)
from colors import * 

# Load DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Get best and worst AF2 models
af2_data = data[data['model'] == 'AF2']
af2_data = af2_data.sort_values(by='DockQ')
best_pdb = af2_data.iloc[-1]['pdb']
med_pdb = af2_data.iloc[len(af2_data) // 2]['pdb']
worst_pdb = af2_data.iloc[0]['pdb']

print(f"Best AF2 model: {best_pdb}")
print(f"Median AF2 model: {med_pdb}")
print(f"Worst AF2 model: {worst_pdb}")
