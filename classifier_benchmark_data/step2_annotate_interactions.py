""" From the valid_interactions.csv from step 1, create the dataset with positive samples of the classifier benchmark.
    
    - Drop experimental duplicates
    - Add the GPCRdb ID (such as oprk_human)
    - Add the GPCR class (such as Opioid, Neurotensin, Apeline, etc..)
    - Add the GPCR family (such as A (Rhodopsin))
    - Add the GPCR sequence

"""
import pathlib
import requests
import argparse
import os 

import pandas as pd
import pygtop
import numpy as np


def get_GPCR_json_dict(GPCRdb_id):
    """ Get the json dict for a GPCR from GPCRdb.
    
    returns: <dict>
            example:
            {'entry_name': 'adrb2_human', 'name': '&beta;<sub>2</sub>-adrenoceptor', 'accession': 'P07550', 'family': '001_001_003_008', 
            'species': 'Homo sapiens', 'source': 'SWISSPROT', 'residue_numbering_scheme': 'GPCRdb(A)', 
            'sequence': 'MGQPGNGSAFLLAPNGSHAPDHDVTQERDEVWVVGMGIVMSLIVLAIVFGNVLVITAIAKFERLQTVTNYFITSLACADLVMGLAVVPFGAAHILMKMWTFGNFWCEFWTSIDVLCVTASIETLCVIAVDRYFAITSPFKYQSLLTKNKARVIILMVWIVSGLTSFLPIQMHWYRATHQEAINCYANETCCDFFTNQAYAIASSIVSFYVPLVIMVFVYSRVFQEAKRQLQKIDKSEGRFHVQNLSQVEQDGRTGHGLRRSSKFCLKEHKALKTLGIIMGTFTLCWLPFFIVNIVHVIQDNLIRKEVYILLNWIGYVNSGFNPLIYCRSPDFRIAFQELLCLRRSSLKAYGNGYSSNGNTGEQSGYHVEQEKENKLLCEDLPGTEDFVGHQGTVPSDNIDSQGRNCSTNDSLL',
            'genes': ['ADRB2', 'ADRB2R', 'B2AR']}
    """
    # fetch a protein
    url = f'https://gpcrdb.org/services/protein/{GPCRdb_id}/'
    response = requests.get(url)

    # check status
    if response.status_code != 200:
        raise ValueError(f"GPCRdb returned status code {response.status_code} for {GPCRdb_id}.")
    
    protein_data = response.json()
    return protein_data


def get_GPCR_family_levels(gpcr_json_dict):
    """ Get the numerical family levels.
    returns: <tuple> of <str>
                example: ('001', '001', '003', '008')
                which are the levels of the GPCR family
                with the following hierarchy:
                001: Class
                001: Family
                003: Subfamily
                008: Sub-subfamily
    """
    family_str = gpcr_json_dict["family"] # example: '001_001_003_008'

    # split into levels
    segments = family_str.split("_")
    class_level = segments[0]
    family_level = "_".join(segments[:2])
    subfamily_level = "_".join(segments[:3])
    subsubfamily_level = "_".join(segments[:4])    

    return class_level, family_level, subfamily_level, subsubfamily_level


def get_GPCR_sequence(gpcr_json_dict):
    return gpcr_json_dict["sequence"]


def fix_missing_GPCRdb_ids(df):
    """ Manually fixed some of the missing GPCRdb IDs.
        These were not found by the pygtop API,
        so I manually looked them up on GtP & GPCRdb.org based on the name of the target.
    """
    missing_GPCRdb_id_dict = {"44":"calcr_human", # AMY1 receptor, family calcitonin receptors
                              "45":"calcr_human", # AMY2 receptor, family calcitonin receptors
                              "46":"calcr_human", # AMY3 receptor, family calcitonin receptors
                              "47":"calcr_human", # calrl_human = 47 = calcitonin receptor-like receptor 
                              "48":"calrl_human", # CGRP receptor
                              "49":"calrl_human", # AM1 receptor 
                              "50":"calrl_human", # AM2 receptor
                              "229":"fzd1_human", # FZD1, Class Frizzled GPCRs
                              "230":"fzd2_human", # FZD2, Class Frizzled GPCRs
                              "234": "fzd6_human", # FZD6, class Frizzled GPCRs
                              "257":"gnrhr_human", # GnRH2 receptor,  Family: Gonadotrophin-releasing hormone receptors 
                              "284":"mc3r_human", # MC3 receptor, Melanocortin receptors
                              "651":"gp107_human", # GPR107, other 7TM proteins
                              }
    for i, row in df.iterrows():
        if str(row["Target ID"]) in missing_GPCRdb_id_dict:
            df.at[i, "Target GPCRdb ID"] = missing_GPCRdb_id_dict[str(row["Target ID"])]
    return df


def fix_wrong_GPCRdb_ids(df):
    """ Manually fixed some of the wrong GPCRdb IDs
    """
    wrong_GPCRdb_id_dict = {"gpr1_human":"cml2_human",
                            "etbr2_human":"g37l1_human",
                            "gnrr2_human":np.nan, # gnrr2_human is a putative receptor, don't include
                            }
    for i, row in df.iterrows():
        if row["Target GPCRdb ID"] in wrong_GPCRdb_id_dict:
            df.at[i, "Target GPCRdb ID"] = wrong_GPCRdb_id_dict[row["Target GPCRdb ID"]]
    return df


