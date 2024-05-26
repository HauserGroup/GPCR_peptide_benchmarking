import pathlib
import os
import pandas as pd


def run_main():
    script_dir = pathlib.Path(__file__).parent
    models_dir = script_dir / "models"
    models = [x for x in models_dir.iterdir() if x.is_dir()]
    model_names = [x.name for x in models]
    model_names = [x.replace("fold_", "") for x in model_names]
    model_names = [x.replace("human_", "human___") for x in model_names]

    # get the ground truth
    truth_p = script_dir / "1on1.csv"
    truth_df = pd.read_csv(truth_p)
    # identifiers
    identifiers = truth_df["Identifier"].unique()

    # check missing identifiers (identifiers - model_names)
    missing = set(identifiers) - set(model_names)

    # print(missing)
    missing_df_cols = ["pdb", "receptor_pdb_seq", "ligand_pdb_seq"]
    missing_df = pd.DataFrame(columns=missing_df_cols)

    for m in missing:
        # get the row
        row = truth_df[truth_df["Identifier"] == m]

        receptor_seq = row["GPCR Sequence"].values[0]
        ligand_seq = row["Ligand Sequence"].values[0]

        out_row = {
            "pdb": m,
            "receptor_pdb_seq": receptor_seq,
            "ligand_pdb_seq": ligand_seq,
        }
        missing_df = pd.concat([missing_df, pd.DataFrame([out_row])])

    missing_df.to_csv(script_dir / "missing.csv", index=False)


if __name__ == "__main__":
    run_main()
