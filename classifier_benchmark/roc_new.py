import pathlib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import logging

from sklearn.metrics import roc_curve, auc
from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values


def main():
    # settings
    script_dir = pathlib.Path(__file__).parent
    model_dir = script_dir / "models"
    plot_p = script_dir / "plots/roc.png"
    log_p = script_dir / "plots/roc.log"
    identifier_col = "identifier"
    score_col = "InteractionProbability"

    # run
    logging.basicConfig(filename=log_p, level=logging.INFO, filemode="w")
    models = get_models(model_dir)
    ground_truth = get_ground_truth_df()
    print(ground_truth.head())

    # empty fig
    fig, ax = plt.subplots()

    # iterate over models
    for model_name, prediction_df in models:
        logging.info(f"Processing model {model_name}")
        logging.info(f"Number of predictions: {len(prediction_df)}")
        nan_count = len(prediction_df) - len(prediction_df.dropna(subset=[score_col]))
        prediction_df = prediction_df.dropna(subset=[score_col])
        logging.info(f"Number of dropped NaNs in predictions: {nan_count}")
        y_pred = prediction_df[score_col].to_numpy()
        y_true = get_ground_truth_values(ground_truth, prediction_df[identifier_col])

        if len(y_pred) != len(ground_truth):
            logging.warning(
                f"Number of predictions ({len(y_pred)}) does not match the number of ground truth values ({len(ground_truth)})"
            )

        # calculate ROC curve
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        ax.plot(
            fpr,
            tpr,
            label=f"{model_name} (AUC = {roc_auc:.2f}, {nan_count} NaN values removed)",
        )

    ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.0])
    # adjust legend font dict
    for text in ax.get_legend().get_texts():
        text.set_fontsize("small")
    plt.savefig(plot_p, dpi=300)
    logging.info(f"Wrote ROC curve to {plot_p}")


if __name__ == "__main__":
    main()
