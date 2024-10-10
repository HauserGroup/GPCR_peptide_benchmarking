"""Score comparison of af2 vs af3, side by side."""

"""Visualize the ranking of the decoys per GPCR

example:
/usr/bin/python3 classifier_benchmark/plot_decoy_ranking.py -p "classifier_benchmark/models/AF2 (no templates)/predictions.csv" -o classifier_benchmark/plots/AF2_no_temp_ranking.png
# todo: fix so it works with new setup
"""

import argparse
import pathlib
from collections import OrderedDict

import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import spearmanr
from parse_predictions import get_ground_truth_df, get_models, get_ground_truth_values
import sys
import pandas as pd

# append '.'
sys.path.append(".")
from colors import COLOR


def get_color_mapping():
    """Get RGB colors for each decoy type.
        The decoy types are ordered from BEST AGONIST to WORST AGONIST in the dictionary.

    returns: dict
                with keys: column names
                    Principal Agonist,
                    Similar0, Similar1, Similar2, Similar3, Similar4,
                    Dissimilar0, Dissimilar1, Dissimilar2, Dissimilar3, Dissimilar4,

                and values: color for plotting. Tuple of 3 floats, Red Green Blue.
    """
    valid_keys = [
        "Principal Agonist",
        "Similar4",
        "Similar3",
        "Similar2",
        "Similar1",
        "Similar0",
        "Dissimilar4",
        "Dissimilar3",
        "Dissimilar2",
        "Dissimilar1",
        "Dissimilar0",
    ]
    return {k: COLOR[k] for k in valid_keys}


def plot_decoy_rankings(
    predictions_df,
    score_col,
    output_path,
    decoy_colors,
    gpcr_col="Target ID",
    decoy_type_col="Decoy Type",
    decoy_rank_col="Decoy Rank",
    ymin=0.0,
    ymax=1.0,
    add_names=False,
):
    gpcrs = predictions_df[gpcr_col].unique()
    ground_truth = get_ground_truth_df()
    xvals = list()
    yvals = list()
    colors = list()
    labels = list()
    peptide_names = list()

    for gpcr in gpcrs:
        gpcr_df = predictions_df[predictions_df[gpcr_col] == gpcr]
        for i, row in gpcr_df.iterrows():
            iptm = row[score_col]
            rank = row[decoy_rank_col]
            decoy_type = row[decoy_type_col]
            # check if nan
            if pd.isna(rank):
                rank_label = f"{decoy_type}"
            else:
                rank_label = f"{decoy_type}{int(rank)}"
            color = decoy_colors.get(rank_label)
            xvals.append(gpcr)
            yvals.append(iptm)
            peptide_names.append(row["identifier"])
            colors.append(color)
            labels.append(rank_label)

    # plot scatter
    plt.figure(figsize=(2, 4))
    # plt.grid(axis="x", linestyle="--", linewidth=1, alpha=0.3)

    # stripplot, only dodge if there are multiple points overlapping on the y-axis
    # jitterplot
    # other plots, such as swarmplot, will not work with the current setup
    xvals = [0] * len(xvals)
    sns.swarmplot(
        x=xvals,
        y=yvals,
        hue=labels,
        palette=decoy_colors,
        s=7,
        # dodge ONLY if needed
        dodge=False,
        linewidth=0.5,
    )

    # make a legend where the labels follow this order
    correct_legend_order = ["Principal Agonist", 
     "Similar4", "Similar3", "Similar2", "Similar1", "Similar0", 
     "Dissimilar4", "Dissimilar3", "Dissimilar2", "Dissimilar1", "Dissimilar0"]

    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=decoy_colors[label], label=label) for label in correct_legend_order]
    plt.legend(handles=handles, title="Decoy Type", loc="upper left", fontsize=6, title_fontsize=6)
    

    # after scatter, add text at each y value
    if add_names:
        for iptm, name in zip(yvals, peptide_names):
            plt.text(
                0.0,  # x is always 0
                iptm,
                name,
                fontsize=4,
                ha="left",
                va="bottom",
                rotation=0,
            )

    # plt.ylabel("Interaction Probability")
    plt.ylim(ymin, ymax)
    # plt.xlabel("GPCR")

    # set fontsize 10 everywhere
    plt.yticks(fontsize=10)
    

    # save
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()


def run_main(add_names=False):
    script_dir = pathlib.Path(__file__).parent.absolute()
    models = get_models(script_dir / "models")
    ground_truth = get_ground_truth_df()
    identifier_to_rank = dict()
    identifier_to_type = dict()
    for i, row in ground_truth.iterrows():
        identifier_to_rank[row["identifier"]] = row["Decoy Rank"]
        identifier_to_type[row["identifier"]] = row["Decoy Type"]

    for model_name, pred_df in models:
        plot_p = script_dir / f"plots/{model_name}_decoy_ranking.svg"
        pred_df["Decoy Rank"] = pred_df["identifier"].apply(
            lambda x: identifier_to_rank.get(x, None)
        )
        pred_df["Decoy Type"] = pred_df["identifier"].apply(
            lambda x: identifier_to_type.get(x, None)
        )
        pred_df["Target ID"] = pred_df["identifier"].apply(lambda x: x.split("_")[0])

        ranking_dir = script_dir / "plots/rankings"
        ranking_dir.mkdir(exist_ok=True)
        # # plot all targets
        # plot_decoy_rankings(
        #     pred_df,
        #     "InteractionProbability",
        #     ranking_dir / f"{model_name}_decoy_ranking.svg",
        #     get_color_mapping(),
        # )

        # plot individual targets
        for unique_target in pred_df["Target ID"].unique():
            # skip if exists
            unique_target_plot_p = (
                ranking_dir / f"{model_name}_{unique_target}_decoy_ranking.svg"
            )
            # if unique_target_plot_p.exists():
            #     continue

            print(f"Plotting {unique_target}")
            plot_decoy_rankings(
                pred_df[pred_df["Target ID"] == unique_target],
                "InteractionProbability",
                unique_target_plot_p,
                get_color_mapping(),
                add_names=add_names,
            )



if __name__ == "__main__":
    # handle_args() # outdated
    run_main()
