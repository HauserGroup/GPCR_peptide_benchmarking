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


def get_top_ranked_name_for_GPCR(pred_df, gpcr):
    ""
    pred_df = pred_df[pred_df["Target ID"] == gpcr]
    pred_df = pred_df.sort_values("InteractionProbability", ascending=False)
    identifier = pred_df.iloc[0]["identifier"]
    return identifier.rpartition("___")[2]


def get_principal_agonist_name(ground_truth, gpcr):
    ""
    agonists = get_principal_agonist_identifiers(ground_truth)
    for a in agonists:
        if gpcr in a:
            return a.rpartition("___")[2]
    return None


def get_plot_df(gpcr_class, models, agonists, gpcr_to_class_dict):
    """
    gpcr_class: str, which GPCR classes to return
    models: list of tuples (model_name, pred_df)
    agonists: list of agonist identifiers
    gpcr_to_class_dict: dict, mapping gpcr to class
    """
    ground_truth = get_ground_truth_df()
    # plot df will store all rankings per model
    plot_df = pd.DataFrame(columns=["Model", "GPCR", "AgonistRank"])
    for model_name, pred_df in models:
        # add info to prediction df required for plotting
        pred_df["Target ID"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["Target ID"].apply(lambda x: gpcr_to_class_dict[x])

        # keep only relevant class and agonists
        pred_df = pred_df[pred_df["class"] == gpcr_class]
        rankings = get_rankings_from_df(pred_df, agonists)
        rankings_df = pd.DataFrame(
            {
                "Model": model_name,
                "GPCR": list(rankings.keys()),
                "AgonistRank": list(rankings.values()),
            }
        )
        rankings_df["TopRankedName"] = rankings_df["GPCR"].apply(
            lambda x: get_top_ranked_name_for_GPCR(pred_df, x)
        )
        rankings_df["PrincipalAgonist"] = rankings_df["GPCR"].apply(
            lambda x: get_principal_agonist_name(ground_truth, x)
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


def plot_3_classes():
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}

    agonists = get_principal_agonist_identifiers(ground_truth)

    # plot details
    plot_p = script_dir / "plots/class_distributions.png"
    fig, ax = plt.subplots(
        1,
        4,
        figsize=(4 * 3, 3),
        # do not share y-axis, as F is much smaller
        sharey=False,
    )
    # add whitespace
    plt.subplots_adjust(wspace=0.5)

    for plot_index, gpcr_class in enumerate(
        [
            "Class A (Rhodopsin)",
            "Class B1 (Secretin)",
            "Class F (Frizzled)",
        ]
    ):
        plot_df = get_plot_df(gpcr_class, models, agonists, gpcr_to_class_dict)

        # save the rankings for the last plot
        if plot_index < 1:
            combine_df = plot_df.copy()
            combine_df["class"] = gpcr_class
        else:
            append_df = plot_df.copy()
            append_df["class"] = gpcr_class
            combine_df = pd.concat([combine_df, append_df])
        if plot_index > 1:
            combine_df.to_csv(script_dir / "agonist_rankings.csv", index=False)

        bins = np.arange(1, 12)
        bin_width = 1

        # boxplots with jitter for the rankings, with rank of y-axis
        sns.boxplot(
            data=plot_df,
            x="Model",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=COLOR,
            hue="Model",
            # mean line
            meanline=True,
            # make the mean line more visible
            showmeans=True,
            # mean color = black
            meanprops={"color": "black", "linewidth": 1},
            showfliers=False,
        )
        # plot jitter
        sns.stripplot(
            data=plot_df,
            x="Model",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=COLOR,
            hue="Model",
            dodge=False,
            jitter=0.2,
            linewidth=0.5,
            alpha=0.5,
        )
        # remove all labels
        ax[plot_index].set_xlabel("")
        ax[plot_index].set_ylabel("")
        if plot_index < 1:
            ax[plot_index].set_ylabel("Agonist Rank")
        # remove xticks
        ax[plot_index].set_xticks([])
        # set title
        gpcr_count = len(plot_df["GPCR"].unique())
        ax[plot_index].set_title(f"{gpcr_class}\n({gpcr_count} GPCRs)")
        # set ylims
        ax[plot_index].set_ylim(0, 12)

    # add legend in last subplot
    add_legend(plot_df, models, ax, bins, bin_width, last_index=3)

    plt.tight_layout()
    plt.savefig(plot_p, dpi=300)


def plot_seen_vs_unseen():
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")
    unseen_gpcrs = pd.read_csv(script_dir / "gpcrs_no_complex_before_2021-09-30.txt")
    unseen_gpcrs = unseen_gpcrs.values.flatten()

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    gpcr_is_unseen = dict()
    for g in gpcrs:
        if g in unseen_gpcrs:
            gpcr_is_unseen[g] = True
        else:
            gpcr_is_unseen[g] = False

    agonists = get_principal_agonist_identifiers(ground_truth)

    # plot details
    plot_p = script_dir / "plots/class_distributions.png"
    fig, ax = plt.subplots(
        1,
        4,
        figsize=(4 * 3, 3),
        # do not share y-axis, as F is much smaller
        sharey=False,
    )
    # add whitespace
    plt.subplots_adjust(wspace=0.5)

    for plot_index, gpcr_class in enumerate(
        [
            "Class A (Rhodopsin)",
            "Class B1 (Secretin)",
            "Class F (Frizzled)",
        ]
    ):
        plot_df = get_plot_df(gpcr_class, models, agonists, gpcr_to_class_dict)
        plot_df["unseen"] = plot_df["GPCR"].apply(lambda x: gpcr_is_unseen[x])

        # save the rankings for the last plot
        if plot_index < 1:
            combine_df = plot_df.copy()
            combine_df["class"] = gpcr_class
        else:
            append_df = plot_df.copy()
            append_df["class"] = gpcr_class
            combine_df = pd.concat([combine_df, append_df])
        if plot_index > 1:
            combine_df.to_csv(script_dir / "agonist_rankings.csv", index=False)

        bins = np.arange(1, 12)
        bin_width = 1

        # boxplots with jitter for the rankings, with rank of y-axis
        sns.boxplot(
            data=plot_df,
            x="Model",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=COLOR,
            hue="Model",
            # mean line
            meanline=True,
            # make the mean line more visible
            showmeans=True,
            # mean color = black
            meanprops={"color": "black", "linewidth": 1},
            showfliers=False,
        )
        # plot jitter
        sns.stripplot(
            data=plot_df,
            x="Model",
            y="AgonistRank",
            ax=ax[plot_index],
            palette=COLOR,
            hue="Model",
            dodge=False,
            jitter=0.2,
            linewidth=0.5,
            alpha=0.5,
        )
        # remove all labels
        ax[plot_index].set_xlabel("")
        ax[plot_index].set_ylabel("")
        if plot_index < 1:
            ax[plot_index].set_ylabel("Agonist Rank")
        # remove xticks
        ax[plot_index].set_xticks([])
        # set title
        gpcr_count = len(plot_df["GPCR"].unique())
        ax[plot_index].set_title(f"{gpcr_class}\n({gpcr_count} GPCRs)")
        # set ylims
        ax[plot_index].set_ylim(0, 12)

    # add legend in last subplot
    add_legend(plot_df, models, ax, bins, bin_width, last_index=3)

    plt.tight_layout()
    plt.savefig(plot_p, dpi=300)


if __name__ == "__main__":
    plot_3_classes()
    plot_seen_vs_unseen()
