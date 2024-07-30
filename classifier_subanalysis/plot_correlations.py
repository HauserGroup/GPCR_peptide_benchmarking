"""
Create a linear correlation pot between principal agonist position and principal agonist activity.

TODO: correlate to scores.

      correlate to ranking. <--- first
"""

import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from scipy import stats
from correlation import get_spearman_correlation

sys.path.append(".")
from colors import COLOR
from parse_predictions import get_ground_truth_df, get_ground_truth_values, get_models


def dict_string_to_dict(dict_string, key_to_int=True, value_to_int=True):
    """
    So no data is lost, I saved some dicts as strings like this:
    1:428|2:8
    which should be:
    {1: 428, 2: 8}
    """
    out_dict = {}
    for pair in dict_string.split("|"):
        key, value = pair.split(":")
        if key_to_int:
            key = int(key)
        if value_to_int:
            value = int(value)
        out_dict[key] = value
    return out_dict


def load_msa_data():
    script_dir = pathlib.Path(__file__).parent.absolute()
    msa_dir = script_dir / "seq_and_msa"
    parts = [
        msa_dir / "classifier_no_temp_p1.csv",
        msa_dir / "classifier_no_temp_p2.csv",
        msa_dir / "classifier_no_temp_p3.csv",
    ]
    df = pd.concat([pd.read_csv(part) for part in parts])
    df = df.drop_duplicates()

    df = df.assign(chain_lengths=df["chain_lengths"].apply(dict_string_to_dict))
    df = df.assign(msa_seq_lengths=df["msa_seq_lengths"].apply(dict_string_to_dict))

    # check all have only two chains
    for i, row in df.iterrows():
        assert len(row["chain_lengths"]) == 2, row["identifier"]
        assert len(row["msa_seq_lengths"]) == 2, row["identifier"]
    return df


def plot_seaborn_linear_correlation(x, y, save_path):
    sns.set(style="whitegrid")
    sns.set_context("talk")
    sns.set_palette("colorblind")
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.regplot(
        x=x,
        y=y,
        ax=ax,
    )
    # add correlation
    rho, p_val = get_spearman_correlation(x, y)
    ax.text(
        0.05,
        0.95,
        f"ρ = {rho:.2f}, p = {p_val:.2e}",
        transform=ax.transAxes,
        fontsize=14,
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.5),
    )

    ax.set_xlabel(x.name)
    ax.set_ylabel(y.name)
    plt.savefig(save_path)
    plt.close()


def main():
    msa_data = load_msa_data()
    script_dir = pathlib.Path(__file__).parent.absolute()
    ground_truth = get_ground_truth_df()
    plot_dir = script_dir / "plots"
    agonist_rankings_p = script_dir / "agonist_rankings.csv"
    agonist_rankings_df = pd.read_csv(agonist_rankings_p)

    # get models
    for model_name, pred_df in get_models(model_dir=script_dir / "models"):
        # add msa data to pred_df by matching identifier
        assert pred_df["identifier"].is_unique, "Identifier column is not unique."
        assert msa_data["identifier"].is_unique, "Identifier column is not unique."
        pred_df = pred_df.merge(msa_data, on="identifier")

        y_true = get_ground_truth_values(
            ground_truth, identifiers=pred_df["identifier"]
        )
        y_pred = pred_df["InteractionProbability"]

        # index 1 of chain_lengths is the gpcr
        gpcr_lengths = pred_df["chain_lengths"].apply(lambda x: x[1]).values
        ligand_lengths = pred_df["chain_lengths"].apply(lambda x: x[2]).values
        gpcr_depth = pred_df["msa_seq_lengths"].apply(lambda x: x[1]).values
        ligand_depth = pred_df["msa_seq_lengths"].apply(lambda x: x[2]).values

        # plot spearman correlation
        for variable_name, values in zip(
            ["gpcr_lengths", "ligand_lengths", "gpcr_depth", "ligand_depth"],
            [gpcr_lengths, ligand_lengths, gpcr_depth, ligand_depth],
        ):
            save_p = plot_dir / f"{model_name}_{variable_name}_correlation.png"
            plot_seaborn_linear_correlation(
                pd.Series(values, name=variable_name),
                pd.Series(y_pred, name="InteractionProbability"),
                save_p,
            )

        # get rankings
        rankings = agonist_rankings_df[agonist_rankings_df["Model"] == model_name]
        print(rankings)


if __name__ == "__main__":
    main()
