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
from plot_heatmap_combined import apply_first_pick_to_predictions
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# add "."
sys.path.append(".")
from colors import COLOR


def get_rank_dist_for_pred_df(pred_df):
    rank_dist = []
    for i, row in pred_df.iterrows():
        rank_dist.append(row["rank"])
    return rank_dist


def run_main():
    """ """
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir / "models")


if __name__ == "__main__":
    run_main()
