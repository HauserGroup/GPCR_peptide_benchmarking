""" """

import pathlib
import pandas
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


def get_GPCR_to_GPCR_similarity_percent(
    sim_df: pandas.DataFrame, source_gpcr: str, target_gpcr: str
):
    """
    sim_df: pandas.DataFrame, the GPCR to GPCR similarity matrix
    source_gpcr: str, for example 'oprm_human'
    target_gpcr: str, for example 'oprd_human'

    returns: numpy.float64, the similarity between the two GPCRs
    """
    # get the similarity
    sim = sim_df.loc[source_gpcr, target_gpcr]
    return sim


def get_similarity_between_multispecific_hormones(inter_df, sim_df):
    """For all hormones that bind multiple GPCRs, get the similarity of the GPCR binding pockets.
    This gives us a sense of how similar the binding pockets are for hormones that bind multiple GPCRs.

    inter_df: pandas.DataFrame, the interactions of all hormones (~460)
    sim_df: pandas.DataFrame, the GPCR to GPCR similarity matrix
    returns: dict, {hormone : [similarity, similarity, ...]}
    """
    # define the empty out dict. Will be {hormone : [similarity, similarity, ...]}
    out_dict = dict()

    # get all hormones that bind multiple GPCRs
    multi_gpcr_hormones = inter_df["Ligand ID"].value_counts()
    multi_gpcr_hormones = multi_gpcr_hormones[multi_gpcr_hormones > 1].index
    print(f"Number of hormones that bind multiple GPCRs: {len(multi_gpcr_hormones)}")

    # {1004: ['ednrb_human', 'ednra_human'], 3649: ['ccr10_human', 'ccr3_human'], ...}
    hormone_to_gpcr = dict()
    for hormone in multi_gpcr_hormones:
        gpcrs = inter_df[inter_df["Ligand ID"] == hormone]["Target GPCRdb ID"].values
        hormone_to_gpcr[hormone] = gpcrs

    # for the hormones that bind multiple GPCRs, get the similarity of the two binding pockets
    for hormone, targeted_gpcrs in hormone_to_gpcr.items():
        # get the target_gpcrs pairwise similarity
        targeted_pair_df = pandas.DataFrame(
            index=targeted_gpcrs, columns=targeted_gpcrs
        )
        # fill df with get_GPCR_to_GPCR_similarity_percent
        targeted_pair_df = get_GPCR_to_GPCR_similarity_percent(
            sim_df, targeted_pair_df.index, targeted_pair_df.columns
        )

        # keep only the upper triangle
        targeted_pair_df = targeted_pair_df.where(
            np.triu(np.ones(targeted_pair_df.shape)).astype(np.bool_)
        )
        # set diagonal to nan
        np.fill_diagonal(targeted_pair_df.values, np.nan)
        # set the out_dict
        vals = targeted_pair_df.values.flatten()
        out_dict[hormone] = vals[~np.isnan(vals)]

    return out_dict


def rgb_to_hex(rgb):
    """
    rgb, str, "rgb(0,142,215)"
    """
    rgb = rgb.replace("rgb(", "").replace(")", "")
    rgb = [int(x) for x in rgb.split(",")]
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])


def get_similarity_between_nonbinding_hormones(inter_df, sim_df):
    """For all hormones, get the similarity of the GPCR binding pockets of GPCRs it DOES NOT bind.
    This gives us a sense of how similar the binding pockets are for hormones that bind different GPCRs.

    inter_df: pandas.DataFrame, the interactions of all hormones (~460)
    sim_df: pandas.DataFrame, the GPCR to GPCR similarity matrix
    returns: dict, {hormone : [similarity, similarity, ...]}
    """
    # define the empty out dict. Will be {hormone : [similarity, similarity, ...]}
    out_dict = dict()

    # get all hormones that bind multiple GPCRs
    all_hormones = inter_df["Ligand ID"].unique()
    all_gpcrs = inter_df["Target GPCRdb ID"].unique()

    for hormone in all_hormones:
        hormone_rows = inter_df[inter_df["Ligand ID"] == hormone]
        # get the GPCRs that are targeted
        gpcrs_targeted = hormone_rows["Target GPCRdb ID"].values
        # get the GPCRs that are not targeted
        gpcrs_not_targeted = list(set(all_gpcrs) - set(gpcrs_targeted))

        # now, get the similarity between the targeted and non-targeted GPCRs
        pairwise_df = pandas.DataFrame(index=gpcrs_targeted, columns=gpcrs_not_targeted)
        pairwise_df = get_GPCR_to_GPCR_similarity_percent(
            sim_df, pairwise_df.index, pairwise_df.columns
        )
        # fill the diagonal with nan
        np.fill_diagonal(pairwise_df.values, np.nan)
        # set the out_dict, add everything except nan
        vals = pairwise_df.values.flatten()
        out_dict[hormone] = vals[~np.isnan(vals)]
    return out_dict


