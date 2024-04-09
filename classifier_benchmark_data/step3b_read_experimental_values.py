""" Get the activity values for each target - peptide sequence pair in the annotated interactions csv.
"""
import pathlib
import argparse
import os 

import pandas as pd
import matplotlib.pyplot as plt

from step1_get_valid_interactions import read_GtP_csv


def get_activity_rows(endo_detailed_df, target_ids, ligand_ids):
    """
    target_ids: list of int, GtP target IDs
    ligand_ids: list of int, GtP ligand IDs

    returns:
        
    """
    is_human_func = lambda x: "Human" in str(x)
    # correct ligand
    rows = endo_detailed_df[endo_detailed_df["Ligand ID"].isin(ligand_ids)]
    # Correct target
    rows =  rows[rows["Target ID"].isin(target_ids)]

    # human peptide
    rows = rows[rows["Ligand Species"].apply(is_human_func)]
    # human target species
    rows = rows[rows["Target Species"].apply(is_human_func)]
    # human interaction species
    rows = rows[rows["Interaction Species"].apply(is_human_func)]

    # check interaction units are not null
    rows = rows[rows["Interaction Units"].notnull()]

    return rows


def plot_parameter_counts_barplot(parameter, plot_df, save_path):
    """ Create a simple barplot with two bars for each unique row in plot_df
            The first bar is the number of unique ligands for this target
            The second bar is the number of values for this parameter for this target
    """
    fig, ax = plt.subplots(figsize=(30, 4)) # place 4 below each other in ppt
    # fig, ax = plt.subplots(figsize=(16, 4))
    # get the x values
    x = range(len(plot_df))
    # get the x labels
    x_labels = plot_df.index.tolist()
    # number of ligands
    values = plot_df[0].tolist()
    unique_ligands = [v[0] for v in values]
    experimental_values_count = [v[1] for v in values]

    # set bar width to 0.4 to make space for the second bar
    bar_width = 0.4

    # plot the first bar
    ax.bar(x, unique_ligands, width=bar_width, color="blue", label="Unique ligands")
    # plot the second bar
    ax.bar([i + bar_width for i in x], experimental_values_count, width=bar_width, color="red", label=f"{parameter} values")

    # add a line for count = 1
    ax.axhline(y=1, color="black", linestyle="--", label="Count = 1")

    # add labels
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, rotation=90)
    ax.set_xlabel("GPCRdb ID", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)
    ax.set_title(f"Unique ligands vs {parameter} values", fontsize=16)
    ax.legend()
    # save
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def get_activity_df(annotated_df, endo_detailed_df, parameters):
    """ Get a dataframe with all the activity values for each 
        GPCR target - peptide sequence combination in the annotated df.

        The dataframe will have the following columns:
        Target GPCRdb ID,Peptide Sequence,Target ID,Ligand ID,Interaction parameter,Interaction units

        Example of the values:
        grpr_human,VPLPAGGGTVLTKMYPRGNHWAVGHLM,39,612,pKi,6.3 - 8.2
        grpr_human,VPLPAGGGTVLTKMYPRGNHWAVGHLM,39,612,pIC50,9.9 - 10.0
        vipr2_human,HSDAVFTDNYTRLRKQMAVKKYLNSILN,372,1152,pIC50,8.5|8.0|8.5|7.7|8.3

        # In case there are multiple Target IDs, Ligand IDs or Interaction units,
        they will be separated by a "|".

    """
    # define empty df
    output_df = pd.DataFrame(columns=["Target GPCRdb ID", "Peptide Sequence",
                                      "Target ID", "Ligand ID", "Interaction parameter", 
                                      "Interaction units"])
    # get unique GPCRdb ids 
    unique_GPCRdb_ids = annotated_df["Target GPCRdb ID"].unique().tolist()

    # for each parameter (experiment type)
    for parameter in parameters:
        # for each unique target (GPCRdb id)
        for GPCRdb_id in unique_GPCRdb_ids:
            # get the target ids and peptide sequences from the annotated df
            target_rows = annotated_df[annotated_df["Target GPCRdb ID"] == GPCRdb_id]
            target_ids = target_rows["Target ID"].unique().tolist()
            peptide_sequences = target_rows["Ligand Sequence"].unique().tolist()
            
            # for each sequence targetting this GPCR
            for pep_seq in peptide_sequences:
                # get the ligand ids (in case one peptide sequence has multiple ligands)
                ligand_ids = target_rows[target_rows["Ligand Sequence"] == pep_seq]["Ligand ID"].unique().tolist()
                # get the rows for this target and peptide sequence from the endo_detailed_df
                activity_rows = get_activity_rows(endo_detailed_df=endo_detailed_df,
                                                  target_ids=target_ids,
                                                  ligand_ids=ligand_ids)                     
                # get the rows for this parameter
                activity_rows = activity_rows[activity_rows["Interaction Parameter"] == parameter]
                # get the units (values, for example: "8.6 - 10.4")
                values = activity_rows["Interaction Units"].tolist()
                # add new row to df with pd.concat
                new_row = pd.DataFrame({"Target GPCRdb ID": GPCRdb_id,
                                        "Peptide Sequence": pep_seq,
                                        "Target ID": "|".join(map(str, target_ids)),
                                        "Ligand ID": "|".join(map(str, ligand_ids)),
                                        "Interaction parameter": parameter,
                                        "Interaction units": "|".join(map(str, values)),
                                        }, index=[0])
                output_df = pd.concat([output_df, new_row], ignore_index=True)

    return output_df


