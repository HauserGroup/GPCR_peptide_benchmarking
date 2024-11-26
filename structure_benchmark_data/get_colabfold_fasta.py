import pathlib
from Bio import SeqIO


def main(fasta_dir: pathlib.Path, out_p: pathlib.Path):
    # Ensure output path exists
    out_p.parent.mkdir(parents=True, exist_ok=True)

    with open(out_p, "w") as outfile:
        for fasta_file in fasta_dir.glob("*.fasta"):
            sequences = list(SeqIO.parse(fasta_file, "fasta"))
            if len(sequences) == 2:  # Ensure we have exactly two chains
                identifier_a = sequences[0].id
                identifier_a = identifier_a.replace("_receptor", "")
                sequence_a = str(sequences[0].seq)
                identifier_b = sequences[1].id
                sequence_b = str(sequences[1].seq)

                # Use the first identifier for the pair, followed by chain sequences
                outfile.write(f">{identifier_a}\n{sequence_a}:\n{sequence_b}\n")


if __name__ == "__main__":
    main(fasta_dir=pathlib.Path("structure_benchmark_data/fastas/pairs"),
         out_p=pathlib.Path("structure_benchmark_data/fastas/pairs_colabfold.fasta"))
