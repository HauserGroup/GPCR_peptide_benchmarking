"""Visualize the ranking of the decoys per GPCR

example:
/usr/bin/python3 classifier_benchmark/plot_decoy_ranking.py -p "classifier_benchmark/models/AF2 (no templates)/predictions.csv" -o classifier_benchmark/plots/AF2_no_temp_ranking.png
# todo: fix so it works with new setup
"""

import argparse
import pathlib
from collections import OrderedDict

import pandas
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import spearmanr
from parse_predictions import get_ground_truth_df, get_models, get_ground_truth_values
import sys
import pandas as pd

# append '.'
sys.path.append(".")
from colors import COLOR


def get_color_mapping():
    """Get RGB colors for each decoy type.
        The decoy types are ordered from BEST AGONIST to WORST AGONIST in the dictionary.

    returns: dict
                with keys: column names
                    Principal Agonist,
                    Similar0, Similar1, Similar2, Similar3, Similar4,
                    Dissimilar0, Dissimilar1, Dissimilar2, Dissimilar3, Dissimilar4,

                and values: color for plotting. Tuple of 3 floats, Red Green Blue.
    """
    valid_keys = [
        "Principal Agonist",
        "Similar4",
        "Similar3",
        "Similar2",
        "Similar1",
        "Similar0",
        "Dissimilar4",
        "Dissimilar3",
        "Dissimilar2",
        "Dissimilar1",
        "Dissimilar0",
    ]
    return {k: COLOR[k] for k in valid_keys}


def calculate_spearman_rank_correlation(predicted_order, true_order):
    """
    Calculate the Spearman Rank Correlation Coefficient between predicted and true ranking orders.

    Parameters:
    - predicted_order (list): The predicted ranking order.
    - true_order (list): The true ranking order.

    Returns:
    - float: Spearman Rank Correlation Coefficient.
    """

    # Assign ranks to the items based on the true order
    true_ranks = {item: rank for rank, item in enumerate(true_order)}

    # Assign ranks to the items based on the predicted order using the true ranks
    predicted_ranks = [true_ranks[item] for item in predicted_order]

    # Calculate the Spearman Rank Correlation Coefficient
    correlation, _ = spearmanr(list(range(len(predicted_order))), predicted_ranks)

    return correlation


def calculate_spearman_rank_correlation(
    identifiers, scores, ground_truth_df, score_col="InteractionProbability"
):
    ""


def plot_decoy_rankings(
    predictions_df,
    score_col,
    output_path,
    decoy_colors,
    gpcr_col="Target ID",
    decoy_type_col="Decoy Type",
    decoy_rank_col="Decoy Rank",
    ymin=0.0,
    ymax=1.0,
    add_names=False,
    title="",
    show_legend=True,
):
    gpcrs = predictions_df[gpcr_col].unique()
    ground_truth = get_ground_truth_df()
    xvals = list()
    yvals = list()
    colors = list()
    labels = list()
    peptide_names = list()

    for gpcr in gpcrs:
        gpcr_df = predictions_df[predictions_df[gpcr_col] == gpcr]
        for i, row in gpcr_df.iterrows():
            iptm = row[score_col]
            rank = row[decoy_rank_col]
            decoy_type = row[decoy_type_col]
            # check if nan
            if pd.isna(rank):
                rank_label = f"{decoy_type}"
            else:
                rank_label = f"{decoy_type}{int(rank)}"
            color = decoy_colors.get(rank_label)
            xvals.append(gpcr)
            yvals.append(iptm)
            peptide_names.append(row["identifier"])
            colors.append(color)
            labels.append(rank_label)

    # plot scatter
    plt.figure(figsize=(1, 5))
    plt.grid(axis="x", linestyle="--", linewidth=1, alpha=0.3)

    sns.scatterplot(
        x=xvals,
        y=yvals,
        hue=labels,
        color=colors,
        palette=decoy_colors,
        # add labels to each point
        # order of the legend
        hue_order=decoy_colors.keys(),
        s=100,
        alpha=0.8,
    )
    if show_legend:
        plt.legend(
            title="Decoy Type",
            title_fontsize=6,
            fontsize=4,
            loc="upper left",
            bbox_to_anchor=(1.1, 1),
            ncol=1,
            # set size of legend
            markerscale=0.5,
        )
    else:
        # disable legend
        plt.legend().remove()

    # after scatter, add text at each y value
    if add_names:
        for iptm, name in zip(yvals, peptide_names):
            name = name.rpartition("___")[2]
            name = f"  {name}"
            plt.text(
                0.0,  # x starts at 0
                iptm,
                name,
                fontsize=4,
                ha="left",
                va="bottom",
                rotation=0,
            )

    # plt.xlabel("GPCR")
    # plt.ylabel("Interaction Probability")
    plt.ylim(ymin, ymax)
    # plt.xlabel("GPCR")
    plt.xticks(
        rotation=0,
        # fontsize
        fontsize=12,
    )

    # save
    plt.title(title, fontsize=10)
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()


