""" """

import pathlib
import pandas
import numpy as np


def run_main():
    script_dir = pathlib.Path(__file__).parent
    df_p = script_dir / "result_df.csv"
    df_new_p = script_dir / "result_df_withid.csv"
    out_p = script_dir / "predictions.csv"

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

    # save df
    df.to_csv(df_new_p, index=False)

    # save only the identifier and LIS columns
    df = df[["identifier", "LIS"]]
    # rename LIS to InteractionProbability
    df = df.rename(columns={"LIS": "InteractionProbability"})
    df.to_csv(out_p, index=False)


if __name__ == "__main__":
    run_main()
