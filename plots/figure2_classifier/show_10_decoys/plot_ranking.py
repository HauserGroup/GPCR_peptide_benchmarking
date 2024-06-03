"""Ranked list of the 10 decoys and pa, with their scores"""

import pathlib
import pandas as pd
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(".")
from colors import COLOR, hex_to_rgb
from show import get_decoy_df


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    out_p = script_dir / "show.pm"

    # truth
    decoy_df = get_decoy_df()
    gpcr = "agtr2"
    decoy_df["Identifier"] = decoy_df["Identifier"].str.replace("_human", "")
    decoy_df["Identifier"] = decoy_df["Identifier"].str.replace("___", "_")
    decoy_df = decoy_df[decoy_df["Identifier"].str.contains(gpcr)]
    decoy_df["Full Rank"] = ""
    for i, row in decoy_df.iterrows():
        if np.isnan(row["Decoy Rank"]):
            decoy_df.at[i, "Full Rank"] = f"{row['Decoy Type']}"
        else:
            decoy_df.at[i, "Full Rank"] = f"{row['Decoy Type']}{int(row['Decoy Rank'])}"
    identifier_to_rank = dict()
    for i, row in decoy_df.iterrows():
        identifier_to_rank[row["Identifier"]] = row["Full Rank"]

    # predicted
    pred_p = (
        script_dir.parent.parent.parent
        / "classifier_benchmark/models/AF2 (no templates)/predictions.csv"
    )
    pred_df = pd.read_csv(pred_p)
    pred_df = pred_df[pred_df["identifier"].str.contains(gpcr)]
    plt.figure(figsize=(4, 8))
    xvals = list()
    yvals = list()
    colors = list()
    labels = list()
    pred_df = pred_df.sort_values(by="InteractionProbability", ascending=False)
    for index, row in pred_df.iterrows():
        identifier = row["identifier"]
        identifier = identifier.replace("_human", "")
        identifier = identifier.replace("___", "_")
        iptm = row["InteractionProbability"]
        rank = identifier_to_rank[identifier]
        color = COLOR.get(rank)
        xvals.append(0)
        yvals.append(iptm)
        colors.append(color)
        labels.append(rank)
        print(f"{identifier} {iptm} {rank}")

    plt.figure(figsize=(3, 4))
    plt.yticks(
        np.arange(0, 1.1, step=0.1),
        # fontsize
        fontsize=8,
    )
    plt.ylabel("iptm+ptm")
    plt.xticks([])
    plt.grid(
        axis="y",
        alpha=0.3,
        linestyle="--",
        linewidth=1,
        # ticks every 10
        which="major",
    )
    sns.scatterplot(
        x=xvals,
        y=yvals,
        hue=labels,
        palette=colors,
        s=50,
        edgecolor="black",
        linewidth=0.5,
    )
    plt.ylim(0, 1)
    plt.xlabel("")
    plt.xlim(-0.1, 0.1)
    # place legend outside of plot
    plt.legend(loc="lower left", bbox_to_anchor=(1.0, 0.0), title="Ranking", fontsize=8)
    # make sure the legend handles follow the colors

    plt.tight_layout()
    plt.savefig(script_dir / "ranking.png", dpi=300)


if __name__ == "__main__":
    run_main()
