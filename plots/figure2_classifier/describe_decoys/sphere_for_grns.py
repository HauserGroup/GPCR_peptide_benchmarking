import pandas as pd
import numpy as np


def run_main():
    df_p = "~/Documents/GitHub/GPRC_peptide_benchmarking/classifier_benchmark_data/output/3d_generic_residues_binding_pocket_all.csv"
    df = pd.read_csv(df_p)
    generic_residues = {
        "6x44",
        "5x47",
        "6x38",
        "3x40",
        "5x51",
        "6x54",
        "1x32",
        "7x45",
        "6x47",
        "7x35",
        "7x38",
        "6x58",
        "1x36",
        "5x44",
        "3x36",
        "45x51",
        "7x42",
        "5x62",
        "7x41",
    }
    gpcr = "glr_human"
    # remove index col, use the first column as index
    df = df.set_index(df.columns[0])
    # get row where index is gpcr
    df = df.loc[gpcr]

    # for each generic residue, get the amino acid
    for g in generic_residues:
        if g in df.index:
            aa = df.loc[g]
            # if aa is nan
            if pd.isnull(aa):
                continue
            res_nr = aa[1::]
            print(f"#{g} {res_nr}, {aa}")
            sphere_command = f"show sphere, complex and chain B and resi {res_nr}"
            print(sphere_command)
            # color
            color_command = f"color custom_blue, complex and chain B and resi {res_nr}"
            print(color_command)


if __name__ == "__main__":
    run_main()
