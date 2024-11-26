import os 
import sys
import pandas as pd
import glob
import json
import ast
import csv 
import matplotlib.pyplot as plt
import subprocess 
from Bio.PDB.NeighborSearch import NeighborSearch
from Bio.PDB import PDBParser

"""
Script to analyse the recovery of principal peptide-GPCR interactions in the tournament benchmark.
This script annotates the chosen generic residue numbers on the receptor that interact with the principal agonist.
The predicted complexes are then analysed by finding out in which predictions the principal peptide interacts with
the receptor and the percentage of such predictions is calculated. The results are then plotted in a bar plot.
"""

def list_chain_ids(pdb_file):
    """
    Lists all chain IDs in a PDB file.
    
    Args:
    pdb_file (str): Path to the PDB file.
    
    Returns:
    list: A list of chain IDs found in the PDB file.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure('pdb_structure', pdb_file)
    
    # Set to store unique chain IDs
    chain_ids = set()
    
    # Iterate through all models, chains, and residues to collect chain IDs
    for model in structure:
        for chain in model:
            chain_ids.add(chain.id)
    
    return sorted(list(chain_ids))

def get_chains_from_pdb(pdb_path, chain_to_get, output_path):
    """
    Helper function to get specific chains from a pdb file
    Note: requires pdb-tools to be installed using: pip install pdb-tools
    """
    chain_to_get = ",".join(chain_to_get)

    # Command to run on terminal - uses pdb-tools pdb_selchain to extract receptor and peptide chain from PDB file
    command = f"pdb_selchain -{chain_to_get} {pdb_path} > {output_path}"

    # Run command on terminal
    os.system(command)

    return output_path

def apply_generic_numbering(pdb_path, output_path, chain_to_get="B"):
    '''
    Function to apply generic numbering to a PDB file of a receptor. 
    '''
    # Apply generic numbering to the pdb file
    command = f'curl -X POST -F "pdb_file=@{pdb_path}" https://gpcrdb.org/services/structure/assign_generic_numbers'
    output = subprocess.check_output(command, shell=True)
    # Make sure output directory exists
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(output_path, 'wb') as f:
        f.write(output)

    # Compare lines in the input pdb and the output pdb 
    # and empty b-factor field in the output pdb so that only GRN
    # is stored in the b-factor field
    with open(pdb_path, 'r') as f:
        pdb = f.readlines()
        pdb = [line.strip() for line in pdb]
        pdb = [line for line in pdb if line.startswith("ATOM")]
        pdb = [line for line in pdb if line[21] == chain_to_get]
        
    with open(output_path, 'r') as f:
        output_pdb = f.readlines()
        output_pdb = [line.strip() for line in output_pdb]     
        output_pdb = [line for line in output_pdb if line.startswith("ATOM")] 
        output_pdb = [line for line in output_pdb if line[21] == chain_to_get]

    # Make a dictionary from residue number to generic residue number
    grn_dict = {}
    for i in range(len(pdb)):
        if pdb[i] != output_pdb[i]:
            residue_number = pdb[i][22:26].strip()
            generic_number = output_pdb[i][60:66].strip()
            grn_dict[residue_number] = generic_number
        else:
            # Replace the b-factor field with empty space
            output_pdb[i] = output_pdb[i][:60] + "     0" + output_pdb[i][66:]

    # Save the dictionary into a json file
    grn_json_path = output_path.replace(".pdb", ".json")
    with open(grn_json_path, 'w') as f:
        json.dump(grn_dict, f)

    # Save the pdb file with generic residue numbers
    with open(output_path, 'w') as f:
        for line in output_pdb:
            f.write(line + "\n")

    return output_path

def get_grn_positions(grn_pdb_path, receptor_chain):

    # Open grn_pdb file
    with open(grn_pdb_path, 'r') as f:
        grn_pdb = f.readlines()
        grn_pdb = [line.strip() for line in grn_pdb]

    # Get only CA atoms from the receptor chain
    ca_grn_pdb = [line for line in grn_pdb if "CA" == line[12:16].strip()]
    ca_grn_pdb = [line for line in ca_grn_pdb if line[21] == receptor_chain]

    # Make a dictionary with residue numbers as keys and generic residue numbers as values
    grn_dict = {}
    for grn_position in ca_grn_pdb:
        residue_number = grn_position[22:26].strip()
        generic_number = grn_position[60:66].strip()
        grn_dict[residue_number] = generic_number

    return grn_dict

def get_atom_list(pdb_path, grn_folder, pdb_name = None, receptor_chain = "B", ligand_chain = "C", search_radius = 6.6):

    # Open pdb using biopython
    from Bio.PDB import PDBParser
    parser = PDBParser()
    if pdb_name is None:
        pdb_name = pdb_path.split("/")[-1].split(".")[0]
        receptor_name = pdb_name.split("___")[0]
    else:
        receptor_name = pdb_name
    structure = parser.get_structure(pdb_name, pdb_path)

    # Save atom objects into two lists: one for the receptor and one for the peptide
    atom_list_receptor = []
    atom_list_peptide = []
    for atom in structure.get_atoms():
        chain_id = atom.get_full_id()[2]
        if chain_id == receptor_chain:
            atom_list_receptor.append(atom)
        elif chain_id == ligand_chain:
            atom_list_peptide.append(atom)

    # Apply generic numbering to the receptor
    grn_path = os.path.join(grn_folder, receptor_name + "_grn.pdb")
    grn_json_path = grn_path.replace(".pdb", ".json")
    if not os.path.exists(grn_path):
        apply_generic_numbering(pdb_path, grn_path)

    # Load the generic residue numbers from the json file
    with open(grn_json_path, 'r') as f:
        generic_residue_numbers = json.load(f)
     
    # Filter receptor atom list based on generic residue numbers
    grn_list_receptor = []
    for atom in atom_list_receptor:
        # Get residue number of atom
        residue_number = str(atom.get_parent().get_id()[1])
        if residue_number in generic_residue_numbers:
            grn_list_receptor.append(atom)

    # Concatenate two lists
    grn_list_receptor.extend(atom_list_peptide)

    # Get interactions between receptor and peptide
    ns = NeighborSearch(grn_list_receptor)
    all_neighbors = ns.search_all(search_radius, "R")
    all_neighbors = [pair for pair in all_neighbors if pair[0].get_full_id()[2] != pair[1].get_full_id()[2]]
    all_neighbors = sorted(all_neighbors, key=lambda x: x[0].get_full_id())
    
    # Return generic residue numbers for interacting receptor positions
    grns = []
    for pair in all_neighbors:
        res_n = pair[0].get_full_id()[-1][1]
        grns.append(generic_residue_numbers[str(res_n)])
    grns = list(set(grns))
    return sorted(grns)

# Build paths for the input and output files
file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
interactions_with_decoys_df = pd.read_csv(f"{repo_dir}/classifier_benchmark_data/output/6_interactions_with_decoys.csv")
principal_agonists_df = interactions_with_decoys_df[interactions_with_decoys_df["Decoy Type"] == "Principal Agonist"]

# Make folders for plots
plot_dir = f'{repo_dir}/tournament_benchmark/plots'
os.makedirs(plot_dir, exist_ok=True)

# Append the repository directory to the path to import the colors module
sys.path.append(repo_dir)
from colors import COLOR

# Read in the chosen generic residue numbers defining the orthosteric binding pocket
chosen_grn_path = f"{repo_dir}/grn_analysis/chosen_grns.txt"
with open(chosen_grn_path) as f:
    chosen_grns = f.readlines()
    chosen_grns = [x.strip() for x in chosen_grns]
    chosen_grns = [x.replace("x", ".") for x in chosen_grns]

# Ranks/tournament setups of interest 
ranks = ["one_to_zero", "one_to_two", "one_to_four", "one_to_eight", "one_to_ten"]

# Path to the folder that contains the generic residue numbers for each receptor
grn_folder = f"{repo_dir}/tournament_benchmark/grn_pdbs"

# List all pdbs in pdb_directory and its subdirectories
pdb_directory = f"{repo_dir}/tournament_benchmark"
output_csv = f"{repo_dir}/tournament_benchmark/interacting_grns.csv"

# Process each PDB file and write results to the CSV file line by line
if not os.path.exists(output_csv):
    with open(output_csv, "w", newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["setup","pdb", "chain", "interacting_grns"])
        for rank in ranks:
            c = 0
            pdb_files = glob.glob(f"{pdb_directory}/{rank}/*/*.pdb")
            for pdb in pdb_files:
                chain_ids = list_chain_ids(pdb)
                chain_ids = sorted(chain_ids)
                chain_ids = chain_ids[1:]
                c += 1
                if os.path.exists(pdb):
                    for chain in chain_ids:
                        pdb_name = os.path.basename(pdb).split("_")[0]
                        grns = get_atom_list(pdb, grn_folder, pdb_name = pdb_name, ligand_chain = chain) 
                        pdb_name = os.path.basename(pdb).split(".")[0]
                        csv_writer.writerow([rank, pdb_name, chain, grns])
    
interactions_df = pd.read_csv(output_csv)

# Loop over interactions_df and keep only those rows that have at least 
# one generic residue number that is in chosen_grns
chosen_interactions = []
for index, row in interactions_df.iterrows():

    # Convert string back to list
    interacting_grns = ast.literal_eval(row["interacting_grns"])

    # Check if any of the interacting grns are in chosen_grns,
    # if so, keep the row, otherwise discard it
    c = 0
    results = list(row)
    interacting_pocket_grns = []
    for grn in interacting_grns:
        if grn in chosen_grns:
            interacting_pocket_grns.append(grn)
            c +=1
    results.append(interacting_pocket_grns)
    results.append(c)
    chosen_interactions.append(results)

# Convert the list of lists into a pandas dataframe
chosen_interactions = pd.DataFrame(chosen_interactions, columns=["setup", "pdb", "chain", "interacting_grns", "interacting_pocket_grns", "num_interactions"])

# Sort the data frame first based on pdb, then by num_interactions descending
chosen_interactions = chosen_interactions.sort_values(by=["pdb", "num_interactions"], ascending=[True, False])
chosen_interactions = chosen_interactions[chosen_interactions["num_interactions"] > 0]
chosen_interactions = chosen_interactions.groupby("pdb").first().reset_index()

# Get the percentage of predictions in which principal agonist interacts with the receptor
plot_percentages = {}
for rank in ranks:
    plot_data = chosen_interactions[chosen_interactions["setup"] == rank]["chain"].value_counts()
    plot_data = plot_data.reset_index()
    plot_data.columns = ["Chain", "Count"]
    plot_data["Percentage"] = plot_data["Count"] / 124 * 100
    plot_percentages[rank] = plot_data[plot_data["Chain"] == "C"]["Percentage"].values[0]

# Make dictionary into a dataframe
plot_data = pd.DataFrame(plot_percentages.items(), columns=["Setup", "Percentage"])
plot_data["Setup"] = plot_data["Setup"].replace("one_to_zero", "1:0")
plot_data["Setup"] = plot_data["Setup"].replace("one_to_two", "1:2")
plot_data["Setup"] = plot_data["Setup"].replace("one_to_four", "1:4")
plot_data["Setup"] = plot_data["Setup"].replace("one_to_eight", "1:8")
plot_data["Setup"] = plot_data["Setup"].replace("one_to_ten", "1:10")

# Create a bar plot
plt.figure(figsize=(8, 6))
bars = plt.bar(plot_data['Setup'], plot_data['Percentage'], color = COLOR["Receptor"], edgecolor='black', linewidth=0.2)

# Adding text labels to bars with percentage higher than 10
for bar in bars:
    height = bar.get_height()
    if height > 10 and height < 100:
        height = round(height, 1)
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{float(height)}%', ha='center', va='bottom', fontsize=12, color='black')

plt.title("AF2's Recovery of Principal Peptide–GPCR Interactions in the Tournament Benchmark")
plt.xlabel('Principal Agonist to Receptor Ratio')
plt.ylabel('Percentage')
plt.ylim(0, 100)

# Customize ticks and remove spines
plt.tick_params(axis='y', direction='in')
plt.tick_params(axis='x', which='both', bottom=False, top=False)
plt.tight_layout()
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Save as an .svg file
plt.rcParams['svg.fonttype'] = 'none'
plt.savefig(f"{plot_dir}/interactions_recovery_by_rank.svg")