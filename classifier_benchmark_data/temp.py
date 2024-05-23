"""Fix decoy rankings"""

import pathlib
import os
import pandas as pd
import numpy as np


def main():
    script_dir = pathlib.Path(__file__).resolve().parent
    out_p = script_dir / "output/6_interactions_with_decoys.csv"
    df = pd.read_csv(out_p)

    # add identifier column
    df["Identifier"] = df["Target ID"] + "___" + df["Decoy ID"].astype(str)

    # remove the ranking column
    df.drop(columns=["Decoy Rank"], inplace=True)

    # add new ranking column
    df["Decoy Rank"] = np.nan

    unique_targets = df["Target ID"].unique()
    for target in unique_targets:
        target_rows = df[df["Target ID"] == target]
        # add rank to similar decoys, from 0 to 4
        similar_rows = target_rows[target_rows["Decoy Type"] == "Similar"]
        similar_rows.sort_values(
            by=["Target Similarity to Original Target"], inplace=True, ascending=False
        )
        # set rank
        for rank, row in enumerate(similar_rows.iterrows()):
            df.loc[row[0], "Decoy Rank"] = rank

        # add rank to dissimilar decoys, from 0 to 4
        dissimilar_rows = target_rows[target_rows["Decoy Type"] == "Dissimilar"]
        dissimilar_rows.sort_values(
            by=["Target Similarity to Original Target"], inplace=True, ascending=True
        )
        for rank, row in enumerate(dissimilar_rows.iterrows()):
            df.loc[row[0], "Decoy Rank"] = rank

    # sort on target
    df.sort_values(
        by=["Target ID", "Target Similarity to Original Target"], inplace=True
    )
    # place rank and sim columns at the front
    cols = df.columns.tolist()
    cols = cols[-2:] + cols[:-2]
    df = df[cols]

    df.to_csv(out_p, index=False)


if __name__ == "__main__":
    main()
