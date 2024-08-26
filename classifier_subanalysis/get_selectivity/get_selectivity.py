"""
Using all agonist interactions, get the 'selectivity'.
Number of peptides for a gpcr. (selective vs non-selective). Hypothesis: selective gpcrs perform better?
Number of gpcrs for a peptide. Hypothesis: peptides that interact with more gpcrs perform worse?
"""

import pathlib
import pandas as pd
import logging
import seaborn as sns
import numpy as np
import sys
import matplotlib.pyplot as plt

sys.path.append(".")
from colors import COLOR

# add parent directory to path
sys.path.append(str(pathlib.Path(__file__).parent.parent))
import correlation
from correlation import get_spearman_correlation


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


def plot_ranking_with_gpcr_selectivity(ligands_per_target, ranking_df, plot_p):
    """ """
    # for ranking df, match on GPCR and fill in the number of targets per ligand
    ranking_df["number of peptides"] = ranking_df["GPCR"].map(
        lambda x: ligands_per_target.get(x, np.nan)
    )
    models = ranking_df["Model"].unique()
    palette = {m: COLOR[m] for m in models}

    # subplots per model
    fig, ax = plt.subplots(
        1,
        len(models),
        figsize=(5 * len(models), 5),
        # share y
        sharey=True,
    )
    for i, model in enumerate(models):
        # plot linear correlation
        model_df = ranking_df[ranking_df["Model"] == model]
        # set i as active axis
        plt.sca(ax[i])
        # correlation plot
        sns.regplot(
            data=model_df,
            x="number of peptides",
            y="AgonistRank",
            color=palette[model],
            # use spearman correlation
            scatter_kws={"alpha": 0.5},
            x_jitter=0.2,
        )
        # add spearman correlation
        rho, p_val = get_spearman_correlation(
            model_df["number of peptides"], model_df["AgonistRank"]
        )
        plt.text(
            0.05,
            0.95,
            f"Spearman: {rho:.2f} (p={p_val:.2e})",
            transform=ax[i].transAxes,
            verticalalignment="top",
        )
        plt.xlabel("Number of peptides")
        plt.title(model)
        plt.tight_layout()

    plt.savefig(plot_p)
    plt.close()


def plot_ranking_with_peptide_selectivity(
    targets_per_ligand, ranking_df, plot_p, target_to_principal_agonist
):
    """
    ligand_id_to_target: dict
        ligand ID (str) -> target ID (str)
        where ligand is the peptide
        and target is the gpcr
    """
    # print(targets_per_ligand)
    # Decoy ID -> <int>

    ranking_df["number of targets"] = np.nan
    # problem, need to match on ligand ID but ranking_df does not have ligand ID
    # add ligand ID using the target to principal agonist dict
    ranking_df["PA ID"] = ranking_df["GPCR"].map(target_to_principal_agonist)
    ranking_df["number of targets"] = ranking_df["PA ID"].map(
        lambda x: targets_per_ligand.get(x, np.nan)
    )

    models = ranking_df["Model"].unique()
    palette = {m: COLOR[m] for m in models}

    # subplots per model
    fig, ax = plt.subplots(
        1,
        len(models),
        figsize=(5 * len(models), 5),
        # share y
        sharey=True,
    )
    for i, model in enumerate(models):
        # plot linear correlation
        model_df = ranking_df[ranking_df["Model"] == model]
        # set i as active axis
        plt.sca(ax[i])
        # correlation plot
        sns.regplot(
            data=model_df,
            x="number of targets",
            y="AgonistRank",
            color=palette[model],
            # use spearman correlation
            scatter_kws={"alpha": 0.5},
            # make space if overlap
            x_jitter=0.2,
        )
        # add spearman correlation
        rho, p_val = get_spearman_correlation(
            model_df["number of targets"], model_df["AgonistRank"]
        )
        plt.text(
            0.05,
            0.95,
            f"Spearman: {rho:.2f} (p={p_val:.2e})",
            transform=ax[i].transAxes,
            verticalalignment="top",
        )
        plt.xlabel("Total targets of principal agonist")
        plt.title(model)
        plt.tight_layout()

    plt.savefig(plot_p)
    plt.close()


def get_gpcr_to_principal_agonist(classifier_df):
    """
    Get the principal agonist for each GPCR.
    """
    # get the principal agonist for each GPCR

    df = classifier_df.copy()
    # only keep principal agonists
    df = df[df["Acts as agonist"] == 1]

    # assert each GPCR has only one principal agonist
    gpcr_to_principal_agonist = df.groupby("Target ID")["Decoy ID"].nunique()
    assert (gpcr_to_principal_agonist > 1).sum() == 0

    # return as dict, with 'Target ID' -> 'Decoy ID'
    out_dict = df.set_index("Target ID")["Decoy ID"].to_dict()
    return out_dict


def run_main():
    # get data
    script_dir = pathlib.Path(__file__).parent
    classifier_data = script_dir.parent.parent / "classifier_benchmark_data"
    agonist_p = classifier_data / "output/2_hormone_interactions.csv"
    agonist_df = pd.read_csv(agonist_p)
    classifier_df = pd.read_csv(
        classifier_data / "output/6_interactions_with_decoys.csv"
    )

    plot_dir = script_dir
    plot_base = "selectivity"
    # ranking performance
    ranking_p = script_dir.parent / "agonist_rankings.csv"
    ranking_df = pd.read_csv(ranking_p)

    # targets per ligand
    plot_targets_per_ligand(agonist_df, plot_dir, plot_base)

    # ligands per target
    plot_ligands_per_target(agonist_df, plot_dir, plot_base)

    # plot gpcr selectivity and agonist rank
    ligands_per_target = agonist_df.groupby("Target GPCRdb ID")["Ligand ID"].nunique()
    plot_p = plot_dir / f"{plot_base}_ranking_vs_gpcr_selectivity.png"
    plot_ranking_with_gpcr_selectivity(ligands_per_target, ranking_df, plot_p)

    # plot peptide selectivity and agonist rank
    "Rethink how to plot this. what is x, what is y?"
    # y = rank
    # x = number of targets per peptide (principal agonist for gpcr)

    # {'Decoy ID' -> <int>}
    targets_per_ligand = agonist_df.groupby("Ligand ID")["Target ID"].nunique()
    # rename "Target ID" to number of targets
    targets_per_ligand = targets_per_ligand.rename("number of targets")

    target_to_principal_agonist = get_gpcr_to_principal_agonist(classifier_df)
    plot_p = plot_dir / f"{plot_base}_ranking_vs_peptide_selectivity.png"
    plot_ranking_with_peptide_selectivity(
        targets_per_ligand, ranking_df, plot_p, target_to_principal_agonist
    )
    targets_per_ligand.to_csv(plot_dir / f"{plot_base}_targets_per_ligand.csv")


if __name__ == "__main__":
    run_main()
