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


def add_legend(plot_df, models, ax, bins, bin_width, last_index=3):
    sns.histplot(
        data=plot_df,
        x="AgonistRank",
        hue="Model",
        bins=bins,
        multiple="dodge",
        ax=ax[3],
        binwidth=bin_width,
        element="bars",
        palette=COLOR,
        legend=True,
        shrink=0.6,
        discrete=True,
        # line connecting the bins
    )
    legend = ax[last_index].get_legend()
    # delete all but legend
    ax[last_index].cla()
    # remove background
    ax[last_index].set_axis_off()
    ax[last_index].legend(
        handles=legend.legendHandles,
        labels=[model[0] for model in models],
        loc="center",
        title="Model",
    )


def unseen_vs_seen():
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    agonists = get_principal_agonist_identifiers(ground_truth)

    unseen_gpcrs = pd.read_csv(script_dir / "gpcrs_no_complex_before_2021-09-30.txt")
    unseen_gpcrs = unseen_gpcrs.values.flatten()
    gpcr_is_unseen = dict()
    for g in gpcrs:
        if g in unseen_gpcrs:
            gpcr_is_unseen[g] = "Unseen"
        else:
            gpcr_is_unseen[g] = "Seen"

    # plot details
    plot_p = script_dir / "plots/class_seen_vs_unseen.svg"
    fig, ax = plt.subplots(
        1,
        4,
        figsize=(6 * 3, 3),
        # do not share y-axis, as F is much smaller
        sharey=False,
    )
    # add whitespace
    plt.subplots_adjust(wspace=0.5)

    gpcr_classes = ["Class A (Rhodopsin)", "Class B1 (Secretin)", "Class F (Frizzled)"]
    # rename
    gpcr_renamed = {k: k.split(" (")[0] for k in gpcr_classes}

    for plot_index, (model_name, model_df) in enumerate(models):
        # title
        ax[plot_index].set_title(model_name)

        plot_df = get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict)
        plot_df["unseen"] = plot_df["GPCR"].apply(lambda x: gpcr_is_unseen[x])

        # drop Other
        plot_df = plot_df[plot_df["Class"].isin(gpcr_classes)]
        # rename
        plot_df["Class"] = plot_df["Class"].apply(lambda x: gpcr_renamed[x])
        # modify COLOR so it matches the classes
        new_color = {}
        for k, v in COLOR.items():
            if k in gpcr_renamed:
                new_color[gpcr_renamed[k]] = v
        new_color["Seen"] = "lightgray"
        new_color["Unseen"] = "green"

        # boxplots with jitter for the rankings, with rank of y-axis
        sns.boxplot(
            data=plot_df,
            x="Class",
            y="AgonistRank",
            palette=new_color,
            hue="unseen",
            ax=ax[plot_index],
            # mean line
            meanline=True,
            # make the mean line more visible
            showmeans=False,
            # mean color = black
            meanprops={"color": "black", "linewidth": 1},
            showfliers=False,
            legend=False,
            hue_order=["Seen", "Unseen"],
        )
        # plot jitter
        sns.stripplot(
            data=plot_df,
            x="Class",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=new_color,
            hue="unseen",
            dodge=True,
            # order of the legend
            hue_order=["Seen", "Unseen"],
            s=5,
            alpha=0.8,
        )
    plt.tight_layout()
    plt.savefig(plot_p, dpi=300)


if __name__ == "__main__":
    unseen_vs_seen()
