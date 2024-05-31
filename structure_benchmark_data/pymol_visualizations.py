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

def hex_to_rgb(hex_code):
    """
    Convert a hex color code to an RGB tuple.
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def generate_pymol_color_command(hex_code, color_name):
    """
    Generate a PyMOL set_color command string.
    """
    rgb = hex_to_rgb(hex_code)
    return f"set_color {color_name}, [{rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f}]"

def visualize_pdb(config_path, repo_dir, model, pdb, color, name):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """
    
    # Parse path to the predicted structure
    model_name = pdb
    if "RFAA" in model:
        model += "_chain"
    model_dir = f"{repo_dir}/structure_benchmark/{model}"
    if 'no_templates' in model:
        model_dir += '_no_templates'
        if 'RFAA' in model:
            model_name += '_no_templates'
    model_path = f"{model_dir}/{model_name}.pdb"

    # Parse path to the experimental structure
    exp_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb}_AB.pdb"

    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    print(config_file)

    # Write the pymol script
    script = "\n".join(config_file)
    script += f"load {model_path}, {pdb}_prediction\n"
    script += f"load {exp_path}, {pdb}_experimental\n"

    # Align the structures
    script += f"alignto {pdb}_prediction, {pdb}_experimental\n"

    # Color the structures
    # Define custom color in pymol using hex code
    script += generate_pymol_color_command(color, f"{pdb}_prediction_color") + "\n"
    script += f"color {pdb}_prediction_color, {pdb}_prediction\n"
    script += f"color grey, {pdb}_experimental\n"

    # For chain B, hide cartoon and show sticks
    script += "hide cartoon, chain B\n"
    script += "show sticks, chain B\n"
    
    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/{model}"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}_{model}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)

visualize_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_config.txt", repo_dir, "AF2", best_pdb, COLOR["AF2"], "test")