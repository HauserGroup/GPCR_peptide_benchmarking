"""
Use oprm_human as displayed structure
https://gpcrdb.org/structure/refined/6PT3

"""
import os
import pathlib

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt


def amino_acid_colors_and_groups():
    """
    """

    # polar -> blue
    polar = ["S", "T", "Y", "N", "Q"]
    polar_colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(polar)))

    # non polar -> yellow
    non_polar = ["G", "A", "V", "C", "P", "L", "I", "M", "W", "F"]
    # get a color range for non_polar
    non_polar_colors = plt.cm.YlOrBr(np.linspace(0.2, 0.7, len(non_polar)))

    # pos -> green
    pos_charge = ["K", "R", "H"]
    pos_charge_colors = plt.cm.Greens(np.linspace(0.6, 0.8, len(pos_charge)))

    # neg -> red
    neg_charge = ["D", "E"]
    neg_charge_colors = plt.cm.Reds(np.linspace(0.6, 0.8, len(neg_charge)))


    color_dict = {}
    for i, aa in enumerate(polar):
        color_dict[aa] = polar_colors[i]
    for i, aa in enumerate(non_polar):
        color_dict[aa] = non_polar_colors[i]
    for i, aa in enumerate(pos_charge):
        color_dict[aa] = pos_charge_colors[i]
    for i, aa in enumerate(neg_charge):
        color_dict[aa] = neg_charge_colors[i]
    color_dict["NaN"] = plt.cm.Greys(0.5)

    # group dict
    group_dict = {}
    group_dict["polar"] = polar
    group_dict["non_polar"] = non_polar
    group_dict["pos_charge"] = pos_charge
    group_dict["neg_charge"] = neg_charge

    return color_dict, group_dict


def create_pie_chart(amino_acid_counts, out_path, title,
                     legend=False):
    """
    amino_acid_counts: dict
        {"A": 20,
        "R": 10,
        ...
        }
    """
    aa_colors, aa_groups = amino_acid_colors_and_groups()

    # create the pie chart
    fig, ax = plt.subplots(figsize=(10, 10))

    aa_color_order = aa_colors.keys()
    # sort amino_acid_counts by aa_color_order
    amino_acid_counts = {k:amino_acid_counts[k] for k in aa_color_order}

    print(title, amino_acid_counts)


    # get the labels and counts
    labels = []
    counts = []
    colors = []
    for aa, count in amino_acid_counts.items():
        if count == 0:
            continue
        labels.append(aa)
        counts.append(count)
        colors.append(aa_colors[aa])
    
    # create the pie chart
    ax.pie(counts, labels=labels, colors=colors, startangle=90,
           # place thet label inside and in the middle
              textprops={'fontsize': 18},
                pctdistance=0.85,
                # place label inside the pie chart

                labeldistance=1.05,
                wedgeprops=dict(width=0.5, edgecolor='w'),
                )
    ax.set_title(title, fontsize=30)

    if legend is True:
        # above the legend, add the total
        total = sum(counts)
        # move the legend outside the pie chart (left)
        ax.legend(labels, loc='center left', bbox_to_anchor=(-0.15, 0.75), fontsize=14,
                    title=f"Amino acids\n n={total}", title_fontsize=14)

    # set background transparent
    fig.patch.set_alpha(0.0)

    # save the pie chart
    fig.savefig(out_path)


if __name__ == "__main__":
    """
    """
    OUT_DIR = "/Users/kcd635/Documents/GitHub/Interspecies_GPCR_pipeline/classifier_benchmark_data/output/3e_GR_plots"
    OUT_DIR = pathlib.Path(OUT_DIR)
    # save create
    if not OUT_DIR.exists():
        os.mkdir(OUT_DIR)
    
    # read in the generic residue data
    GENERIC_RESIDUES_PATH = pathlib.Path("/Users/kcd635/Documents/GitHub/Interspecies_GPCR_pipeline/test.csv")
    GENERIC_RESIDUES_DF = pd.read_csv(GENERIC_RESIDUES_PATH)

    # generic res IDs
    generic_residues_to_save = ["7x34", "7x38", "3x32", "3x33", "45x52", "45x51"]
    aa_colors, aa_groups = amino_acid_colors_and_groups()

    # get the amino acid counts for each generic residue
    for res_id in generic_residues_to_save:
        out_path = OUT_DIR / f"{res_id}.png"
        # get the amino acid counts for this residue
        amino_acids = GENERIC_RESIDUES_DF[res_id].tolist()

        amino_acid_counts = {a:0 for a in aa_colors.keys()}
        amino_acid_counts["NaN"] = 0

        for aa in amino_acids:
            if pd.isna(aa):
                amino_acid_counts["NaN"] += 1
            else:
                amino_acid_counts[aa[0]] += 1
            
        # create the pie chart
        create_pie_chart(amino_acid_counts, out_path, res_id)
