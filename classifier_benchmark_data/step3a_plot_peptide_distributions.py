import pathlib
import argparse
import os 

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import pygtop

from step1_get_valid_interactions import show_or_save_plot, read_GtP_csv


def plot_distribution_of_occurence(save_path, data_dict, xlabel="Frequency", ylabel="Occurence", title="Distribution of occurence"):
    """ This function will create a barplot of the distribution of occurence of the peptides.
        For example, 10 receptors have 1 peptide, 5 receptors have 2 peptides, etc.
        In this example the receptor id is the key in the data dict,
        and the list of values are the peptide IDs.

    data_dict: dictionary with the format:
              {"Key", "List of values"}
    save_path: pathlib.Path to where the plot should be saved.
    """
    # use a scientific plot style
    plt.style.use("bmh")
    # set up the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    x = sorted(list(set(len(v) for v in data_dict.values())))
    y = list()
    for x_val in x:
        # number of receptors with x_val peptides
        y.append(len([k for k, v in data_dict.items() if len(v) == x_val]))
    # x ticks
    ax.set_xticks(x)
    # plot the data
    ax.bar(x, y, color="blue")
    # add the total count
    total_label = f"n={sum(y)}"
    # place total count in top right
    ax.text(max(x), max(y), total_label, fontsize=14, ha="right", va="top")
    # add labels
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.set_title(title, fontsize=16)
    # add y values to the bars
    for x_val, y_val in zip(x, y):
        ax.text(x_val, y_val, y_val, fontsize=9, ha="center", va="bottom")
    # save
    show_or_save_plot(save_path=save_path, transparent=False)


def plot_peptide_distributions(interactions_path, plot_path):
    if plot_path is None:
        plot_path = interactions_path.parent / "3a_peptide_distribution.png"
    # read the annotated interactions

    df = pd.read_csv(interactions_path)
    peptides_per_target_path = plot_path
    unique_targets = df["Target GPCRdb ID"].unique()
    endogenous_df = read_GtP_csv("data/endogenous_benchmark/classifier_benchmark/input/endogenous_ligand_detailed.csv")

    # empty dict, will contain {target_id: [peptide_ids]}
    peptides_per_target = dict()
    
    # find the primary ligand for each target
    for target in unique_targets:
        # Get all guide to pharmacology ID(s) for this target
        target_ids = df[df["Target GPCRdb ID"] == target]["Target ID"].unique()

        # get candidates with unique ligand sequences
        candidate_rows = df[df["Target GPCRdb ID"] == target]
        candidate_rows = candidate_rows.drop_duplicates(subset=["Ligand Sequence"])
        peptides_per_target[target] = candidate_rows["Ligand ID"].tolist()

    # plot the distribution of peptides per target
    plot_distribution_of_occurence(save_path=peptides_per_target_path,
                                   data_dict=peptides_per_target,
                                   xlabel="Number of peptides (unique ligand sequence)",
                                   ylabel="Number of receptors (unique GPCRdb ID)",
                                   title="Distribution of peptides per receptor")


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("--interactions_path", type=pathlib.Path, help="Path to the annotated interactions csv", required=True)
    PARSER.add_argument("--plot_path", type=pathlib.Path,
                        help="Path to where the plot should be saved. Set to None to save in the same folder as the interactions csv with the name '3a_peptide_distribution.png'", default=None)
    
    ARGS = PARSER.parse_args()
    # check args
    if not os.path.exists(ARGS.interactions_path):
        raise FileNotFoundError(f"Could not find the interactions csv at {ARGS.interactions_path}")
    
    plot_peptide_distributions(interactions_path=ARGS.interactions_path, plot_path=ARGS.plot_path)
