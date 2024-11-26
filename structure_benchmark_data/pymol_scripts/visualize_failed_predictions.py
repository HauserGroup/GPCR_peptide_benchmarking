# Script to visualize failed predictions of RF-AA
import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking" 
repo_dir = file_dir.split(repo_name)[0] + repo_name
plot_dir = f'{file_dir}/plots'
sys.path.append(repo_dir)
from colors import * 

# Visualize failed predictions using PyMol
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

def pymol_script(config_path, repo_dir, pdbs, colors, model, name):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """
    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    model_color = model
    if "RFAA" in model:
        model_color = model_color.replace("RFAA", "RF-AA")
    if "no_templates" in model:
        model_color = model_color.replace("_no_templates", " (no templates)")
    if "no_MSAs" in model:
        model_color = model_color.replace("_no_MSAs", " (no MSAs)")
    
    # Write the pymol script and define custom colors
    script = "".join(config_file)
    script += f"\n\n\n"
    script += f"\n\n\n"
    script += generate_pymol_color_command(colors["Agonist"], "experimental_color") + "\n"
    script += generate_pymol_color_command(colors[model_color], model_color) + "\n"

    # Parse model folder
    model_folder = model
    if "RFAA" in model:
        model_folder = model_folder.replace("RFAA", "RFAA_chain")
    if "neuralplexer" in model.lower():
        model_folder = "neuralplexer_chain"

    if "Chai" in model:
        model_folder += "/renamed_chains"

    for pdb in pdbs:
        # Parse path to the experimental structure
        exp_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb}_AB.pdb"

        if "no_MSAs" in model:
            model_path = f"{repo_dir}/structure_benchmark/{model_folder}/{pdb}_no_MSAs.pdb"
        else:
            model_path = f"{repo_dir}/structure_benchmark/{model_folder}/{pdb}.pdb"

        # Load experimental and predicted model
        script += f"load {exp_path}, {pdb}_experimental\n"
        script += f"load {model_path}, {pdb}_{model}\n"
        if pdbs[0] != pdb:
            script += f"align {pdb}_experimental, {pdbs[0]}_experimental \n"
        script += f"align {pdb}_{model}, {pdb}_experimental\n"
        
        # Color structures
        script += f"color grey70, chain A and {pdb}_{model}\n"
        script += f"color white, chain A and {pdb}_experimental\n"
        script += f"color {model_color}, {pdb}_{model} and chain B\n"
        script += f"color experimental_color, {pdb}_experimental and chain B\n"

        # Separate ligand into its own object
        script += f"create {pdb}_exp_ligand, {pdb}_experimental and chain B\n"
        script += f"create {pdb}_{model}_ligand, {pdb}_{model} and chain B\n"
        script += f"show cartoon, {pdb}_exp_ligand\n"
        script += f"show cartoon, {pdb}_{model}_ligand\n"

        # Set loop width
        loop_radius = 0.7
        script += f"set cartoon_oval_width, {loop_radius}, {pdb}_exp_ligand\n"
        script += f"set cartoon_oval_width, {loop_radius}, {pdb}_{model}_ligand\n"
        script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_exp_ligand\n"
        script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_{model}_ligand\n"

    # Set grid slots for specific structures
    grid_slot = 1
    script += f"\n\n\n"
    script += f"set grid_mode, 1\n"
    for pdb in pdbs:
        script += f"set grid_slot, {grid_slot}, {pdb}_experimental\n"
        script += f"set grid_slot, {grid_slot}, {pdb}_exp_ligand\n"
        script += f"set grid_slot, {grid_slot}, {pdb}_{model}\n"
        script += f"set grid_slot, {grid_slot}, {pdb}_{model}_ligand\n"
        grid_slot += 1

    # Finetune the visualization
    script += f"set cartoon_transparency, 0.25, chain A\n"
    script += "hide (hydro)\n"
    script += "hide everything, not polymer\n"
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_loop_radius, 0.4\n"
    script += "center\n"
    script += "zoom\n"

    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/failed_predictions"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)

# Benchmark data path
structural_benchmark_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30_cleaned.csv"
structural_benchmark_df = pd.read_csv(structural_benchmark_path)

# Receptor RMSD data
receptor_rmsd_path = f"{repo_dir}/structure_benchmark_data/subanalyses/receptor_rmsds.csv"
receptor_rmsd_df = pd.read_csv(receptor_rmsd_path)

# Load DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
dockq_df = pd.read_csv(dockq_path)

# Merge the DockQ data with the structural benchmark data and RMSD data
dockq_df = dockq_df.merge(structural_benchmark_df, on="pdb")
dockq_df = dockq_df.merge(receptor_rmsd_df, on=["pdb", "model"])

# Check whether DockQ score is significantly correlated with the number of residues in the receptor
dockq_df["receptor_length"] = dockq_df["receptor_pdb_seq"].str.len()

# Make a new column "success" based on DockQ score
dockq_df["success"] = "Fail"
dockq_df.loc[dockq_df["DockQ"] >= 0.23, "success"] = "Acceptable"
dockq_df.loc[dockq_df["DockQ"] >= 0.49, "success"] = "Medium"
dockq_df.loc[dockq_df["DockQ"] >= 0.80, "success"] = "High"
dockq_df["correct"] = "False"
dockq_df.loc[dockq_df["DockQ"] >= 0.23, "correct"] = "True"

# Keep only RF-AA predictions (model contains RF-AA)
rf_aa_df = dockq_df[dockq_df["model"].str.contains("RFAA")]
rf_aa_no_templates = rf_aa_df[rf_aa_df["model"].str.contains("no_templates")]
rf_aa_templates = rf_aa_df[~rf_aa_df["model"].str.contains("no_templates")]
rf_aa_template_success = rf_aa_templates["success"].value_counts()
print("\nRF-AA predictions:")
print(rf_aa_template_success)

# Get value counts of success for RF-AA predictions without templates
rf_aa_no_templates_success = rf_aa_no_templates["success"].value_counts()
print("\nTemplate free RF-AA predictions:")
print(rf_aa_no_templates_success)

# List failed PDB codes for RF-AA predictions
failed_rf_aa = rf_aa_templates[rf_aa_templates["success"] == "Fail"]
print("\nPDB codes of failed RF-AA predictions:")
print(failed_rf_aa["pdb"].values)

# Make pymol scripts for failed predictions of each model
config_path = f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt"
failed_pdbs = {}
for model in dockq_df["model"].unique():
    failed_pdbs[model] = dockq_df[(dockq_df["model"] == model) & (dockq_df["success"] == "Fail")]["pdb"].values
    name = f"{model}_failed_predictions"
    pymol_script(config_path, repo_dir, failed_pdbs[model], COLOR, model, name)

# Visualize failed predictions of RF-AA in specific instances (large extracellular loops and large receptors)
extracellular_pdb = ["7F6I", "7W40", "7W3Z", "7W56", "7W53"]
pymol_script(config_path, repo_dir, extracellular_pdb, COLOR, "RFAA", "RFAA_extracellular_fail")

receptor_fold_pdb = ["8IA8", "8HK2", "7P00", "7Y64", "7W55", "8F7W", "8F7Q", "8F7X", "7T10", "7T11", "7XMS"]
pymol_script(config_path, repo_dir, receptor_fold_pdb, COLOR, "RFAA", "RFAA_receptor_fold_fail")