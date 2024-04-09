""" From all endogenous human hormone-GPCR interactions, 
    get 1 principal agonist for each GPCR.

        Step A: Receptors with 1 (known) ligand.
        Step B (manual): Receptors with "List comments" about the endogenous ligand.
                - Pick the shortest peptide in case of multiple ligands
        Step C: Receptors with no comments
                - Pick the shortest peptide with experimental proof of activity
        Step D (manual): Receptors with no comments and no experimental proof of activity
                - Pick the shortest peptide with experimental proof of activity in other species (orthologs)
"""
import pathlib
import os
import csv 
import argparse

import pandas as pd
import pygtop
import matplotlib.pyplot as plt

from step3a_plot_peptide_distributions import plot_distribution_of_occurence


def get_manual_defined_principal_agonist_dict(check=True):
    """ I manually wrote this dictionary based on the "List Comment" of each 
        GPCR in the Guide to Pharmacology database. 
        
        If the GPCRdb id of a GPCR is in the dictionary, it means that the GtP
        mentioned a principal agonist in the comment (as of 21 nov 2023). 

        check: <bool> whether to check whether the ligand name and ID match in GtP
              (only do once, just to check that the dictionary is correct)

        returns:
            dict: {<str> GPCRdb id : (<str> ligand name from commment,
                                      <str> ligand name on GtP,
                                      <int> ligand GtP id)}
    """
    out_dict = { 
            "c3ar_human" : ("C3a anaphylatoxin", "C3a", 3640),
            "c5ar1_human" : ("C5a anaphylatoxin", "C5a", 573),
            "nmbr_human" : ("Neuromedin B", "neuromedin B", 613),
            "grpr_human" : ("Gastrin-releasing peptide", "gastrin-releasing peptide", 612),
            "bkrb1_human" : ("[des-Arg<sup>10</sup>]kallidin", "[des-Arg<sup>10</sup>]kallidin", 644),

            # comments for calcr_human (with these target IDs [43 44 45 46]):
            # 'calcitonin and amylin are the principal endogenous agonists.', 
            # 'amylin, &alpha;-CGRP, and &beta;-CGRP are the most potent endogenous agonists', 
            # 'amylin is the most potent endogenous agonist',
            # 'amylin is the principal endogenous agonist'
            "calcr_human" : ("amylin", "amylin", 687), # amylin was chosen as principal agonist, because it is present for all 3 comments
            
            # comments for calcrl_human (with these target IDs [48 49 50]):
            # '&alpha;-CGRP and &beta;-CGRP are the principal endogenous agonists',
            # 'adrenomedullin and adrenomedullin 2/intermedin are the most likely physiological  agonists.',
            # 'adrenomedullin and adrenomedullin 2/intermedin are the most potent endogenous agonists'
            "calrl_human" : ("&alpha;-CGRP", "&alpha;-CGRP", 681), # &alpha;-CGRP and &beta;-CGRP were the only ligands labelled as principal agonists. Length is identical. Alpha was chosen

            "ccr1_human" : ("CCL15", "CCL15", 754), # options were CCL15 and CCL23. CCL15 is shorter
            "ccr2_human" : ("CCL2", "CCL2", 771),
            "ccr3_human" : ("CCL26", "CCL26", 776), # options were CCL11, CCL24, CCL26. CCL26 is shorter
            "cxcr1_human" : ("CXCL8", "CXCL8", 821),
            "galr1_human" : ("Galanin", "galanin", 3592),
            "galr3_human" : ("Galanin-like peptide", "galanin-like peptide", 3594),
            "gnrhr_human" : ("GnRH I", "GnRH I", 1162),
            "mshr_human" : ("&alpha;-MSH", "&alpha;-MSH", 1320),
            "mc3r_human" : ("&gamma;-MSH", "&gamma;-MSH", 1333),
            "mc4r_human" : ("&beta;-MSH", "&beta;-MSH", 3606),
            "mc5r_human" : ("&alpha;-MSH", "&alpha;-MSH", 1320),
            "npff1_human" : ("neuropeptide FF", "neuropeptide FF", 1479),
            "npff2_human" : ("neuropeptide AF", "neuropeptide AF", 3735),
            "npy1r_human" : ("neuropeptide Y", "neuropeptide Y", 1504),
            "npy2r_human" : ("neuropeptide Y", "neuropeptide Y", 1504),
            "npy4r_human" : ("peptide YY", "peptide YY", 1514),
            "npy5r_human" : ("neuropeptide Y", "neuropeptide Y", 1504),
            "ntr1_human" : ("neurotensin", "neurotensin", 1579),
            "ntr2_human" : ("neurotensin", "neurotensin", 1579),
            "oprk_human" : ("dynorphin A", "dynorphin A", 1620), # options were dynorphin A and big dynorphin. dynorphin A is shorter
            "oprm_human" : ("&beta;-endorphin", "&beta;-endorphin", 1643),
            "pkr1_human" : ("prokineticin-2", "prokineticin-2", 1867),
            "pkr2_human" : ("prokineticin-2", "prokineticin-2", 1867),
            "nk1r_human" : ("substance P", "substance P", 2098),
            "nk2r_human" : ("neurokinin A", "neurokinin A", 2089),
            "nk3r_human" : ("neurokinin B", "neurokinin B", 2090),
            "v1ar_human" : ("vasopressin", "vasopressin", 2168),
            "v1br_human" : ("vasopressin", "vasopressin", 2168),
            "v2r_human" : ("vasopressin", "vasopressin", 2168),
            "pacr_human" : ("PACAP-27", "PACAP-27", 2257), # options were: PACAP-27 and PACAP-38. PACAP-27 is shorter
            "vipr1_human" : ("VIP", "VIP", 1152), # options were: VIP, PACAP-27 and PACAP-38. PACAP-27 is shorter, VIP was chosen because pacr_human was already assigned PACAP-27
            "vipr2_human" : ("VIP", "VIP", 1152), # options were: VIP, PACAP-27 and PACAP-38 
            }

    # if check, do check using the pygtop API
    if check:
        print("Checking ligand name and ID match in GtP for manually defined principal agonists")
        for k, v in out_dict.items():
            ids_correct = check_ligand_name_and_id_match_in_GtP(ligand_name=v[1], ligand_id=v[2])
            if ids_correct is False:
                ligand = pygtop.get_ligand_by_id(v[2])
                print(ligand.name())
                raise ValueError("ligand name and ID do not match in GtP for entry", k, v)
        print("All ligand names and IDs match in GtP")

    return out_dict

