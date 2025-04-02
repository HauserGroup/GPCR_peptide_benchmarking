""" Plot a timeline, including the training cutoff dates of all structural models.

"""

import logging
import pathlib
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import json


def save(save_p):
    plt.savefig(save_p.with_suffix(".svg"))
    plt.savefig(save_p.with_suffix(".png"), dpi=600)
    plt.close()


def plot_structure_discovery(df, cutoff_datetime, save_path):
    """On x-axis plot the month of the year.
    On the y-axis the number of structures discovered.
    """
    min_date = df["publication_date"].min()
    max_date = df["publication_date"].max()
    # months between (x-axis)
    months = pd.date_range(start=min_date, end=max_date, freq="M")

    # count the number of structures per month
    structure_classes = df["class"].unique()
    structure_classes = [s for s in structure_classes if not pd.isna(s)]

    counts_per_class = {structure_class: [] for structure_class in structure_classes}
    for month in months:
        for structure_class in structure_classes:
            count = df[
                (df["publication_date"] < month) & (df["class"] == structure_class)
            ].shape[0]
            counts_per_class[structure_class].append(count)

    # plot
    plt.figure(figsize=(6, 3))
    # plot total
    # plt.plot(
    #     months,
    #     [df[df["publication_date"] < month].shape[0] for month in months],
    #     label="Total",
    # )
    # # plot for each class
    # for structure_class in structure_classes:
    #     plt.plot(months, counts_per_class[structure_class], label=structure_class)

    # sns plot total
    sns.set_style("whitegrid")
    # # set blue red color scheme
    # # "ESMFold": "#478347",
    # # "RF-AA": "#A676D6",
    # # "AF2": "#115185",
    # # "AF3": "#061f4a",
    colors = ["#0b3d91", "#478347", "#A676D6", "#115185", "#061f4a"]
    line_width = 2

    sns.lineplot(
        x=months,
        y=[df[df["publication_date"] < month].shape[0] for month in months],
        label="Total",
        color=colors[0],
        linewidth=line_width,
        # add dots
        marker=".",
    )
    # plot for each class
    for structure_class in structure_classes:
        sns.lineplot(
            x=months,
            y=counts_per_class[structure_class],
            label=structure_class,
            color=colors[structure_classes.index(structure_class) + 1],
            linewidth=line_width,
            # add dots
            marker=".",
        )


    add_training_cutoff_dates(ymax=df.shape[0],
                              fontsize=12)
    fontsize = 12 
    # plt.xlabel("Date")
    plt.xlabel("")
    plt.ylabel("Total structures discovered", fontsize=fontsize)
    plt.title("Number of GPCR structures discovered per month", fontsize=fontsize,
              # align left
                loc="left")
    plt.legend(fontsize=fontsize, loc="upper left",
               # add border
                frameon=True)

    # set font size to 12
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.tight_layout()
    save(save_path)


def add_training_cutoff_dates(ymax, fontsize=12):
    # AF2: We have fine-tuned new AlphaFold-Multimer weights using identical model architecture but a new training cutoff of 2021-09-30.
    # NeuralPlexer (v2): The datasets used for training and testing end-to-end structure prediction were constructed from chains of all monomeric proteins and homomeric complexes in the PDB accessed in April 2022.
    # RF-AA: Similar to RF2 [11], we train on protein monomer and protein complexes structures deposited into the PDB before April 30, 2020.
    ymax = ymax * 0.90
    fontdict={"size": fontsize,
              "rotation": 270,
              "verticalalignment" : "top",
              "horizontalalignment" : "left",
    }

    plt.axvline(
        datetime.datetime(2021, 9, 30),
        color="black",
        linestyle="--",
        # label="AlphaFold2 2.3 model training cutoff",
    )
    # instead of labelling, add short name of the model
    plt.text(
        datetime.datetime(2021, 9, 30),
        ymax,
        "AF2 + AF3",
        color="black",
        fontdict = fontdict,
    )

    plt.axvline(
        datetime.datetime(2020, 4, 30),
        # grey
        color="gray",
        # opacity
        alpha=0.5,
        linestyle="--",
        # label="RF-AA training cutoff",
    )
    plt.text(
        datetime.datetime(2020, 4, 30),
        ymax,
        "RF-AA",
        color="gray",
        fontdict=fontdict,

    )

    plt.axvline(
        datetime.datetime(2019, 1, 1),
        color="gray",
        linestyle="--",
        alpha=0.5,
        # label="NeuralPlexer training cutoff",
    )
    plt.text(
        datetime.datetime(2019, 1, 1),
        ymax,
        "NeuralPlexer",
        color="gray",
        fontdict=fontdict,
    )


