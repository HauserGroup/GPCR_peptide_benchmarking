"""Create a batch fasta for colabfold"""

import argparse
import pathlib
import pandas as pd


def run_main():
    # load dataset and create fasta
    script_dir = pathlib.Path(__file__).parent.absolute()
    fasta_p = script_dir / "benchmark_batch.fasta"

    data_dir = script_dir.parent.parent.parent / "classifier_benchmark_data"
    df = data_dir / "output/6_interactions_with_decoys.csv"
    df = pd.read_csv(df)
    # only keep identifier, "GPCR Sequence", "Ligand Sequence"
    df = df[["Identifier", "GPCR Sequence", "Ligand Sequence"]]

    # create fasta
    with open(fasta_p, "w") as f:
        pass
    for i, row in df.iterrows():
        identifier = row["Identifier"]
        gpcr_seq = row["GPCR Sequence"]
        ligand_seq = row["Ligand Sequence"]
        with open(fasta_p, "a") as f:
            f.write(f">{identifier}\n")
            f.write(f"{gpcr_seq}:\n")
            f.write(f"{ligand_seq}\n")


if __name__ == "__main__":
    run_main()
