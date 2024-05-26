"""Plot a heatmap of the performance of the classifiers

include:
- confusion matrix
- precision
- recall
- f1 score
- accuracy

"""

import logging
import pathlib
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
)
from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values


def apply_first_pick_to_predictions(prediction_df, pos_or_neg_col):
    """
    Rank per GPCR, then set the first one to 1, the rest to 0

    prediction_df: two columns, identifier and InteractionProbability
    """
    # add gpcr column
    prediction_df["gpcr"] = prediction_df["identifier"].apply(
        lambda x: x.split("___")[0]
    )
    # sort by gpcr and InteractionProbability
    prediction_df = prediction_df.sort_values(
        by=["gpcr", "InteractionProbability"], ascending=[True, False]
    )
    # set the first one to 1, the rest to 0
    prediction_df[pos_or_neg_col] = 0
    prediction_df.loc[prediction_df.groupby("gpcr").head(1).index, pos_or_neg_col] = 1
    return prediction_df


def get_metrics(models, ground_truth, pos_or_neg_col):
    # define df
    df = pd.DataFrame(
        columns=[
            "Model",
            "TP",
            "FP",
            "TN",
            "FN",
            "Precision",
            "Recall",
            "F1",
            "Accuracy",
        ]
    )

    # iterate over models
    for model_name, prediction_df in models:
        y_pred = prediction_df[pos_or_neg_col]
        y_true = get_ground_truth_values(ground_truth, prediction_df["identifier"])

        # calculate metrics
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        accuracy = accuracy_score(y_true, y_pred)

        # add to df
        pred_df = pd.DataFrame(
            {
                "Model": model_name,
                "TP": tp,
                "FP": fp,
                "TN": tn,
                "FN": fn,
                "Precision": precision,
                "Recall": recall,
                "F1": f1,
                "Accuracy": accuracy,
            },
            index=[0],
        )
        df = pd.concat([df, pred_df])

    # make model index
    df = df.reset_index(drop=True)
    df = df.set_index("Model")

    return df


def plot_heatmap(metric_df, out_p):
    """example output:
    #                                 TP   FP    TN   FN  Precision    Recall        F1  Accuracy
    # Model
    # DSCRIPT2_TTV1                9  115  1124  115   0.072581  0.072581  0.072581  0.831255
    # Neuralplexer_sm_lig_plddt   12  112  1127  112   0.096774  0.096774  0.096774  0.835657
    # AF2_template_LIS            83   32  1045   27   0.721739  0.754545  0.737778  0.950295
    # AF3                        110   14   110   13   0.887097  0.894309  0.890688  0.890688
    # RFAA_template_pae_prot      25   99  1138   98   0.201613  0.203252  0.202429  0.855147
    # AF2_template_iptm+ptm       70   54  1185   54   0.564516  0.564516  0.564516  0.920763
    # RFAA_no_template_pae_prot   18  106  1133  105   0.145161  0.146341  0.145749  0.845081
    """

    # plot
    fig, ax = plt.subplots()
    columns_to_plot = ["Precision", "Recall", "F1", "Accuracy"]
    # swap columns and rows
    metric_df = metric_df[columns_to_plot]
    metric_df = metric_df.sort_values(by="F1", ascending=False)

    sns.heatmap(
        metric_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        # make cbar smaller
        cbar_kws={"shrink": 0.5},
        # set cbar limit to 0-1
        vmin=0,
        vmax=1,
        ax=ax,
        # horizontal alignment of the annotation text
        annot_kws={"ha": "center"},
        # widen the cells
        linewidths=0.5,
        # square cells
        square=True,
    )
    # place xtick labels on the top
    ax.xaxis.set_ticks_position("top")
    # rotate ytick labels
    plt.yticks(rotation=0)

    ax.set_title("Performance of the classifiers")
    ax.set_ylabel("Model")
    ax.set_xlabel("Metric")
    plt.savefig(out_p)


def run_main():
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/heatmap.png"
    log_p = script_dir / "plots/heatmap.log"
    model_dir = script_dir / "models"
    pos_or_neg_col = "y_pred"

    # get data
    ground_truth = get_ground_truth_df()
    models = get_models(model_dir)

    # apply first pick to predictions
    models = [
        (name, apply_first_pick_to_predictions(df, pos_or_neg_col))
        for name, df in models
    ]

    # get metrics
    metric_df = get_metrics(models, ground_truth, pos_or_neg_col)
    print(metric_df)

    # plot heatmap
    plot_heatmap(metric_df, plot_p)


if __name__ == "__main__":
    run_main()