def get_status_of_unique_GPCRs(df, month):
    """
    return 3 lists, 
    1. GPCRs without any known structures
    2. GPCRs with known structures, that are complexes
    3. GPCRs with known structures, that are peptide/protein complexes

    """
    # get unique GPCRs
    unique_gpcrs = df["Target GPCRdb ID"].unique()

    without_structures = list()
    with_complexes = list()
    with_peptide_complex = list()


    for gpcr in unique_gpcrs:
        # check if there are any structures for this GPCR, before the month
        gpcr_df = df[df["Target GPCRdb ID"] == gpcr]
        gpcr_df = gpcr_df[gpcr_df["publication_date"] < month]
        # if there are none, add to the list
        if gpcr_df.shape[0] == 0:
            without_structures.append(gpcr)
            continue

        # check if they have a complex
        for i, row in gpcr_df.iterrows():
            ligands = row["ligands"]
            if len(ligands) > 0:
                with_complexes.append(gpcr)
                break

        # for the existing structures, check if they are complexes
        for i, row in gpcr_df.iterrows():
            # check if type is peptide
            if any([ligand["type"] == "peptide" for ligand in row["ligands"]]):
                with_peptide_complex.append(gpcr)
                break

    return without_structures, with_complexes, with_peptide_complex


def plot_gpcr_status_per_month(df, cutoff_datetime, save_path):
    """On x-axis plot the month of the year.
    On the y-axis the number of GPCRs with known structures.

    Based on ligands:
    Look for GPCR structures without known complexes.
    Look for GPCRs with known structures, that are complexes.
    """
    min_date = df["publication_date"].min()
    max_date = df["publication_date"].max()
    # months between (x-axis)
    months = pd.date_range(start=min_date, end=max_date, freq="M")

    # count the number of structures per month
    without_structures = []
    with_complexes = []
    with_peptide_complex = []
    without_peptide_complex = []

    for month in months:
        without_struct, with_complex, with_peptide = get_status_of_unique_GPCRs(df, month)
        without_structures.append(len(without_struct))
        with_complexes.append(len(with_complex))
        with_peptide_complex.append(len(with_peptide))
        without_peptide_complex.append(len(without_struct) - len(with_peptide))

    print(with_peptide_complex[-1])

    # plot
    plt.figure(figsize=(5, 3))
    # plt.plot(months, without_structures, label="Without resolved complex")
    # plt.plot(months, with_complexes, label="With any complex")
    plt.plot(months, with_peptide_complex, label="With resolved\npeptide complex")
    # plt.plot(months, without_peptide_complex, label="Without resolved complex (peptide)")

    add_training_cutoff_dates(ymax=df["Target GPCRdb ID"].nunique())

    # add dataset size of the y-axis
    plt.ylim(0, df["Target GPCRdb ID"].nunique() + 1)
    # add yticks in steps of 31
    plt.yticks(range(0, df["Target GPCRdb ID"].nunique() + 1, 31))

    plt.xlim(min_date, max_date)
    # plt.xlabel("Date")
    plt.xlabel("")
    # add xticks every 12 months
    plt.xticks(months[::12], [month.strftime("%Y") for month in months[::12]], rotation=45)
    plt.ylabel("Number of GPCRs")
    plt.title("Structurally resolved status of peptide GPCRs")
    
    # place the cutoff labels next to the lines
    plt.legend()
    plt.tight_layout()
    save(save_path)


def run_main():
    script_dir = pathlib.Path(__file__).resolve().parent
    main_dir = script_dir.parent.parent
    cutoff_datetime = datetime.datetime(2021, 9, 30)

    structure_dir = main_dir / "classifier_benchmark_data/output"
    known_structs = structure_dir / "3f_known_structures.csv"
    known_df = pd.read_csv(known_structs)
    known_df["publication_date"] = pd.to_datetime(known_df["publication_date"])
    for i, row in known_df.iterrows():
        # if not nan
        if not pd.isna(row["ligands"]):
            known_df.at[i, "ligands"] = json.loads(row["ligands"])
        else:
            known_df.at[i, "ligands"] = []

        if not pd.isna(row["signalling_protein"]):
            known_df.at[i, "signalling_protein"] = json.loads(row["signalling_protein"])
        else:
            known_df.at[i, "signalling_protein"] = []

    disc_plot_p = script_dir / "plot_structure_discovery.svg"
    # plot the number of structures discovered per month
    plot_structure_discovery(df=known_df, cutoff_datetime=cutoff_datetime, 
                             save_path=disc_plot_p)
    
    # plot the number of GPCRs with known structures per month
    status_plot_p = script_dir / "plot_gpcr_status_per_month.png"
    plot_gpcr_status_per_month(
        df=known_df, cutoff_datetime=cutoff_datetime, save_path=status_plot_p
    )

    # summary_structs = main_dir / "classifier_benchmark_data/output/3f_known_structures_summary_2021-09-30.csv"
    # summary_df = pd.read_csv(summary_structs)
    # print(summary_df.columns)
    # summary_df["publication_date"] = pd.to_datetime(summary_df["publication_date"])



if __name__ == "__main__":
    run_main()
