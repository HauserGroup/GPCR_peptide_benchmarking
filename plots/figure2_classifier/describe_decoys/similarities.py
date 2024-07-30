"""Plot sim distributions of all other GPCRs"""

import os
import pathlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import sys

# append '.'
sys.path.append(".")
from colors import COLOR


def get_gpcrs_that_also_have_decoy_as_principal_agonist(
    decoy: int, gpcr: str, decoy_df: pd.DataFrame
):
    """ """
    # only principal agonists
    decoy_df = decoy_df[decoy_df["Decoy Type"] == "Principal Agonist"]
    # same decoy
    decoy_df = decoy_df[decoy_df["Decoy ID"] == decoy]
    # if not != gpcr
    decoy_df = decoy_df[decoy_df["Target ID"] != gpcr]
    return decoy_df["Target ID"].values


def get_gpcr_color(
    gpcr: str, original_target: str, decoy_df: pd.DataFrame, color_dict: dict
):
    # get decoy rank from decoy_df
    decoy_df = decoy_df[decoy_df["Target ID"] == gpcr]
    # target
    decoy_df = decoy_df[decoy_df["Original Target"] == original_target]
    # assert len(decoy_df) == 1
    assert len(decoy_df) == 1
    decoy_rank = decoy_df["Decoy Rank"].values[0]
    decoy_type = decoy_df["Decoy Type"].values[0]
    decoy_color_label = f"{decoy_type}{int(decoy_rank)}"
    return color_dict[decoy_color_label]


def run_main():
    gpcr = "glr_human"
    sim_df_p = "~/Documents/GitHub/GPRC_peptide_benchmarking/classifier_benchmark_data/output/3c_similarity_matrix_binding_pocket.csv"
    sim_df = pd.read_csv(sim_df_p, index_col=0)
    sim_df = sim_df.loc[gpcr]
    script_dir = pathlib.Path(__file__).parent.absolute()

    # decoy df
    decoy_df_p = "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    decoy_df = pd.read_csv(decoy_df_p)
    decoy_df = decoy_df[decoy_df["Target ID"] == gpcr]
    similar = decoy_df[decoy_df["Decoy Type"] == "Similar"]
    dissimilar = decoy_df[decoy_df["Decoy Type"] == "Dissimilar"]
    decoy_df = pd.read_csv(decoy_df_p)

    sim_col = "Target Similarity to Original Target"
    sim_df = sim_df.sort_values(ascending=True)
    # from sim_df, drop 'glr_human' and glp1r_human since they share a principal agonist
    sim_df = sim_df.drop(["glr_human", "glp1r_human"])
    original_target_col = "Original Target"

    # manually drop vipr1_human, which was included as we used the PA of vipr2
    sim_df = sim_df.drop("vipr1_human")
    sim_df = sim_df.drop("ghrhr_human")

    # PLOT OLD
    colors = []
    opacity = []
    for gpcr_key, gpcr_sim in sim_df.items():
        # get color for similar
        if gpcr_key in similar[original_target_col].values:
            color = get_gpcr_color(gpcr, gpcr_key, decoy_df, COLOR)
            colors.append(color)
            opacity.append(1)
        # get color for dissimilar
        elif gpcr_key in dissimilar[original_target_col].values:
            color = get_gpcr_color(gpcr, gpcr_key, decoy_df, COLOR)
            colors.append(color)
            opacity.append(1.0)
        # color of others
        else:
            colors.append("lightgrey")
            opacity.append(0.5)

    # plot
    plt.figure(figsize=(4, 4))
    # get index of first sim value > 30
    cutoff_index_key = sim_df[sim_df > 30].index[0]
    # one before
    one_before = sim_df.index.get_loc(cutoff_index_key) - 2
    index_of_cutoff = one_before

    # plt.bar(
    #     sim_df.index,
    #     sim_df,
    #     color=colors,
    #     # barsize
    #     width=3,
    #     # decorate bars more
    #     edgecolor="black",
    #     linewidth=0.5,
    #     # use opacity for color, in list
    # )
    width = 2
    # plot the others with opacity
    plt.bar(
        sim_df.index,
        sim_df,
        color="lightgrey",
        width=width,
        edgecolor="black",
        linewidth=0.5,
        alpha=0.5,
    )
    # plot similar bars individually
    for i, (gpcr_key, gpcr_sim) in enumerate(sim_df.items()):
        if gpcr_key in similar[original_target_col].values:
            plt.bar(
                gpcr_key,
                gpcr_sim,
                color=colors[i],
                width=width,
                edgecolor="black",
                linewidth=0.5,
                alpha=1,
            )
        elif gpcr_key in dissimilar[original_target_col].values:
            plt.bar(
                gpcr_key,
                gpcr_sim,
                color=colors[i],
                width=width,
                edgecolor="black",
                linewidth=0.5,
                alpha=1,
            )

    # plot vertical line
    plt.axvline(x=index_of_cutoff, color="black", linestyle="--", linewidth=1)

    plt.xticks(rotation=90)
    # set xlabels to ''
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.xlim(-1, len(sim_df))
    plt.grid(axis="y")
    plt.ylabel("")
    plt.xlabel("GPCR")
    plt.title(f"Similarity", fontsize=20)
    plt.tight_layout()
    plt.savefig(script_dir / f"{gpcr}_similarity_distribution.svg")


if __name__ == "__main__":
    run_main()
