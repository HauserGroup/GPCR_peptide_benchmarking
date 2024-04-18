# Script to score the models using DockQ script
import pandas as pd
import glob
import os
import time
import subprocess
import ast
from Bio.PDB import PDBParser, PDBIO, Select, PDBList
from pathlib import Path

def list_missing_residues(pdb_filename):
    """
    Helper function to create a dictionary of missing residues per chain in an experimental PDB file.
    The missing residues are extracted from REMARK 465 lines in the PDB file.

    :param pdb_filename: str, path to the PDB file.
    :return: dict, dictionary with missing residues, chain IDs as keys.
    """

    # Check that input file exists
    if not os.path.exists(pdb_filename):
        raise FileNotFoundError(f"File {pdb_filename} not found!")

    # Read contents of the PDB file
    with open(pdb_filename, 'r') as f:
        content = f.readlines()

    # Dictionary to store the missing residue indices
    result_dict = {}

    # Iterate over the lines of the PDB file and extract missing residues, saving them in the dictionary
    for line in content:
        if line[0:10] == 'REMARK 465':
            try:
                seqn = int(line[21:26].strip())
            except ValueError:
                continue 
            if line[19] not in result_dict.keys():
                result_dict[line[19]] = [seqn]
            else:
                result_dict[line[19]].append(seqn)  
    return result_dict 

def remove_missing_residues(pdb_path, missing_atom_dict, output_pdb_path = ""):
    """
    Helper function that removes missing residues from a PDB file.

    :param pdb_path: str, path to the PDB file.
    :param missing_atom_dict: dict, dictionary with missing residues, chain IDs as keys.
    :param output_pdb_path: str, path to the output PDB file.
    """

    # Read lines of pdb file
    with open(pdb_path, 'r') as f:
        content = f.readlines()

    # Remove missing residues from the PDB file - assuming that the residues are missing in the same order as they appear in the file
    # and indexing starts from 1. 
    for chain in missing_atom_dict.keys():
        if len(missing_atom_dict[chain]) > 0 and missing_atom_dict[chain][0] < 0:
            offset = abs(missing_atom_dict[chain][0])
            missing_atom_dict[chain] = [x + offset + 1 for x in missing_atom_dict[chain]]

    # Create a new file to store the corrected PDB
    if output_pdb_path == "":
        output_pdb_path = pdb_path.replace(".pdb", "_cleaned.pdb")
        
    with open(output_pdb_path, 'w') as f:
        for line in content:

            # Skip "TER" lines
            if line[0:3] == 'TER':
                continue

            # Skip lines that are not ATOM or HETATM
            if line[0:4] not in ['ATOM', 'HETA']:
                f.write(line)
                continue

            # Extract chain ID and residue number
            chain_id = line[21]
            residue_number = int(line[22:26].strip())

            # Skip residues that are not missing
            if chain_id not in missing_atom_dict.keys() or residue_number not in missing_atom_dict[chain_id]:
                f.write(line)

    return output_pdb_path

def download_pdb(pdb_code, file_format='pdb', output_path='.', overwrite=False):
    """
    Download a PDB file using a PDB code.

    :param pdb_code: str, PDB code of the structure.
    :param file_format: str, format of the PDB file ('pdb' or 'mmCif').
    :param output_path: str, directory where the file will be saved.
    :param overwrite: bool, whether to overwrite the file if it already exists.
    """

    # Build the output path
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_file = output_path / f"{pdb_code}.pdb"

    # Check if the file already exists
    if not output_file.exists() or (output_file.exists() and overwrite):
        pdbl = PDBList()
        filename = pdbl.retrieve_pdb_file(pdb_code, file_format=file_format, pdir=output_path, overwrite=False)
        Path(filename).rename(output_file)

    # Return the path to the file
    return output_file

class ChainSelect(Select):
    def __init__(self, chain_letters):
        self.chain_letters = chain_letters

    def accept_chain(self, chain):
        return chain.get_id() in self.chain_letters
    
def get_chains(pdb, chains, path, overwrite=False):
    """
    Helper function to extract chains from a PDB file.

    :param pdb: str or Path, path to the PDB file.
    :param chains: list, list of chain IDs to extract.
    :param path: str or Path, directory where the file will be saved.
    :param overwrite: bool, whether to overwrite the file if it already exists.
    """

    # Get pdb code
    pdb_code = str(Path(pdb).name.split(".")[0])

    # Create output directory
    Path(path).mkdir(parents=True, exist_ok=True)

    # Check if the file already exists
    output_file = str(Path(path) / f"{pdb_code}_{''.join(chains)}.pdb")
    if Path(output_file).exists() and not overwrite:
        return output_file

    # Parse the pdb file
    parser = PDBParser()
    structure = parser.get_structure('X', pdb)

    # Sort chains alphabetically
    chains.sort()

    # Create an object to select the chains
    chain_selector = ChainSelect(chains)

    # Write the selected chains to a new file
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_file, chain_selector)

    return output_file

