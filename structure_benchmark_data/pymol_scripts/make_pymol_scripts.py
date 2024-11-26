# Script to make pymol visualizations of best and worst structures according to DockQ score
import sys
import os 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.font_manager as fm

def rename_chains_in_pdb(input_pdb, output_pdb):
    # Open the input PDB file for reading
    with open(input_pdb, 'r') as infile:
        # Open the output PDB file for writing
        with open(output_pdb, 'w') as outfile:
            # Loop over each line in the input PDB file
            for line in infile:
                # Only modify lines that start with 'ATOM' or 'HETATM'
                if line.startswith(('ATOM', 'HETATM')):
                    # Get the current chain identifier (which is in column 22, index 21 in the string)
                    chain_id = line[21]

                    # Rename chain B to A, and C to B
                    if chain_id == 'B':
                        line = line[:21] + 'A' + line[22:]
                    elif chain_id == 'C':
                        line = line[:21] + 'B' + line[22:]

                # Write the (potentially modified) line to the output file
                outfile.write(line)

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

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

# Fix Chai models to have AB suffix and change chain B to A and C to B
for model in [worst_pdb, med_pdb, best_pdb]:
    for chai_model in ["Chai-1", "Chai-1_no_MSAs"]:
        if "no_MSAs" in chai_model:
            model += "_no_MSAs"
        input_pdb = f"{repo_dir}/structure_benchmark/{chai_model}/{model}.pdb"
        output_pdb = f"{repo_dir}/structure_benchmark/{chai_model}/{model}_AB.pdb"
        rename_chains_in_pdb(input_pdb, output_pdb)

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

