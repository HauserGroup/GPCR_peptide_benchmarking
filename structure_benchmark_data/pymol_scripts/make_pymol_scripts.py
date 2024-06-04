# Script to make pymol visualizations of best and worst structures according to DockQ score
import sys
import os 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

# Get the top-level directory
repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(repo_dir)
from colors import * 

# Get path to the current script
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

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

def visualize_pdb(config_path, repo_dir, model, pdb, color):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """

    name = pdb + "_" + model
    
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

    # Write the pymol script
    script = "".join(config_file)
    script += f"\n\n\n"
    script += f"load {model_path}, {pdb}_prediction\n"
    script += f"load {exp_path}, {pdb}_experimental\n"

    # Align the structures
    script += f"alignto {pdb}_experimental\n"
    script += "center\n"

    # Color the structures
    # Define custom color in pymol using hex code
    script += generate_pymol_color_command(color, f"{pdb}_prediction_color") + "\n"

    script += "color white, chain A\n"
    script += f"color {pdb}_prediction_color, {pdb}_prediction and chain B\n"
    script += f"color grey70, {pdb}_experimental\n"

    # Increase transparency for the experimental structure
    script += f"set cartoon_transparency, 0.25, {pdb}_experimental and chain A\n"
    script += f"set cartoon_transparency, 0.25, {pdb}_prediction and chain A\n"

    # Separate ligand into its own object
    script += f"create {pdb}_exp_ligand, {pdb}_experimental and chain B\n"
    script += f"create {pdb}_pred_ligand, {pdb}_prediction and chain B\n"

    # Set loop width
    script += f"set cartoon_loop_radius, 0.7, {pdb}_exp_ligand\n"
    script += f"set cartoon_loop_radius, 0.7, {pdb}_pred_ligand\n"

    # Hide hydrogens
    script += "hide (hydro)\n"

    # Hide all waters and small molecules
    script += "hide everything, not polymer\n"
    
    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/{model}"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)

visualize_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, "AF2", best_pdb, COLOR["AF2"])
visualize_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, "AF2", med_pdb, COLOR["AF2"])
visualize_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, "AF2", worst_pdb, COLOR["AF2"])

def visualize_af_rfaa_pdb(config_path, repo_dir, pdb, colors):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """

    name = pdb + "_alphafold_rfaa"
    af2_path = f"{repo_dir}/structure_benchmark/AF2/{pdb}.pdb"
    af2_no_templates_path = f"{repo_dir}/structure_benchmark/AF2_no_templates/{pdb}.pdb"
    af3_path = f"{repo_dir}/structure_benchmark/AF3/{pdb}.pdb"
    rfaa_path = f"{repo_dir}/structure_benchmark/RFAA_chain/{pdb}.pdb"
    rfaa_no_templates_path = f"{repo_dir}/structure_benchmark/RFAA_chain_no_templates/{pdb}_no_templates.pdb"

    # Parse path to the experimental structure
    exp_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb}_AB.pdb"

    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    # Write the pymol script and define custom colors
    script = "".join(config_file)
    script += f"\n\n\n"
    script += generate_pymol_color_command(colors["AF2"], f"{pdb}_af2_color") + "\n"
    script += generate_pymol_color_command(colors["AF3"], f"{pdb}_af3_color") + "\n"
    script += generate_pymol_color_command(colors["AF2 (no templates)"], f"{pdb}_af2_nt_color") + "\n"
    script += generate_pymol_color_command(colors["Agonist"], f"{pdb}_experimental_color") + "\n"
    script += generate_pymol_color_command(colors["RF-AA"], f"{pdb}_rfaa_color") + "\n"
    script += generate_pymol_color_command(colors["RF-AA (no templates)"], f"{pdb}_rfaa_nt_color") + "\n"
    script += "set grid_mode, 1\n"
    script += f"\n\n\n"

    # Load AlphaFold models
    script += f"load {af2_path}, {pdb}_af2\n"
    script += f"load {af2_no_templates_path}, {pdb}_af2_no_templates\n"
    script += f"load {af3_path}, {pdb}_af3\n"
    script += f"load {exp_path}, {pdb}_experimental\n"

    # Color AlphaFold structures
    script += f"color {pdb}_af2_color, {pdb}_af2 and chain B\n"
    script += f"color {pdb}_af2_nt_color, {pdb}_af2_no_templates and chain B\n"
    script += f"color {pdb}_af3_color, {pdb}_af3 and chain B\n"

    # Load RF-AA models
    script += f"\n\n\n"
    script += f"load {rfaa_path}, {pdb}_rfaa\n"
    script += f"load {rfaa_no_templates_path}, {pdb}_rfaa_no_templates\n"
    script += f"load {exp_path}, {pdb}_experimental_2\n"

    # Color RFAA structures
    script += "color white, chain A\n"
    script += f"color {pdb}_rfaa_color, {pdb}_rfaa and chain B\n"
    script += f"color {pdb}_rfaa_nt_color, {pdb}_rfaa_no_templates and chain B\n"

    # Color experimental structure
    script += f"color {pdb}_experimental_color, {pdb}_experimental_2 and chain B\n"
    script += f"color {pdb}_experimental_color, {pdb}_experimental and chain B\n"
    script += f"color grey60, {pdb}_experimental_2 and chain A\n"
    script += f"color grey60, {pdb}_experimental and chain A\n"

    # Align the structures
    script += f"alignto {pdb}_experimental\n"

    # Finetune the visualization
    script += f"set cartoon_transparency, 0.25, chain A\n"
    script += "hide (hydro)\n"
    script += "hide everything, not polymer\n"
    script += "hide everything, chain B\n"
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_loop_radius, 0.4\n"

    # Separate ligand into its own object
    script += f"create {pdb}_exp_ligand, {pdb}_experimental and chain B\n"
    script += f"create {pdb}_exp_2_ligand, {pdb}_experimental_2 and chain B\n"
    script += f"create {pdb}_rfaa_ligand, {pdb}_rfaa and chain B\n"
    script += f"create {pdb}_rfaa_nt_ligand, {pdb}_rfaa_no_templates and chain B\n"
    script += f"create {pdb}_af2_ligand, {pdb}_af2 and chain B\n"
    script += f"create {pdb}_af2_nt_ligand, {pdb}_af2_no_templates and chain B\n"
    script += f"create {pdb}_af3_ligand, {pdb}_af3 and chain B\n"

    script += f"show cartoon, {pdb}_exp_ligand\n"
    script += f"show cartoon, {pdb}_exp_2_ligand\n"
    script += f"show cartoon, {pdb}_rfaa_ligand\n"
    script += f"show cartoon, {pdb}_rfaa_nt_ligand\n"
    script += f"show cartoon, {pdb}_af3_ligand\n"
    script += f"show cartoon, {pdb}_af2_nt_ligand\n"
    script += f"show cartoon, {pdb}_af2_ligand\n"

    # Set loop width
    loop_radius = 0.7
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_exp_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_exp_2_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af2_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af2_nt_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_rfaa_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_rfaa_nt_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af3_ligand\n"

    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_exp_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_exp_2_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af2_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af2_nt_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_rfaa_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_rfaa_nt_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af3_ligand\n"

    # Set grid slots for specific structures
    script += f"set grid_slot, 1, {pdb}_experimental\n"
    script += f"set grid_slot, 1, {pdb}_experimental_2\n"
    script += f"set grid_slot, 1, {pdb}_exp_2_ligand\n"
    script += f"set grid_slot, 1, {pdb}_exp_ligand\n"

    script += f"set grid_slot, 2, {pdb}_af2\n"
    script += f"set grid_slot, 2, {pdb}_af2_no_templates\n"
    script += f"set grid_slot, 2, {pdb}_af3\n"
    script += f"set grid_slot, 2, {pdb}_af2_ligand\n"
    script += f"set grid_slot, 2, {pdb}_af2_nt_ligand\n"
    script += f"set grid_slot, 2, {pdb}_af3_ligand\n"

    script += f"set grid_slot, 3, {pdb}_rfaa\n"
    script += f"set grid_slot, 3, {pdb}_rfaa_no_templates\n"
    script += f"set grid_slot, 3, {pdb}_rfaa_ligand\n"
    script += f"set grid_slot, 3, {pdb}_rfaa_nt_ligand\n"
    script += f"center {pdb}_experimental\n"
    script += f"zoom\n"

    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/{pdb}"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)


