"""Get the .txt with unseen GPCRs from the df"""

import pathlib
import pandas


def main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df_p = "classifier_benchmark_data/output/3f_known_structures_summary_2021-09-30.csv"
    df = pandas.read_csv(df_p)
    print(df)

    no_complex = df[df["has_peptide_complex"] == False]["Target GPCRdb ID"].tolist()
    out_p = script_dir / "gpcrs_no_complex.txt"
    with open(out_p, "w") as out_f:
        out_f.write("\n".join(no_complex))

    # 'Peptide complex PDBs before' should be nan
    out_p = script_dir / "gpcrs_no_complex_before_2021-09-30.txt"
    no_complex_before = df[df["Peptide complex PDBs before"].isna()][
        "Target GPCRdb ID"
    ].tolist()
    with open(out_p, "w") as out_f:
        out_f.write("\n".join(no_complex_before))


if __name__ == "__main__":
    main()
