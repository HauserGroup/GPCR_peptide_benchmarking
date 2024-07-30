""" """

import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# import spearman
import scipy.stats as stats


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings = script_dir.parent / "agonist_rankings.csv"
    rankings = pd.read_csv(rankings)
    print(rankings)
    #                 Model         GPCR  AgonistRank  unseen                class
    # 0  AF2 (no templates)  ednrb_human            1   False  Class A (Rhodopsin)
    # 1  AF2 (no templates)  ednra_human            1    True  Class A (Rhodopsin)

    identity = script_dir / "identity.csv"
    identity = pd.read_csv(identity)
    #       pdb        e_value  Identity         gpcr model
    # 0    7VV0   5.211000e-09     0.250  mrgx2_human  rfaa
    # 1    8F7R  5.182000e-217     0.927   oprm_human  rfaa

    # add the largest identity to the rankings dataframe
    rankings["HighestIdentity"] = 0.0
    for i, row in rankings.iterrows():
        model = row["Model"]
        if "af2" in model.lower():
            model_identities = identity[identity["model"] == "af2"]
        elif "rf-aa" in model.lower():
            model_identities = identity[identity["model"] == "rfaa"]
        else:
            continue

        gpcr = row["GPCR"]
        gpcr_identities = model_identities[model_identities["gpcr"] == gpcr]
        if gpcr_identities.shape[0] == 0:
            print("no match found for", model, gpcr)
            continue
        highest_identity = gpcr_identities["Identity"].max()
        rankings.loc[i, "HighestIdentity"] = highest_identity

    # rankings, only with identity > 0
    rankings_with_complex = rankings[rankings["HighestIdentity"] > 0]

    # plot the data
    sns.set_theme()
    sns.set_context("paper")
    sns.set_style("whitegrid")
    plt.figure(figsize=(8, 6))

    # put identity on the x-axis into bins. Include 0.0 as first bin
    rankings["IdentityBin"] = pd.cut(
        rankings["HighestIdentity"],
        bins=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        include_lowest=True,
        labels=["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"],
    )

    sns.boxplot(x="IdentityBin", y="AgonistRank", data=rankings)
    sns.stripplot(x="IdentityBin", y="AgonistRank", data=rankings, color=".25")
    plt.savefig(script_dir / "identity_vs_ranking.png")
    plt.close()

    # also make a spearman regression plot
    sns.jointplot(
        data=rankings_with_complex,
        x="HighestIdentity",
        y="AgonistRank",
        kind="reg",
    )
    # add spearman stats
    spearman = stats.spearmanr(
        rankings_with_complex["HighestIdentity"], rankings_with_complex["AgonistRank"]
    )
    plt.text(
        0.05,
        0.95,
        f"Spearman R: {round(spearman.correlation, 3)} p: {round(spearman.pvalue, 3)}",
        ha="left",
        va="top",
        transform=plt.gca().transAxes,
    )

    plt.savefig(script_dir / "identity_vs_ranking_spearman.png")
    plt.close()


if __name__ == "__main__":
    run_main()
