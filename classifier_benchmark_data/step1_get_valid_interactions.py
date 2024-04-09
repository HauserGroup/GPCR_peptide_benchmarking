""" A script to get all human agonist peptide - GPCR interactions from Guide to Pharmacology 
and write them to a csv file.
"""
import requests
import csv
import pathlib
import argparse
import os

import pygtop
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


def read_GtP_csv(path_to_csv):
    """ Read a .csv file from GtP, such as GtP_interactions.csv
        After downloading the columns look like this:
        "Target","Target ID","Target Subunit IDs","Target Gene Symbol", ...

        So read the file with pandas and remove the quote characters.

        path_to_csv: pathlib.Path
        returns: pandas.DataFrame
    """
    df = pd.read_csv(path_to_csv,
                       # each value is surrounded by "", remove these
                       quotechar='"',
                       quoting=csv.QUOTE_ALL,
                       # skip the first row, second row is headers
                       skiprows=1,
                       # do not allow mixed types
                       )
    
    return df


def get_all_GPCR_targets_GtP():
    """ Get all GPCR targets from Guide to Pharmacology.

    returns: list of pygtop.Target objects
    """
    query = {"type": "GPCR"}
    targets = pygtop.get_targets_by(query)
    return targets


def get_output_row_dict(target, ligand):
    """ Get the information for each interaction.
    returns: dict
    """
    # look in databases
    database_links = target.database_links()
    target_uniprot_ids = list()
    target_GPCRdb_ids = list()
    for link in database_links:
        # get the uniprot ID
        if link.database() == "UniProtKB":
            if "Human" in link.species():
                target_uniprot_ids.append(link._accession)
        # get the GPCRdb ID
        elif link.database() == "GPCRdb":
            if "Human" in link.species():
                target_GPCRdb_ids.append(link._accession)
    
    # parse uniprot IDs
    if len(target_uniprot_ids) == 0:
        target_uniprot_id = np.nan
    elif len(target_uniprot_ids) == 1:
        target_uniprot_id = target_uniprot_ids[0]
    else:
        target_uniprot_id = "|".join(target_uniprot_ids)
    
    # parse GPCRdb IDs
    if len(target_GPCRdb_ids) == 0:
        target_GPCRdb_id = np.nan
    elif len(target_GPCRdb_ids) == 1:
        target_GPCRdb_id = target_GPCRdb_ids[0]
    else:
        target_GPCRdb_id = "|".join(target_GPCRdb_ids)


    return {"Target ID" : target._target_id,
            "Ligand ID" : ligand._ligand_id,
            "Target Type" : target._target_type,
            "Ligand Type" : ligand._ligand_type,
            
            "Target GPCRdb ID" : target_GPCRdb_id,
            "Target UniProt ID" : target_uniprot_id,

            "Ligand Species" : ligand._species,
            "Ligand Sequence" : ligand.one_letter_sequence(),
            }


def get_endogenous_human_target_ligand_pairs(endogenous_ligand_csv):
    """ Parse the endogenous ligand csv file and get all human ligand-target pairs.
    """
    df = read_GtP_csv(endogenous_ligand_csv)
    
    # remove all non-human ligands
    filter_for_human = lambda x: "Human" in str(x)
    df = df[df["Target Species"].apply(filter_for_human)]

    # get all unique pairs of target ID and ligand ID
    pairs = df[["Target ID", "Ligand ID"]].drop_duplicates()
    # turn into a list of tuples
    pairs = list(map(tuple, pairs.to_numpy()))
    return pairs


def filter_ligand(ligand_id, loss_dict):
    """ Adds to loss_dict if failed.

      Returns (none, loss_dict) if failed,
      Returns (pygtop.Ligand, loss_dict) if passed
    """
    # get the ligand
    ligand = pygtop.get_ligand_by_id(ligand_id)
    # peptide ligands
    ligand_type = ligand.ligand_type()
    if ligand_type != "Peptide":
        loss_dict["ligand_type"].append(ligand_type)
        return None, loss_dict
    # human (the species in which the ligand is found)
    ligand_species = ligand.species()
    if "Human" not in ligand_species:
        loss_dict["non_human_ligand"].append(ligand_species)
        return None, loss_dict
    # ligand has a sequence
    ligand_sequence = ligand.one_letter_sequence()
    if ligand_sequence is None:
        loss_dict["no_sequence"].append(ligand_sequence)
        return None, loss_dict
    if len(ligand_sequence) < 1:
        loss_dict["no_sequence"].append(ligand_sequence)
        return None, loss_dict
    return ligand, loss_dict


