"""
Plot a small heatmap with the correlation characteristics of the peptides.

For the columns:
- Peptide length
- Peptide MSA depth
- Peptide selectivity
- Activity (pKi)

For the rows:
= all models

For the values:
Spearman rank correlation of peptide rank and the respective column value.
"""

import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import pathlib
import matplotlib.pyplot as plt

# spearman rank correlation
from scipy.stats import spearmanr


def load_classifier_df():
    """
       Decoy Type  Decoy Rank Original Target  ...    Target ID Decoy ID Acts as agonist
    0  Dissimilar         3.0      mtlr_human  ...  ackr1_human     1458           False
    1  Dissimilar         4.0     nmur2_human  ...  ackr1_human     1470           False
    2  Dissimilar         0.0     ednra_human  ...  ackr1_human      989           False
    3  Dissimilar         1.0      xcr1_human  ...  ackr1_human     3647           False
    4  Dissimilar         2.0      ntr1_human  ...  ackr1_human     1579           False
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    classifier_df_path = (
        script_dir.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )

    classifier_df = pd.read_csv(classifier_df_path)
    return classifier_df


def load_rankings():
    """
                    Model         GPCR  AgonistRank  unseen                class
    0  AF2 (no templates)  ednrb_human            1   False  Class A (Rhodopsin)
    1  AF2 (no templates)  ednra_human            1    True  Class A (Rhodopsin)
    2  AF2 (no templates)   ccr5_human            1   False  Class A (Rhodopsin)
    3  AF2 (no templates)   v1ar_human            1    True  Class A (Rhodopsin)
    4  AF2 (no templates)  galr2_human            1    True  Class A (Rhodopsin)
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings_path = os.path.join(script_dir, "agonist_rankings.csv")
    rankings = pd.read_csv(rankings_path)
    return rankings


def get_len_and_msa():
    """
              identifier  msa_dim0  msa_dim1  num_templates  num_alignments chain_lengths msa_seq_lengths
    0  cckar_human___864      2065       436              1            2065     1:428|2:8     1:1248|2:18
    1  ghsr_human___2156      2121       374              1            2121     1:366|2:8     1:1653|2:73
    2  ednrb_human___613      2082       452              1            2082    1:442|2:10     1:1767|2:34
    3  ssr1_human___5654      2048       404              1            2048    1:391|2:13      1:1962|2:1
    4  ntr2_human___1099      2150       438              1            2150    1:410|2:28    1:1054|2:160
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    # classifier_subanalysis/seq_and_msa/combined.csv
    seq_and_msa_path = script_dir / "seq_and_msa/combined.csv"
    seq_and_msa = pd.read_csv(seq_and_msa_path)
    seq_and_msa["gpcr"] = seq_and_msa["identifier"].str.split("___").str[0]
    seq_and_msa["decoy"] = seq_and_msa["identifier"].str.split("___").str[1]

    return seq_and_msa


def get_selectivity_df():
    """
         Ligand ID  number of targets
    0          573                  3
    1          574                  1
    2          582                  1
    3          585                  2
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    # classifier_subanalysis/get_selectivity/selectivity_targets_per_ligand.csv
    selectivity_path = script_dir / "get_selectivity/selectivity_targets_per_ligand.csv"
    selectivity_df = pd.read_csv(selectivity_path)
    return selectivity_df


def get_pki_df():
    """
                 identifier  mean_activity                class
    0     ackr1_human___758            NaN  Class A (Rhodopsin)
    1     ackr2_human___758            NaN  Class A (Rhodopsin)
    2    ackr3_human___4358            NaN  Class A (Rhodopsin)
    3     ackr4_human___810       8.400000  Class A (Rhodopsin)
    4    acthr_human___3633            NaN  Class A (Rhodop
    """
    script_dir = pathlib.Path(__file__).parent.absolute()
    # classifier_subanalysis/get_activity/pKi.csv
    pki_path = script_dir / "get_activity/pKi.csv"
    pki_df = pd.read_csv(pki_path)

    # add gpcr
    pki_df["gpcr"] = pki_df["identifier"].str.split("___").str[0]
    # assert unique
    assert len(pki_df["gpcr"].unique()) == len(pki_df)

    return pki_df


def get_msa_depth_from_seq_lengths(s: str, peptide_chain: int):
    "s = '1:1248|2:18'  chain = 2  --> 18"
    lengths = s.split("|")
    s = lengths[peptide_chain - 1]
    return int(s.split(":")[1])


