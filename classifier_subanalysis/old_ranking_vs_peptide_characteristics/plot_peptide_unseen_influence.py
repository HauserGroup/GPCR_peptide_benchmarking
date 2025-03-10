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



def get_all_plot_df():
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir.parent / "classifier_benchmark/models")
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    agonists = get_principal_agonist_identifiers(ground_truth)
    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    all_plot_df["Class"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_class_dict[x])
    return all_plot_df



def run_main_barplot(plot_p, models_to_keep):
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    plot_p.parent.mkdir(parents=True, exist_ok=True)
    models = get_models(script_dir.parent / "classifier_benchmark/models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}

    agonists = get_principal_agonist_identifiers(ground_truth)
    # create figure
    gpcr_classes = ["Class A (Rhodopsin)", "Class B1 (Secretin)"] # , "Class F (Frizzled)"]
    # rename
    gpcr_renamed = {k: k.split(" (")[0] for k in gpcr_classes}
    # keep only the models we want to plot
    models = [(model_name, model_df) for model_name, model_df in models if model_name in models_to_keep]

    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    # add class
    all_plot_df["Class"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_class_dict[x])
    # drop other GPCRs
    all_plot_df = all_plot_df[all_plot_df["Class"].isin(gpcr_classes)]
   
    all_plot_df['Model_class'] = all_plot_df['Model'] + ' ' + all_plot_df['Class']
    
    # get unseen
    unseen_gpcrs = pd.read_csv(script_dir / "gpcrs_no_complex_before_2021-09-30.txt")
    unseen_gpcrs = unseen_gpcrs.values.flatten()
    gpcr_is_unseen = dict()
    for g in gpcrs:
        if g in unseen_gpcrs:
            gpcr_is_unseen[g] = "Unseen"
        else:
            gpcr_is_unseen[g] = "Seen"
    all_plot_df["Unseen"] = all_plot_df["GPCR"].apply(lambda x: gpcr_is_unseen[x])

 
    fig, axes = plt.subplots(
                             len(models_to_keep),
                             1,
                             figsize=(1.5, 4.5),
                             # share y-axis
                             sharey=True,
                             # reduce padding
                             gridspec_kw={'wspace': 0.1, 'hspace': 0.1,
                                          'left': 0.05, 'right': 0.95, 'top': 0.95, 'bottom': 0.05},
                             # share x axis per row
                             sharex='col',
                             constrained_layout=True,
    )
    for model_i, model in enumerate(sorted(models_to_keep)):
        ax = axes[model_i]
        # get only the data for this model
        model_df = all_plot_df[all_plot_df["Model"] == model]
        # sort by class
        model_df = model_df.sort_values("Unseen")
        # plot
        sns.barplot(
            x="Unseen",
            y="AgonistRank",
            data=model_df,
            ax=ax,
            hue="Unseen",
            linewidth=0.5,
            # add error bars
            
            capsize=0.2,
            errwidth=1,
            errcolor="black",
            # inner = None,
            # scale="count",
            # crop at min (0) and max(11)
            # cut=0,
        )
 
        # set yticks 1 - 11
        yticks = range(1, 12)
        yticklabels = [str(i) if i % 2 == 1 else "" for i in yticks]
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
        ax.tick_params(axis='y', pad=-2)  # Adjust pad for y-axis labels
        ax.set_ylim(0.5, 11.5)
        ax.tick_params(axis='x', pad=-3)  # Adjust pad for x-axis labels

        # set a grid with opacity 0.5
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        ax.grid(axis="x", linestyle="-", alpha=0.6)
        mean_rank_dict = model_df.groupby("Unseen")["AgonistRank"].mean().to_dict()
        ax.set_title (f"Δˉ(unseen-seen): {mean_rank_dict['Unseen'] - mean_rank_dict['Seen']:.2f}",
                      fontsize=8, pad=0,
                      # text left
                        loc="right")
        ax.set_xlabel("")
        ax.set_ylabel("")

    # add right adjust padding
    # save plot
    plt.savefig(plot_p)
    plt.savefig(plot_p.with_suffix(".png"), dpi=600)
    print("Saved plot to", plot_p)

    # save df
    all_plot_df.to_csv(plot_p.with_suffix(".csv"), index=False)
    print("Saved plot df to", plot_p.with_suffix(".csv"))



if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    sns.set(style="whitegrid")
    sns.set_context("paper")
    sns.set_palette("colorblind")
    # set default fontsize to 10
    plt.rcParams.update({"font.size": 10})
    models_to_keep = [
        "AF2 (no templates)",
        "AF2 (no templates) LIS",
        "Chai-1",
        "AF3",
        "AF3 LIS",
        # "RF-AA",
        # "Peptriever",
        ]
    
    run_main_barplot(plot_p = script_dir / "ranking_vs_unseen/unseen_comparisons_barplot.svg",
                     models_to_keep=models_to_keep)