def get_manual_chosen_principal_agonist_dict_for_missing_GPCRs(check=True):
    """ See the top docstring, this function is used in step D.
    I manually chose principal agonists for the GPCRs that were not caught in step A, B or C.
    These GPCRs had no comments in the Guide to Pharmacology database, and no experimental activity data

    if check, do check using the pygtop API
    
    returns:
    dict: {<str> GPCRdb id : (<str> ligand name on GtP,
                              <int> ligand GtP id)}
    """
    out_dict = {
         # chemokine receptor. Options CCL27, CCL28. No experimental data, but comment says both have been shown to be ligands. pick shortest = CCL27
        'ccr10_human' : ('CCL27', 3646),

        # CCK-8 is the only endogenous ligand with activity values on GtP (albeit from mice)
        'cckar_human' : ('CCK-8', 864), 

        # all 4 endogenous ligands have activity (but only in mice). pick shortest = R-spondin-4
        'lgr6_human' : ('R-spondin-4', 3700), 

        # options annexin I and cathepsin G. Interestingly they are endogenous but not labelled as such in the activity table. 
        # turns out both have experimental data, so pick shortest (cathepsin G)
        'fpr1_human' : ('cathepsin G', 3570), 

        # optionsL Wnt-1, Wnt-2, Wnt-5a, Wnt-3a, Wnt-7b. No experimental data, but comments says all bind to FZD1. Pick shortest = Wnt-5a
        'fzd1_human' : ('Wnt-5a', 3548), 

        # no data in GtP, but comment mentions that all are proven to bind. Pick shortest = Wnt-5a
        'fzd6_human' :  ('Wnt-5a', 3548), 

        # many endogenous ligands: CCL2 (CCL2, P13500), CCL3 (CCL3, P10147), CCL4 (CCL4, P13236), CCL5 (CCL5, P13501), CCL7 (CCL7, P80098), CCL8 (CCL8, P80075), CCL11 (CCL11, P51671), CCL13 (CCL13, Q99616), CCL14 (CCL14, Q16627), CCL17 (CCL17, Q92583), CCL22 (CCL22, O00626)
        # chose shortest, CCL5
        'ackr2_human' : ('CCL5', 758), 

        # many endogenous ligands: CXCL5 (CXCL5, P42830), CXCL6 (CXCL6, P80162), CXCL8 (CXCL8, P10145), CXCL11 (CXCL11, O14625), CCL2 (CCL2, P13500), CCL5 (CCL5, P13501), CCL7 (CCL7, P80098), CCL11 (CCL11, P51671), CCL14 (CCL14, Q16627), CCL17 (CCL17, Q92583)
        # chose shortest, CCL5
        'ackr1_human' : ('CCL5', 758),
        }
    
    if check:
        print("Checking ligand name and ID match in GtP for missing principal agonists")
        for k, v in out_dict.items():
            ids_correct = check_ligand_name_and_id_match_in_GtP(ligand_name=v[0], ligand_id=v[1])
            if ids_correct is False:
                raise ValueError("ligand name and ID do not match in GtP for entry", k, v)
    
    return out_dict


