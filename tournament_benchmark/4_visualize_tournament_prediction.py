import os
import json
import sys
import glob
import pandas as pd

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
interactions_with_decoys_df = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv")
principal_agonists_df = interactions_with_decoys_df[interactions_with_decoys_df["Decoy Type"] == "Principal Agonist"]

sys.path.append(repo_dir)
from colors import COLOR

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

def tournament_pymol(config_path, repo_dir, pdb_path, colors, chain_map):
    """
    Create a pymol script to visualize predicted vs experimental structures for a given PDB file
    """

    pdb = pdb_path.split("/")[-1].split(".")[0]
    pdb = pdb.split("_")[0]
    object_name = pdb + "_tournament"

    # Shift chain map ids by one letter ahead
    chain_map = {key: chr(ord(value) + 1) for key, value in chain_map.items()}

    # Read lines from the config file
    with open(config_path, 'r') as f:
        config_file = f.readlines()

    # Write the pymol script and define custom colors
    script = "".join(config_file)
    script += f"\n\n\n"

    script += generate_pymol_color_command(colors["Principal Agonist"], f"PrincipalAgonist") + "\n"
    for i in range(5):
        script += generate_pymol_color_command(colors[f"Similar{i}"], f"Similar{i}") + "\n"
        script += generate_pymol_color_command(colors[f"Dissimilar{i}"], f"Dissimilar{i}") + "\n"
    
    script += f"\n\n\n"

    # Load model
    script += f"load {pdb_path}, {object_name}\n"

    # Color receptor
    script += f"color white, {object_name} and chain {chain_map['Receptor']}\n"

    # Color AlphaFold structures
    script += f"color PrincipalAgonist, {object_name} and chain {chain_map['Principal Agonist']}\n"
    for i in range(5):
        script += f"color Similar{i}, {object_name} and chain {chain_map[f'Similar{i}']}\n"
        script += f"color Dissimilar{i}, {object_name} and chain {chain_map[f'Dissimilar{i}']}\n"
   
    # Finetune the visualization
    script += "\n\n\n"
    script += f"set cartoon_transparency, 0.25, chain {chain_map['Receptor']}\n"
    script += "hide (hydro)\n"
    script += "hide everything, not polymer\n"
    for chain in ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]:
        script += f"hide everything, chain {chain}\n"
        script += f"set cartoon_transparency, 0, chain {chain}\n"
        script += f"set cartoon_transparency, 0, chain {chain}\n"
    script += f"set cartoon_loop_radius, 0.4\n\n\n"

    # Separate ligand into its own object
    for chain in chain_map.keys():
        chain_cleaned = chain.replace(" ", "_")
        script += f"create {chain_cleaned}, {object_name} and chain {chain_map[chain]}\n"
        script += f"show cartoon, {chain_cleaned}\n"

        # Set loop width
        loop_radius = 0.7
        script += f"set cartoon_oval_width, {loop_radius}, {chain_cleaned}\n"
        script += f"set cartoon_loop_radius, {loop_radius}, {chain_cleaned}\n"
    script += f"zoom\n"

    # Save script
    output_dir = f"{repo_dir}/tournament_benchmark/pymol_scripts/"
    os.makedirs(output_dir, exist_ok=True)
    script_path = f"{output_dir}/{object_name}.pml"    
    with open(script_path, 'w') as f:
        f.write(script)

# Use glob to find all matching files - only one_to_ten set up
pattern = os.path.join(repo_dir, "tournament_benchmark/one_to_ten/*/msas/chain_id_map.json")
matching_files = glob.glob(pattern)
chain_map_dict = {}

# Print the list of matching files
for file_path in matching_files:

    # Model name
    model_name = file_path.split("/")[-3]
    receptor_name = model_name.split("one_to_")[0] + "human"

    # Get principal agonist from the dataframe
    receptor_df = interactions_with_decoys_df[interactions_with_decoys_df["Target ID"] == receptor_name]

    # Get principal agonist
    principal_agonist = receptor_df[receptor_df["Decoy Type"] == "Principal Agonist"]["Decoy ID"].values[0]

    # Read the chain_id_map.json file
    chain_id_map = json.load(open(file_path))
    chain_map_dict[model_name] = {}

    for key in chain_id_map:
        description = chain_id_map[key]["description"]
        # Save receptor and principal agonist chains to dictionary
        if "_human" in description:
            chain_map_dict[model_name]["Receptor"] = key
            continue
        elif description == str(principal_agonist):
            chain_map_dict[model_name]["Principal Agonist"] = key
            continue

        # Get decoy type
        decoy_type = receptor_df[receptor_df["Decoy ID"] == int(description)]["Decoy Type"].values[0]
        decoy_rank = str(int(receptor_df[receptor_df["Decoy ID"] == int(description)]["Decoy Rank"].values[0]))
        chain_map_dict[model_name][f"{decoy_type}{decoy_rank}"] = key

# Create pymol script for an example case of one_to_ten prediction
pdb = f"{repo_dir}/tournament_benchmark/one_to_ten/nmur1_one_to_ten/nmur1_one_to_ten.pdb"
config_path = f"{repo_dir}/structure_benchmark_data/pymol_scripts/pymol_config.txt"
chain_map = chain_map_dict[pdb.split("/")[-2]]
tournament_pymol(config_path, repo_dir, pdb, COLOR, chain_map)