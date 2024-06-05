"""
Create a linear correlation pot between principal agonist position and principal agonist activity.

g = sns.jointplot(x="total_bill", y="tip", data=tips, kind='reg')
"""

import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from scipy import stats

sys.path.append(".")
from colors import COLOR
from parse_predictions import get_models, get_ground_truth_df
from correlation import get_spearman_correlation


def plot_correlation_activity_and_score(
    pred_df,
    activity_df,
    plot_p: pathlib.Path,
    model_name: str,
):
    peptides_with_activity = activity_df["peptide"].unique()
    pred_df = pred_df[pred_df["Decoy ID"].isin(peptides_with_activity)]

    # make a plot df, that has the mean activity for each peptide and the InteractionProbability
    plot_df = pred_df.groupby("Decoy ID").agg(
        mean_score=("InteractionProbability", "mean")
    )
    plot_df = plot_df.reset_index()
    plot_df = plot_df.merge(activity_df, left_on="Decoy ID", right_on="peptide")
    g = sns.jointplot(
        data=plot_df,
        x="mean_score",
        y="mean_activity",
        kind="reg",  # 'hex' or 'reg'
    )
    # stats
    rho, p_value = get_spearman_correlation(
        plot_df["mean_score"], plot_df["mean_activity"]
    )
    # add text
    g.ax_joint.text(
        0.5,
        0.5,
        f"R={rho:.2f}\np={p_value:.2f}",
        horizontalalignment="center",
        verticalalignment="center",
        transform=g.ax_joint.transAxes,
    )
    g.set_axis_labels("InteractionProbability", "mean pKi")
    g.fig.suptitle(
        f"{model_name}\nPrincipal agonists only (n={len(plot_df)})",
        # up
        y=1.05,
    )
    g.savefig(plot_p, dpi=300)
    plt.close()


def main():
    # ranking data
    script_dir = pathlib.Path(__file__).resolve().parent
    # activity
    activity_p = script_dir / "get_activity/pKi.csv"
    activity_df = pd.read_csv(activity_p)
    activity_df.drop(columns=["class"], inplace=True)
    activity_df["GPCR"] = activity_df["identifier"].str.split("___").str[0]
    activity_df["peptide"] = activity_df["identifier"].str.split("___").str[1]
    activity_df.dropna(inplace=True)
    # models
    models = get_models(script_dir / "models")
    # ground truth
    ground_truth_df = get_ground_truth_df()
    # get principal agonist identifiers
    principal_agonists = ground_truth_df[
        ground_truth_df["Acts as agonist"].astype(int) == 1
    ]["identifier"].values

    for model_name, pred_df in models:
        plot_p = script_dir / f"plots/activity_vs_score_{model_name}.png"
        pred_df = pred_df.copy()
        pred_df = pred_df[pred_df["identifier"].isin(principal_agonists)]
        pred_df["Decoy ID"] = pred_df["identifier"].str.split("___").str[1]
        plot_correlation_activity_and_score(
            pred_df,
            activity_df,
            plot_p,
            model_name,
        )


if __name__ == "__main__":
    main()
