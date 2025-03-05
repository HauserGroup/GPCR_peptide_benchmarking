import os
import glob
import csv
import re
from pymol import cmd  # Importing PyMOL cmd module

# This script should be run with PyMOL installed and from command line using the following command:
# pymol -cq calculate_receptor_rmsd.py

file_dir = "/Users/pqh443/Documents/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/subanalyses"
folder_name = file_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]
model_folder = f"{repo_dir}/structure_benchmark"

model_path_dict = {
    "Chai-1": f"{model_folder}/Chai-1",
    "RFAA": f"{model_folder}/RFAA",
    "RFAA_no_templates": f"{model_folder}/RFAA_no_templates",
    "AF2": f"{model_folder}/AF2",
    "AF2_no_templates": f"{model_folder}/AF2_no_templates",
    "AF3": f"{model_folder}/AF3",
    "AF3_server": f"{model_folder}/AF3_server",
    "AF3_no_templates": f"{model_folder}/AF3_no_templates",
    "ESMFold": f"{model_folder}/ESMFold",
    "NeuralPLexer": f"{model_folder}/NeuralPLexer",
}

def calculate_rmsd(model, protein1, protein2, chain_id_1, chain_id_2):
    # Reinitialize PyMOL session
    cmd.reinitialize()

    # Parse protein names
    object_name_1 = protein1.split("/")[-1].split(".")[0] + "_exp"
    object_name_2 = protein2.split("/")[-1].split(".")[0].split("_")[0] + "_pred"

    # Load the PDB files
    cmd.load(protein1, object_name_1)
    cmd.load(protein2, object_name_2)

    # Align the chains and calculate RMSD
    rmsd = cmd.align(f"{object_name_1} and chain {chain_id_1} and name CA",
                     f"{object_name_2} and chain {chain_id_2} and name CA")

    print(f"{model}: RMSD between chain {chain_id_1} of {object_name_1} and chain {chain_id_2} of {object_name_2}: {rmsd[0]:.3f} Å")

    # Clean up loaded objects
    cmd.delete(object_name_1)
    cmd.delete(object_name_2)

    # Return only RMSD value
    return rmsd[0]

structure_list_path = f"{repo_dir}/structure_benchmark_data/structural_benchmark_dataset_cleaned.csv"
pdbs = []
with open(structure_list_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pdbs.append(row["pdb"])

results = []

for pdb in pdbs:
    experimental_path = f"{repo_dir}/structure_benchmark_data/cleaned_pdbs/{pdb}_AB.pdb"
    if not os.path.exists(experimental_path):
        print(f"Experimental PDB {pdb} not found.")
        continue
    
    for model, model_dir in model_path_dict.items():

        model_pattern = f"{model_dir}/{pdb}*"
        model_files = glob.glob(model_pattern)
        model_files = [f for f in model_files if not os.path.isdir(f)]        
        if model_files:
            for model_path in model_files:

                # Extract seed from model path. It is stored in the file name as _*.pdb
                rmsd = None
                match = re.search(r'_(\d+)\.pdb$', model_path)
                seed = match.group(1) if match else "1"
                print(f"Calculating RMSD for {pdb} with model {model} and seed {seed}.")
                model_path = repo_dir + model_path.split(repo_name)[1]
                try:
                    rmsd = calculate_rmsd(model, experimental_path, model_path, "A", "A")
                    results.append([model, pdb, seed, rmsd])
                except Exception as e:
                    print(f"Error calculating RMSD for {pdb} with model {model}: {e}")

# Sort results by model
results.sort(key=lambda x: x[0])

# Save the results to a CSV file
output_csv_path = f"{repo_dir}/structure_benchmark_data/subanalyses/receptor_rmsds.csv"
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["model", "pdb", "seed", "rmsd"])
    writer.writerows(results)