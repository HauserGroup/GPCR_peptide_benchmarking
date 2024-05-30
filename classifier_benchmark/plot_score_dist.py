"""
For each model.
    Plot a y-axis with the InteractionProbability.
    Plot each of the 124 GPCRs on the x-axis (unlabelled, 0-123).
    Use circles for the agonists, triangles for decoys.
    
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import random
import pandas as pd

from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values
from parse_predictions import get_gpcr_class


def plot_score_dist(model_name, y_pred, y_true, gpcrs, classes, ax):
    """
    Plot the score distribution for a model.
    """
    # color GPCRs according to class. Use "light" version of color if decoy.
    sns.set_context("talk")
    colors = list()
    shapes = list()
    for i, gpcr_class in enumerate(classes):
        if y_true[i] == 1:
            color_key = f"{gpcr_class} PA"
            shape = "x"
        else:
            color_key = f"{gpcr_class} decoy"
            shape = "s"
        colors.append(GPCR_TO_COLOR[color_key])
        shapes.append(shape)

    # plot
    ax.scatter(range(len(y_pred)), y_pred, c=colors, marker='D', s=1)
    ax.set_title(model_name)
    ax.set_xlabel("GPCRs")
    ax.set_ylabel("InteractionProbability")
    ax.set_xticks([])


def run_main():
    ""
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / 'models')
    unique_models = list([m[0] for m in models])
    plot_p = script_dir / "plots/score_dist.png"
    ground_truth = get_ground_truth_df()
    
    # create subplots, vertically
    fig, axs = plt.subplots(len(unique_models), 1, figsize=(len(unique_models), 2*len(unique_models)))
    
    all_gpcrs = ground_truth['identifier'].apply(lambda x: x.split("___")[0]).unique()
    gpcr_to_class = {g: get_gpcr_class(g) for g in all_gpcrs}

    for model_index, (model_name, prediction_df) in enumerate(models):
        prediction_df['gpcr_id'] = prediction_df["identifier"].apply(lambda x: x.split("___")[0])
        prediction_df['class'] = prediction_df['gpcr_id'].apply(lambda x: gpcr_to_class[x])
        prediction_df['gpcr'] = prediction_df['gpcr_id'].apply(lambda x: x.split("_human")[0])
        
        # sort on class, then gpcr
        prediction_df = prediction_df.sort_values(['class', 'gpcr'])
        y_true = get_ground_truth_values(ground_truth=ground_truth, identifiers=prediction_df['identifier'].values)
        y_pred = prediction_df['InteractionProbability'].values

        # plot
        ax = axs[model_index]
        plot_score_dist(model_name, y_pred, y_true, prediction_df['gpcr'].values, prediction_df['class'].values, ax)

    plt.tight_layout()
    plt.savefig(plot_p, dpi=300)


if __name__ == "__main__":
    GPCR_TO_COLOR = {"Class A (Rhodopsin) PA": "rgba(17,81,133,0.4)",
                     "Class A (Rhodopsin) decoy": "rgba(17,81,133,0.9)",
                        "Class B1 (Secretin) PA": "rgba(72,45,141,0.4)",
                        "Class B1 (Secretin) decoy": "rgba(72,45,141,1.0)",
                        "Class F (Frizzled) PA": "rgba(71,131,71,0.4)",
                        "Class F (Frizzled) decoy": "rgba(71,131,71,1.0)",
                        "Other GPCRs PA": "rgba(128,128,128,0.4)",
                        "Other GPCRs decoy": "rgba(128,128,128,1.0)"}
    # fix rgba
    for key in GPCR_TO_COLOR:
        # convert to 0-1
        color = GPCR_TO_COLOR[key]
        color = color.replace("rgba(", "").replace(")", "")
        color = color.split(",")
        color = [int(c)/255 for c in color[:3]]

        GPCR_TO_COLOR[key] = color

        
    run_main()