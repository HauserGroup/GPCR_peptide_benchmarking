"""For each dir in /models/ that does not contain '+pocket'
Read the predictions. If the complex does not have a peptide in the pocket, halve the score.
Create a new dir with '+pocket' and save the predictions there.
"""

import pathlib
import pandas as pd


def get_pocket_data():
    script_dir = pathlib.Path(__file__).parent
    pocket_p = script_dir / "in_pocket/in_pocket_results.csv"
    pocket_df = pd.read_csv(pocket_p)

    #             model          identifier  shortest_distance
    # 0     ESMFold  vipr2_human___1152           6.243616
    # 1     ESMFold   ccr6_human___2257          34.367416
    return pocket_df


def get_pocket_distance(pocket_df, identifier, model):
    pocket_df = pocket_df[
        (pocket_df["identifier"] == identifier) & (pocket_df["model"] == model)
    ]
    if len(pocket_df) == 0:
        return None
    elif len(pocket_df) == 1:
        return pocket_df["shortest_distance"].values[0]
    else:
        raise ValueError("More than one pocket found.")


def run_main():
    # settings
    script_dir = pathlib.Path(__file__).parent
    model_dir = script_dir / "models"
    pocket_suffix = "+pocket"
    distance_cutoff = 12.0  # angstroms
    interaction_col = "InteractionProbability"

    # map models to which structure they rely on
    model_map = {
        "AF2 (no templates)": "AF2_no_templates",
        "AF2 LIS (no templates)": "AF2_no_templates",
        #
        "AF2": "AF2",
        "AF2 LIS": "AF2",
        #
        "RF-AA (no templates)": "RFAA_no_templates",
        "RF-AA": "RFAA",
        # ESMFold
        "ESMFold": "ESMFold",
    }

    models = [
        d for d in model_dir.iterdir() if d.is_dir() and pocket_suffix not in d.name
    ]
    pocket_df = get_pocket_data()

    for m in models:
        pred_df = pd.read_csv(m / "predictions.csv")
        model = m.name
        new_dir = model_dir / f"{model}{pocket_suffix}"
        model_to_match = model_map.get(model, None)
        if model_to_match is None:
            print(f"Skipping {model} as it is not in the model_map.")
            continue

        pred_df["pocket_distance"] = pred_df.apply(
            lambda x: get_pocket_distance(pocket_df, x["identifier"], model_to_match),
            axis=1,
        )
        # drop those with pocket_distance = None
        drop_count = pred_df["pocket_distance"].isna().sum()
        pred_df = pred_df.dropna(subset=["pocket_distance"])
        print(f"Dropped {drop_count} rows with no pocket distance.")

        pred_df["in_pocket"] = pred_df["pocket_distance"] < distance_cutoff

        # halve the score if not in pocket
        pred_df[interaction_col] = pred_df.apply(
            lambda x: x[interaction_col] / 2
            if not x["in_pocket"]
            else x[interaction_col],
            axis=1,
        )

        # save
        new_dir.mkdir(exist_ok=True)
        pred_df.to_csv(new_dir / "predictions.csv", index=False)
        print(pred_df)


if __name__ == "__main__":
    run_main()
