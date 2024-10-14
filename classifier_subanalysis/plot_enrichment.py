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

from colors_subanalysis import COLOR, MARKER

# add "."
sys.path.append(".")
from plot_heatmap_combined import apply_first_pick_to_predictions


def run_main(plot_p,
             only_GPCRs_without_complex=False,
             ):
    """ """
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")
    # remove models with LIS or APPRAISE
    unique_models = list([m[0] for m in models])
    ground_truth = get_ground_truth_df()

    gpcrs = ground_truth["identifier"].apply(lambda x: x.split("___")[0]).unique()
    gpcr_to_class = {g: get_gpcr_class(g) for g in gpcrs}
    agonist_identifiers = ground_truth[ground_truth["Acts as agonist"] == 1][
        "identifier"
    ].values

    # remove AF3 from models
    models = [m for m in models if m[0] != "AF3"]

    # read gpcr_no_complex.txt
    no_complex_txt = script_dir / 'gpcrs_no_complex.txt'
    no_complex = no_complex_txt.read_text().splitlines()

    # get gpcr, class, is_agonist
    new_models = []
    for model_name, pred_df in models:
        pred_df["gpcr"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["gpcr"].apply(lambda x: gpcr_to_class[x])
        pred_df["is_agonist"] = pred_df["identifier"].apply(
            lambda x: x in agonist_identifiers
        )
        pred_df = pred_df.sort_values(["class", "gpcr"])
        # if filter to only GPCRs without complex
        if only_GPCRs_without_complex:
            # gpcrs without complex
            gpcrs_with_complex_count = pred_df[pred_df["gpcr"].isin(no_complex)].shape[0]
            print('Removing this many GPCRs with complex:', gpcrs_with_complex_count)
            pred_df = pred_df[~pred_df["gpcr"].isin(no_complex)]
        new_models.append((model_name, pred_df))
    models = new_models


    plot_df = pd.DataFrame(
        columns=["model", "keep_top_n", "pa_count", "decoy_count", "total_pa"]
    )

    for keep_top_n in range(1, 12):
        for model_name, pred_df in models:
            # print stats if keep_top_n == 1
            if keep_top_n == 1:
                pa_count = pred_df[pred_df["is_agonist"]].shape[0]
                decoy_count = pred_df[~pred_df["is_agonist"]].shape[0]
                total_pa = pred_df["is_agonist"].sum()
                print(
                    f"Model: {model_name}, PA count: {pa_count}, Decoy count: {decoy_count}, Total PA: {total_pa}"
                )

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
    sns.set_context("paper")
    sns.set_style("whitegrid") 
    fig, ax = plt.subplots(figsize=(3, 3))

    # add marker to plot df so we can sort on marker and model, for legend
    plot_df['marker'] = plot_df['model'].apply(lambda x: MARKER[x])
    plot_df['color'] = plot_df['model'].apply(lambda x: COLOR[x])
    plot_df = plot_df.sort_values(['model', 'marker'])

    colors = [COLOR[m] for m in plot_df["model"].unique()]
    markers = [MARKER[m] for m in plot_df["model"].unique()]
    # plot dashed line at random performance
    random_performance_yvals = 1 / 11 * plot_df["keep_top_n"]
    # random perf line
    ax.plot(
        plot_df["keep_top_n"],
        random_performance_yvals,
        linestyle="--",
        color="black",
        label="Random",
        # opacity
        alpha=0.5,
        # width = 2
        linewidth=1,
        marker="",
    )
    # lines
    sns.lineplot(
        data=plot_df,
        x="keep_top_n",
        y="pa_retained",
        ax=ax,
        # color for models
        palette=colors,
        hue="model",
        # markers for rescoring methods
        markers=False,
        # line style is solid
        dashes=False,
        linewidth=1,
        legend=False,
        linestyle="--",
        # line opacity
        alpha=0.5,
    )

    # markers
    sns.scatterplot(
        data=plot_df,
        x="keep_top_n",
        y="pa_retained",
        ax=ax,
        # color for models
        palette=colors,
        hue="model",
        # markers for rescoring methods
        markers=markers,
        # do not fill markers
        edgecolor="black",
        style="model",
        # make markers same size
        # line opacity
        alpha=1.0,
    )

    # save
    plt.xlim(0.8, 11.2)
    plt.ylim(0, 1.01)
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    # reduce legend font size
    # zoom
    plt.xticks(range(1, 12))
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()

    # fontsize of x and y labels
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
 
    # disable labels (add in illustrator)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("")
    plt.tight_layout()

    plt.savefig(plot_p)
    print(f"Saved plot to {plot_p}")

    # also save as png
    plot_png = plot_p.with_suffix(".png")
    plt.savefig(plot_png)
    plt.close()
    print(f"Saved plot to {plot_png}")


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/enrichment_plot.svg"
    run_main(plot_p)
    plot_p = script_dir / "plots/enrichment_plot_no_complex.svg"
    run_main(plot_p, only_GPCRs_without_complex=True)
