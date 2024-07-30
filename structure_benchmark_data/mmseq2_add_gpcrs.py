"""Short script to add gpcrs to mmseq2 identity data."""

import pathlib
import pandas
import requests


def run_main():
    ""
    script_dir = pathlib.Path(__file__).parent.absolute()
    known_structs = script_dir / "3f_known_structures.csv"
    known_structs = pandas.read_csv(known_structs)
    # make dict with 'pdb_code' -> 'protein'
    pdb_to_protein = dict(zip(known_structs["pdb_code"], known_structs["protein"]))

    af2_p = script_dir / "mmseq2_af_training_structures.csv"
    af2 = pandas.read_csv(af2_p)
    if "gpcr" in af2.columns:
        print("GPCRs already added.")
        return
    else:
        af2["gpcr"] = af2["pdb"].map(pdb_to_protein)
        af2.to_csv(af2_p, index=False)

    rfaa_p = script_dir / "mmseq2_rfaa_training_structures.csv"
    rfaa = pandas.read_csv(rfaa_p)
    if "gpcr" in rfaa.columns:
        print("GPCRs already added.")
        return
    else:
        rfaa["gpcr"] = rfaa["pdb"].map(pdb_to_protein)
        rfaa.to_csv(rfaa_p, index=False)


if __name__ == "__main__":
    run_main()
