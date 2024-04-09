"""Get a list of PDBs of active structures before 2022-04-01."""

import pathlib
import datetime
import pandas as pd


def run_main(known_struct_p):
    df = pd.read_csv(known_struct_p)
    # drop if 'state' is not 'Active'
    df = df[df["state"] == "Active"]
    # drop if data => 2022-04-01notn
    df["publication_date"] = pd.to_datetime(df["publication_date"])
    df = df[df["publication_date"] < datetime.datetime(2022, 4, 1)]

    unique_pdbs = df["pdb_code"].unique()
    print(f"Number of unique active PDBs before 2022-04-01: {len(unique_pdbs)}")

    # format it as a string with comma separated
    unique_pdbs_str = ",".join(unique_pdbs)
    print(f'"{unique_pdbs_str}"')


if __name__ == "__main__":
    SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
    KNOWN_STRUCT_P = SCRIPT_DIR / "3f_known_structures.csv"
    run_main(KNOWN_STRUCT_P)