def run_main(annotated_df_path, endo_detailed_path, parameters, save_activity_path):
    annotated_df = pd.read_csv(annotated_df_path)
    unique_pair_count = len(annotated_df.drop_duplicates(subset=["Target GPCRdb ID", "Ligand Sequence"]))
    print(f"Getting the activity values for {unique_pair_count} unique target - peptide sequence pairs")

    endo_detailed_df = read_GtP_csv(endo_detailed_path)
    activity_df = get_activity_df(annotated_df, endo_detailed_df, parameters)
    # report stats
    print(f"Percent of interactions (out of {unique_pair_count}) with activity values:")
    receptor_ids_without_activity = set(activity_df["Target GPCRdb ID"].unique().tolist())
    for parameter in parameters:
        rows_for_parameter = activity_df[activity_df["Interaction parameter"] == parameter]
        # empty Interaction units
        rows_without_data = rows_for_parameter[rows_for_parameter["Interaction units"] == ""]
        rows_with_data = rows_for_parameter[rows_for_parameter["Interaction units"] != ""]
        percent_with_data = round((len(rows_with_data) / len(rows_for_parameter)) * 100, 2)
        print(f"\t{parameter}: {percent_with_data}%")
        # remove the receptor ids that have no activity values
        receptor_ids_without_activity -= set(rows_with_data["Target GPCRdb ID"].unique().tolist())

    print("Receptor ids without ANY activity values:", receptor_ids_without_activity)

    # save
    activity_df.to_csv(save_activity_path, index=False)


if __name__ == "__main__":
    """
    """
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--interactions_path", type=pathlib.Path, help="Path to the annotated interactions csv", required=True)
    PARSER.add_argument("--endo_detailed_path", type=pathlib.Path, help="Path to the endogenous_ligand_detailed.csv file", required=True)
    PARSER.add_argument("--save_activity_path", type=pathlib.Path, help="Path to save the activity values csv", required=True)

    PARSER.add_argument("--parameters", type=str, nargs="+",
                        help="List of parameters to get the activity values for", default=["pKi", "pEC50", "pIC50", "pKd"])

    # check args
    ARGS = PARSER.parse_args()
    if not os.path.exists(ARGS.interactions_path):
        raise FileNotFoundError(f"Could not find the interactions_path: {ARGS.interactions_path}")
    if not os.path.exists(ARGS.endo_detailed_path):
        raise FileNotFoundError(f"Could not find the endo_detailed_path: {ARGS.endo_detailed_path}")
    
    run_main(annotated_df_path=ARGS.interactions_path,
             endo_detailed_path=ARGS.endo_detailed_path,
             parameters=ARGS.parameters,
             save_activity_path=ARGS.save_activity_path)
