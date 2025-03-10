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
from correlation import get_spearman_correlation

sys.path.append(".")
from colors import COLOR


def plot_correlation_activity_model_ranking(
    plot_df: pd.DataFrame,
    plot_dir: pathlib.Path,
    xlabel: str,
    ylabel: str,
):
    """
    plot_df: pd.DataFrame
        'Model', 'GPCR', 'AgonistRank', 'class', 'identifier', 'mean_activity'
    plot_p: pathlib.Path
        path to save the plot
    """
    models = plot_df["Model"].unique()
    model_colors = {m: COLOR[m] for m in models}
    classes = plot_df["class"].unique()
    class_colors = {c: COLOR[c] for c in classes}

    # make plot for each model
    for model in models:
        model_df = plot_df[plot_df["Model"] == model]
        ranks = model_df["AgonistRank"].unique()
        number_of_samples = len(model_df)
        g = sns.jointplot(
            data=model_df,
            x="AgonistRank",
            y="mean_activity",
            # kind="reg",  # 'hex' or 'reg'
            kind="reg",
            color=model_colors[model],
            # hue="class",
            palette=class_colors,
        )

        # stats
        rho, p_value = get_spearman_correlation(
            model_df["AgonistRank"], model_df["mean_activity"]
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

        g.set_axis_labels(xlabel, ylabel)
        g.fig.suptitle(f"{model}\nnumber of GPCRs = {number_of_samples}")
        plot_p = plot_dir / f"activity_vs_ranking_{model}.png"
        plt.xlim(0, max(ranks) + 1)
        plt.tight_layout()
        plt.grid()

        g.savefig(plot_p, dpi=300)

        plt.close()


def main():
    # ranking data
    script_dir = pathlib.Path(__file__).resolve().parent
    agonist_rankings_p = script_dir / "agonist_rankings.csv"
    agonist_rankings_df = pd.read_csv(agonist_rankings_p)

    # activity
    activity_p = script_dir / "get_activity/pKi.csv"
    activity_df = pd.read_csv(activity_p)
    activity_df.drop(columns=["class"], inplace=True)
    activity_df["GPCR"] = activity_df["identifier"].str.split("___").str[0]

    # get plot df, merge rankings and activity
    plot_df = pd.merge(agonist_rankings_df, activity_df, on="GPCR")

    # drop nan values in activity
    plot_df = plot_df.dropna(subset=["mean_activity"])
    plot_correlation_activity_model_ranking(
        plot_df,
        plot_dir=script_dir / "plots",
        xlabel="agonist rank",
        ylabel="mean pKi",
    )


if __name__ == "__main__":
    main()
