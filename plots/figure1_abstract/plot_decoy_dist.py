"""
Plot the distributions of similarity to original receptor for dissimilar and similar hormones

"""

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib


def hex_to_rgb(value):
    """
    Convert hex to rgb
    """
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_sns(value):
    """
    Convert rgb to sns
    """
    return tuple([x / 255 for x in value])


def main(
    decoy_p="classifier_benchmark_data/output/6_interactions_with_decoys.csv",
    out_p="plots/figure1_abstract/decoy_dist.png",
):
    """
    Create the plots
    """
    # settings
    bin_count = 10
    bin_size = int(100 / bin_count)
    # data
    decoy_p = pathlib.Path(decoy_p)
    decoy_df = pd.read_csv(decoy_p)
    # Columns: 'Target ID', 'Decoy ID', 'Acts as agonist', 'Decoy Type', 'Decoy Rank', 'Original Target', 'Target Similarity to Original Target', 'Ligand Sequence', 'GPCR Sequence'

    # hues
    color_dict = {}
    # the hue of PA is 220, 139, 3
    color_dict["Principal Agonist"] = (220 / 255, 139 / 255, 3 / 255)
    # we have to choose a decoy color. They are bad binders so red.
    color_dict["Dissimilar"] = rgb_to_sns(hex_to_rgb("#99231b"))
    color_dict["Similar"] = rgb_to_sns(hex_to_rgb("#c62d1f"))

    # create the plot, values are 'Target Similarity to Original Target' and hue is 'Decoy Type'
    sns.set(style="whitegrid")
    sns.set_context("talk")

    # set xlim
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.histplot(
        decoy_df,
        x="Target Similarity to Original Target",
        hue="Decoy Type",
        palette=color_dict,
        element="step",
        stat="percent",
        common_norm=False,
        ax=ax,
        bins=bin_size,
        # bar outline a little bigger
        linewidth=3,
    )
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    # dashed line for 30
    ax.axvline(
        30,
        color="black",
        linestyle="--",
        # make transparent
        alpha=0.5,
    )
    # remove the percent ylabel
    plt.ylabel("")
    # increase all fonts by percentage
    increase_perc = 125

    # title
    plt.title("Similarities of interactions")
    plt.xlabel("Similarity to original receptor (%)")
    for item in (
        [ax.title, ax.xaxis.label, ax.yaxis.label]
        + ax.get_xticklabels()
        + ax.get_yticklabels()
    ):
        item.set_fontsize(item.get_fontsize() * increase_perc / 100)

    # add % to each ytick
    yticks = ax.get_yticks()
    ax.set_yticklabels([f"{int(y)}%" for y in yticks])
    # add a legend
    legend_values = ["Similar", "Dissimilar", "Principal Agonist"]
    plt.legend(
        title="Decoy Type",
        labels=legend_values,
        # order
        handles=[
            plt.Line2D([0], [0], color=color_dict["Similar"], lw=4),
            plt.Line2D([0], [0], color=color_dict["Dissimilar"], lw=4),
            plt.Line2D([0], [0], color=color_dict["Principal Agonist"], lw=4),
        ],
        loc="upper center",
        bbox_to_anchor=(0.6, 1.0),
    )

    # same for xticks
    plt.tight_layout()
    plt.savefig(out_p, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main()
