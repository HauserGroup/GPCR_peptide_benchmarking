"""
Using all agonist interactions, get the 'selectivity'.
Number of peptides for a gpcr. (selective vs non-selective). Hypothesis: selective gpcrs perform better?
Number of gpcrs for a peptide. Hypothesis: peptides that interact with more gpcrs perform worse?
"""

import pathlib
import pandas
import logging
import seaborn as sns
import matplotlib.pyplot as plt


def plot_targets_per_ligand(agonist_df, plot_dir, plot_base):
    # targets per ligand
    targets_per_ligand = agonist_df.groupby("Ligand ID")["Target ID"].nunique()
    sns.histplot(targets_per_ligand, discrete=True)
    plt.xlabel("Number of GPCRs")
    plt.ylabel("Number of Ligands")
    plt.xticks(range(max(targets_per_ligand) + 1))
    plt.grid()
    plt.savefig(plot_dir / f"{plot_base}_targets_per_ligand.png")
    plt.close()


def plot_ligands_per_target(agonist_df, plot_dir, plot_base):
    # ligands per target
    ligands_per_target = agonist_df.groupby("Target ID")["Ligand ID"].nunique()
    sns.histplot(ligands_per_target, discrete=True)
    plt.xlabel("Number of Ligands")
    plt.ylabel("Number of GPCRs")
    plt.xticks(range(max(ligands_per_target) + 1))
    plt.grid()
    plt.savefig(plot_dir / f"{plot_base}_ligands_per_target.png")
    plt.close()


def plot_ranking_with_gpcr_selectivity(agonist_df, ranking_df, plot_p):
    ""


def run_main():
    # get data
    script_dir = pathlib.Path(__file__).parent
    classifier_data = script_dir.parent.parent / "classifier_benchmark_data"
    agonist_p = classifier_data / "output/2_hormone_interactions.csv"
    agonist_df = pandas.read_csv(agonist_p)
    plot_dir = script_dir
    plot_base = "selectivity"
    # ranking performance
    ranking_p = script_dir.parent / "agonist_rankings.csv"
    ranking_df = pandas.read_csv(ranking_p)
    # Model, GPCR, AgonistRank, class

    # targets per ligand
    plot_targets_per_ligand(agonist_df, plot_dir, plot_base)

    # ligands per target
    plot_ligands_per_target(agonist_df, plot_dir, plot_base)

    # plot gpcr selectivity and agonist rank
    plot_ranking_with_gpcr_selectivity(
        agonist_df, ranking_df, plot_dir / f"{plot_base}_rank_vs_selectivity.png"
    )


if __name__ == "__main__":
    run_main()
