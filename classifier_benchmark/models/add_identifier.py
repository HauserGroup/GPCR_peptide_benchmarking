"""Quickly add identifier column"""

import pathlib
import os
import pandas as pd

if __name__ == "__main__":
    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    IDENTIFIER_COL = "identifier"
    PREDICTION_COL = "InteractionProbability"

    PRED_COL_DICT = {"ESM2": "mlm_loss"}

    for SUB_DIR in ["DSCRIPT2_TTV1", "ESM2"]:
        print(f"Processing {SUB_DIR}")
        DF_P = SCRIPT_DIR / SUB_DIR / "predictions.csv"
        DF = pd.read_csv(DF_P)
        # check if identifier column already exists
        if "identifier" in DF.columns:
            print("Identifier column already exists")
        else:
            # combine Target ID and Decoy ID with "___" separator
            DF["identifier"] = (
                DF["Target ID"].astype(str) + "___" + DF["Decoy ID"].astype(str)
            )
            DF.to_csv(DF_P, index=False)
        # check if prediction column exists
        if PREDICTION_COL not in DF.columns:
            print("Prediction column not found")
            # use the dictionary to get the correct prediction column
            DF[PREDICTION_COL] = DF[PRED_COL_DICT[SUB_DIR]]
            DF.to_csv(DF_P, index=False)
        else:
            print("Prediction column found")