def handle_args():
    ARGS = argparse.ArgumentParser(description=__doc__)
    ARGS.add_argument(
        "--predictions_csv",
        "-p",
        type=pathlib.Path,
        required=True,
        help="Path to the predictions .csv file with the decoy and principal agonist scores",
    )
    ARGS.add_argument(
        "--output_plot_path",
        "-o",
        type=pathlib.Path,
        required=True,
        help="Path to the output plot (.png) file",
    )
    ARGS.add_argument(
        "--score_col",
        type=str,
        required=False,
        default="InteractionProbability",
        help="Name of the column with the ranking scores",
    )
    ARGS.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite the output plot file if it already exists",
    )

    PARSED = ARGS.parse_args()
    DECOY_COLORS = get_color_mapping()

    # check args
    if not PARSED.predictions_csv.exists():
        raise FileNotFoundError(
            f"Predictions CSV file not found: {PARSED.predictions_csv}"
        )
    if PARSED.output_plot_path.exists() and not PARSED.overwrite:
        raise FileExistsError(
            f"Output plot file already exists: {PARSED.output_plot_path}"
        )

    PREDICTIONS_DF = pandas.read_csv(PARSED.predictions_csv)
    if PARSED.score_col not in PREDICTIONS_DF.columns:
        raise ValueError(
            f"Score column not found in predictions file: {PARSED.score_col}"
        )
    # if not "Decoy Rank" in PREDICTIONS_DF.columns:
    GROUND_TRUTH = get_ground_truth_df()
    # to predictions df, add all column by merging on identifier
    PREDICTIONS_DF = PREDICTIONS_DF.merge(
        GROUND_TRUTH,
        how="left",
        on=["identifier"],
    )
    plot_decoy_rankings(
        PREDICTIONS_DF,
        PARSED.score_col,
        PARSED.output_plot_path,
        decoy_colors=DECOY_COLORS,
    )


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    models = get_models(script_dir / "models")
    ground_truth = get_ground_truth_df()
    identifier_to_rank = dict()
    identifier_to_type = dict()
    for i, row in ground_truth.iterrows():
        identifier_to_rank[row["identifier"]] = row["Decoy Rank"]
        identifier_to_type[row["identifier"]] = row["Decoy Type"]

    for model_name, pred_df in models:
        # if model_name not in ["AF2 (no templates)", "AF2 LIS (no templates)"]:
        #     continue
        print(f"Processing {model_name}")

        plot_p = script_dir / f"plots/{model_name}_decoy_ranking.svg"
        pred_df["Decoy Rank"] = pred_df["identifier"].apply(
            lambda x: identifier_to_rank.get(x, None)
        )
        pred_df["Decoy Type"] = pred_df["identifier"].apply(
            lambda x: identifier_to_type.get(x, None)
        )
        pred_df["Target ID"] = pred_df["identifier"].apply(lambda x: x.split("_")[0])

        ranking_dir = script_dir / "plots/rankings"
        ranking_dir.mkdir(exist_ok=True)
        # plot all targets
        plot_decoy_rankings(
            pred_df,
            "InteractionProbability",
            ranking_dir / f"{model_name}_decoy_ranking.svg",
            get_color_mapping(),
        )

        # plot individual targets
        for unique_target in pred_df["Target ID"].unique():
            # skip if exists
            unique_target_plot_p = (
                ranking_dir / f"{model_name}_{unique_target}_decoy_ranking.svg"
            )
            # if unique_target_plot_p.exists():
            #     continue

            print(f"Plotting {unique_target}")
            plot_decoy_rankings(
                pred_df[pred_df["Target ID"] == unique_target],
                "InteractionProbability",
                unique_target_plot_p,
                get_color_mapping(),
                add_names=False,
                title="",
                show_legend=True,
            )


if __name__ == "__main__":
    # handle_args() # outdated
    run_main()
