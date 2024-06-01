"""Combine the previously missing predictions with the old existing ones."""

import pathlib
import pandas as pd


def run_main():
    script_dir = pathlib.Path(__file__).parent
    p1 = script_dir / "p1.csv"
    p2 = script_dir / "p2.csv"
    p3 = script_dir / "p3.csv"

    # combine on identifier
    df1 = pd.read_csv(p1)
    df2 = pd.read_csv(p2)
    df3 = pd.read_csv(p3)

    # drop those with nan iptm+ptm
    df1 = df1.dropna(subset=["iptm+ptm"])
    df2 = df2.dropna(subset=["iptm+ptm"])
    df3 = df3.dropna(subset=["iptm+ptm"])

    # combine on identifier
    df = pd.concat([df1, df2, df3], ignore_index=True)

    # drop duplicates
    df = df.drop_duplicates(subset=["identifier"])

    # rename iptm+ptm to InteractionProbability
    df = df.rename(columns={"iptm+ptm": "InteractionProbability"})
    df.to_csv(script_dir / "predictions.csv", index=False)


if __name__ == "__main__":
    run_main()