def check_ligand_name_and_id_match_in_GtP(ligand_name, ligand_id):
    ligand = pygtop.get_ligand_by_id(ligand_id)
    if ligand.name() != ligand_name:
        return False
    return True


def get_ligand_rows_with_activity(target_GPCRdb_id, activity_df):
    """ Check if the activity dataframe contains any ligand with activity for the target GPCR.

    target_GPCRdb_id: <str> target id, example = "adrb2_human"
    activity_df: <pd.DataFrame> with experimental data of pairs (pEC50, pIC50, pKd, pKi)
                 created in script step3_get_activity_data.py
    
    returns: <pd.DataFrame> with rows of ligands with activity for the target GPCR
            if no ligands with activity are found, returns an empty dataframe
    """
    rows = activity_df[activity_df["Target GPCRdb ID"] == target_GPCRdb_id]

    # get rows with a non-empty Interaction units column
    rows_with_activity = rows[rows["Interaction units"].notnull()]

    return rows_with_activity


def get_receptor_id_and_principal_agonist_id(annotated_interactions_path, activity_interactions_path):
    """
    annotated_interactions_path: path to csv with annotated interactions of GPCRs-peptides.
                                 made in script step2_annotate_interactions.py
    activity_interactions_path: path to csv with experimental data of pairs (pEC50, pIC50, pKd, pKi)
    """
    interactions_df = pd.read_csv(annotated_interactions_path)
    activity_df = pd.read_csv(activity_interactions_path)

    unique_receptors = interactions_df["Target GPCRdb ID"].unique()
    known_principal_agonists_dict = get_manual_defined_principal_agonist_dict(check=False)
    missing_principal_agonists_dict = get_manual_chosen_principal_agonist_dict_for_missing_GPCRs(check=False)

    principal_agonist_pairs = list()

    for receptor_id in unique_receptors:
        rows = interactions_df[interactions_df["Target GPCRdb ID"] == receptor_id]
        unique_peptide_sequences = rows["Ligand Sequence"].unique()
        rows_with_activity = get_ligand_rows_with_activity(receptor_id, activity_df)

        # Step A: Receptors with 1 (known) ligand.
        if len(unique_peptide_sequences) == 1:
            peptide_sequence = unique_peptide_sequences[0]
            peptide_id = rows[rows["Ligand Sequence"] == peptide_sequence]["Ligand ID"].unique()[0]

        # Step B (manual): Receptors with "List comments" about the endogenous ligand.
        elif  receptor_id in known_principal_agonists_dict:
            peptide_id = known_principal_agonists_dict[receptor_id][2]

        # Step C: Shortest peptide with experimental proof of activity
        elif len(rows_with_activity) > 0:
            # sort the activity rows by length of peptide sequence
            sorted_rows = rows_with_activity.sort_values(by="Peptide Sequence", key=lambda x: x.str.len())
            # peptide_sequences = sorted_rows["Peptide Sequence"].unique()
            peptide_id = sorted_rows["Ligand ID"].unique()[0]

        # Step D (manual): if multiple ligands, no experimental data, lookup manually
        else:
            if receptor_id not in missing_principal_agonists_dict:
                raise ValueError("receptor_id not in missing_principal_agonists_dict. Add it to the dictionary (manually).")
            peptide_id = missing_principal_agonists_dict[receptor_id][1]

        principal_agonist_pairs.append((receptor_id, peptide_id))
    
    return principal_agonist_pairs


