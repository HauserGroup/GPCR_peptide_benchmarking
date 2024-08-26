""" """

import pathlib
import pandas
import numpy as np


def filter_df(df_p, out_p):
    df = pandas.read_csv(df_p)
    # sort on "ipTM"
    df = df.sort_values("ipTM", ascending=False)

    # take the first row for each unique "saved folder" value
    df = df.groupby("saved folder", as_index=False).first()

    # add identifier column, by taking the "saved folder" name
    df["identifier"] = ""
    for i, row in df.iterrows():
        dir_p = pathlib.Path(str(row["saved folder"]))
        df.at[i, "identifier"] = dir_p.name

    # save only the identifier and LIS columns
    df = df[["identifier", "LIS"]]
    # rename LIS to InteractionProbability
    df = df.rename(columns={"LIS": "InteractionProbability"})
    df.to_csv(out_p, index=False)


def combine_df(df_paths: list):
    dfs = [pandas.read_csv(p) for p in df_paths]
    # merge the dataframes on "identifier"
    df = pandas.concat(dfs)
    # sort on "identifier"
    df = df.sort_values("identifier")
    # drop samples that have the same identifier AND the same InteractionProbability
    df = df.drop_duplicates(subset=["identifier"])
    # save the dataframe
    script_dir = pathlib.Path(__file__).parent
    df.to_csv(script_dir / "predictions.csv", index=False)


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    filter_df(script_dir / "p1.csv", script_dir / "p1_new.csv")
    filter_df(script_dir / "p2.csv", script_dir / "p2_new.csv")
    filter_df(script_dir / "p3.csv", script_dir / "p3_new.csv")

    # combine the three dataframes
    combine_df(
        [
            script_dir / "p1_new.csv",
            script_dir / "p2_new.csv",
            script_dir / "p3_new.csv",
        ]
    )
