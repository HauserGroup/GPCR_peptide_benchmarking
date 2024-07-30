""" """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
import pathlib
import logging

from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values
from parse_predictions import get_gpcr_class


def get_gpcr(identifier):
    return identifier.split("___")[0]


def plot_position_of_positives(plot_df, model_name, fig, ax, subplot_index):
    """Make a stacked histplot, colored based on class and with percent as stat."""
    # take only y_true = 1
    gpcr_to_pa_index = {}
    plot_df.sort_values(by="gpcr")
    for gpcr in plot_df["gpcr"].unique():
        gpcr_df = plot_df[plot_df["gpcr"] == gpcr]
        # get the index of the PA RELATIVE TO WITHIN the gpcr_df
        index_of_PA = np.where(gpcr_df["y_true"] == 1)[0][0]
        gpcr_to_pa_index[gpcr] = index_of_PA

    plot_df["pa_index"] = plot_df.apply(lambda x: gpcr_to_pa_index[x["gpcr"]], axis=1)
    plot_df = plot_df[plot_df["y_true"] == 1]

    # set the plot to be active with the index
    try:
        plt.sca(ax[subplot_index])
    except TypeError as E:
        print(E)
        print("ax is not iterable")
        plt.sca(ax)

    plt.grid(axis="y")
    plt.yticks(np.arange(0, 101, 10))

    # plot histplot for the pa_index distribution
    sns.histplot(
        plot_df,
        x="pa_index",
        hue="class",
        multiple="stack",
        stat="percent",
        binrange=(0, 11),
        discrete=True,
        # do not start at 0
        binwidth=1,
        palette="tab10",
    )
    # ylim to 100
    plt.ylim(0, 100)
    # yticks every 10

    # set title
    plt.title(f"Position of Principal Agonist in {model_name}")
    # set xticks (centered)
    plt.xticks([i for i in range(11)], np.arange(1, 12))
    plt.tight_layout()
    plt.xlim(-0.5, 10.5)


def run_main():
    script_dir = pathlib.Path(__file__).parent
    # plot_p = script_dir / "plots/ranking_of_PA.svg"
    log_p = script_dir / "plots/ranking_of_PA.log"
    logging.basicConfig(filename=log_p, level=logging.INFO, filemode="w")

    # get the ground truth
    ground_truth = get_ground_truth_df()
    models = get_models(script_dir / "models")
    # fig, ax = plt.subplots(
    #     len(models),
    #     1,
    #     figsize=(
    #         8,
    #         6 * len(models),
    #     ),
    # )

    # iterate over the predictions, show where each model places the principal agonist
    plot_index = -1
    for model_name, prediction_df in models:
        logging.info(f"Processing model {model_name}")

        fig, ax = plt.subplots(1, 1, figsize=(8, 6))

        # group by GPCR
        prediction_df["gpcr"] = prediction_df["identifier"].apply(get_gpcr)
        # drop NaNs in case there is no InteractionProbability
        prediction_df = prediction_df.dropna(subset=["InteractionProbability"])

        # count how often each GPCR appears
        gpcr_counts = prediction_df["gpcr"].value_counts()
        prediction_df["gpcr_count"] = prediction_df["gpcr"].apply(gpcr_counts.get)

        # see which GPCRs we do not have the full benchmark data for
        non_full_gpcrs = prediction_df[prediction_df["gpcr_count"] < 11][
            "gpcr"
        ].unique()
        logging.warning(f"GPCRs with less than 11 data points: {non_full_gpcrs}")
        logging.warning(f"Totalling {len(non_full_gpcrs)} GPCRs")
        prediction_df = prediction_df.sort_values(
            by=["gpcr", "InteractionProbability"], ascending=[True, False]
        )
        if len(prediction_df) == 0:
            logging.warning(f"No data for model {model_name}")
            continue
        # drop if we do not have full data
        prediction_df = prediction_df[~prediction_df["gpcr"].isin(non_full_gpcrs)]
        if len(prediction_df) == 0:
            logging.warning(f"No data for model {model_name}")
            continue

        y_pred = prediction_df["InteractionProbability"].to_numpy()
        y_true = get_ground_truth_values(ground_truth, prediction_df["identifier"])
        gpcr_token_dict = {
            gpcr: i for i, gpcr in enumerate(prediction_df["gpcr"].unique())
        }
        gpcr_tokens = prediction_df["gpcr"].apply(gpcr_token_dict.get)
        gpcr_class = prediction_df["gpcr"].apply(get_gpcr_class)

        # group by GPCR
        plot_df = pd.DataFrame(
            {
                "y_true": y_true,
                "y_pred": y_pred,
                "gpcr": gpcr_tokens,
                "class": gpcr_class,
            }
        )
        # set active plot to the plot_index
        plot_position_of_positives(
            plot_df,
            model_name,
            fig,
            ax,
            subplot_index=0,
        )
        plot_p = script_dir / f"plots/position_of_PA_{model_name}.svg"
        print(f"Saving plot to {plot_p}")
        plt.savefig(plot_p, dpi=300)
        plt.close()


if __name__ == "__main__":
    run_main()
