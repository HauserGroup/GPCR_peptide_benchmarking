import pathlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings = pd.read_csv(script_dir / "agonist_rankings.csv")
    # Model,GPCR,AgonistRank,unseen,class
    # AF2 (no templates),ednrb_human,1,False,Class A (Rhodopsin)

    models_to_compare = ["AF2 (no templates)", "AF2 LIS (no templates)"]
    rankings = rankings[rankings["Model"].isin(models_to_compare)]

    # Count occurrences of each combination
    rankings_count = (
        rankings.groupby(["Model", "AgonistRank", "class"])
        .size()
        .reset_index(name="Count")
    )

    rename_dict = {
        "AF2 (no templates)": "AF2",
        "AF2 LIS (no templates)": "AF2-LIS",
    }
    rankings_count["Model"] = rankings_count["Model"].map(rename_dict)

    # create a subplot for all 11 possible positions
    ranks = list(range(1, 12))
    fig, ax = plt.subplots(
        1,
        len(ranks) + 1,
        figsize=(1 * len(ranks), 7),
        # share y axis
        sharey=True,
    )
    total_complexes = len(rankings["GPCR"].unique())

    # set seaborn style
    sns.set_style("whitegrid")
    sns.set_context("paper", font_scale=1.5)

    for rank in ranks:
        rank_data = rankings_count[rankings_count["AgonistRank"] == rank]
        legend = False
        if rank == ranks[-1]:
            legend = True

        histplot = sns.histplot(
            data=rank_data,
            x="Model",
            weights="Count",
            hue="class",
            multiple="stack",
            ax=ax[rank - 1],
            legend=legend,
            edgecolor="black",
            # include missing legend values
            hue_order=[
                "Class A (Rhodopsin)",
                "Class B1 (Secretin)",
                "Class F (Frizzled)",
            ],
        )

        # add text inside bars
        for p in histplot.patches:
            height = p.get_height()
            histplot.text(
                p.get_x() + p.get_width() / 2.0,
                height / 2.0,
                # make the text a percentage that's rounded to 2 decimal places
                f"{height:.0f}",
                ha="center",
                va="center",
                color="black",
                fontsize=10,
                # do not show if 0
                visible=height > 0,
            )
        # rotate xlabel
        for tick in ax[rank - 1].get_xticklabels():
            tick.set_rotation(90)
        ax[rank - 1].set_xlabel(f"")
        ax[rank - 1].set_ylim(0, total_complexes)
        ax[rank - 1].set_title(f"{rank}")
        ax[rank - 1].set_ylabel("Complexes with this rank (count)")
        ax[rank - 1].grid(axis="y", linestyle="-", alpha=0.5)

    plt.subplots_adjust(wspace=0.0)
    # plot bottom adjust
    plt.subplots_adjust(bottom=0.15)
    plt.subplots_adjust(top=0.85)

    # add large title for the whole plot
    plt.suptitle("Agonist Rankings Comparison")
    plt.savefig(script_dir / "plots/agonist_rankings_comparison.svg")
    print("Saved plot to plots/agonist_rankings_comparison.svg")


if __name__ == "__main__":
    run_main()
