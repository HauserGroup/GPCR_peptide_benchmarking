""" """

import pandas as pd
import pathlib


def run_main():
    script_dir = pathlib.Path(__file__).parent
    in_df = script_dir / "RFAA_scores_without_templates.csv"
    in_df = pd.read_csv(in_df)

    # for pae_prot, invert the values
    in_df["pae_prot"] = in_df["pae_prot"] * -1

    # rename "pae_prot" to "InteractionProbability"
    in_df = in_df.rename(columns={"pae_prot": "InteractionProbability"})

    # drop others adn save
    in_df = in_df[["identifier", "InteractionProbability"]]
    in_df.to_csv(script_dir / "predictions.csv", index=False)


if __name__ == "__main__":
    run_main()