def add_principal_agonists_to_annotated_interactions_df(df, principal_agonist_pairs):
    df["Principal Agonist"] = False

    for pair in principal_agonist_pairs:
        receptor_id = pair[0]
        peptide_id = pair[1]
        df.loc[(df["Target GPCRdb ID"] == receptor_id) & (df["Ligand ID"] == peptide_id), "Principal Agonist"] = True
    
    return df


def run_main(annotated_interactions_path, activity_interactions_path, output_path):
    # get pairs
    principal_agonist_pairs = get_receptor_id_and_principal_agonist_id(annotated_interactions_path, activity_interactions_path)
    unique_principal_agonists = set([x[1] for x in principal_agonist_pairs])
    # count how many receptors each agonist is principal for
    agonist_receptors = {x[1]: [] for x in principal_agonist_pairs}
    for pair in principal_agonist_pairs:
        agonist_receptors[pair[1]].append(pair[0])
    # print the ones that have more than one
    for agonist, receptors in agonist_receptors.items():
        if len(receptors) > 1:
            print(agonist, receptors)

    # plot distribution of occurence
    dist_of_occ_path = output_path.parent / (output_path.stem + "_principal_agonists_per_ligand.png")
    plot_distribution_of_occurence(save_path=dist_of_occ_path,
                                      data_dict=agonist_receptors,
                                        xlabel="Number of receptors (unique GPCRdb ID)",
                                        ylabel="Number of ligands (unique ligand ID)",
                                        title="Distribution of principal agonists per ligand")

    # write new version of annotated interactions with whether or not a pair is principal
    out_df = add_principal_agonists_to_annotated_interactions_df(df=pd.read_csv(annotated_interactions_path),
                                                                 principal_agonist_pairs=principal_agonist_pairs)

    # sort out_df by peptide length
    out_df = out_df.sort_values(by="Ligand Sequence", key=lambda x: x.str.len())

    # check for duplicate edges (GPCR target ID and Ligand ID)
    final_df = out_df.drop_duplicates(subset=["Target GPCRdb ID", "Ligand Sequence", "Principal Agonist"], keep="first")
    
    # see which (if any) rows were dropped (not in final_df.index)
    dropped_df = out_df[~out_df.index.isin(final_df.index)]
    print("A number of rows were dropped because they were duplicate interactions:", len(dropped_df))
    print("The dropped rows were for the following GPCRs", dropped_df["Target GPCRdb ID"].unique())
    # save these dropped rows to csv with the same path as the output_path, but "dropped" at the end
    dropped_df.to_csv(output_path.parent / (output_path.stem + "_dropped.csv"), index=False)

    # report unique ligands, targets and edges
    print("unique ligands:", len(final_df["Ligand Sequence"].unique()))
    print("unique targets:", len(final_df["Target GPCRdb ID"].unique()))
    print("unique edges:", len(final_df[["Target GPCRdb ID", "Ligand ID"]].drop_duplicates()))
    print("Number of principal agonist pairs:", len(principal_agonist_pairs))
    print("Unique number of principal agonists:", len(unique_principal_agonists))
    print("Unique number of receptors:", len(set([x[0] for x in principal_agonist_pairs])))
    
    # write to csv
    final_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    ARGS = argparse.ArgumentParser()
    ARGS.add_argument("--interactions_path", type=pathlib.Path,
                      help="Path to the annotated interactions csv", required=True)
    ARGS.add_argument("--activity_interactions_path", type=pathlib.Path,
                      help="Path to the activity interactions csv", required=True)
    ARGS.add_argument("--output_path", type=pathlib.Path,
                      help="Path to where the output should be saved", required=True)
    
    ARGS = ARGS.parse_args()
    # check args
    if not os.path.exists(ARGS.interactions_path):
        raise FileNotFoundError(f"Could not find the annotated_interactions_path: {ARGS.interactions_path}")
    if not os.path.exists(ARGS.activity_interactions_path):
        raise FileNotFoundError(f"Could not find the activity_interactions_path: {ARGS.activity_interactions_path}")
    
    run_main(annotated_interactions_path=ARGS.interactions_path,
                activity_interactions_path=ARGS.activity_interactions_path,
                output_path=ARGS.output_path)
    