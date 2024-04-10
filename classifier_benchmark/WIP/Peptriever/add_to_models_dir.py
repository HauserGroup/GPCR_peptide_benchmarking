""" """

import os
import pathlib
import pandas as pd
import numpy as np


def normalize_predictions(distances):
    distances = np.array(distances)
    # get np.max, ignore nan
    max_dist = np.nanmax(distances)

    y_pred = 1 - distances / max_dist

    return y_pred


# settings
def run_main():
    script_dir = pathlib.Path(__file__).resolve().parent
    model_dir = script_dir.parent.parent / "models"
    pred_df = pd.read_csv(script_dir / "distances.csv", index_col=0)
    output_col = "InteractionProbability"

    # average distance
    out_dir = model_dir / "Peptriever_avg"
    out_dir.mkdir(exist_ok=True)
    avg_dist_df = pred_df.copy()
    # calc average of all columns
    avg_dist_df["avg_distance"] = avg_dist_df.mean(axis=1)
    # normalize
    avg_dist_df[output_col] = normalize_predictions(avg_dist_df["avg_distance"])
    # the index column should be the first column, called 'identifier'
    avg_dist_df = avg_dist_df.reset_index()
    avg_dist_df = avg_dist_df.rename(columns={"index": "identifier"})
    avg_dist_df.to_csv(out_dir / "predictions.csv")

    # ECL distance
    out_dir = model_dir / "Peptriever_ECL"
    out_dir.mkdir(exist_ok=True)
    ecl_dist_df = pred_df.copy()
    # columns to use
    ecl_cols = [col for col in pred_df.columns if "ECL" in col]
    # calc average of all columns
    ecl_dist_df["avg_distance"] = ecl_dist_df[ecl_cols].mean(axis=1)
    # normalize
    ecl_dist_df[output_col] = normalize_predictions(ecl_dist_df["avg_distance"])
    # the index column should be the first column, called 'identifier'
    ecl_dist_df = ecl_dist_df.reset_index()
    ecl_dist_df = ecl_dist_df.rename(columns={"index": "identifier"})
    ecl_dist_df.to_csv(out_dir / "predictions.csv")

    # only ECL1
    out_dir = model_dir / "Peptriever_ECL1"
    out_dir.mkdir(exist_ok=True)
    ecl1_dist_df = pred_df.copy()
    # columns to use
    ecl1_cols = [col for col in pred_df.columns if "ECL1" in col]
    # calc average of all columns
    ecl1_dist_df["avg_distance"] = ecl1_dist_df[ecl1_cols].mean(axis=1)
    # normalize
    ecl1_dist_df[output_col] = normalize_predictions(ecl1_dist_df["avg_distance"])
    # the index column should be the first column, called 'identifier'
    ecl1_dist_df = ecl1_dist_df.reset_index()
    ecl1_dist_df = ecl1_dist_df.rename(columns={"index": "identifier"})
    ecl1_dist_df.to_csv(out_dir / "predictions.csv")


if __name__ == "__main__":
    run_main()
