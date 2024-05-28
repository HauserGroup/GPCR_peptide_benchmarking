"""Combine the previously missing predictions with the old existing ones."""

import pathlib
import pandas as pd


def run_main():
    script_dir = pathlib.Path(__file__).parent
    predictions = pd.read_csv(script_dir / "old_scores.csv")
    # drop predictions with nan iptm+ptm
    predictions = predictions.dropna(subset=["iptm+ptm"])
    new_predictions = pd.read_csv(script_dir / "benchmiss_scores.csv")
    # combine the predictions, on the 'identifier'
    combined = pd.concat([predictions, new_predictions], ignore_index=True)
    print(combined)
    # rename iptm+ptm to InteractionProbability
    combined = combined.rename(columns={"iptm+ptm": "InteractionProbability"})
    combined.to_csv(script_dir / "predictions.csv", index=False)


if __name__ == "__main__":
    run_main()
