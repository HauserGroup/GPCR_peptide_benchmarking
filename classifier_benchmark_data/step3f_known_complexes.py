"""If AlphaFold2 has been trained on a receptor complex, then the complex is considered known.
Especially if the true complex with the (principal agonist) exists in the PDB.
This script looks for known complexes for the dataset.

Approach:
For a given GPCR:
    -> Get all structures from GPCRdb.
        Per structure:
            -> Get the PDB code (id)
            -> Get the publication date (to check if it was published before the AlphaFold2 model was trained)
            -> Check ligands
"""

import json
import argparse
import pathlib
import os
import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import numpy as np


def get_structures_for_gpcr_from_GPCRdb(gpcr_id):
    """
    gpcr_id: str
        The GPCRdb ID for the GPCR. For example, 'oprm_human'

    Returns: list of dicts for each structure, where one dict looks like:
        {'pdb_code': '8EF5',
        'protein': 'oprm_human',
        'class': 'Class A (Rhodopsin)',
        'family': '001_002_022_003',
        'species': 'Homo sapiens',
        'preferred_chain': 'R',
        'resolution': 3.3,
        'publication_date': '2022-11-09',
        'type': 'Electron microscopy',
        'state': 'Active',
        'distance': None,
        'publication': 'https://dx.doi.org/10.1016/J.CELL.2022.09.041',
        'ligands': [{'name': 'fentanyl', 'type': 'small-molecule', 'function': 'Agonist', 'PDB': '7V7', 'SMILES': 'CCC(=O)N(c1ccccc1)C1CCN(CC1)CCc1ccccc1'}],
        'signalling_protein': {'type': 'G protein', 'data': {'entity1': {'entry_name': 'gnai1_human', 'chain': 'A'}, 'entity2': {'entry_name': 'gbb1_rat', 'chain': 'B'}, 'entity3': {'entry_name': 'gbg2_bovin', 'chain': 'C'}}}
        },
    """
    # get a list of structures of a protein
    url = f"https://gpcrdb.org/services/structure/protein/{gpcr_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Ensure data is a list, even if the API returned a single dictionary
    if not isinstance(data, list):
        data = [data]

    return data


def create_csv_with_all_known_structs(interactions_df, out_csv_path):
    """
    interactions_df: df, with a 'Target GPCRdb ID' column that contains the GPCR ids,
                     such as 'oprm_human' or 'adrb1_human'
    out_csv_path: pathlib.Path, where to save the csv file with all known structures for the GPCRs
                  in the interactions_df
    """
    unique_gpcrs = interactions_df["Target GPCRdb ID"].unique()
    # check if the file exists
    if os.path.exists(out_csv_path):
        raise ValueError(f"The file {out_csv_path} already exists. Please remove it.")

    # create the file
    with open(out_csv_path, "w") as f:
        headers = [
            "Target GPCRdb ID",
            "pdb_code",
            "protein",
            "class",
            "family",
            "species",
            "preferred_chain",
            "resolution",
            "publication_date",
            "type",
            "state",
            "distance",
            "publication",
            "ligands",
            "signalling_protein",
        ]
        # write header
        f.write(",".join(headers) + "\n")

        # for each GPCR, get the structures and write them to the file
        for gpcr_index, gpcr in enumerate(unique_gpcrs):
            struct_data = get_structures_for_gpcr_from_GPCRdb(gpcr)
            # if the length of the struct_data is 0, then there are no known structures.
            # create a df with just the GPCRdb ID and write it to the file
            if len(struct_data) == 0:
                struct_df = pd.DataFrame({"Target GPCRdb ID": [gpcr]})
                struct_df.to_csv(f, index=False, header=False)
                continue
            # if structures are found
            else:
                struct_df = pd.DataFrame(struct_data)
                # add 'Target GPCRdb ID' column as the first column
                struct_df.insert(0, "Target GPCRdb ID", gpcr)
                # if headers are missing, set to None
                for header in headers:
                    if header not in struct_df.columns:
                        struct_df[header] = np.nan
                # fix ligands, signalling_protein columns. Ligands is a (list) of dicts, make it python loadable
                struct_df["ligands"] = struct_df["ligands"].apply(json.dumps)
                struct_df["signalling_protein"] = struct_df["signalling_protein"].apply(
                    json.dumps
                )
                # reorder columns
                struct_df = struct_df[headers]
                struct_df.to_csv(f, index=False, header=False)


def read_csv_with_all_known_structs_csv(csv_path):
    """ """
    df = pd.read_csv(csv_path)
    # make nan, NaN, None, etc. all the same
    df = df.where(pd.notna(df), np.nan)

    # for ligands, signalling_protein, convert back to list of dicts (if not None)
    for col in ["ligands", "signalling_protein"]:
        df[col] = df[col].apply(lambda x: json.loads(x) if not pd.isna(x) else x)

    df["publication_date"] = pd.to_datetime(df["publication_date"])

    return df


