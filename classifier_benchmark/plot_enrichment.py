"""
lineplot
 y-axis = percent agonists in scores
 x-axis = number of samples chosen (out of 11 per GPCR)
"""

import sys
import pathlib
from parse_predictions import (
    get_ground_truth_df,
    get_ground_truth_values,
    get_gpcr_class,
    get_models,
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# add "."
sys.path.append(".")
from colors import COLOR
from plot_heatmap_combined import apply_first_pick_to_predictions


def run_main():
    """ """
    # set models to keep to [] to use all models
    MODELS_TO_KEEP = [
        # "AF2 (no templates)",
        # "AF2 LIS (no templates)",
        "AF2",
        "AF2 LIS",
        "AF2 APPRAISE",
        # "RF-AA (no templates)",
        # "AF2 (no templates)+pocket",
        # "AF2 LIS (no templates)+pocket",
        # "RF-AA (no templates)+pocket",
    ]
    print("models to keep", MODELS_TO_KEEP)
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")
    unique_models = list([m[0] for m in models])
    plot_p = script_dir / "plots/enrichment.svg"
    ground_truth = get_ground_truth_df()

    gpcrs = ground_truth["identifier"].apply(lambda x: x.split("___")[0]).unique()
    gpcr_to_class = {g: get_gpcr_class(g) for g in gpcrs}
    agonist_identifiers = ground_truth[ground_truth["Acts as agonist"] == 1][
        "identifier"
    ].values

    # remove AF3 from models
    models = [m for m in models if m[0] != "AF3"]
    # remove models not in MODELS_TO_KEEP
    if len(MODELS_TO_KEEP) > 0:
        models = [m for m in models if m[0] in MODELS_TO_KEEP]

    for model_name, pred_df in models:
        pred_df["gpcr"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["gpcr"].apply(lambda x: gpcr_to_class[x])
        pred_df["is_agonist"] = pred_df["identifier"].apply(
            lambda x: x in agonist_identifiers
        )
        pred_df = pred_df.sort_values(["class", "gpcr"])

    plot_df = pd.DataFrame(
        columns=["model", "keep_top_n", "pa_count", "decoy_count", "total_pa"]
    )
    for keep_top_n in range(1, 12):
        for model_name, pred_df in models:
            # sort
            filter_df = pred_df.sort_values(
                ["class", "gpcr", "InteractionProbability"],
                ascending=[True, True, False],
            )
            # keep top n
            filter_df = filter_df.groupby(["class", "gpcr"]).head(keep_top_n)
            pa_count = filter_df[filter_df["is_agonist"]].shape[0]
            decoy_count = filter_df[~filter_df["is_agonist"]].shape[0]
            total_pa = pred_df["is_agonist"].sum()
            row_df = pd.DataFrame(
                {
                    "model": model_name,
                    "keep_top_n": keep_top_n,
                    "pa_count": pa_count,
                    "decoy_count": decoy_count,
                    "total_pa": total_pa,
                },
                index=[0],
            )
            plot_df = pd.concat([plot_df, row_df], ignore_index=True)

    # calculate 'pa_retained' and 'decoy_retained'
    plot_df["pa_retained"] = plot_df["pa_count"] / plot_df["total_pa"]
    plot_df["decoy_retained"] = plot_df["decoy_count"] / (
        plot_df["pa_count"] + plot_df["decoy_count"]
    )

    # plot
    sns.set_context("talk")
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(5, 5))
    colors = [COLOR.get(m, "black") for m in plot_df["model"].unique()]
    sns.lineplot(
        x="keep_top_n",
        y="pa_retained",
        hue="model",
        palette=colors,
        data=plot_df,
        ax=ax,
        # add markers
        marker="o",
        markersize=5,
        linewidth=2,
    )
    # plot dashed line at random performance
    random_performance_yvals = 1 / 11 * plot_df["keep_top_n"]
    ax.plot(
        plot_df["keep_top_n"],
        random_performance_yvals,
        linestyle="--",
        color="black",
        label="Random",
        # opacity
        alpha=0.5,
    )

    # save
    plt.xlim(0, 12)
    plt.ylim(0, 1.05)
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    # reduce legend font size
    # zoom
    plt.title("True agonist retention")
    plt.ylabel("Percent agonists retained")
    plt.xlabel("Number of samples chosen")
    plt.legend(title="Model", loc="lower right", fontsize=8, title_fontsize=8)
    plt.xticks(range(1, 12))
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()

    # sort legend on number of samples chosen
    handles, labels = ax.get_legend_handles_labels()
    plot_df = plot_df[plot_df["keep_top_n"] == 1]
    labels = plot_df.sort_values("pa_retained")["model"].unique()
    # reverse
    labels = labels[::-1]
    colors = [COLOR.get(m, "black") for m in labels]
    handles = [plt.Line2D([0], [0], color=c, lw=2) for c in colors]
    ax = plt.gca()
    ax.legend(
        handles,
        labels,
        title="Model",
        loc="lower right",
        fontsize=8,
        title_fontsize=8,
    )
    # fontsize of x and y labels
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    plt.savefig(plot_p, dpi=300)
    print(f"Saved plot to {plot_p}")


if __name__ == "__main__":
    run_main()
