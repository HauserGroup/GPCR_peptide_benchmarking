# Script to list missing neuralplexer structures
import os
import json

def list_files_in_directory_and_subdirectories(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

def get_missing_pdbs(pdb_codes, pdb_files):
    """
    Helper function to get the missing PDB codes from a list of predicted protein structures.
    
    Args:
    pdb_codes: list of PDB codes
    pdb_files: list of PDB files
    return: list of missing PDB codes
    """
    missing_pdb_codes = [code for code in pdb_codes if not any(code.lower() in file.lower() for file in pdb_files)]
    return missing_pdb_codes

file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_name = "GPRC_peptide_benchmarking"
repo_dir = file_dir.split(repo_name)[0] + repo_name
fasta_folder = f"{repo_dir}/structure_benchmark_data/fastas/pairs/"

if __name__ == "__main__":
    # Get the list of PDBs
    pdb_list = []
    for file in os.listdir(fasta_folder):
        if file.endswith(".fasta"):
            pdb = file.split(".")[0]
            pdb_list.append(pdb)

    # Get the list of PDBs in the neuralplexer dataset
    neuralplexer_chain = f"{repo_dir}/structure_benchmark/neuralplexer_chain"
    af2 = f"{repo_dir}/structure_benchmark/AF2"
    af2_no_template = f"{repo_dir}/structure_benchmark/AF2_no_templates"
    af3 = f"{repo_dir}/structure_benchmark/AF3"
    RFAA = f"{repo_dir}/structure_benchmark/RFAA_chain"
    RFAA_no_templates = f"{repo_dir}/structure_benchmark/RFAA_chain_no_templates"
    ESMFold = f"{repo_dir}/structure_benchmark/ESMFold"

    # Dictionary to store the missing PDBs per model
    missing_pdb_dict = {}

    # Get the missing PDBs for each model
    for folder in [neuralplexer_chain, af2, af2_no_template, af3, RFAA, RFAA_no_templates, ESMFold]:
        files = list_files_in_directory_and_subdirectories(folder)
        files = [f for f in files if f.endswith('.pdb')]

        # Filter the files to only include the PDBs
        missing_pdbs = get_missing_pdbs(pdb_list, files)
        if len(missing_pdbs) > 0:
            missing_pdb_dict[folder.split("/")[-1]] = missing_pdbs
                    
    # Save to json  
    with open(f'{file_dir}/missing_pdbs_per_model.json', 'w') as f:
        json.dump(missing_pdb_dict, f, indent=4)