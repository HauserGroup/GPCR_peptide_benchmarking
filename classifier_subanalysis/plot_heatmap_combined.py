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
import numpy as np
import itertools

# colors.py is in working directory
sys.path.append(".")
from colors import CMAP_GOOD_BAD

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


def plot_heatmap(metric_df, out_p, title):
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
    metric_df = metric_df.sort_values(by="F1", ascending=True)
    metric_df = metric_df.T

    sns.heatmap(
        metric_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm_r",  # RdYlBu, coolwarm, viridis, plasma, inferno, magma, cividis
        cbar=True,
        # make cbar smaller
        cbar_kws={
            "shrink": 0.5,
            # move cbar to the right
            "location": "right",
            # pad between cbar and plot
            # move on x-axis
            "anchor": (1.0, 0.5),
        },
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
    # make it to the xlabels have enough space
    # place xtick labels on the top
    ax.xaxis.set_ticks_position("top")
    # rotate ytick labels
    # place yticks on right side
    ax.yaxis.set_ticks_position("right")
    # rotate xtick
    plt.xlabel("")
    plt.xticks(rotation=15, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    ax.set_title(title)
    plt.savefig(out_p, dpi=300)


def get_metrics_for_all():
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/heatmap.svg"
    log_p = script_dir / "plots/heatmap.log"
    model_dir = script_dir / "models"
    pos_or_neg_col = "y_pred"

    # get data
    ground_truth = get_ground_truth_df()
    models = get_models(model_dir)
    models = [model for model in models if model[0] != "AF3"]

    # apply first pick to predictions
    models = [
        (name, apply_first_pick_to_predictions(df, pos_or_neg_col))
        for name, df in models
    ]

    # get metrics
    metric_df = get_metrics(models, ground_truth, pos_or_neg_col)
    return metric_df


def get_metrics_for_similar():
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/heatmap_dissimilar.png"
    log_p = script_dir / "plots/heatmap_dissimilar.log"
    model_dir = script_dir / "models"
    pos_or_neg_col = "y_pred"

    # get data
    ground_truth = get_ground_truth_df()
    models = get_models(model_dir)
    # drop "AF3" model
    models = [model for model in models if model[0] != "AF3"]

    # filter ground truth, for decoy type in ["Dissimilar", "Principal Agonist"]
    filtered = ground_truth["Decoy Type"].isin(["Similar", "Principal Agonist"])
    ground_truth = ground_truth[filtered]
    valid_identifiers = ground_truth["identifier"].values

    # filter models
    models = [
        (name, df[df["identifier"].isin(valid_identifiers)]) for name, df in models
    ]

    # apply first pick to predictions
    models = [
        (name, apply_first_pick_to_predictions(df, pos_or_neg_col))
        for name, df in models
    ]

    # get metrics
    metric_df = get_metrics(models, ground_truth, pos_or_neg_col)
    return metric_df


def get_metrics_for_dissimilar():
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/heatmap_dissimilar.png"
    log_p = script_dir / "plots/heatmap_dissimilar.log"
    model_dir = script_dir / "models"
    pos_or_neg_col = "y_pred"

    # get data
    ground_truth = get_ground_truth_df()
    models = get_models(model_dir)
    # drop "AF3" model
    models = [model for model in models if model[0] != "AF3"]

    # filter ground truth, for decoy type in ["Dissimilar", "Principal Agonist"]
    filtered = ground_truth["Decoy Type"].isin(["Dissimilar", "Principal Agonist"])
    ground_truth = ground_truth[filtered]
    valid_identifiers = ground_truth["identifier"].values

    # filter models
    models = [
        (name, df[df["identifier"].isin(valid_identifiers)]) for name, df in models
    ]

    # apply first pick to predictions
    models = [
        (name, apply_first_pick_to_predictions(df, pos_or_neg_col))
        for name, df in models
    ]

    # get metrics
    metric_df = get_metrics(models, ground_truth, pos_or_neg_col)
    # print metric sample stats
    logging.info(metric_df.describe())

    return metric_df


def get_metrics_for_1on1():
    script_dir = pathlib.Path(__file__).parent
    model_dir = script_dir / "models"
    pos_or_neg_col = "y_pred"

    # get data
    ground_truth = get_ground_truth_df()
    models = get_models(model_dir)

    # get 1on1 identifiers from af3 predictions
    for m in models:
        if m[0] == "AF3":
            af3 = m[1]
            valid_identifiers = af3["identifier"].values
            break
    # filter models
    models = [
        (name, df[df["identifier"].isin(valid_identifiers)]) for name, df in models
    ]

    # apply first pick to predictions
    models = [
        (name, apply_first_pick_to_predictions(df, pos_or_neg_col))
        for name, df in models
    ]

    # get metrics
    metric_df = get_metrics(models, ground_truth, pos_or_neg_col)
    return metric_df


def show_nans_as_x(df):
    for i, j in itertools.product(range(df.shape[0]), range(df.shape[1])):
        value = df.iat[i, j]
        if pd.isna(value):
            plt.text(
                j + 0.5,
                i + 0.5,
                "x",
                ha="center",
                va="center",
                color="black",
                fontsize=12,
            )


def add_random(df, negatives_per_positive):
    """
    Add a row for a random model to the DataFrame with a given positive to negative ratio.

    Parameters:
    df: pandas DataFrame containing the original data.
    positive_to_negative_ratio: float. The ratio of positive to negative samples for the random model.

    Returns:
    Updated DataFrame with the random model added.
    """
    # Assume 100 gpcrs
    n_pos = 100
    n_neg = n_pos * negatives_per_positive
    total = n_pos + n_neg
    pos_neg_ratio = n_pos / total
    # only 1 positive may be chosen per gpcr
    tp = n_pos * pos_neg_ratio
    fn = n_pos - tp
    tn = n_neg * (1 - pos_neg_ratio)
    fp = n_neg - tn
    # stats
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * (precision * recall) / (precision + recall)
    accuracy = (tp + tn) / total

    # Add to df
    pred_df = pd.DataFrame(
        {
            "Model": ["random"],
            "TP": [tp],
            "FP": [fp],
            "TN": [tn],
            "FN": [fn],
            "Precision": [precision],
            "Recall": [recall],
            "F1": [f1],
            "Accuracy": [accuracy],
        }
    )
    pred_df = pred_df.set_index("Model")
    pred_df = pred_df.astype(float)
    df = pd.concat([df, pred_df])
    return df


def plot_combined():
    """Create a heatmap.
    - summarizes the 3 evaluation modes

    """
    # print(plt.style.available)
    # ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    plt.style.use("seaborn-v0_8-whitegrid")
    metric_all = get_metrics_for_all()
    metric_all = add_random(metric_all, 10)
    metric_all = metric_all.sort_values(by="F1", ascending=False)
    models = metric_all.index

    # remove models if 'LIS' in model name or 'APPRAISE'
    models = [model for model in models if "LIS" not in model and "APPRAISE" not in model.upper()]
    # place AF3 after 'AF2'
    af2_index = models.index("AF2")
    models = models[:af2_index + 1] + ["AF3"] + models[af2_index + 1:]
    rows = models
    cols = ["Accuracy", "Precision", "Recall", "F1"]
    for col in cols:
        metric_all.loc["AF3", col] = np.nan
    metric_all = metric_all.apply(pd.to_numeric, errors="coerce")
    metric_all = metric_all.loc[rows, cols]

    metric_1on1 = get_metrics_for_1on1()
    metric_1on1 = add_random(metric_1on1, 1)
    metric_1on1 = metric_1on1.sort_values(by="F1", ascending=False)
    metric_1on1 = metric_1on1.loc[rows, cols]
    metric_1on1 = metric_1on1.apply(pd.to_numeric, errors="coerce")

    metric_similar = get_metrics_for_similar()
    for col in cols:
        metric_similar.loc["AF3", col] = np.nan
    metric_similar = metric_similar.apply(pd.to_numeric, errors="coerce")
    metric_similar = add_random(metric_similar, 5)
    metric_similar = metric_similar.loc[rows, cols]

    metric_dissimilar = get_metrics_for_dissimilar()
    for col in cols:
        metric_dissimilar.loc["AF3", col] = np.nan
    metric_dissimilar = metric_dissimilar.apply(pd.to_numeric, errors="coerce")
    metric_dissimilar = add_random(metric_dissimilar, 5)
    metric_dissimilar = metric_dissimilar.loc[rows, cols]

    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/combined_heatmap.svg"

    # create a figure with 5 subplots (4 modes, 1 cbar)
    fig, axs = plt.subplots(1, 5, figsize=(15, 5))
    cmap = CMAP_GOOD_BAD
    vmin = 0
    vmax = 1.0
    fmt = ".2f"
    annot = True
    cell_width = 5
    cell_height = 5
    linewidths = 0.5
    square = True

    # plot 1on1 first in slot 1
    metric_1on1 = metric_1on1.astype(float)
    plt.sca(axs[0])
    sns.heatmap(
        metric_1on1,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        cbar=False,
        fmt=fmt,
        annot=annot,
        linewidths=linewidths,
        square=square,
        # set cell size
        # cbar_kws={"shrink": 0.5},
    )
    plt.xlabel("")
    plt.ylabel("")
    plt.title("agonist vs most dissimilar (1:1)")

    # plot 5on1 in slot 2
    metric_similar = metric_similar.astype(float)
    plt.sca(axs[1])
    sns.heatmap(
        metric_similar,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        # hide cbar
        cbar=False,
        fmt=fmt,
        annot=annot,
        linewidths=linewidths,
        square=square,
    )
    # disable the row labels (already in slot 1)
    plt.yticks([])
    plt.xlabel("")
    plt.ylabel("")
    show_nans_as_x(metric_similar)
    plt.title("similar (5:1)")

    # plot 5 on 1 in slot 3
    metric_dissimilar = metric_dissimilar.astype(float)
    plt.sca(axs[2])
    sns.heatmap(
        metric_dissimilar,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        # hide cbar
        fmt=fmt,
        annot=annot,
        mask=metric_dissimilar.isna(),
        linewidths=linewidths,
        cbar=False,
        square=square,
    )
    show_nans_as_x(metric_dissimilar)
    # disable the row labels (already in slot 1)
    plt.yticks([])
    plt.xlabel("")
    plt.ylabel("")
    plt.title("dissimilar (5:1)")

    # plot all in slot 4
    metric_all = metric_all.astype(float)
    plt.sca(axs[3])
    sns.heatmap(
        metric_all,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        # hide cbar
        fmt=fmt,
        annot=annot,
        mask=metric_all.isna(),
        linewidths=linewidths,
        cbar=False,
        square=square,
    )

    # disable the row labels (already in slot 1)
    plt.yticks([])
    plt.xlabel("")
    plt.ylabel("")
    show_nans_as_x(metric_all)
    plt.title("all (10:1)")

    # place xtick labels on the top for all
    for ax in axs:
        ax.xaxis.set_ticks_position("top")
        # remove ticks
        ax.tick_params(axis="both", which="both", length=0)
        # tighten the layout
        ax.set_aspect("equal")  # auto instead of equal

    # in the 4th plot, place the cbar (no heatmap)
    plt.sca(axs[4])
    plt.axis("off")
    sns.heatmap(
        [[]],
        vmin=vmin,
        vmax=vmax,
        cbar=True,
        fmt=fmt,
        annot=annot,
        linewidths=linewidths,
        square=square,
        cmap=cmap,
        cbar_kws={
            "shrink": 0.5,
            "location": "left",
            # center
            "anchor": (0.5, 0.5),
            # left pad
            "pad": 0.1,
        },
    )
    plt.tight_layout()

    # increase font size of heatmap labels
    for ax in axs:
        for item in (
            [ax.title, ax.xaxis.label, ax.yaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
        ):
            item.set_fontsize(9)

        # increase font size of annotations
        for text in ax.texts:
            text.set_fontsize(11)

    plt.savefig(
        plot_p,
        dpi=300,
        # transp bgr
        transparent=True,
    )


def plot_10_to_1_only():
    """Create a heatmap.
    - summarizes the 3 evaluation modes

    """
    # print(plt.style.available)
    # ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
    plt.style.use("seaborn-v0_8-whitegrid")
    metric_all = get_metrics_for_all()
    # metric_all = add_random(metric_all, 10)
    metric_all = metric_all.sort_values(by="F1", ascending=False)
    models = metric_all.index
    rows = models
    cols = ["Accuracy", "Precision", "Recall", "F1"]
    for col in cols:
        metric_all.loc["AF3", col] = np.nan
    metric_all = metric_all.apply(pd.to_numeric, errors="coerce")
    metric_all = metric_all.loc[rows, cols]

    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/combined_heatmap_10on1.svg"

    # create a figure with 5 subplots (4 modes, 1 cbar)
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    cmap = CMAP_GOOD_BAD
    vmin = 0
    vmax = 1.0
    fmt = ".2f"
    annot = True
    cell_width = 10
    cell_height = 10
    linewidths = 0.5
    square = True

    # plot all 
    metric_all = metric_all.astype(float)
    plt.sca(axs[0])
    sns.heatmap(
        metric_all,
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
        # hide cbar
        fmt=fmt,
        annot=annot,
        mask=metric_all.isna(),
        linewidths=linewidths,
        cbar=False,
        square=square,
        # set cell width
    )

    # disable the row labels (already in slot 1)
    plt.xlabel("")
    plt.ylabel("")
    show_nans_as_x(metric_all)

    # place xtick labels on the top for all
    for ax in axs:
        ax.xaxis.set_ticks_position("top")
        # remove ticks
        ax.tick_params(axis="both", which="both", length=0)
        # tighten the layout
        ax.set_aspect("equal")  # auto instead of equal

    # set cell width wider
    plt.sca(axs[0])
    plt.xticks(rotation=15, fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    # make the cells larger of the heatmap in the 1st plot
    plt.sca(axs[0])
    plt.yticks(rotation=0, fontsize=9)
    plt.xticks(rotation=15, fontsize=9)
    plt.title("")
    cell_width = 10
    cell_height = 7
    plt.gcf().set_size_inches(cell_width, cell_height)


    # in the 2nd plot, place the cbar (no heatmap)
    plt.sca(axs[1])
    plt.axis("off")
    sns.heatmap(
        [[]],
        vmin=vmin,
        vmax=vmax,
        cbar=True,
        fmt=fmt,
        annot=annot,
        linewidths=linewidths,
        square=square,
        cmap=cmap,
        cbar_kws={
            "shrink": 0.25,
            "location": "left",
            # center
            "anchor": (0.1, 0.5),
            # left pad
            "pad": 0.1,
        },
    )
    plt.tight_layout()

    # increase font size of heatmap labels
    for ax in axs:
        for item in (
            [ax.title, ax.xaxis.label, ax.yaxis.label]
            + ax.get_xticklabels()
            + ax.get_yticklabels()
        ):
            item.set_fontsize(9)

        # increase font size of annotations
        for text in ax.texts:
            text.set_fontsize(11)

    plt.savefig(
        plot_p,
        dpi=300,
        # transp bgr
        transparent=True,
    )


if __name__ == "__main__":
    plot_combined()
    plot_10_to_1_only()
