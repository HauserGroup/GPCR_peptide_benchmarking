""" """

import pathlib
import logging
import pandas as pd


def run_main():
    """ """
    script_dir = pathlib.Path(__file__).parent
    p1 = script_dir / "p1.csv"
    p1 = pd.read_csv(p1)
    # set identifier as index
    p1.set_index("identifier", inplace=True)

    p2 = script_dir / "p2.csv"
    p2 = pd.read_csv(p2)
    # set identifier as index
    p2.set_index("identifier", inplace=True)

    # combine
    combined = pd.concat([p1, p2], axis=0)

    # only keep identifier and avg_plddt
    combined = combined[["avg_plddt"]]

    # rename to 'InteractionProbability'
    combined.rename(columns={"avg_plddt": "InteractionProbability"}, inplace=True)

    # save to csv
    combined.to_csv(script_dir / "predictions.csv")


if __name__ == "__main__":
    run_main()