def get_attributes():
    """ """
    attributes = [
        "agonist",
        "agonist length",
        "agonist selectivity",
        "pKi",
        "agonist MSA depth",
    ]

    # only keep agonists
    classifier_df = load_classifier_df()
    classifier_df = classifier_df[classifier_df["Acts as agonist"]]

    # load attribute dfs
    rankings = load_rankings()
    seq_and_msa = get_len_and_msa()
    selectivity = get_selectivity_df()
    pki = get_pki_df()

    gpcrs = classifier_df["Original Target"].unique()
    correlation_df = pd.DataFrame(index=gpcrs, columns=attributes)
    for gpcr in gpcrs:
        # get agonist
        agonist = classifier_df[classifier_df["Original Target"] == gpcr]
        assert len(agonist) == 1
        agonist_id = agonist["Decoy ID"].values[0]
        correlation_df.loc[gpcr, "agonist"] = agonist_id

        # get agonist length
        agonist_len = len(seq_and_msa[seq_and_msa["decoy"] == str(agonist_id)])
        correlation_df.loc[gpcr, "agonist length"] = agonist_len

        # get msa depth
        peptide_chain = 2
        msa_rows = seq_and_msa[seq_and_msa["identifier"] == f"{gpcr}___{agonist_id}"]
        msa_seq_lengths = msa_rows["msa_seq_lengths"].values
        assert len(msa_seq_lengths) == 1
        msa_seq_lengths = msa_seq_lengths[0]
        msa_depth = get_msa_depth_from_seq_lengths(msa_seq_lengths, peptide_chain)
        correlation_df.loc[gpcr, "agonist MSA depth"] = msa_depth

        # get selectivity
        selectivity_val = selectivity[selectivity["Ligand ID"] == agonist_id]
        assert len(selectivity_val) == 1
        selectivity_val = selectivity_val["number of targets"].values[0]
        correlation_df.loc[gpcr, "agonist selectivity"] = selectivity_val

        # get activity
        pki_val = pki[pki["gpcr"] == gpcr]
        assert len(pki_val) == 1
        pki_val = pki_val["mean_activity"].values[0]
        correlation_df.loc[gpcr, "pKi"] = pki_val

    return correlation_df


def create_correlation_df(attributes, rankings):
    """
    attributes:
                    agonist agonist length agonist selectivity       pKi
    ackr1_human     758             36                   7       NaN
    ackr2_human     758             36                   7       NaN
    ackr3_human    4358             11                   3       NaN
    ackr4_human     810              9                   3       8.4
    acthr_human    3633              4                   5       NaN
    """
    # the correlation df should have all spearman rank correlations between the rankings and the attributes
    unique_attributes = attributes.columns
    unique_attributes = unique_attributes[unique_attributes != "agonist"]
    correlation_df = pd.DataFrame(
        index=rankings["Model"].unique(), columns=unique_attributes
    )

    # for each model
    for model in rankings["Model"].unique():
        model_rankings = rankings[rankings["Model"] == model]
        model_gpcrs = model_rankings["GPCR"].unique()
        gpcr_to_rank = model_rankings.set_index("GPCR")["AgonistRank"]
        model_ranks = gpcr_to_rank[model_gpcrs]

        # for each attribute (column)
        for attribute in unique_attributes:
            model_attributes = [attributes.loc[gpcr, attribute] for gpcr in model_gpcrs]
            rho, p_val = spearmanr(model_ranks, model_attributes, nan_policy="omit")
            # count non-nan samples
            sample_count = len(model_ranks) - np.isnan(model_ranks).sum()

            correlation_df.loc[model, attribute] = (rho, p_val, sample_count)

    return correlation_df


def plot_correlation_heatmap(correlation_df):
    script_dir = pathlib.Path(__file__).parent.absolute()
    plot_path = script_dir / "peptide_correlation_characteristics.png"
    fig, ax = plt.subplots(figsize=(10, 5))

    rho = correlation_df.map(lambda x: x[0])
    rho = rho.astype(float)

    p_vals = correlation_df.map(lambda x: x[1])
    p_vals = p_vals.astype(float)

    counts = correlation_df.map(lambda x: x[2])
    counts = counts.astype(float)
    print(counts)

    sns.heatmap(
        p_vals,
        annot=True,
        cmap="coolwarm_r",
        ax=ax,
        fmt=".3f",
    )
    plt.title("Correlation between peptide characteristics and model rankings")

    # rotate rows
    plt.yticks(rotation=0)
    plt.tight_layout()

    plt.savefig(plot_path)
    plt.close()


def main():
    attributes = get_attributes()
    rankings = load_rankings()

    correlation_df = create_correlation_df(attributes, rankings)
    # to csv
    script_dir = pathlib.Path(__file__).parent.absolute()
    correlation_df.to_csv(script_dir / "peptide_correlation_characteristics.csv")

    plot_correlation_heatmap(correlation_df)


if __name__ == "__main__":
    main()