def summarize_structure_csv_per_GPCR(df, out_path, cutoff_datetime):
    """
    For each GPCR, summarize the structures known for it.

    Output df will contain:
        - GPCR id, for example 'oprm_human'
        - Has complex with peptide/protein before cutoff date, True/False
        - Has complex with peptide/protein, True/False
    """
    # get all unique GPCRdb IDs
    unique_gpcrs = df["Target GPCRdb ID"].unique()
    # create a df to store the summary
    summary_df = pd.DataFrame({"Target GPCRdb ID": unique_gpcrs})
    # add columns for the summary. Use shorter names for the columns
    summary_df["family"] = None
    summary_df["has_peptide_complex_before_cutoff"] = False
    summary_df["has_peptide_complex"] = False
    summary_df["Peptide complex PDBs before"] = (
        None  # list of tuples (pdb_code, publication_date)
    )
    summary_df["Peptide complex PDBs after"] = (
        None  # list of tuples (pdb_code, publication_date)
    )
    has_pep_ligand = lambda x: any(
        [ligand["type"] == "peptide" or ligand["type"] == "protein" for ligand in x]
    )

    # now iterate over the df and fill in the summary_df
    for gpcr_index, gpcr in enumerate(unique_gpcrs):
        summary_df.at[gpcr_index, "family"] = get_parent_family_for_gpcr(
            get_family_for_gpcr(gpcr)
        )

        gpcr_rows = df[df["Target GPCRdb ID"] == gpcr]
        # filter rows without any ligand (is np.nan)
        gpcr_rows = gpcr_rows[gpcr_rows["ligands"].notna()]

        # add 'has_peptide_complex' to gpcr_rows
        gpcr_rows["has_peptide_complex"] = gpcr_rows["ligands"].apply(has_pep_ligand)
        gpcr_rows = gpcr_rows[gpcr_rows["has_peptide_complex"]]
        # set has_peptide_complex to True if there are any rows with peptide ligands
        if len(gpcr_rows) > 0:
            summary_df.at[gpcr_index, "has_peptide_complex"] = True
            pdbs_before = gpcr_rows[gpcr_rows["publication_date"] < cutoff_datetime][
                "pdb_code"
            ].tolist()
            dates_before = gpcr_rows[gpcr_rows["publication_date"] < cutoff_datetime][
                "publication_date"
            ].tolist()
            dates_before = [d.strftime("%Y-%m-%d") for d in dates_before]
            if len(pdbs_before) > 0:
                summary_df.at[gpcr_index, "Peptide complex PDBs before"] = list(
                    zip(pdbs_before, dates_before)
                )

            pdbs_after = gpcr_rows[gpcr_rows["publication_date"] >= cutoff_datetime][
                "pdb_code"
            ].tolist()
            dates_after = gpcr_rows[gpcr_rows["publication_date"] >= cutoff_datetime][
                "publication_date"
            ].tolist()
            dates_after = [d.strftime("%Y-%m-%d") for d in dates_after]
            if len(pdbs_after) > 0:
                summary_df.at[gpcr_index, "Peptide complex PDBs after"] = list(
                    zip(pdbs_after, dates_after)
                )

            # set has_peptide_complex_before_cutoff to True if there are any rows with peptide ligands before the cutoff date
            if len(gpcr_rows[gpcr_rows["publication_date"] < cutoff_datetime]) > 0:
                summary_df.at[gpcr_index, "has_peptide_complex_before_cutoff"] = True

    # save the summary_df
    summary_df.to_csv(out_path, index=False)

def get_parent_family_for_gpcr(family_id):
    """
    family_id: str, for example '001_002_006_001'
    """
    url = f"https://gpcrdb.org/services/proteinfamily/{family_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # {'slug': '001_002_006_001', 'name': 'C3a receptor', 'parent': {'slug': '001_002_006', 'name': 'Complement peptide receptors'}}
    return data["parent"]["name"]


def get_family_for_gpcr(gpcr_id):
    """
    gpcr_id: str, for example 'oprm_human'
    """
    url = f"https://gpcrdb.org/services/protein/{gpcr_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["family"]


