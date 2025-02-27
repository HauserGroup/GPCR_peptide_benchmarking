""" """

import pathlib
import pandas as pd


def run_main():
    script_dir = pathlib.Path(__file__).parent
    # get the ground truth
    ground_truth_p = (
        script_dir.parent.parent.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    df = pd.read_csv(ground_truth_p)

    for i, row in df.iterrows():
        # if the type is "Principal Agonist"
        if row["Decoy Type"] == "Principal Agonist":
            continue
        elif row["Decoy Rank"] < 1 and row["Decoy Type"] == "Dissimilar":
            continue
        # if conditions aren't met, drop the row
        else:
            df.drop(i, inplace=True)

    # save df
    df.to_csv(script_dir / "1on1.csv", index=False)


if __name__ == "__main__":
    run_main()