def annotate_interactions(valid_interactions_file, output_file):
    """ From all valid interactions listed in the GtP, 
        create a dataset with positive samples for the classifier benchmark.
        The GPCR family and sequence info is added and experimental duplicates are dropped.

    valid_interactions_file: pathlib.Path
                    The csv file with the valid interactions from step 1.
    output_file: pathlib.Path
                    The output path for the .csv file with the positive dataset.

    returns: None
            Writes a csv file to disk.
    """
    # read the valid interactions file
    valid_interactions = pd.read_csv(valid_interactions_file)

    # (manual) fix missing GPCRdb IDs
    valid_interactions = fix_missing_GPCRdb_ids(valid_interactions)
    # (manual) fix wrong GPCRdb IDs
    valid_interactions = fix_wrong_GPCRdb_ids(valid_interactions)

    # raise ValueError if there are NaNs in the GPCRdb ID column
    if valid_interactions["Target GPCRdb ID"].isna().sum() > 0:
         # report the NaNs by their target ID and name
        for i, row in valid_interactions.iterrows():
            if pd.isna(row["Target GPCRdb ID"]):
                print(row["Target ID"])
        raise ValueError(f"Found {valid_interactions['Target GPCRdb ID'].isna().sum()} NaNs in the GPCRdb ID column.")

    print(f"Manually drop identical peptides with different IDs...")
    # drop duplicates
    ligand_ids_to_drop = [8524, # apj_human
                          3558, 3562, 3566, 8408, # gasr_human 
                          1499, 1500]
    for ligand_id_to_drop in ligand_ids_to_drop:
        valid_interactions = valid_interactions[valid_interactions["Ligand ID"] != ligand_id_to_drop]
    # check all peptides with the same sequence have the same ID
    for ligand_sequence in valid_interactions["Ligand Sequence"].unique():
        ligand_ids = valid_interactions[valid_interactions["Ligand Sequence"] == ligand_sequence]["Ligand ID"].unique()
        if len(ligand_ids) > 1:
            raise ValueError(f"Found {len(ligand_ids)} ligand IDs for ligand sequence {ligand_sequence}.")
    # check all peptides have a unique sequence
    for ligand_id in valid_interactions["Ligand ID"].unique():
        ligand_sequences = valid_interactions[valid_interactions["Ligand ID"] == ligand_id]["Ligand Sequence"].unique()
        if len(ligand_sequences) > 1:
            raise ValueError(f"Found {len(ligand_sequences)} ligand sequences for ligand ID {ligand_id}.")
        
    print(f"This dataset has {len(valid_interactions)} interactions, with {len(valid_interactions['Ligand Sequence'].unique())} peptides and {len(valid_interactions['Target GPCRdb ID'].unique())} receptors")
    # number of duplicates before dropping
    duplicates = valid_interactions.duplicated(subset=["Ligand Sequence", "Target GPCRdb ID"], keep=False).sum()
    print(f"Out of these, {duplicates} interactions are experimental duplicates. (Same peptide sequence, same GPCR)")
    
    # add the target and ligand names
    print("Adding the names of the targets and ligands.")
    valid_interactions["Target Name"] = np.nan
    valid_interactions["Ligand Name"] = np.nan
    for i, row in valid_interactions.iterrows():
        print(f"Adding names for interaction {i+1}/{len(valid_interactions)}", end="\r")
        target = pygtop.get_target_by_id(row["Target ID"])
        ligand = pygtop.get_ligand_by_id(row["Ligand ID"])
        valid_interactions.at[i, "Target Name"] = target._name
        valid_interactions.at[i, "Ligand Name"] = ligand._name

    # add the GPCR sequence, class, family, subfamily, subsubfamily
    valid_interactions["GPCR Sequence"] = np.nan
    valid_interactions["GPCR Class"] = np.nan
    valid_interactions["GPCR Family"] = np.nan
    valid_interactions["GPCR Subfamily"] = np.nan
    valid_interactions["GPCR Sub-subfamily"] = np.nan
    print("Adding the GPCR sequence, class, family, subfamily, subsubfamily.")
    for i, row in valid_interactions.iterrows():
        print(f"Adding GPCR info for interaction {i+1}/{len(valid_interactions)}", end="\r")
        gpcr_json_dict = get_GPCR_json_dict(row["Target GPCRdb ID"])
        gpcr_sequence = get_GPCR_sequence(gpcr_json_dict)
        valid_interactions.at[i, "GPCR Sequence"] = gpcr_sequence
        class_level, family_level, subfamily_level, subsubfamily_level = get_GPCR_family_levels(gpcr_json_dict)
        valid_interactions.at[i, "GPCR Class"] = class_level
        valid_interactions.at[i, "GPCR Family"] = family_level
        valid_interactions.at[i, "GPCR Subfamily"] = subfamily_level
        valid_interactions.at[i, "GPCR Sub-subfamily"] = subsubfamily_level

    # count the number of unique interactions (unique peptide sequence, unique GPCR)
    unique_interactions = valid_interactions.drop_duplicates(subset=["Ligand Sequence", "Target GPCRdb ID"])
    print("Out of these, there are", len(unique_interactions), "unique interactions.")

    # write the dataframe to disk
    print(f"Writing {len(valid_interactions)} annotated interactions to {output_file}")
    valid_interactions.to_csv(output_file, index=False)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--valid_interactions_csv", type=pathlib.Path, required=True)
    PARSER.add_argument("--output_file", type=pathlib.Path, required=True)
    PARSER.add_argument("--overwrite", action="store_true")

    ARGS = PARSER.parse_args()

    # check ARGS
    if ARGS.output_file.exists() and not ARGS.overwrite:
        raise ValueError(f"Output file {ARGS.output_file} already exists. Use --overwrite to overwrite.")
    if ARGS.output_file.exists() and ARGS.overwrite:
        os.remove(ARGS.output_file)
    if not ARGS.valid_interactions_csv.exists():
        raise FileNotFoundError(f"Valid interactions file {ARGS.valid_interactions_csv} does not exist.")
    
    annotate_interactions(ARGS.valid_interactions_csv, ARGS.output_file)