def plot_peptide_GPCR_complexes_per_receptor(df, save_path, show_only_useable=True):
    """
    Color by family.
    On the x-axis, plot the GPCRdb ID.
    On the y-axis, plot the number of peptide complexes (before and after the cutoff date).
    """
    # drop rows without any peptide complexes
    df = df[df["has_peptide_complex"]]

    # replace the "_human" in the GPCRdb ID with ""
    df["Target GPCRdb ID"] = df["Target GPCRdb ID"].apply(
        lambda x: x.replace("_human", "")
    )

    # drop gpcrs with complexes before the cutoff date
    if show_only_useable:
        df = df[~df["has_peptide_complex_before_cutoff"]]

    # sort df on family counts
    family_counts = df["family"].value_counts()
    family_counts = family_counts.sort_values(ascending=False)
    family_order = family_counts.index
    df["family"] = df["family"].astype("category")
    df["family"] = df["family"].cat.set_categories(family_order, ordered=True)

    # read the "Peptide complex PDBs before" ,"Peptide complex PDBs after" columns
    df["Peptide complex PDBs before"] = df["Peptide complex PDBs before"].apply(
        lambda x: eval(x) if not pd.isna(x) else []
    )
    df["Peptide complex PDBs after"] = df["Peptide complex PDBs after"].apply(
        lambda x: eval(x) if not pd.isna(x) else []
    )

    df["Complexes before"] = df["Peptide complex PDBs before"].apply(lambda x: len(x))
    df["Complexes after"] = df["Peptide complex PDBs after"].apply(lambda x: len(x))
    # sort on family, then on the number of complexes (after)
    df = df.sort_values(by=["family", "Complexes after"], ascending=[True, False])

    sns.set(style="ticks")
    plt.figure(figsize=(10, 5))
    # color xlabel background by family
    family_colors = sns.color_palette("tab10", n_colors=len(family_order))
    plt.xticks(rotation=90)
    plt.xlabel("GPCR family")
    plt.ylabel("Number of peptide complexes")
    cutoff_date = CUTOFF_DATE.strftime("%Y-%m-%d")

    # add background color for each family
    family_counts = df["family"].value_counts()
    counter = 0
    for family, color in zip(family_order, family_colors):
        family_count = family_counts[family]
        plt.axvspan(
            counter - 0.5, counter + family_count - 0.5, facecolor=color, alpha=0.3
        )
        counter += family_count

        # add the family name in the center of the span
        plt.text(
            counter - family_count / 2.5 - 0.5,
            max(df["Complexes before"].max(), df["Complexes after"].max()),
            family,
            ha="center",
            va="top",
            fontsize=8,
            rotation=90,
            color="black",
        )

    # plot the number of complexes before and after the cutoff date
    # stacked bar plot
    plt.bar(
        df["Target GPCRdb ID"],
        df["Complexes before"],
        label="Before",
        hatch="//",
        edgecolor="black",
        color="blue",
        width=0.5,
    )
    plt.bar(
        df["Target GPCRdb ID"],
        df["Complexes after"],
        bottom=df["Complexes before"],
        label="After",
        hatch="",
        color="green",
        edgecolor="black",
        width=0.5,
    )
    # color the xlabels based on "has_peptide_complex_before_cutoff"
    for xl, has_before in zip(
        plt.gca().get_xticklabels(), df["has_peptide_complex_before_cutoff"]
    ):
        if not has_before:
            # give bold name
            if not show_only_useable:
                xl.set_fontweight("bold")

    if not show_only_useable:
        plt.title(
            f"Experimentally determined peptide complexes per GPCR (before and after {cutoff_date})"
        )
    else:
        plt.title(
            f"Peptide complexes of GPCRs first modelled after {cutoff_date} (Neuralplexer training cutoff)."
        )

    # reduce the empty space on the x-axis, especially between the start of the x-axis and the first bar
    plt.tight_layout()
    plt.xlim(-0.5, len(df) - 0.5)
    if not show_only_useable:
        plt.legend()
    plt.savefig(save_path)
    plt.close()

    useful_pdbs = 0
    for fam in family_order:
        fam_rows = df[df["family"] == fam]
        # drop GPCRs with any complexes before the cutoff date
        fam_rows = fam_rows[~fam_rows["has_peptide_complex_before_cutoff"]]
        print(fam)
        useful_pdbs += fam_rows["Complexes after"].sum()
        for gpcr in fam_rows["Target GPCRdb ID"]:
            print(
                "\t",
                gpcr,
                "\t",
                fam_rows[fam_rows["Target GPCRdb ID"] == gpcr][
                    "Peptide complex PDBs after"
                ].values[0],
            )

    print("Total number of unseen GPCRs:", len(df))
    print("Total useful pdbs:", useful_pdbs)


if __name__ == "__main__":
    """
    """
    DF_PATH = pathlib.Path(
        "./classifier_benchmark_data/output/2_hormone_interactions.csv"
    )
    OUT_PATH = pathlib.Path(
        "./classifier_benchmark_data/output/3f_known_structures.csv"
    )
    # get all GPCRs from our df, get structure info for each GPCR, and save to a csv
    if not os.path.exists(OUT_PATH):
        create_csv_with_all_known_structs(
            interactions_df=pd.read_csv(DF_PATH), out_csv_path=OUT_PATH
        )

    # read test.csv
    DF = read_csv_with_all_known_structs_csv(OUT_PATH)
    # (the cutoff date for when the AlphaFold2 2.3 model was trained)
    CUTOFF_DATE = datetime.datetime(2021, 9, 30)

    # summarize the structures known for each GPCR
    SUMMARY_P = (
        OUT_PATH.parent
        / f"3f_known_structures_summary_{CUTOFF_DATE.strftime('%Y-%m-%d')}.csv"
    )
    if not os.path.exists(SUMMARY_P):
        summarize_structure_csv_per_GPCR(
            df=DF, out_path=SUMMARY_P, cutoff_datetime=CUTOFF_DATE
        )
