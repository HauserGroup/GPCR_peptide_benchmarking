""" Get all generic residue indexes for each GPCR in the dataset
"""
import pathlib
import argparse
import requests
import json
import pandas as pd
import numpy as np


def get_extended_residue_data(gpcrdb_id):
    """
    """
    url = f"https://gpcrdb.org/services/residues/extended/{gpcrdb_id}/"
    
    response = requests.get(url)
    data = json.loads(response.text)
    return data


def get_generic_residue_data_for_id(extended_data, residue_id):
    """
    extended_data: obtained through get_extended_residue_data()
    residue_id: string, e.g. "7x34"
                The ID from GPCRdb(A), see https://gpcrdb.org/residue/residuetabledisplay
                the first number denotes the helix (1-7)
                read more about generic numbers here: https://docs.gpcrdb.org/generic_numbering.html

    This script looks for the residue_id in the extended_data,
    more specifically in the "display_generic_number" keys and the "alternative_generic_numbers" key
    for each residue in the extended_data.
    """
    for residue in extended_data:
        # see if this residue matches the residue_id
        alt_gen_nums = residue["alternative_generic_numbers"]
        if len(alt_gen_nums) < 1:
            continue
        # go through the alternative generic numbers and see if any of them match the residue_id
        for alt_gen_num in alt_gen_nums:
            if alt_gen_num["scheme"] == "GPCRdb(A)":
                label = alt_gen_num["label"]
                # see if label matches residue_id. Label examples are "1.40x40", "2.53x53"
                label_helix = label.split(".")[0]
                label_residue_id = label.split("x")[1]
                label_trimmed = f"{label_helix}x{label_residue_id}"
                if label_trimmed == residue_id:
                    # match found, return the residue data
                    return residue
    
    # return None if no match was found
    return None


def test_generic_residue_search():
    """ Test the functions of this script with 2 GPCRs (class A and B1)
    """
    def nested_check_generic_residues_search(known_dict, receptor_id):
        data_extended = get_extended_residue_data(receptor_id)
        for id, known_res in known_dict.items():
            res_data = get_generic_residue_data_for_id(data_extended, id)
            found_aa = res_data["amino_acid"]
            found_seq_nr = res_data["sequence_number"]
            found_res = f"{found_aa}{found_seq_nr}"
            assert found_res == known_res, f"Error: Found {found_res}, should be {known_res}"
            print(f"\t{found_res} == {known_res}")

    # oprm_human (Class A)
    oprm_human = {"7x34":"W320",
                  "7x38":"I324",
                  "3x32":"D149",
                  "3x33":"Y150",
                  "45x52":"L221",
                  "45x51":"T220"}
    print("oprm_human test")
    nested_check_generic_residues_search(oprm_human, "oprm_human")
    print("oprm_human test passed")

    # glp1r_human (Class B1)
    glp1r_human = {"7x34":"L384",
                  "7x38":"L388",
                  "3x32":"M233",
                  "3x33":"Q234",
                  "45x52":"T298",
                  "45x51":"W297"}
    print("glp1r_human test")
    nested_check_generic_residues_search(glp1r_human, "glp1r_human")
    print("glp1r_human test passed")


def get_generic_residue_indexes(interactions_df,
                                out_path,
                                generic_residues_to_save = ["7x34", "7x38", "3x32", "3x33", "45x52", "45x51"],
                                ):
    """
    """
    # all GPCRs
    gpcrs = interactions_df["Target GPCRdb ID"].unique().tolist()

    # new df, the index is the GPCRdb ID and each of the 'generic_residues_to_save' is a column
    df = pd.DataFrame(index=gpcrs, columns=generic_residues_to_save)

    for row_index, (gpcr_id, row) in enumerate(df.iterrows()):
        print(f"Processing {gpcr_id} ({row_index+1}/{len(df)})")
        # get all generic residue data for this GPCR
        extended_data = get_extended_residue_data(gpcr_id)

        # look for the 6 generic residue numbers considered essential for the binding pocket.
        for residue_id in generic_residues_to_save:
            residue_data = get_generic_residue_data_for_id(extended_data, residue_id)
            if residue_data is None:
                # no residue data found, set to NaN
                df.loc[gpcr_id, residue_id] = np.nan
            else:
                # save the sequence number of this residue
                res_name = f"{residue_data['amino_acid']}{residue_data['sequence_number']}"
                df.loc[gpcr_id, residue_id] = res_name
            
    
    # save df
    df.to_csv(out_path, index=True)


if __name__ == "__main__":
    ARGS = argparse.ArgumentParser()
    ARGS.add_argument("--interactions_path", type=pathlib.Path, required=True)
    ARGS.add_argument("--out_path", type=pathlib.Path, required=True)
    ARGS.add_argument("--generic_residues_to_save", nargs="+", 
                      default=["7x34", "7x38", "3x32", "3x33", "45x52", "45x51"])
    ARGS = ARGS.parse_args()

    # check args
    if not ARGS.interactions_path.exists():
        raise FileNotFoundError(f"Interactions file not found: {ARGS.interactions_path}")
    if ARGS.out_path.exists():
        raise FileExistsError(f"Output path already exists: {ARGS.out_path}")

    print("Testing generic residue search (GPCRdb(A)) on two known GPCRs")
    test_generic_residue_search()

    print("Getting generic residue indexes for each GPCR in the dataset", ARGS.interactions_path)

    get_generic_residue_indexes(pd.read_csv(ARGS.interactions_path),
                                ARGS.out_path,
                                generic_residues_to_save = ARGS.generic_residues_to_save)
    
    print("Saved generic residue indexes to", ARGS.out_path)