def violin_plot(binder_dict, non_binder_dict, save_path):
    """
    binder_dict: dict, {hormone : [similarity, similarity, ...]}
    non_binder_dict, dict, {hormone : [similarity, similarity, ...]}
    save_path: pathlib.Path, where to save the plot
    """
    # turn data_dict into a flat list
    non_binder_data = list()
    # extend
    for similarities in non_binder_dict.values():
        non_binder_data.extend(similarities)
    non_binder_data = np.array(non_binder_data)

    # turn data_dict into a flat list
    binder_data = list()
    # extend
    for similarities in binder_dict.values():
        binder_data.extend(similarities)
    binder_data = np.array(binder_data)

    # set scientific style
    plt.rcParams["axes.formatter.useoffset"] = True
    sns.set_context("talk")
    sns.set_style("white")
    # set font to helvetica
    plt.rcParams["font.family"] = "Helvetica"
    plt.rcParams["font.sans-serif"] = "Helvetica"

    plt.figure(figsize=(5, 6))

    # plot the violin plot
    sns.violinplot(
        data=[binder_data],
        palette=[rgb_to_hex("rgb(0,142,215)")],
        linewidth=2,
        inner=None,
    )
    # add swarm
    # downsample the data for non_binder_data
    sns.swarmplot(
        data=[binder_data],
        color="black",
        size=4,
        alpha=0.5,
        # every 5
        dodge=False,
    )
    plt.ylabel("Binding pocket similarity (%)", fontdict={"fontsize": 20})

    plt.xlabel(
        f"n={len(binder_data)}",
        fontdict={"fontsize": 20},
    )
    plt.xticks([0], [""])
    # yticks every 10
    plt.yticks(np.arange(0, 110, 10))
    # add a horizontal line at 30
    plt.axhline(y=30, color="black", linestyle="--")

    # calculate the percentage of values below 30
    below_30 = np.sum(binder_data < 30) / len(binder_data) * 100
    above_30 = 100 - below_30
    # show the below 30% percentage
    plt.text(0.04, 5, f"< 30% similarity:\n{round(below_30, 2)}%", fontsize=15)

    below_30 = round(below_30, 1)
    above_30 = round(above_30, 1)
    title = "Binding pocket similarity among\nGPCRs sharing a ligand"
    # title = f"2.1% of Peptide-GPCR Interactions at < 30% GPCR Similarity"
    plt.title(
        title,
        fontsize=22,
    )

    plt.xticks(fontsize=20)
    # yticks every 20
    plt.yticks(np.arange(0, 110, 20), fontsize=20)
    plt.tight_layout()

    # save the plot
    plt.savefig(save_path, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    DECOY_P = "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    DECOY_P = pathlib.Path(DECOY_P)
    DECOY_DF = pandas.read_csv(DECOY_P)
    # Index(['Target ID', 'Decoy ID', 'Acts as agonist', 'Decoy Type', 'Decoy Rank', 'Original Target', 'Target Similarity to Original Target', 'Ligand Sequence', 'GPCR Sequence'],

    INTER_P = "classifier_benchmark_data/output/4_principal_agonists_interactions.csv"
    INTER_P = pathlib.Path(INTER_P)
    INTER_DF = pandas.read_csv(INTER_P)
    # Index(['Target ID', 'Ligand ID', 'Target Type', 'Ligand Type', 'Target GPCRdb ID', 'Target UniProt ID', 'Ligand Species', 'Ligand Sequence', 'Target Name', 'Ligand Name', 'GPCR Sequence', 'GPCR Class', 'GPCR Family', 'GPCR Subfamily', 'GPCR Sub-subfamily'],

    # Sim DF
    SIM_P = "classifier_benchmark_data/output/3c_similarity_matrix_binding_pocket.csv"
    SIM_P = pathlib.Path(SIM_P)
    SIM_DF = pandas.read_csv(SIM_P, index_col=0)

    # get the similarity between multispecific hormones
    MULTI_SPECIFIC_SIMILARITY = get_similarity_between_multispecific_hormones(
        INTER_DF, SIM_DF
    )
    # get the similarity between non-binding hormones
    NON_BINDING_SIMILARITY = get_similarity_between_nonbinding_hormones(
        INTER_DF, SIM_DF
    )

    OUT_P = "plots/figure1_abstract/violin.svg"
    OUT_P = pathlib.Path(OUT_P)
    violin_plot(MULTI_SPECIFIC_SIMILARITY, NON_BINDING_SIMILARITY, OUT_P)
    print(f"Saved violin plot to {OUT_P}")
