"""
"""
import pathlib
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values
from parse_predictions import get_gpcr_class

def run_main():
    ground_truth = get_ground_truth_df()
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/class_dist.png"

    # get the class counts of principal agonists
    ground_truth = ground_truth[ground_truth["Decoy Type"] == "Principal Agonist"]
    ground_truth["Class"] = ground_truth["Target ID"].apply(get_gpcr_class)
    # replace "(" with "\n("
    ground_truth["Class"] = ground_truth["Class"].str.replace("(", "\n(")
    class_counts = ground_truth["Class"].value_counts()
    ground_truth.to_csv("ground_truth_with_class.csv")
    # plt figure size 10, 5
    fig, ax = plt.subplots(figsize=(4, 3))
    # sns barplot
    sns.barplot(x=class_counts.index, y=class_counts.values, ax=ax)
    # add counts on top
    for i, count in enumerate(class_counts.values):
        ax.text(i, count, str(count), ha="center", va="bottom")

    # if other, print
    ax.set_title("GPCR classes")
    plt.tight_layout()
    plt.xlabel("")
    # adjust ymax
    ax.set_ylim(0, 120)
    # shrink on height because of empty x label
    plt.subplots_adjust(bottom=0.2)
    plt.show()
    plt.savefig(plot_p, dpi=300)



if __name__ == "__main__":
    run_main()

    