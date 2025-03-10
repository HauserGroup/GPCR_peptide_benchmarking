"""
Create figure with 3 subplots. Each subplot is for one of the classes.
Each subplot contains the distribution of agonist ranks.
Use a barplot, with rank 1 to 11 on the x-axis and the count on the y-axis.
"""

import pathlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from parse_predictions import (
    get_models,
    get_ground_truth_df,
    get_ground_truth_values,
    get_gpcr_class,
)
import sys

# append "."
sys.path.append(".")
from colors import COLOR


def get_principal_agonist_identifiers(ground_truth):
    """ """
    # get the principal agonist identifiers

    return ground_truth[ground_truth["Decoy Type"] == "Principal Agonist"][
        "identifier"
    ].values


def get_rankings_from_df(df, agonists):
    """
    df: pandas.DataFrame
        with columns "identifier" and "InteractionProbability"
    agonists: list
        list of agonist identifiers

    returns: {"gpcr" <str> : rank <int>}
    """
    # sort by "InteractionProbability"
    df = df.sort_values("InteractionProbability", ascending=False)
    gpcrs = df["Target ID"].unique()

    # for each gpcr, get the RELATIVE ranking of the agonists
    rankings = {}
    for gpcr in gpcrs:
        # get rows for this gpcr (should be 11 rows)
        gpcr_df = df[df["Target ID"] == gpcr]
        # iterate over the rows and find the first agonist
        for relative_i, (i, row) in enumerate(gpcr_df.iterrows()):
            if row["identifier"] in agonists:
                rankings[gpcr] = relative_i + 1
                break

    return rankings


def get_plot_df(models, agonists, gpcr_to_class_dict):
    """
    models: list of tuples (model_name, pred_df)
    agonists: list of agonist identifiers
    gpcr_to_class_dict: dict, mapping gpcr to class
    """
    # plot df will store all rankings per model
    plot_df = pd.DataFrame(columns=["Model", "GPCR", "AgonistRank"])
    for model_name, pred_df in models:
        # add info to prediction df required for plotting
        pred_df["Target ID"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["Target ID"].apply(lambda x: gpcr_to_class_dict[x])

        # keep only relevant class and agonists
        rankings = get_rankings_from_df(pred_df, agonists)
        rankings_df = pd.DataFrame(
            {
                "Model": model_name,
                "GPCR": list(rankings.keys()),
                "AgonistRank": list(rankings.values()),
            }
        )
        rankings_df["Class"] = rankings_df["GPCR"].apply(
            lambda x: gpcr_to_class_dict[x]
        )
        plot_df = pd.concat([plot_df, rankings_df])

    return plot_df


def add_legend(plot_df, models, ax, bins, bin_width, new_color):
    for color_label, color in new_color.items():
        ax[-1].bar(
            [0],
            [0],
            color=color,
            label=color_label,
            linewidth=0,
            edgecolor="black",
        )
    ax[-1].legend(
        title="GPCR Class",
        title_fontsize=10,
        fontsize=10,
        loc="center",
        bbox_to_anchor=(0.5, 0.5),
    )
    # remove grid
    ax[-1].grid(False)
    # remove y-axis
    ax[-1].set_yticks([])
    ax[-1].set_ylabel("")
    # remove x-axis
    ax[-1].set_xticks([])
    # remove box around plot
    ax[-1].spines["top"].set_visible(False)
    ax[-1].spines["right"].set_visible(False)
    ax[-1].spines["bottom"].set_visible(False)
    ax[-1].spines["left"].set_visible(False)

    

def run_main(plot_p, models_to_keep):
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}

    agonists = get_principal_agonist_identifiers(ground_truth)
    subplots_count = len(models_to_keep) + 1
    fig, ax = plt.subplots(
        1,
        subplots_count,
        figsize=(subplots_count * 2, 2.5),
        sharey=True,
        # join the spines so only the first plot has an x-label
        sharex=False,

    )
    gpcr_classes = ["Class A (Rhodopsin)", "Class B1 (Secretin)", "Class F (Frizzled)"]
    # rename
    gpcr_renamed = {k: k.split(" (")[0] for k in gpcr_classes}
    # keep only the models we want to plot
    models = [(model_name, model_df) for model_name, model_df in models if model_name in models_to_keep]

    for plot_index, (model_name, model_df) in enumerate(models):
        # title
        ax[plot_index].set_title(model_name)
        plot_df = get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict)
        # drop Other
        plot_df = plot_df[plot_df["Class"].isin(gpcr_classes)]
        # rename
        plot_df["Class"] = plot_df["Class"].apply(lambda x: gpcr_renamed[x])
        # modify COLOR so it matches the classes
        new_color = {}
        for k, v in COLOR.items():
            if k in gpcr_renamed:
                new_color[gpcr_renamed[k]] = v

        # calculate mean and error
        means = plot_df.groupby("Class")["AgonistRank"].mean()
        sems = plot_df.groupby("Class")["AgonistRank"].sem()
        # Add error bars and mean points
        for i, gpcr_class in enumerate(plot_df["Class"].unique()):
            ax[plot_index].errorbar(
                i,
                means[gpcr_class],
                yerr=sems[gpcr_class],
                color='black',
                capsize=10,
                # width
                elinewidth=2,
                # no legned
                label=None,
            )
        # Add jitter for better visualization
        sns.swarmplot(
            data=plot_df,
            x="Class",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=new_color,
            hue="Class",
            alpha=0.5,  # Set transparency
            size=3,  # Size of points
            legend=False,
        )
        ax[plot_index].set_ylabel("")
        ax[plot_index].set_xlabel("")
        ax[plot_index].set_yticks([])
        # disable grid
        ax[plot_index].grid(False)

    add_legend(plot_df, models, ax, bins=11, bin_width=1, new_color=new_color)

    # add grid (not for legend)
    for a in ax[:subplots_count-1]:
        a.set_ylim(0, 12)
        a.set_yticks(range(1, 12))
        # ygrid opacity
        a.grid(alpha=0.5)

    plt.tight_layout()
    plt.savefig(plot_p)
    plt.savefig(plot_p.with_suffix(".png"), dpi=600)
    plt.close()


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    sns.set(style="whitegrid")
    sns.set_context("paper")
    sns.set_palette("colorblind")
    # set default fontsize to 10
    plt.rcParams.update({"font.size": 10})
    run_main(plot_p = script_dir / "plots/class_comparisons.svg",
             models_to_keep=["Peptriever", "AF2 (no templates)", "AF2 LIS (no templates)"])