def filter_target(target_id, loss_dict):
    """ Adds to loss_dict if failed.

      Returns (none, loss_dict) if failed,
      Returns (pygtop.Target, loss_dict) if passed
    """
    # get the target
    target = pygtop.get_target_by_id(target_id)
    # check target is GPCR
    target_type = target.target_type()
    if target_type != "GPCR":
        loss_dict["non_GPCR_target"].append(target_type)
        return None, loss_dict
    return target, loss_dict


def bool_all_interactions_are_agonist(ligand, target, loss_dict):
    """ Check if the ligand-target pair has an agonist interaction.
        (If any are labelled otherwise, it's not a positive sample)
            
        Returns (False, loss_dict) if failed,
        Returns (True, loss_dict) if passed
    """
    # interactions
    interactions = ligand.interactions()
    # filter for interactions with the target
    interactions = [interaction for interaction in interactions if interaction._target_id == target._target_id]
    actions = [i.action() for i in interactions]
    
    # check that all actions are valid
    if not all([action in ["Agonist", "Full agonist"] for action in actions]):
        loss_dict["non_agonist"].append("|".join(actions))
        return False, loss_dict
    
    return True, loss_dict


def get_empty_loss_dict():
    loss_dict = {"ligand_type":[], "non_human_ligand":[], "no_sequence":[],
                 "non_GPCR_target":[], "non_agonist":[]}
    return loss_dict


def filter_pairs(pairs):
    """ Filter the pairs for valid interactions.
        Returns:
            valid_pairs: list of tuples (pygtop.Target, pygtop.Ligand)
            loss_dict: dict with the number of interactions lost per filter step
    """
    # track loss of interactions (ordered on filter step in queue)
    loss_dict = get_empty_loss_dict()

    valid_pairs = list()

    for index, (target_id, ligand_id) in enumerate(pairs):
        print(f"Processing pair {index+1}/{len(pairs)}.", end="\r")
        target_id = int(target_id)
        ligand_id = int(ligand_id)

        ligand, loss_dict = filter_ligand(ligand_id, loss_dict)
        if ligand is None:
            continue

        target, loss_dict = filter_target(target_id, loss_dict)
        if target is None:
            continue

        interactions_are_valid, loss_dict = bool_all_interactions_are_agonist(ligand=ligand, target=target, loss_dict=loss_dict)
        if interactions_are_valid is False:
            continue

        # add the pair to the list of valid pairs
        valid_pairs.append((target, ligand))
    
    return valid_pairs, loss_dict


def show_or_save_plot(save_path, transparent=True):
    """ Show or save a matplotlib plot.
    """
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path, 
                    # transparent background
                    transparent=transparent,
                    )
    plt.close()


def plt_pie_chart(df, col, save_path, size=(10, 10), transparent=True):
    """ Plot a pie chart of the class counts for a column in a dataframe.
    """
    #counts = df[col].value_counts()
    # count but include NaN
    counts = df[col].value_counts(dropna=False)

    # increase font size
    plt.rcParams.update({'font.size': 20})

    # size
    plt.figure(figsize=size)
    # make a pie chart that shows the counts and the percentages
    plt.pie(counts,
            labels=counts.index,
            autopct='%1.1f%%',
            shadow=False,
            startangle=90,
            textprops={'fontsize': 12},
            pctdistance=0.85,
            labeldistance=1.1,
            wedgeprops={'linewidth': 1, 'edgecolor': 'black'})
    
    # if there are counts
    if len(counts) > 0:
        table_height = len(counts) * 0.06 + 0.2
        # add table that contains the counts
        plt.table(cellText=counts.values.reshape(-1, 1),
            #rowLabels=list(map(lambda x: f"{x}", counts.index)),
            rowLabels=counts.index,
            colLabels=['Counts'],
            loc='left',
            # place the bbox at he top left of the plot
            bbox=[-0.15, 0.5, 0.2, table_height],
            # open the edges
            edges='open',
            # give the table a bigger font
            cellLoc='center',
            )
    plt.tight_layout()
    # title font size is 200%
    plt.title(f'{col} counts', fontsize=20)
    # show or save the plot
    show_or_save_plot(save_path, transparent=transparent)