def visualize_af_rfaa_pdb(config_path, repo_dir, pdb, colors):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """
    name = pdb + "_alphafold_rfaa_chai"
    af2_path = f"{repo_dir}/structure_benchmark/AF2/{pdb}.pdb"
    af2_no_templates_path = f"{repo_dir}/structure_benchmark/AF2_no_templates/{pdb}.pdb"
    af3_path = f"{repo_dir}/structure_benchmark/AF3/{pdb}.pdb"
    rfaa_path = f"{repo_dir}/structure_benchmark/RFAA_chain/{pdb}.pdb"
    rfaa_no_templates_path = f"{repo_dir}/structure_benchmark/RFAA_chain_no_templates/{pdb}_no_templates.pdb"
    chai_path = f"{repo_dir}/structure_benchmark/Chai-1/{pdb}_AB.pdb"
    chai_no_msas_path = f"{repo_dir}/structure_benchmark/Chai-1_no_MSAs/{pdb}_no_MSAs_AB.pdb"

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
    script += generate_pymol_color_command(colors["Chai-1"], f"{pdb}_chai_color") + "\n"
    script += generate_pymol_color_command(colors["Chai-1 (no MSAs)"], f"{pdb}_chai_no_msas_color") + "\n"
    script += "set grid_mode, 1\n"
    script += f"\n\n\n"

    # Load experimental model
    script += f"load {exp_path}, {pdb}_experimental\n"

    # Load AlphaFold models
    script += f"load {af2_path}, {pdb}_af2\n"
    script += f"load {af2_no_templates_path}, {pdb}_af2_no_templates\n"
    script += f"load {af3_path}, {pdb}_af3\n"

    # Color AlphaFold structures
    script += f"color {pdb}_af2_color, {pdb}_af2 and chain B\n"
    script += f"color {pdb}_af2_nt_color, {pdb}_af2_no_templates and chain B\n"
    script += f"color {pdb}_af3_color, {pdb}_af3 and chain B\n"

    # Load RF-AA models
    script += f"\n\n\n"
    script += f"load {rfaa_path}, {pdb}_rfaa\n"
    script += f"load {rfaa_no_templates_path}, {pdb}_rfaa_no_templates\n"

    # Color RFAA structures
    script += "color white, chain A\n"
    script += f"color {pdb}_rfaa_color, {pdb}_rfaa and chain B\n"
    script += f"color {pdb}_rfaa_nt_color, {pdb}_rfaa_no_templates and chain B\n"

    # Load Chai models
    script += f"\n\n\n"
    script += f"load {chai_path}, {pdb}_chai\n"
    script += f"load {chai_no_msas_path}, {pdb}_chai_no_msas\n"

    # Color Chai structures
    script += f"color white, chain A\n"
    script += f"color {pdb}_chai_color, {pdb}_chai and chain B\n"
    script += f"color {pdb}_chai_no_msas_color, {pdb}_chai_no_msas and chain B\n"

    # Color experimental structure
    script += f"color {pdb}_experimental_color, {pdb}_experimental and chain B\n"
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
    script += f"create {pdb}_rfaa_ligand, {pdb}_rfaa and chain B\n"
    script += f"create {pdb}_rfaa_nt_ligand, {pdb}_rfaa_no_templates and chain B\n"
    script += f"create {pdb}_af2_ligand, {pdb}_af2 and chain B\n"
    script += f"create {pdb}_af2_nt_ligand, {pdb}_af2_no_templates and chain B\n"
    script += f"create {pdb}_af3_ligand, {pdb}_af3 and chain B\n"
    script += f"create {pdb}_chai_ligand, {pdb}_chai and chain B\n"
    script += f"create {pdb}_chai_no_msas_ligand, {pdb}_chai_no_msas and chain B\n"

    script += f"show cartoon, {pdb}_exp_ligand\n"
    script += f"show cartoon, {pdb}_rfaa_ligand\n"
    script += f"show cartoon, {pdb}_rfaa_nt_ligand\n"
    script += f"show cartoon, {pdb}_af3_ligand\n"
    script += f"show cartoon, {pdb}_af2_nt_ligand\n"
    script += f"show cartoon, {pdb}_af2_ligand\n"
    script += f"show cartoon, {pdb}_chai_ligand\n"
    script += f"show cartoon, {pdb}_chai_no_msas_ligand\n"

    # Set loop width
    loop_radius = 0.7
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_exp_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af2_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af2_nt_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_rfaa_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_rfaa_nt_ligand\n"
    script += f"set cartoon_oval_width, {loop_radius}, {pdb}_af3_ligand\n"

    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_exp_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af2_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af2_nt_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_rfaa_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_rfaa_nt_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_af3_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_chai_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb}_chai_no_msas_ligand\n"

    # Set grid slots for specific structures
    script += f"set grid_slot, 1, {pdb}_experimental\n"
    script += f"set grid_slot, 1, {pdb}_exp_ligand\n"

    script += f"set grid_slot, 2, {pdb}_rfaa\n"
    script += f"set grid_slot, 2, {pdb}_rfaa_no_templates\n"
    script += f"set grid_slot, 2, {pdb}_rfaa_ligand\n"
    script += f"set grid_slot, 2, {pdb}_rfaa_nt_ligand\n"

    script += f"set grid_slot, 3, {pdb}_chai\n"
    script += f"set grid_slot, 3, {pdb}_chai_no_msas\n"
    script += f"set grid_slot, 3, {pdb}_chai_ligand\n"
    script += f"set grid_slot, 3, {pdb}_chai_no_msas_ligand\n"


    script += f"set grid_slot, 4, {pdb}_af2\n"
    script += f"set grid_slot, 4, {pdb}_af2_no_templates\n"
    script += f"set grid_slot, 4, {pdb}_af3\n"
    script += f"set grid_slot, 4, {pdb}_af2_ligand\n"
    script += f"set grid_slot, 4, {pdb}_af2_nt_ligand\n"
    script += f"set grid_slot, 4, {pdb}_af3_ligand\n"

    script += f"center {pdb}_experimental\n"
    script += f"zoom\n"

    # Save script
    output_dir = f"{repo_dir}/structure_benchmark_data/pymol_scripts/{pdb}"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)


visualize_af_rfaa_pdb(f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, worst_pdb, COLOR)
visualize_af_rfaa_pdb(f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, med_pdb, COLOR)
visualize_af_rfaa_pdb(f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt", repo_dir, best_pdb, COLOR)

colors_to_plot = ["Agonist", "AF2", "AF3", "RF-AA", "RF-AA (no templates)", "AF2 (no templates)", "Chai-1", "Chai-1 (no MSAs)"]

# Create a list of legend entries
legend_entries = [mpatches.Patch(color=color, label=model) for model, color in COLOR.items() if model in colors_to_plot]

# Rename Agonist to Experimental
legend_entries[0] = mpatches.Patch(color=COLOR["Agonist"], label="Experimental")

# Create a figure and a legend
fig, ax = plt.subplots(figsize=(2, 1.5))  # Adjust the size as needed
legend = ax.legend(handles=legend_entries, loc='center')

# Increase the size of the legend
plt.setp(legend.get_texts())
legend_frame = legend.get_frame()
legend_frame.set_linewidth(0)  # Remove the border

# Hide the axes
ax.axis('off')

# Adjust the layout to fit the legend size
fig.tight_layout(pad=0)

# Save the legend as a PNG file
plt.rcParams['svg.fonttype'] = 'none'
plt.savefig(f'{script_dir}/legend.svg', dpi=600)

columns = ["model", "pdb","DockQ", "irms", "Lrms", "fnat", "fnonnat"]
models_to_check = ["AF2", "AF2_no_templates","AF3", "RFAA", "RFAA_no_templates", "Chai-1", "Chai-1_no_MSAs"]
data = data[data["model"].isin(models_to_check)][columns]
# Rename RFAA_no_templates to RF-AA (without templates)
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (no templates)")
data["model"] = data["model"].replace("Chai-1_no_MSAs", "Chai-1 (no MSAs)")

# Get only the best and worst models
data = data[data["pdb"].isin([best_pdb, med_pdb, worst_pdb])]
data = data.round(2)
data.columns = ["Model", "PDB", "DockQ", "iRMS", "lRMS", "Fnat", "Fnonnat"]

model_order = ["AF2", "AF2 (no templates)","AF3", "RF-AA", "RF-AA (no templates)", "Chai-1", "Chai-1 (no MSAs)"]

# Convert the PDB and Model columns to categorical types with the specified order
data['PDB'] = pd.Categorical(data['PDB'], categories=[worst_pdb, med_pdb, best_pdb], ordered=True)
data['Model'] = pd.Categorical(data['Model'], categories=model_order, ordered=True)

# Sort the DataFrame based on the ordered categorical columns
data = data.sort_values(by=['PDB', 'Model'])

save_path = f"{script_dir}/DockQ_worst_to_best.csv"
data.to_csv(save_path, index=False)

# Drop iRMS, lRMS, Fnat and Fnonnat columns
data = data.drop(columns=["iRMS", "lRMS", "Fnat", "Fnonnat"])

# Reformat the data so that each model has a column for each PDB dockq scores
data = data.pivot(index='Model', columns='PDB', values='DockQ').reset_index()
data.to_csv(f"{script_dir}/DockQ_figure_table.csv", index=False)