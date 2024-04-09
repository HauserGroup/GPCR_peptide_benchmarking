"""Receiver operating characteristic for the classifier benchmark."""

import sys
import pathlib
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc


def get_ground_truth(
    path_to_decoy_csv,
    interaction_column="Acts as agonist",
    decoy_type_column="Decoy Type",
    identifier_column="identifier",
    # for creating the identifier if it isn't found
    receptor_col="Target ID",
    peptide_col="Decoy ID",
):
    """Get a pandas df for the ground truth of the decoys interactions."""
    df = pd.read_csv(path_to_decoy_csv)

    # check if identifier column exists
    if identifier_column not in df.columns:
        print(
            f"Identifier column not found in the decoy csv. Creating one from {receptor_col} and {peptide_col}..."
        )
        df[identifier_column] = (
            df[receptor_col].astype(str) + "___" + df[peptide_col].astype(str)
        )
    assert df[identifier_column].is_unique, "Identifier column is not unique"
    # make interaction column boolean
    df[interaction_column] = df[interaction_column].astype(bool)
    # make decoy type column categorical
    df[decoy_type_column] = df[decoy_type_column].astype("category")
    return df


def get_models(model_dir, identifier_column="identifier"):
    """Get the models in the model directory.

    returns a list of tuples with the model name and the prediction df.
    """
    models = []
    for model in model_dir.iterdir():
        if model.is_dir():
            # get name of model
            model_name = model.name
            print("Getting data for model", model_name)
            # get path to prediction csv
            prediction_csv = model / "predictions.csv"
            if not prediction_csv.exists():
                print(f"Predictions not found for {model_name}. Skipping...")
                continue
            # read df
            prediction_csv = pd.read_csv(prediction_csv)
            # check identifier column is unique
            assert prediction_csv[
                identifier_column
            ].is_unique, "Identifier column is not unique."
            # append list and df
            models.append((model_name, prediction_csv))

    return models


def plot_ROC_curve(
    truth_df,
    prediction_list,
    save_path,
    identifier_column="identifier",
    interaction_column="Acts as agonist",
    prediction_column="InteractionProbability",
):
    """
    Plot the ROC curve for the models.
    use roc_curve and auc from sklearn.metrics
    add the AUC to the legend

    match the rows based on the identifier column
    """
    pos_identifiers = truth_df[truth_df[interaction_column]][identifier_column]
    neg_identifiers = truth_df[~truth_df[interaction_column]][identifier_column]

    # plot
    plt.figure()
    plt.plot([0, 1], [0, 1], "k--")
    for model_name, prediction_df in prediction_list:
        print("Plotting ROC curve for", model_name)
        # match the rows based on the identifier column
        prediction_df = prediction_df.set_index(identifier_column)
        pos_predictions = prediction_df.loc[pos_identifiers][prediction_column]
        neg_predictions = prediction_df.loc[neg_identifiers][prediction_column]

        # calculate ROC curve
        y_true = np.concatenate(
            [np.ones_like(pos_predictions), np.zeros_like(neg_predictions)]
        )
        y_score = np.concatenate([pos_predictions, neg_predictions])
        fpr, tpr, _ = roc_curve(y_true, y_score)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{model_name} (AUC = {roc_auc:.2f})")

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.savefig(save_path, dpi=300)


if __name__ == "__main__":
    # settings
    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    MODEL_DIR = SCRIPT_DIR / "models"
    DECOY_CSV_P = (
        SCRIPT_DIR.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    PLOT_PATH = SCRIPT_DIR / "roc_curve.png"

    PREDICTION_COLUMN = "InteractionProbability"
    INTERACTION_COLUMN = "Acts as agonist"

    # get the model names, and prediction DFs
    TRUTH_DF = get_ground_truth(DECOY_CSV_P)
    PREDICTION_LIST = get_models(MODEL_DIR)
    plot_ROC_curve(
        TRUTH_DF,
        PREDICTION_LIST,
        SCRIPT_DIR / "plots/roc_curve.png",
        interaction_column=INTERACTION_COLUMN,
        prediction_column=PREDICTION_COLUMN,
    )
