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
    get_gpcr_family,
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


def get_all_plot_df():
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    agonists = get_principal_agonist_identifiers(ground_truth)
    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    all_plot_df["Class"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_class_dict[x])
    return all_plot_df

def run_main(plot_p, models_to_keep):
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    gpcr_to_family_dict = {g: get_gpcr_family(g) for g in gpcrs}

    agonists = get_principal_agonist_identifiers(ground_truth)
    # create figure
    plt.figure(figsize=(20, 4))
    # keep only the models we want to plot
    models = [(model_name, model_df) for model_name, model_df in models if model_name in models_to_keep]

    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    # add family
    all_plot_df["family"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_family_dict[x])
    # take first word for family
    all_plot_df["family"] = all_plot_df["family"].apply(lambda x: x.split()[0])

    family_value_counts = all_plot_df["family"].value_counts()
    all_plot_df['Model_family'] = all_plot_df['Model'] + ' ' + all_plot_df['family']
    # add a little noise to rank so it's still visible
    all_plot_df["AgonistRankJitter"] = all_plot_df["AgonistRank"] + np.random.uniform(-0.1, 0.1, size=len(all_plot_df))
    # also add the stdev
    sns.barplot(data=all_plot_df, 
                y="AgonistRankJitter", 
                x="Model_family", 
                hue="family",
                ci="sd",
                capsize=0.2,
                errwidth=1.0,
                # make errorbar color transparent
                errcolor=(0, 0, 0, 0.5),
                alpha=0.0,
                # centralize
                dodge=False,
                # no legend
                # set errorbar opacity
                )
    # swarmplot, hue=class
    sns.swarmplot(data=all_plot_df, 
                  y="AgonistRankJitter", 
                  x="Model_family", 
                hue="family",
                  size=1.2,
                  alpha=1.0,
                  dodge=False,
                  # alpha=0.5,
                  linewidth=0.0,
                  # add curvature
                  # alpha=0.8,
                  legend=True,
                  )
    plt.legend(fontsize=8)
    plt.yticks(range(1, 12))
    # set grid opacity
    plt.grid(alpha=0.5, 
             # no vertical lines
                axis="y")
    # rotate xlabels
    plt.xticks(rotation=90)
    plt.tight_layout()
    # show 0.2 more of bottom
    plt.subplots_adjust(bottom=0.2)
    plt.savefig(plot_p)
    plt.savefig(plot_p.with_suffix(".png"), dpi=600)
    plt.close()

    # lastly, print mean rank per family
    mean_rank_df = pd.DataFrame(columns=["Model", "Family", "MeanRank", "Samples"])
    for family in family_value_counts.index:
        for model in models_to_keep:
            model_df = all_plot_df[(all_plot_df["Model"] == model)]
            model_family_df = model_df[model_df["family"] == family]
            mean_rank = model_family_df["AgonistRank"].mean()
            samples = len(model_family_df)
            mean_rank_df = mean_rank_df.append({"Model": model, "Family": family, "MeanRank": mean_rank,
                                                "Samples":samples}, ignore_index=True)

    # sort on rank
    mean_rank_df = mean_rank_df.sort_values(["Model", "MeanRank"])
    print(mean_rank_df)

    all_ranks = all_plot_df["AgonistRank"].values
    print(f"Mean rank: {np.mean(all_ranks)}")


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    sns.set(style="whitegrid")
    sns.set_context("paper")
    sns.set_palette("colorblind")
    # set default fontsize to 10
    plt.rcParams.update({"font.size": 10})
    run_main(plot_p = script_dir / "plots/family_comparisons.svg",
             # models_to_keep=["Peptriever", "AF2 (no templates)", "AF2 LIS (no templates)"])
            models_to_keep=["AF2 (no templates)"])
