import os 
import pandas as pd
import matplotlib.font_manager as fm
import numpy as np
import matplotlib.pyplot as plt
import sys
from get_chosen_grns import get_chosen_grns
import requests
import re

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(top_level_dir)
from colors import * 

def get_pymol_string(residue_numbers):
    """
    Function to get a string that can be used in PyMOL to select residues
    """
    residue_numbers = [str(i) for i in residue_numbers]
    string = f'sel binding_site, resi {"+".join(residue_numbers)}'
    return string

def align_all(pdbs_names):
    commands = ""
    reference = pdbs_names[0]
    for pdb in pdbs_names[1:]:
        commands += f"align {pdb}, {reference}\n"
    commands += f"center {reference}\n"
    return commands 

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

def make_pymol_script(pdb_path, ligand_PDB_chain, receptor_PDB_chain, generic_residue_numbers, color_dict, config_path):
    """
    Function to generate a PyMOL script that can be used to visualize the interactions between a receptor and a ligand
    """

    # Get a string that can be used in PyMOL to select residues
    residue_numbers = [str(i) for i in generic_residue_numbers]
    residue_numbers = "+".join(residue_numbers)

    # Selection name
    pdb_name = pdb_path.split("/")[-1].split(".")[0]
    pdb_code = pdb_name.split("_")[0]
    selection_name = pdb_name + "_selection"
    ligand_name = pdb_name + "_ligand"
    receptor_name = pdb_name + "_receptor"

    # Define selections
    object_selection = f'select {selection_name}, {pdb_name}'
    binding_site_selection = f'sel binding_site_{pdb_code}, {selection_name} and chain {receptor_PDB_chain} and resi {residue_numbers}'
    ligand_selection = f'select {ligand_name}, {selection_name} and chain {ligand_PDB_chain}'

    # Get a string that can be used in PyMOL to select the receptor
    receptor_selection = f'select {receptor_name}, {selection_name} and chain {receptor_PDB_chain}'
    script = ""

    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    # Write the pymol script
    script = "".join(config_file)
    script += f"\n\n\n"

    # Generate color commands
    script += generate_pymol_color_command(color_dict["Receptor"], "receptor_color") + "\n"
    script += generate_pymol_color_command(color_dict["Ligand"], "ligand_color") + "\n"

    # Get a string that can be used in PyMOL to select the ligand and the receptor
    script += f"load '{pdb_path}'\n"
    script += object_selection + "\n"
    script += ligand_selection + "\n"
    script += receptor_selection + "\n"
    script += binding_site_selection + "\n"
    script += f"color white, {selection_name} and chain A\n"
    script += f"color ligand_color, {ligand_name} \n"
    script += f"color receptor_color, binding_site_{pdb_code} \n"
    script += f"show cartoon, {selection_name}\n"

    # Show stick for binding_site_selection
    script += f"show sticks, binding_site_{pdb_code}\n"

    script += "deselect \n"

    script += f"create {pdb_code}_ligand, {selection_name} and chain {ligand_PDB_chain}\n"
    script += f"hide cartoon, {ligand_name}\n"
    script += f"show cartoon, {pdb_code}_ligand\n"
    
    # Set loop width
    loop_radius = 0.5
    script += f"set cartoon_oval_width, {loop_radius}, {pdb_code}_ligand\n"
    script += f"set cartoon_loop_radius, {loop_radius}, {pdb_code}_ligand\n"

    # Center
    script += f"center {selection_name}\n"

    # Zoom out
    script += f"zoom\n"

    return script

def get_structure_gpcrdb(pdb_code):
    response = requests.get(f'https://gpcrdb.org/services/structure/{pdb_code}/')
    structure = response.json()
    return structure

def map_gpcrdb_b_to_a(mapping_file_path):
    # Table containing mapping from GPCRdb A to B general residue numbering
    # Source: https://github.com/protwis/gpcrdb_data/blob/master/residue_data/generic_numbers/mapping_gpcrdbb.txt
    gpcrdb_a_to_b_mapping = []

    # Read text file line by line
    with open(mapping_file_path) as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        line = line.split(" ")
        line = [i for i in line if i != ""]
        if len(line) == 2:
            line = [line[0], line[1]]
            gpcrdb_a_to_b_mapping.append(line)

    gpcrdb_a_to_b_mapping = pd.DataFrame(gpcrdb_a_to_b_mapping)
    gpcrdb_a_to_b_mapping.columns = ["gpcrdb_a", "gpcrdb_b"]

    # Convert to dictionary 
    return dict(zip(gpcrdb_a_to_b_mapping["gpcrdb_b"], gpcrdb_a_to_b_mapping["gpcrdb_a"]))

