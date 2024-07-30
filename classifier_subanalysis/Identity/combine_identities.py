""" """

import pathlib
import pandas as pd


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    base_dir = script_dir.parent.parent
    rfaa = base_dir / "structure_benchmark_data/mmseq2_rfaa_training_structures.csv"
    rfaa = pd.read_csv(rfaa)
    rfaa["model"] = "rfaa"
    af2 = base_dir / "structure_benchmark_data/mmseq2_af_training_structures.csv"
    af2 = pd.read_csv(af2)
    af2["model"] = "af2"

    #     pdb        e_value  Identity         gpcr
    # 0  7VV0   5.211000e-09     0.250  mrgx2_human
    # 1  8F7R  5.182000e-217     0.927   oprm_human

    new_cols = ["pdb", "e_value", "Identity", "gpcr", "model"]

    # combine the two dataframes into 1 with a new column 'model'
    combined = pd.concat([rfaa, af2], axis=0)
    combined.to_csv(script_dir / "identity.csv", index=False)


if __name__ == "__main__":
    run_main()
