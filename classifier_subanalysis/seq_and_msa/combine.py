""" """

import pathlib
import pandas as pd


def combine():
    script_dir = pathlib.Path(__file__).parent.absolute()
    inputs = [
        script_dir / "classifier_no_temp_p1.csv",
        script_dir / "classifier_no_temp_p2.csv",
        script_dir / "classifier_no_temp_p3.csv",
    ]
    # load as dataframes
    dfs = [pd.read_csv(f) for f in inputs]
    # concatenate
    df = pd.concat(dfs)
    # keep first occurence of identifier
    df = df.drop_duplicates(subset=["identifier"])

    df.to_csv(script_dir / "combined.csv", index=False)


if __name__ == "__main__":
    combine()
    print("Done.")