def plot_funnel(funnel_dict, save_dir, initial_count, title="Interaction pairs"):
    """ After the pairs have been filtered, plot a funnel to show the loss of interactions.
    """
    funnel_plot_dict = {"stage":[], "count":[]}
    color_scale = px.colors.sequential.Blues_r
    save_path = save_dir / "0_0_filter_funnel.png"
    
    # add the initial count to the funnel plot
    current_count = initial_count
    funnel_plot_dict["stage"].append("initial")
    funnel_plot_dict["count"].append(current_count)

    # for each filter step, plot a pie chart of which interactions were lost
    for step_index, (filter_step, lost_values) in enumerate(funnel_dict.items()):
        funnel_plot_dict["stage"].append(filter_step)
        current_count -= len(lost_values)
        funnel_plot_dict["count"].append(current_count)
        pie_chart_path = save_dir / f"0_{step_index+1}_{filter_step}_pie_chart.png"
        step_df = pd.DataFrame(lost_values, columns=[filter_step])
        plt_pie_chart(step_df, filter_step, pie_chart_path)
        print("Lost", len(lost_values), "interactions in filter step", filter_step, "with these counts:", step_df[filter_step].value_counts())
    
    # add the final step to the funnel plot
    fig = px.funnel(funnel_plot_dict, x="count",
                    y="stage",
                    # color based on count (from dark to light)
                    color="count",
                    color_discrete_sequence=color_scale,
                    title=title,
                    )
    
    # save px funnel
    fig.write_image(save_path, width=1000, height=600,
                    #increase font size
                    scale=2, engine="kaleido", format="png")


def write_target_ligand_interactions(endogenous_ligand_csv, output_file):
    """ Write the valid interaction IDs to a csv file.

        output_file: pathlib.Path

        Will create a .csv with 3 columns (Target ID, Ligand ID, Interaction ID).
        Example:
        Target ID,Ligand ID,Interaction ID
        80,836,78357
        80,4358,9488
        315,811,77606
        315,817,77607
        ...
    
    returns: None
             Writes a csv file to disk.
    """
    output_file_has_header = False

    # report pygtop version
    print(f"Using pygtop version {pygtop.__version__}")

    # get endogenous targets, ligands
    pairs = get_endogenous_human_target_ligand_pairs(endogenous_ligand_csv)
    print("Found", len(pairs), "endogenous ligand-human target pairs.")

    valid_pairs, loss_dict = filter_pairs(pairs)
    print("Found", len(valid_pairs), "valid endogenous ligand-human target pairs.")

    # write to file
    print("Writing information for these pairs to", output_file)
    for valid_pair_index, (target, ligand) in enumerate(valid_pairs):
        print(f"Writing pair {valid_pair_index+1}/{len(valid_pairs)}.", end="\r")

        output_row_dict = get_output_row_dict(target, ligand)
        with open(output_file, "a") as f:
            writer = csv.DictWriter(f, fieldnames=output_row_dict.keys())
            # write the header if it doesn't exist
            if not output_file_has_header:
                writer.writeheader()
                output_file_has_header = True
            # write the row to the file
            writer.writerow(output_row_dict)    
    print(f"Finished writing {len(pairs)} endogenous ligand-target pairs.")

    # plot funnel
    plot_funnel(loss_dict, save_dir=output_file.parent, initial_count=len(pairs))
    


if __name__ == "__main__":
    # set args
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--endogenous_ligand_csv", type=pathlib.Path, required=True)
    PARSER.add_argument("--output_file", type=pathlib.Path, required=True)
    PARSER.add_argument("--overwrite", action="store_true")
    ARGS = PARSER.parse_args()

    # check args
    if ARGS.output_file.exists() and not ARGS.overwrite:
        raise FileExistsError(f"Output file {ARGS.output_file} already exists. Use --overwrite to overwrite it.")

    if not ARGS.endogenous_ligand_csv.exists():
        raise FileNotFoundError(f"Endogenous ligand csv file {ARGS.endogenous_ligand_csv} does not exist.")
    
    # remove the output file if it exists and overwrite is True
    if ARGS.output_file.exists() and ARGS.overwrite:
        os.remove(ARGS.output_file)

    # write the interactions to a csv file
    write_target_ligand_interactions(output_file=ARGS.output_file, endogenous_ligand_csv=ARGS.endogenous_ligand_csv)
