import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon
from matplotlib.sankey import Sankey
import plotly.graph_objects as go
import matplotlib.colors as mcolors


def get_rankings():
    """
    Model,GPCR,AgonistRank,unseen,class
    AF2 (no templates),ednrb_human,1,False,Class A (Rhodopsin)
    AF2 (no templates),ednra_human,1,True,Class A (Rhodopsin)
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings = script_dir.parent / "agonist_rankings.csv"
    rankings = pd.read_csv(rankings)
    return rankings


def get_comparison_data(rankings):
    """
                    AF2 rank LIS rank                class unseen
    ednrb_human        1        1  Class A (Rhodopsin)  False
    ednra_human        1        1  Class A (Rhodopsin)   True
    """
    # create new df to compare rankings
    cols = ["AF2 rank", "LIS rank", "class", "unseen", "GPCR"]
    rank_diffs = pd.DataFrame(columns=cols)

    # use gpcrs as key
    gpcrs = rankings["GPCR"].unique()
    for gpcr in gpcrs:
        # get rows for 2 models
        af2_row = rankings[
            (rankings["Model"] == "AF2 (no templates)") & (rankings["GPCR"] == gpcr)
        ]
        lis_row = rankings[
            (rankings["Model"] == "AF2 LIS (no templates)") & (rankings["GPCR"] == gpcr)
        ]
        if len(af2_row) == 0 or len(lis_row) == 0:
            print(f"Skipping {gpcr}")
            continue

        # get ranks
        af2_rank = af2_row["AgonistRank"].values[0]
        lis_rank = lis_row["AgonistRank"].values[0]
        gpcr_class = af2_row["class"].values[0]
        gpcr = af2_row["GPCR"].values[0]
        unseen = af2_row["unseen"].values[0]

        # out dict
        out = {
            "AF2 rank": af2_rank,
            "LIS rank": lis_rank,
            "class": gpcr_class,
            "unseen": unseen,
            "GPCR": gpcr,
        }

        rank_diffs = pd.concat([rank_diffs, pd.DataFrame(out, index=[0])])

    return rank_diffs


def plot_comparison(rank_diffs, save_dir):
    """Plot the comparison data with seaborn

    Show the paired difference in ranking between AF2 and AF2 LIS.
    """
    # per gpcr calculate the difference
    rank_diffs["Rank difference"] = rank_diffs["AF2 rank"] - rank_diffs["LIS rank"]

    fig, ax = plt.subplots(figsize=(10, 7))
    min_diff = rank_diffs["Rank difference"].min()
    max_diff = rank_diffs["Rank difference"].max()

    sns.histplot(
        data=rank_diffs,
        x="Rank difference",
        hue="class",
        multiple="stack",
        ax=ax,
        # stat
        shrink=0.8,
        discrete=True,
        # show all x values
        bins=range(min_diff, max_diff + 1),
    )
    plt.xticks(range(min_diff, max_diff + 1))
    plt.xlabel("Rank difference (AF2 - AF2 LIS)")
    plt.title("Principal agonist ranking difference between AF2 and AF2 LIS")

    # plot the names of the gpcrs above each bar
    for rank_diff_val in range(min_diff, max_diff + 1):
        if rank_diff_val == 0:
            continue
        gpcrs = rank_diffs[rank_diffs["Rank difference"] == rank_diff_val]["GPCR"]
        # replace "_human" with ""
        gpcrs = gpcrs.str.replace("_human", "")
        for i, gpcr in enumerate(gpcrs):
            start_y = len(gpcrs)
            ax.text(
                rank_diff_val,
                start_y + 2 * i,
                gpcr,
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )

    plt.savefig(save_dir / "rank_differences.svg")
    plt.close()


def plot_comparison_heatmap(rank_diffs, save_dir):
    """
    Calculate differences.
    Xrows are AF2 rank
    Yrows are LIS rank
    The value is the number of gpcrs
    """
    # create a heatmap
    rank_diffs["Rank difference"] = rank_diffs["AF2 rank"] - rank_diffs["LIS rank"]
    rank_diffs = (
        rank_diffs.groupby(["AF2 rank", "LIS rank"]).size().reset_index(name="count")
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    # set 'AF2 rank' as the index
    rank_diffs = rank_diffs.pivot(index="AF2 rank", columns="LIS rank", values="count")

    sns.heatmap(rank_diffs, ax=ax, cmap="viridis", annot=True)
    plt.title("Principal agonist ranking difference between AF2 and AF2 LIS")
    plt.savefig(save_dir / "rank_differences_heatmap.svg")
    plt.close()


def test_if_rank_is_statistically_better(rank_diffs):
    """It's a paired test, with ranking values (non-continuous).
    So do a wilcoxon signed-rank test.
    """
    # get the values
    af2_ranks = rank_diffs["AF2 rank"].to_numpy()
    lis_ranks = rank_diffs["LIS rank"].to_numpy()
    af2_ranks = [int(i) for i in af2_ranks]
    lis_ranks = [int(i) for i in lis_ranks]

    # wilcoxon signed-rank test
    stat, p = wilcoxon(
        af2_ranks,
        lis_ranks,
        # should be directional and not two-sided
        alternative="greater",
    )
    return stat, p


def get_link_colors(cmap="viridis", n_colors=10, alpha=0.5):
    """
    Get a list of colors for the links in the sankey diagram.
    Use the matplotlib cmap to get the colors.
    Return a list of RGBA color strings with the specified alpha for transparency.
    """
    cmap = plt.get_cmap(cmap)
    colors = [cmap(i / n_colors) for i in range(n_colors)]
    rgba_colors = [mcolors.to_rgba(color, alpha=alpha) for color in colors]
    rgba_strings = [
        f"rgba({int(r*255)}, {int(g*255)}, {int(b*255)}, {a})"
        for r, g, b, a in rgba_colors
    ]
    return rgba_strings


def plot_sankey_diagram(rank_diffs: pd.DataFrame, save_dir: pathlib.Path):
    """ """
    # create a sankey diagram using this dataframe
    #     AF2 rank LIS rank                class unseen         GPCR Rank difference
    # 0         1        1  Class A (Rhodopsin)  False  ednrb_human               0
    # 0         1        1  Class A (Rhodopsin)   True  ednra_human               0
    # 0         1        1  Class A (Rhodopsin)  False   ccr5_human               0

    # Ensure the ranks are ordered and sorted
    rank_diffs["AF2 rank"] = pd.Categorical(rank_diffs["AF2 rank"], ordered=True)
    rank_diffs["LIS rank"] = pd.Categorical(rank_diffs["LIS rank"], ordered=True)
    rank_diffs.sort_values(["AF2 rank", "LIS rank"], inplace=True)

    # Get unique ranks
    unique_ranks_af2 = sorted(rank_diffs["AF2 rank"].unique())
    unique_ranks_lis = sorted(rank_diffs["LIS rank"].unique())

    # Create a mapping from rank to index ensuring order is maintained
    rank_to_index_af2 = {rank: i for i, rank in enumerate(unique_ranks_af2)}
    rank_to_index_lis = {
        rank: i + len(unique_ranks_af2) for i, rank in enumerate(unique_ranks_lis)
    }

    # Prepare data for Sankey diagram
    sources = []
    targets = []
    values = []

    for af2_rank in unique_ranks_af2:
        for lis_rank in unique_ranks_lis:
            value = len(
                rank_diffs[
                    (rank_diffs["AF2 rank"] == af2_rank)
                    & (rank_diffs["LIS rank"] == lis_rank)
                ]
            )
            if value > 0:
                sources.append(rank_to_index_af2[af2_rank])
                targets.append(rank_to_index_lis[lis_rank])
                values.append(value)

    # Define node labels
    node_labels = [f"{rank}" for rank in unique_ranks_af2] + [
        f"{rank}" for rank in unique_ranks_lis
    ]

    # Calculate x and y positions
    total_af2 = len(unique_ranks_af2)
    total_lis = len(unique_ranks_lis)
    x_positions = [0.01] * total_af2 + [0.999] * total_lis
    y_positions = [i / total_af2 for i in range(total_af2)] + [
        i / total_lis for i in range(total_lis)
    ]

    # map color to rank
    node_possible_colors = get_link_colors(n_colors=11, alpha=0.4, cmap="coolwarm")
    node_colors = []
    for r in unique_ranks_af2 + unique_ranks_lis:
        node_colors.append(node_possible_colors[r - 1])

    
    mynode = dict(
        pad=10,
        thickness=25,
        line=dict(color="black", width=0.5),
        label=node_labels,
        x=x_positions,
        y=y_positions,
        color=node_colors,
    )

    link_colors = get_link_colors(n_colors=len(values), alpha=0.3, cmap="coolwarm")

    mylink = dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors,
        line=dict(color="black", width=0.25),  # Add black outline to the flows with width=1
    )

    fig = go.Figure(
        data=[
            go.Sankey(arrangement="snap", node=mynode, link=mylink),
        ],
        # size
        layout=dict(width=250, height=450),
    )


    fig.update_layout(
        title_text="",
        font_size=10,
        font_family="Helvetica",
        title_font_size=14,
        title_font_family="Helvetica",
        title_x=0.5,
    )

    # resize figure
    fig.update_layout(
        autosize=False,
        width=300,
        height=400,
    )

    # Save the plot
    save_p = str(save_dir / "sankey_diagram.svg")
    fig.write_image(save_p)
    print(f"Sankey diagram saved to {save_p}")

    # also save to png
    save_p = str(save_dir / "sankey_diagram.png")
    fig.write_image(save_p)
    print(f"Sankey diagram saved to {save_p}")



def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings = get_rankings()

    # only keep relevant models
    models = ["AF2 (no templates)", "AF2 LIS (no templates)"]
    rankings = rankings[rankings["Model"].isin(models)]

    # save comparison
    rank_diffs = get_comparison_data(rankings)
    rank_diffs.to_csv(script_dir / "rank_differences.csv", index=False)

    # report most extreme
    rank_diffs["Rank difference"] = rank_diffs["AF2 rank"] - rank_diffs["LIS rank"]
    print(rank_diffs[rank_diffs["Rank difference"] > 3])

    plot_comparison(rank_diffs, save_dir=script_dir)
    plot_comparison_heatmap(rank_diffs, save_dir=script_dir)

    # sankey diagram
    plot_sankey_diagram(rank_diffs, save_dir=script_dir)

    # test
    stat, p = test_if_rank_is_statistically_better(rank_diffs)
    print(f"Wilcoxon signed-rank test: stat={stat}, p={p}")


if __name__ == "__main__":
    run_main()
