""" """

import pathlib
import seaborn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys


# append "."
sys.path.append(".")
from colors import COLOR


def plot_class():
    script_dir = pathlib.Path(__file__).parent.absolute()
    plot_p = script_dir / "boxplots_class.svg"
    rankings = script_dir.parent / "agonist_rankings.csv"
    rankings = pd.read_csv(rankings)
    #                   Model         GPCR  AgonistRank  unseen                class
    # 0    AF2 (no templates)  ednrb_human            1   False  Class A (Rhodopsin)
    # 1    AF2 (no templates)  ednra_human            1    True  Class A (Rhodopsin)

    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(6, 4))
    sns.stripplot(
        rankings,
        x="AgonistRank",
        y="class",
        hue="Model",
        dodge=True,
        linewidth=1,
        palette=COLOR,
        # alpha=0.5,
        alpha=0.3,
        legend=False,
    )

    sns.boxplot(
        rankings,
        x="AgonistRank",
        y="class",
        hue="Model",
        width=0.6,
        palette=COLOR,
        # only boxplot, no dots as we add them later
        showfliers=False,
    )
    # use a grid and add x 1 to 11
    ax.xaxis.grid(True, alpha=0.5)
    ax.xaxis.set_ticks(np.arange(1, 12, 1))

    # ax.xaxis.grid(True)
    ax.set(ylabel="")
    # xlim = 0, 11
    ax.set_xlim(0, 12)
    plt.tight_layout()
    plt.savefig(plot_p)
    print(f"Saved to {plot_p}")


def plot_unseen():
    script_dir = pathlib.Path(__file__).parent.absolute()
    plot_p = script_dir / "boxplots_unseen.svg"
    rankings = script_dir.parent / "agonist_rankings.csv"
    rankings = pd.read_csv(rankings)
    #                   Model         GPCR  AgonistRank  unseen                class
    # 0    AF2 (no templates)  ednrb_human            1   False  Class A (Rhodopsin)
    # 1    AF2 (no templates)  ednra_human            1    True  Class A (Rhodopsin)

    sns.set_theme(style="whitegrid")
    f, ax = plt.subplots(figsize=(6, 4))
    sns.stripplot(
        rankings,
        x="AgonistRank",
        y="Model",
        hue="unseen",
        dodge=True,
        linewidth=1,
        # alpha=0.5,
        alpha=0.3,
        legend=False,
        palette=COLOR,
    )

    sns.boxplot(
        rankings,
        x="AgonistRank",
        y="Model",
        hue="unseen",
        width=0.6,
        palette=COLOR,
        # only boxplot, no dots as we add them later
        showfliers=False,
    )
    # use a grid and add x 1 to 11
    ax.xaxis.grid(True, alpha=0.5)
    ax.xaxis.set_ticks(np.arange(1, 12, 1))

    # ax.xaxis.grid(True)
    ax.set(ylabel="")
    # xlim = 0, 11
    ax.set_xlim(0, 12)
    plt.tight_layout()
    plt.savefig(plot_p)
    print(f"Saved to {plot_p}")


if __name__ == "__main__":
    plot_class()
    plot_unseen()
