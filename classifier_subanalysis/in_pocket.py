""" Check if the peptide is placed in the pocket.
    Use shortest distance to pocket & set a threshold based on the findings.

    /projects/ilfgrid/apps/neuralplexer_kcd635/mamba_env/bin/python /projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/in_pocket.py

"""
import pandas as pd
import numpy as np
import pathlib
import os 
import io
# PDB from biopython
from Bio import PDB
import torch
import concurrent.futures


def get_generic_residue_df():
    p = pathlib.Path("/projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/3d_generic_residues_binding_pocket.csv")
    df = pd.read_csv(p)
    # set first col to key
    df.set_index(df.columns[0], inplace=True)
    return df


def get_all_pdbs_from_path(p:pathlib.Path):
    return [x for x in p.iterdir() if x.suffix == ".pdb"]


def get_generic_residues_for_gpcr(gpcr_id : str, df: pd.DataFrame) -> list:
    """ Get the generic residues for a GPCR

    gpcr_id: str, the id of the GPCR
    df: pd.DataFrame, the dataframe with the generic residues
    returns: list of generic residues
    """
    ids = df.loc[gpcr_id]
    # drop nan
    ids = ids.dropna()
    return ids.tolist()


def get_pdb_structure(pdb_path):
    # read the pdb file
    with open(pdb_path, 'rb') as f:
        pdb_str = f.read()

    # parse the pdb file
    parser = PDB.PDBParser()
    handle = io.StringIO(pdb_str.decode())
    structure = parser.get_structure('', handle)
    return structure


def load_model(pdb_path):
    # load structure 
    structure = get_pdb_structure(pdb_path)
    if len(structure) > 1:
        raise ValueError("More than one model in the structure")
    model = structure[0]
    return model


def get_peptide_and_receptor_residues(pdb_path, chains_in_model, peptide_chain):
    """ Get the peptide and receptor residues from the relaxed model
    """
    # load .pdb
    model = load_model(pdb_path)

    # get chain ids for the receptor and the peptide
    receptor_chains = [x for x in chains_in_model if x != peptide_chain]

    # peptide residues
    peptide_residues = list()
    for residue in model[peptide_chain].get_residues():
        peptide_residues.append(residue)

    # receptor residues
    receptor_residues = list()
    for chain in receptor_chains:
        for residue in model[chain].get_residues():
            receptor_residues.append(residue)

    return peptide_residues, receptor_residues



def get_only_pocket_residues_for_receptor(receptor_residues, pocket_GR_ids):
    """ Get only the residues that are in the pocket

    pocket residues are from: get_generic_residues_for_gpcr
    example: ['I357', 'L361', 'L209', 'Q210', 'D273', 'W272']
    """
    # the pocket residues start at index 1
    # so do the IDs of the receptor residues
    # pocket_residues = list()
    # for residue in receptor_residues:
    #     if residue.id[1] in pocket_GR_ids:
    #         pocket_residues.append(residue)
    pocket_indexes = [int(r[1:]) for r in pocket_GR_ids]
    pocket_residues = [r for r in receptor_residues if r.id[1] in pocket_indexes]
    return pocket_residues
    

def get_chains_from_model(model):
    return [c.id for c in model.get_chains()]


def get_receptor_and_peptide_chain(model):
    ""
    chains = get_chains_from_model(model)
    if len(chains) != 2:
        raise ValueError("Model must have 2 chains")
    
    receptor_chain = "A"
    peptide_chain = "B"
    # check if A is in the chains
    if receptor_chain not in chains:
        receptor_chain = chains[0]
        peptide_chain = chains[1]
        print("Warning: Receptor chain is not A, switching to the first chain in the model")

    return receptor_chain, peptide_chain


def get_receptor_peptide_contact_map(pdb_path, peptide, receptor):
    """ Get the contact map between the receptor and the peptide using the CA residues

    peptide: list of peptide residudes
    receptor: list of receptor residues
    returns: torch.tensor with the angstrom distances between the CA atoms.
                with the shape (receptor_residues, peptide_residues)
    """
    peptide_coordinates = [p['CA'].get_coord() for p in peptide]
    peptide_coordinates = np.array(peptide_coordinates)
    peptide_coordinates = torch.tensor(peptide_coordinates)

    receptor_coordinates = [r['CA'].get_coord() for r in receptor]
    receptor_coordinates = np.array(receptor_coordinates)
    receptor_coordinates = torch.tensor(receptor_coordinates)

    # create contact map using the coordinates of the peptide CA atom and receptor CA atom
    contact_map = torch.cdist(receptor_coordinates, peptide_coordinates)

    return contact_map

def get_shortest_peptide_distance_to_pocket(pdb_path : pathlib.Path, generic_residue_df : pd.DataFrame) -> tuple:
    """
    pdb_path: path to the pdb file
              the file name must contain the gpcr_id and the peptide_id, joined by "___"
    """
    gpcr_id, peptide_id = pdb_path.stem.split("___")
    # get the receptor and peptide residues
    model = load_model(pdb_path)
    receptor_chain, peptide_chain = get_receptor_and_peptide_chain(model)
    peptide_residues, receptor_residues = get_peptide_and_receptor_residues(pdb_path, receptor_chain, peptide_chain)
    pocket_generic_residues = get_generic_residues_for_gpcr(gpcr_id, generic_residue_df)
    pocket_residues = get_only_pocket_residues_for_receptor(receptor_residues, pocket_generic_residues)
    
    pocket_cmap = get_receptor_peptide_contact_map(pdb_path, peptide_residues, pocket_residues)
    return pocket_cmap.min().item()


def process_pdb(pdb):
    identifier = pdb.stem
    predictive_model = pdb.parent.stem
    shortest_dist = get_shortest_peptide_distance_to_pocket(pdb, get_generic_residue_df())
    result = (predictive_model, identifier, shortest_dist)
    print(f"{predictive_model},{identifier},{shortest_dist}")
    return result


def main():
    # data
    data_dir = pathlib.Path("/projects/ilfgrid/data/Luuk/Classifier_models/data")
    subdirs = [x for x in data_dir.iterdir() if x.is_dir()]
    all_pdbs = [p for p in subdirs for p in get_all_pdbs_from_path(p)]
    out_p = pathlib.Path("/projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/in_pocket_results.csv")

    # for each pdb, check if the peptide is in the pocket
    with open(out_p, 'w') as f:
        f.write("model,identifier,shortest_distance\n")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(process_pdb, all_pdbs)
            for result in results:
                f.write(f"{result[0]},{result[1]},{result[2]}\n")

    print("All done")

if __name__ == "__main__":
    main()
