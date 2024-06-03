'''
Script to check whether a predicted receptor-ligand complex includes interactions between the ligand and the receptor.
The interactions will only focus on the generic residue numbers that are observed in the dataset of stucturally resolved complexes of 
GPCRs and endogenous peptide ligands or their non-endogenous analogues.
'''

import subprocess 

from Bio.PDB.NeighborSearch import NeighborSearch

def get_chains_from_pdb(pdb_path, chain_to_get, output_path):
    """
    Helper function to get specific chains from a pdb file
    Note: requires pdb-tools to be installed using: pip install pdb-tools
    """
    import os 

    chain_to_get = ",".join(chain_to_get)

    # Command to run on terminal - uses pdb-tools pdb_selchain to extract receptor and peptide chain from PDB file
    command = f"pdb_selchain -{chain_to_get} {pdb_path} > {output_path}"

    # Run command on terminal
    os.system(command)

    return output_path

def apply_generic_numbering(pdb_path, output_path):
    '''
    Function to apply generic numbering to a PDB file of a receptor. 
    '''

    command = f'curl -X POST -F "pdb_file=@{pdb_path}" https://gpcrdb.org/services/structure/assign_generic_numbers'
    output = subprocess.check_output(command, shell=True)

    # Save file
    with open(output_path, 'wb') as f:
        f.write(output)

    return output_path


def find_grn_positions(original_pdb_path, grn_pdb_path, receptor_chain):

    # Find the non-identical lines between two files
    with open(original_pdb_path, 'r') as file1:
        with open(grn_pdb_path, 'r') as file2:
            original_pdb = file1.readlines()
            grn_pdb = file2.readlines()

            # Strip all lines
            original_pdb = [line.strip() for line in original_pdb]
            grn_pdb = [line.strip() for line in grn_pdb]

    # Get lines that appear only in grn_pdb
    difference = [line for line in grn_pdb if line not in original_pdb]
    difference = [line for line in difference if receptor_chain == line[21]]
    difference = [line for line in difference if "ATOM" == line[0:4].strip()]

    # Keep only CA atoms
    difference = [line for line in difference if "CA" == line[12:16].strip()]

    # Save the difference to a file
    with open("difference.txt", "w") as f:
        for line in difference:
            f.write(f"{line}\n")

    difference = [line[22:26].strip() for line in difference]

    # Get residue numbers
    difference = list(set(difference))

    # Sort residue numbers
    difference = sorted(difference, key=lambda x: int(x))

    print(difference)

    return difference

def get_atom_list(pdb_path, receptor_chain = "A", ligand_chain = "B"):

    # Open pdb using biopython
    from Bio.PDB import PDBParser
    parser = PDBParser()

    chains_to_get = [receptor_chain, ligand_chain]

    # Parse pdb name
    pdb_name = pdb_path.split("/")[-1].split(".")[0]
    pdb_path = get_chains_from_pdb(pdb_path, chains_to_get, f'{pdb_name}_{"".join(chains_to_get)}.pdb')

    # Get structure
    structure = parser.get_structure(pdb_name, pdb_path)

    # Get atom list
    atom_list_receptor = []
    atom_list_peptide = []
    for atom in structure.get_atoms():
        # Get chain id of the atom
        chain_id = atom.get_full_id()[2]
        if chain_id == receptor_chain:
            atom_list_receptor.append(atom)
        elif chain_id == ligand_chain:
            atom_list_peptide.append(atom)

    grn_path = pdb_path.replace(".pdb", "_grn.pdb")

    # Apply generic numbering to the receptor
    pdb_with_grn = apply_generic_numbering(pdb_path, grn_path)

    # Get list of generic residue numbers for the receptor
    generic_residue_numbers = find_grn_positions(pdb_path, pdb_with_grn, receptor_chain)

    filtered_atom_list_receptor = []

    for atom in atom_list_receptor:
        # Get residue number of atom
        residue_number = str(atom.get_parent().get_id()[1])
        print(residue_number)

        if residue_number in generic_residue_numbers:
            filtered_atom_list_receptor.append(atom)

    print(generic_residue_numbers)

    # Save atom list receptor to a file
    with open("atom_list_receptor.txt", "w") as f:
        for atom in filtered_atom_list_receptor:
            f.write(f"{atom.get_full_id()}\n")    

    # Concatenate two lists
    filtered_atom_list_receptor.extend(atom_list_peptide)

    # Get interactions
    ns = NeighborSearch(filtered_atom_list_receptor)
    all_neighbors = ns.search_all(6.6, "R")

    # Filter pairs that are within same chain
    all_neighbors = [pair for pair in all_neighbors if pair[0].get_full_id()[2] != pair[1].get_full_id()[2]]
    
    # Sort interactions based on pair[0] residue number
    all_neighbors = sorted(all_neighbors, key=lambda x: x[0].get_full_id())

    # Save interactions to a text file
    with open("interactions.txt", "w") as f:
        for pair in all_neighbors:
            f.write(f"{pair[0].get_full_id()} {pair[1].get_full_id()}\n")

            
get_atom_list("7sk3.pdb")