def rename_chain(pdb_file, chains_to_correct, output_file, overwrite = False):
    """
    Helper function to rename chains in a PDB file.

    :param pdb_file: str or Path, path to the PDB file.
    :param chains_to_correct: dict, dictionary with the correct chain names.
    :param output_file: str or Path, path to the output file.
    :param overwrite: bool, whether to overwrite the file if it already exists.
    """

    # Check if output file already exists
    if Path(output_file).exists() and not overwrite:
        if Path(pdb_file) != Path(output_file):
            os.remove(pdb_file)
        return

    # Parse the PDB file using Biopython
    parser = PDBParser()
    structure = parser.get_structure('X', str(pdb_file))

    # Rename all chains to temporary unique identifiers
    chain_id_map = {}
    c = 1
    for chain in structure[0]:
        temp_id = str(c)
        chain_id_map[temp_id] = chain.id
        chain.id = temp_id
        c += 1

    # Rename chains to their final identifiers
    for chain in structure[0]:
        original_id = chain_id_map[str(chain.id)]
        if original_id in chains_to_correct.keys():
            chain.id = chains_to_correct[original_id]

    # Extract the model (assuming single model structure)
    model = structure[0]

    # Extract and sort chains based on their ID
    chains = list(model.get_chains())
    chains.sort(key=lambda chain: chain.id)

    # Remove existing chains and re-add them in sorted order
    for chain in chains:
        model.detach_child(chain.id)
    for chain in chains:
        model.add(chain)

    # Save the structure to a new file
    io = PDBIO()
    io.set_structure(structure)
    io.save(str(output_file))

    # Remove the original file
    if Path(pdb_file) != Path(output_file):
        os.remove(pdb_file)

def renumber_residues(pdb_file, output_file = ""):
    """
    Helper function to renumber residues in a PDB file so that each chain starts from 1.

    :param pdb_file: str or Path, path to the PDB file.
    :param output_file: str or Path, path to the output file.
    """
    # Parse the PDB file using Biopython
    parser = PDBParser()
    structure = parser.get_structure('X', pdb_file)

    # Renumber residues in each chain
    for chain in structure[0]:
        residue_id = 1
        for residue in chain:
            residue.id = (' ', residue_id, ' ')
            residue_id += 1

    # Save the structure to a new file
    if output_file == "":
        output_file = pdb_file.replace(".pdb", "_renumbered.pdb")
    io = PDBIO()
    io.set_structure(structure)
    io.save(output_file)

    return output_file

def parse_dataset(input_path, output_file, pdb_dir, overwrite = False):
    """
    Helper function to parse the dataset and download the PDB files.
    Outputs a dataframe with the paths to the cleaned PDB files and additional information (missing residues, etc.)

    :param input_path: str, path to the input CSV file.
    :param output_file: str, path to the output CSV file.
    :param pdb_dir: str, path to the directory where the PDB files will be stored.
    :return: pd.DataFrame.
    """

    # Build directory where to store cleaned PDB files
    cleaned_dir = os.path.dirname(output_file) + "/cleaned_pdbs/"

    # Check if output file already exists
    if not os.path.exists(output_file) or overwrite:

        # Loop over rows in the dataset and process each PDB file
        dataset_df = pd.read_csv(input_path)
        for index, row in dataset_df.iterrows():

            print("Processing: ", row["pdb"], row["ligand_chain"], row["receptor_chain"])
            chain_id_mapping = {row["receptor_chain"]: "A", row["ligand_chain"]: "B"}

            # Download the pdb file
            pdb_file_path = download_pdb(row["pdb"], file_format='pdb', output_path=pdb_dir)

            # Get missing residue indices from the experimental PDB file
            missing_residues = list_missing_residues(pdb_file_path)
            missing_ligand_positions = missing_residues.get(row["ligand_chain"], [])
            missing_receptor_positions = missing_residues.get(row["receptor_chain"], [])

            # Get the required chains and save the new pdb file
            pdb_file_path = get_chains(pdb_file_path, [row["receptor_chain"], row["ligand_chain"]], cleaned_dir)

            # Build output path and rename chains to AB
            new_pdb_name = row["pdb"] + "_AB.pdb"
            new_pdb_path = cleaned_dir + new_pdb_name
            rename_chain(pdb_file_path, chain_id_mapping, new_pdb_path)

            # Update the dataframe
            dataset_df.loc[index, "pdb_path"] = new_pdb_path
            dataset_df.loc[index, "missing_ligand_pos"] = str(missing_ligand_positions)
            dataset_df.loc[index, "missing_receptor_pos"] = str(missing_receptor_positions)

        dataset_df.to_csv(output_file, index=False)
    else:
        dataset_df = pd.read_csv(output_file)

    return dataset_df