def visualize_bad_models_pdb(config_path, repo_dir, pdb, colors):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """
    name = pdb + "_esmfold_neuralplexer"
    esm_path = f"{repo_dir}/structure_benchmark/ESMFold/{pdb}.pdb"
    neuralplexer_path = f"{repo_dir}/structure_benchmark/neuralplexer_chain/{pdb}.pdb"

    # Parse path to the experimental structure
    exp_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb}_AB.pdb"

    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    # Write the pymol script
    script = "".join(config_file)
    script += f"\n\n\n"
    script += f"load {esm_path}, {pdb}_esm\n"
    script += f"load {neuralplexer_path}, {pdb}_neuralplexer\n"
    script += f"load {exp_path}, {pdb}_experimental\n"

    # Align the structures
    script += f"alignto {pdb}_experimental\n"
    script += "center\n"

    # Color the structures
    # Define custom color in pymol using hex code
    script += generate_pymol_color_command(colors["NeuralPLexer"], f"{pdb}_neuralplexer_color") + "\n"
    script += generate_pymol_color_command(colors["ESMFold"], f"{pdb}_esmfold_color") + "\n"
    script += generate_pymol_color_command(colors["Agonist"], f"{pdb}_experimental_color") + "\n"

    script += "color white, chain A\n"
    script += f"color {pdb}_esmfold_color, {pdb}_esmfold and chain B\n"
    script += f"color {pdb}_neuralplexer_color, {pdb}_neuralplexer and chain B\n"
    script += f"color {pdb}_experimental_color, {pdb}_experimental and chain B\n"
    script += f"color grey60, {pdb}_experimental and chain A\n"

    # Increase transparency for the experimental structure
    script += f"set cartoon_transparency, 0.25, chain A\n"

    # Hide hydrogens
    script += "hide (hydro)\n"

    # Hide all waters and small molecules
    script += "hide everything, not polymer\n"

    # Adjust transparency and loop width
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_transparency, 0, chain B\n"
    script += "set cartoon_loop_radius, 0.4\n"

    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/{pdb}"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)


visualize_af_rfaa_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, worst_pdb, COLOR)
visualize_af_rfaa_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, med_pdb, COLOR)
visualize_af_rfaa_pdb("/Users/pqh443/Documents/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, best_pdb, COLOR)


colors_to_plot = ["Agonist", "AF2", "AF3", "RF-AA", "RF-AA (no templates)", "AF2 (no templates)"]

# Specify the path to the Aptos font file
font_path = f'{repo_dir}/Aptos.ttf'  
font_prop = fm.FontProperties(fname=font_path)

# Create a list of legend entries
legend_entries = [mpatches.Patch(color=color, label=model) for model, color in COLOR.items() if model in colors_to_plot]

# Rename Agonist to Experimental
legend_entries[0] = mpatches.Patch(color=COLOR["Agonist"], label="Experimental")

# Create a figure and a legend
fig, ax = plt.subplots(figsize=(2, 1.5))  # Adjust the size as needed
legend = ax.legend(handles=legend_entries, loc='center', prop=font_prop)

# Increase the size of the legend
plt.setp(legend.get_texts(), fontproperties=font_prop)
legend_frame = legend.get_frame()
legend_frame.set_linewidth(0)  # Remove the border

# Hide the axes
ax.axis('off')

# Adjust the layout to fit the legend size
fig.tight_layout(pad=0)

# Save the legend as a PNG file
plt.savefig(f'{script_dir}/legend.png', dpi=600)


# Filter DockQ data to only include the models we want to plot
print(data.head())

columns = ["model", "pdb","DockQ", "irms", "Lrms", "fnat", "fnonnat"]
models_to_check = ["AF2", "AF2_no_templates","AF3", "RFAA", "RFAA_no_templates"]
data = data[data["model"].isin(models_to_check)][columns]
# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (no templates)")

# Get only the best and worst models
data = data[data["pdb"].isin([best_pdb, med_pdb, worst_pdb])]

data = data.round(2)
data.columns = ["Model", "PDB", "DockQ", "iRMS", "lRMS", "Fnat", "Fnonnat"]

model_order = ["AF2", "AF2 (no templates)","AF3", "RF-AA", "RF-AA (no templates)"]

# Convert the PDB and Model columns to categorical types with the specified order
data['PDB'] = pd.Categorical(data['PDB'], categories=[worst_pdb, med_pdb, best_pdb], ordered=True)
data['Model'] = pd.Categorical(data['Model'], categories=model_order, ordered=True)

# Sort the DataFrame based on the ordered categorical columns
data = data.sort_values(by=['PDB', 'Model'])

save_path = f"{script_dir}/DockQ_worst_to_best.csv"
data.to_csv(save_path, index=False)

latex_table = data.to_latex(
    index=False,  # To not include the DataFrame index as a column in the table
    label="tab:model_comparison",  # A label used for referencing the table within the LaTeX document
    position="htbp",  # The preferred positions where the table should be placed in the document ('here', 'top', 'bottom', 'page')
    column_format="|l|c|c|c|c|c|c|",  # The format of the columns: left-aligned with vertical lines between them
    escape=False,  # Disable escaping LaTeX special characters in the DataFrame
    float_format="{:0.2f}".format  # Formats floats to two decimal places
)

print(latex_table)