def convert_gpcrdb_class_b_to_a(receptor_grn, mapping_dict):
    # In case the last part of the GRN is three digits, remove the last digit
    # These residues represent helix bulges at a given position. 
    # For example, 5x501 is a bulge following position 5x50
    receptor_grn = re.sub(r'\.\d+', '', receptor_grn)
    if len(receptor_grn.split("x")[-1]) == 3:
        receptor_grn = receptor_grn[:-1]
    try: 
        return mapping_dict[receptor_grn]
    except:
        return None

def get_interacting_grns(pdb_code, mapping_file_path):
    response = requests.get(f'https://gpcrdb.org/services/structure/{pdb_code}/interaction/')
    interactions = response.json()
    grn_interactions = []
    for interaction in interactions:
        try:
            if interaction["interaction_type"] != "accessible":
                grn_interactions.append((interaction["display_generic_number"], interaction["sequence_number"]))
        except KeyError:
            pass

    structure_info = get_structure_gpcrdb(pdb_code)
    if structure_info["class"] == "Class B1 (Secretin)":
        gpcrdb_b_to_a_mapping = map_gpcrdb_b_to_a(mapping_file_path)
        grn_interactions = [(convert_gpcrdb_class_b_to_a(i[0], gpcrdb_b_to_a_mapping), i[1]) for i in grn_interactions]
        grn_interactions = [i for i in grn_interactions if i[0] is not None]

    grn_interactions = sorted(set(grn_interactions))
    grn_interactions = {i[0]: i[1] for i in grn_interactions}

    return grn_interactions

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'
grn_freq_path = f'{file_dir}/grn_frequencies.csv'

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(file_dir, '..'))
sys.path.append(top_level_dir)
from colors import * 

# Font path
font_path = f'{repo_dir}/Aptos.ttf'
font_prop = fm.FontProperties(fname=font_path)

interactions_df = pd.read_csv(interaction_csv_path)
chosen_grns, _, _ = get_chosen_grns(grn_freq_path, interaction_csv_path)
mapping_file_path = f"{file_dir}/mapping_gpcrdbb.txt"

# Loop through interactions_df
grns_per_pdb = {}
for index, row in interactions_df.iterrows():
    if row["pdb_code"] not in grns_per_pdb:
        grns_per_pdb[row["pdb_code"]] = [row["generic_residue_number_a"]]
    elif row["generic_residue_number_a"] not in grns_per_pdb[row["pdb_code"]]:
        grns_per_pdb[row["pdb_code"]].append(row["generic_residue_number_a"])

# Get the pdb codes included in the structural benchmark
structural_benchmark_pdbs = pd.read_csv(f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30_cleaned.csv")["pdb"].tolist()
print("structural_benchmark_pdbs: ", structural_benchmark_pdbs) 
print("Number of structural benchmark pdbs: ", len(structural_benchmark_pdbs))
# Loop through the dictionary and check if a pdb contains all chosen GRNs
pdb_codes = []
max_count = 0
for pdb_code, grns in grns_per_pdb.items():
    # Count how many GRNs are in the chosen GRNs
    count = 0
    for grn in grns:
        if grn in chosen_grns:
            count += 1
    if count >= max_count and pdb_code in structural_benchmark_pdbs:
        best_pdb = pdb_code
        max_count = count

pdb_code = best_pdb
pdb_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb_code}_AB.pdb"
interacting_grns = get_interacting_grns(pdb_code, mapping_file_path)

# Loop through interacting GRNs and remove the ones that are not in chosen GRNs
removed_grns = []
for grn in interacting_grns:
    # Clean up the GRN
    receptor_grn = re.sub(r'\.\d+', '', grn)
    if len(receptor_grn.split("x")[-1]) == 3:
        receptor_grn = receptor_grn[:-1]

    if receptor_grn not in chosen_grns:
        removed_grns.append(grn)
for grn in removed_grns:
    interacting_grns.pop(grn)
    print(f"Removed {grn}")

print("pdb_code: ", pdb_code)  
print("interacting_grns: ", interacting_grns)
print("chosen_grns: ", chosen_grns)
config_path = f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt"
output_path = f"{file_dir}/pymol_scripts/{pdb_code}_grn_interactions.pml"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

pymol_script = "reinit\n"
pymol_script += make_pymol_script(pdb_path, "B", "A", interacting_grns.values(), COLOR, config_path)

with open(output_path, "w") as f:
    f.write(pymol_script)