def run_dockq_scoring(script_path, dockq_path, input_df, model_paths, output_file):
    """
    Function to run DockQ scoring for the models in the dataset.
    
    :param input_df: pd.DataFrame, dataframe with the dataset.
    :param model_paths: dict, dictionary with paths to the models.
    :param output_file: str, path to the output CSV file.
    """

    # List of dictionaries to store the results
    results_dicts = []

    for model_name in model_paths.keys():
        for index, row in input_df.iterrows():

            if "RFAA_no_templates" in model_name:
                model_path = model_paths[model_name] + "/" + row["pdb"] + "_no_templates.pdb"
            else:
                model_path = model_paths[model_name] + "/" + row["pdb"] + ".pdb"

            # Check if model_path exists
            if not os.path.exists(model_path):
                print(f"Model {model_path} not found!")
                continue

            # Print which model is being processed
            print(f"Processing {model_name} model of {row['pdb']}")

            # Renumber residues in the predicted model so that each chain starts from 1
            renumbered_path = renumber_residues(model_path)

            # Remove missing residues from the predicted model
            missing_residues = {
                "A" : ast.literal_eval(row["missing_receptor_pos"]),
                "B" : ast.literal_eval(row["missing_ligand_pos"])
            }
            if "AF2" in model_name:
                cleaned_path = renumbered_path
            else:
                cleaned_path = remove_missing_residues(renumbered_path, missing_residues)

            # Running DockQ command and waiting for it to complete
            dockq_command = [script_path, cleaned_path, row['pdb_path']]
            result = subprocess.run(dockq_command, capture_output=True, text=True)

            # Checking if the command was successful
            if result.returncode != 0:
                print(f"Error running DockQ for {model_name} on {row['pdb']}")
                continue

            # Rename .pdb.fixed
            fixed_pdb_folder = os.path.join(os.path.dirname(cleaned_path), "fixed_pdbs")
            os.makedirs(fixed_pdb_folder, exist_ok=True)
            fixed_pdb = os.path.join(fixed_pdb_folder, row["pdb"] + "_fixed.pdb")
            os.rename(cleaned_path + ".fixed", fixed_pdb)

            # Remove renumbered and cleaned paths
            os.remove(renumbered_path)
            try:
                os.remove(cleaned_path)
            except FileNotFoundError:
                pass

            # Run DockQ and save results into a dictionary
            try:
                dockq_command = [dockq_path, fixed_pdb, row['pdb_path']]
                results = subprocess.run(dockq_command, stdout=subprocess.PIPE, text=True)
                results = results.stdout
                results_dict = ast.literal_eval(results.split("Info dictionary:  ")[-1])
            except SyntaxError:
                print(f"Error running DockQ for {model_name} on {row['pdb']}")
                continue

            # Save results into the dataframe 
            if results_dict["len1"] > results_dict["len2"]:
                results_dict["receptor_matching_AA"] = results_dict["len1"]
                results_dict["ligand_matching_AA"] = results_dict["len2"]
            else:
                results_dict["receptor_matching_AA"] = results_dict["len2"]
                results_dict["ligand_matching_AA"] = results_dict["len1"]

            results_dict["model"] = model_name
            results_dict["pdb"] = row["pdb"]        
            results_dicts.append(results_dict)

    # Make a dataframe from the results and save it
    results_df = pd.DataFrame(results_dicts)
    results_df.to_csv(output_file, index=False)

    return results_df

if __name__ == "__main__":

    # Get directory where the current script is located
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.dirname(script_dir)

    # Path to the directory where the predicted models are stored
    dataset_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_fixed_2022-04-01.csv"
    parsed_file = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_fixed_2022-04-01_cleaned.csv"
    pdb_dir = f"{repo_dir}/structure_benchmark_data/pdbs/"

    # Parse the dataset
    input_df = parse_dataset(dataset_path, parsed_file, pdb_dir)

    # Paths to DockQ scripts
    script_path = "/projects/ilfgrid/people/pqh443/Git_projects/DockQ/scripts/fix_numbering.pl"
    dockq_path = "/projects/ilfgrid/people/pqh443/Git_projects/DockQ/DockQ.py"

    # Paths for predicted models
    model_paths = {
        "NeuralPLexer" : f"{repo_dir}/structure_benchmark/neuralplexer_chain",
        "RFAA" : f"{repo_dir}/structure_benchmark/RFAA_chain",
        "RFAA_no_templates" : f"{repo_dir}/structure_benchmark/RFAA_chain_no_templates",
        "AF2" : f"{repo_dir}/structure_benchmark/AF2",
        "AF2_no_templates" : f"{repo_dir}/structure_benchmark/AF2_no_templates",
        "ESMFold" : f"{repo_dir}/structure_benchmark/ESMFold"
    }

    # Output file path
    output_file = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"

    # Run DockQ scoring
    run_dockq_scoring(script_path, dockq_path, input_df, model_paths, output_file)
