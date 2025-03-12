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
from collections import OrderedDict

# spearman rank correlation
from scipy.stats import spearmanr
import sys 
sys.path.append(".")
# from colors import COLOR
from colors_subanalysis import COLOR
from matplotlib import colors as mcolors
# p-val corrections
from statsmodels.stats.multitest import multipletests

# def corr_plot_peptriever_vs_af2(plot_p):
#     """ On y-axis, rank of agonist, on x-axis, agonist length
#     """
#     script_dir = pathlib.Path(__file__).parent.absolute()

#     # get color from COLOR
#     peptriever_color = COLOR["Peptriever"]
#     af2_color = COLOR["AF2 (no templates)"]

#     attributes = get_attributes()
#     rankings = load_rankings()

#     # keep only models to keep
#     models_to_keep = ["Peptriever", "AF2 (no templates)"]

#     # get the rankings
#     peptriever_rankings = rankings[rankings["Model"] == "Peptriever"]
#     af2_rankings = rankings[rankings["Model"] == "AF2 (no templates)"]

#     # get the gpcrs
#     peptriever_gpcrs = peptriever_rankings["GPCR"].unique()
#     af2_gpcrs = af2_rankings["GPCR"].unique()

#     # get the attributes
#     peptriever_attributes = attributes.loc[peptriever_gpcrs]
#     af2_attributes = attributes.loc[af2_gpcrs]

#     # get the agonist lengths
#     peptriever_agonist_lengths = peptriever_attributes["agonist length"]
#     af2_agonist_lengths = af2_attributes["agonist length"]

#     # get the rankings
#     peptriever_ranks = peptriever_rankings.set_index("GPCR")["AgonistRank"]
#     af2_ranks = af2_rankings.set_index("GPCR")["AgonistRank"]

#     # get the spearman rank correlation
#     rho_peptriever, p_val_peptriever = spearmanr(peptriever_ranks, peptriever_agonist_lengths)
#     rho_af2, p_val_af2 = spearmanr(af2_ranks, af2_agonist_lengths)

#     # plot not as scatter plot, but as a regplot
#     plt.figure(figsize=(2.6, 2.6))
#     sns.set_context("paper")
#     sns.set_style("whitegrid")
#     # use grid with opacity 0,5
#     plt.grid()
#     plt.grid(axis="y", linestyle="--", alpha=0.5)
#     plt.grid(axis="x", linestyle="--", alpha=0.5)
#     scatter_kws={'s': 6}
#     sns.regplot(
#         x=peptriever_agonist_lengths,
#         y=peptriever_ranks,
#         y_jitter=0.1,
#         color=peptriever_color,
#         label="",
#         marker='.',
#         # size
#         line_kws={"linewidth": 2},
#         scatter_kws=scatter_kws,
#     )
#     sns.regplot(
#         x=af2_agonist_lengths,
#         y=af2_ranks,
#         y_jitter=0.1,
#         marker='.',
#         color=af2_color,
#         label="",
#         scatter_kws=scatter_kws,
#     )

#     # create a legend using the colors and a lineplot
#     plt.plot([], [], color=peptriever_color, marker='.', 
#              label=f"Peptriever\n(rho = {rho_peptriever:.3f})")
#     plt.plot([], [], color=af2_color, marker='.',
#              label=f"AF2 (no templates)\n(rho = {rho_af2:.3f})")

#     # save the plot
#     plt.yticks(range(1, 12))
#     plt.xlabel("Agonist length")
#     plt.ylabel("Rank")
#     plt.title("Rank vs agonist length")
#     plt.legend(fontsize=8)
  
#     plt.tight_layout()
#     plt.savefig(plot_p)
#     plt.savefig(plot_p.with_suffix(".png"))
#     plt.close()



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
    rankings = pd.read_csv('classifier_benchmark/agonist_rankings.csv')
    return rankings

def get_agonist_len(chain_lengths_s : str):
    s = chain_lengths_s
    return int(s.split("|")[1].split(":")[1])



def get_msa_depth_from_seq_lengths(s: str, peptide_chain: int):
    "s = '1:1248|2:18'  chain = 2  --> 18"
    lengths = s.split("|")
    s = lengths[peptide_chain - 1]
    return int(s.split(":")[1])


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

    # get the length of the agonists. Agonist is chain 2
    # 1:428|2:8 -> 8
    seq_and_msa["agonist_length"] = seq_and_msa["chain_lengths"].apply(get_agonist_len)
    
    # get msa depth
    peptide_chain = 2
    seq_and_msa["msa_depth"] = seq_and_msa["msa_seq_lengths"].apply(
        lambda x: get_msa_depth_from_seq_lengths(x, peptide_chain)
    )

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


def get_gpcr_selectivity_df():
    script_dir = pathlib.Path(__file__).parent.absolute()
    gpcr_selectivity_path = script_dir / "get_selectivity/selectivity_ligands_per_target.csv"
    gpcr_selectivity_df = pd.read_csv(gpcr_selectivity_path)
    # rename '"Target GPCRdb ID" to "Target ID"
    gpcr_selectivity_df = gpcr_selectivity_df.rename(
        columns={"Target GPCRdb ID": "Target ID"}
    )
    return gpcr_selectivity_df


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


def get_gpcr_n_term_len():
    script_dir = pathlib.Path(__file__).parent.absolute()
    chains = script_dir / 'GPCR_chains_info.csv'
    chain_info = pd.read_csv(chains)
    
    # GPCR,Sequence,Domains
    # ackr1_human,MGNCLHRAELSPSTENSSQLDFEDVWNSSYGVNDSFPDGDYGANLEAAAPCHSCNLLDDSALPFFILTSVLGILASSTVLFMLFRPLFRWQLCPGWPVLAQLAVGSALFSIVVPVLAPGLGSTRSSALCSLGYCVWYGSAFAQALLLGCHASLGHRLGAGQVPGLTLGLTVGIWGVAALLTLPVTLASGASGGLCTLIYSTELKALQATHTVACLAIFVLLPLGLFGAKGLKKALGMGPGPWMNILWAWFIFWWPHGVVLGLDFLVRSKLLLLSTCLAQQALDLLLNLAEALAILHCVATPLLLALFCHQATRTLLPSLPLPEGWSSHLDTLGSKS,"OrderedDict([('N-term', 54), ('TM1', 32), ('ICL1', 6), ('TM2', 30), ('ECL1', 5), ('TM3', 33), ('ICL2', 1), ('TM4', 27), ('ECL2', 14), ('TM5', 30), ('ICL3', 6), ('TM6', 31), ('ECL3', 5), ('TM7', 33), ('H8', 15), ('C-term', 14)])"
    df = pd.DataFrame(columns=['N-term length'])
    for i, row in chain_info.iterrows():
        gpcr = row['GPCR']
        # load the OrderedDict
        domain_dict = eval(row['Domains'])
        n_term_len = domain_dict['N-term']
        # add to df
        df.loc[gpcr, 'N-term length'] = n_term_len

    return df


def get_attributes():
    """ """

    # only keep agonists
    classifier_df = load_classifier_df()
    classifier_df = classifier_df[classifier_df["Acts as agonist"]]

    # load attribute dfs
    rankings = load_rankings()
    seq_and_msa = get_len_and_msa()

    selectivity = get_selectivity_df()
    pki = get_pki_df()
    gpcr_selectivity = get_gpcr_selectivity_df()
    n_term_len = get_gpcr_n_term_len()

    gpcrs = classifier_df["Original Target"].unique()
    correlation_df = pd.DataFrame(index=gpcrs, columns=[])
    for gpcr in gpcrs:
        # get agonist
        agonist = classifier_df[classifier_df["Original Target"] == gpcr]
        assert len(agonist) == 1
        agonist_id = agonist["Decoy ID"].values[0]
        correlation_df.loc[gpcr, "agonist"] = agonist_id

        # get agonist length
        agonist_len = seq_and_msa[seq_and_msa["identifier"] == f"{gpcr}___{agonist_id}"]
        assert len(agonist_len) == 1
        agonist_len = agonist_len["agonist_length"].values[0]
        correlation_df.loc[gpcr, "agonist length"] = agonist_len

        # get msa depth
        msa_depth = seq_and_msa[seq_and_msa["identifier"] == f"{gpcr}___{agonist_id}"]
        assert len(msa_depth) == 1
        msa_depth = msa_depth["msa_depth"].values[0]
        correlation_df.loc[gpcr, "agonist msa depth"] = msa_depth

        # get selectivity
        selectivity_val = selectivity[selectivity["Ligand ID"] == agonist_id]
        assert len(selectivity_val) == 1
        selectivity_val = selectivity_val["number of targets"].values[0]
        correlation_df.loc[gpcr, "agonist selectivity"] = selectivity_val

        # get gpcr selectivity
        gpcr_selectivity_val = gpcr_selectivity[gpcr_selectivity["Target ID"] == gpcr]
        assert len(gpcr_selectivity_val) == 1
        gpcr_selectivity_val = gpcr_selectivity_val["number of peptides"].values[0]
        correlation_df.loc[gpcr, "gpcr selectivity"] = gpcr_selectivity_val

        # get activity
        pki_val = pki[pki["gpcr"] == gpcr]
        assert len(pki_val) == 1
        pki_val = pki_val["mean_activity"].values[0]
        correlation_df.loc[gpcr, "pKi"] = pki_val
        
        # add n-term length of gpcr
        n_term_len_val = n_term_len.loc[gpcr, 'N-term length']
        correlation_df.loc[gpcr, "N-term length"] = n_term_len_val

    return correlation_df



def apply_pval_correction(correlation_df):
    """
    Apply bonferroni to p-values separately for each attribute.
    
    Parameters:
    correlation_df : pd.DataFrame
        DataFrame where each cell contains a tuple (rho, p_val, sample_count)
    
    Returns:
    pd.DataFrame
        DataFrame with corrected p-values.
    """
    corrected_df = correlation_df.copy()
    
    for attribute in correlation_df.columns:
        # Extract p-values for the current attribute
        p_values = [correlation_df.loc[model, attribute][1] for model in correlation_df.index]
        
        # Apply Benjamini-Hochberg correction
        _, p_corrected, _, _ = multipletests(p_values, method='bonferroni')
        
        # Replace corrected p-values back into the dataframe
        for i, model in enumerate(correlation_df.index):
            rho, _, sample_count = correlation_df.loc[model, attribute]
            corrected_df.loc[model, attribute] = (rho, p_corrected[i], sample_count)
    
    return corrected_df




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
   
    # first loop, calculate the correlation df
    for model_i, model in enumerate(sorted(rankings["Model"].unique())):
        model_rankings = rankings[rankings["Model"] == model]
        model_gpcrs = model_rankings["GPCR"].unique()
        gpcr_to_rank = model_rankings.set_index("GPCR")["AgonistRank"]
        model_ranks = gpcr_to_rank[model_gpcrs]

        # for each attribute (column)
        for attribute_i, attribute in enumerate(unique_attributes):
            model_attributes = [attributes.loc[gpcr, attribute] for gpcr in model_gpcrs]
            rho, p_val = spearmanr(model_ranks, model_attributes, nan_policy="omit")
            # count non-nan samples
            sample_count = len(model_ranks) - np.isnan(model_ranks).sum()
            correlation_df.loc[model, attribute] = (rho, p_val, sample_count)
    return correlation_df


def plot_merged_correlation_overview(correlation_df, plot_p, 
                             attributes, rankings):
    plot_save_dir = script_dir / 'ranking_vs_peptide_characteristics'
    os.makedirs(plot_save_dir, exist_ok=True)

    # create empty plot
    models = correlation_df.index
    unique_attributes = correlation_df.columns
    fig, axes = plt.subplots(
                             len(models),
                             len(unique_attributes), 
                             figsize=(1*len(unique_attributes), 4.5),
                             # share y-axis
                             sharey=True,
                             # reduce padding
                             gridspec_kw={'wspace': 0.05, 'hspace': 0.1,
                                          'left': 0.05, 'right': 0.95, 'top': 0.95, 'bottom': 0.05},
                             # share x axis per row
                             sharex='col',
                             constrained_layout=True,
    )

    # create colorbar
    max_corr = 0.4
    min_corr = -0.4
    # create a colorbar
    cmap = plt.get_cmap("coolwarm")
    cmap = mcolors.ListedColormap([(r, g, b, 0.5) for r, g, b, _ in cmap(np.linspace(0, 1, cmap.N))])
    norm = mcolors.Normalize(vmin=min_corr, vmax=max_corr)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

    
    # second loop, plot the regplots
    for model_i, model in enumerate(sorted(models)):
        model_rankings = rankings[rankings["Model"] == model]
        model_gpcrs = model_rankings["GPCR"].unique()
        gpcr_to_rank = model_rankings.set_index("GPCR")["AgonistRank"]
        model_ranks = gpcr_to_rank[model_gpcrs]


        for attribute_i, attribute in enumerate(unique_attributes):
            model_attributes = [attributes.loc[gpcr, attribute] for gpcr in model_gpcrs]
            # select axis
            ax = axes[model_i, attribute_i]
            rho, p_val, sample_count = correlation_df.loc[model, attribute]
            # background fill (red to blue) to indicate correlation quality
            fill_color = cmap(norm(rho))
            # fill the background
            ax.axhspan(0.5, 11.5, 
                       # color=COLOR.get(model, 'white'),
                       color=fill_color,
                       alpha=0.25,
                       zorder=0,
                       )
            sns.regplot(x=model_attributes,
                        y=model_ranks, 
                        y_jitter=0.1,             
                        # color=COLOR.get(model, 'black'),
                        color='black',
                        ax=ax,
                        marker='.',
                        # no outline
                        line_kws={"linewidth": 1.5,
                                  # "color": COLOR.get(model, 'black'),
                                  'color': 'black',
                                  'alpha': 0.8,
                                  'linestyle': '-',
                                  #'dashes': (2, 2)
                                  },
                        # marker not too big
                        scatter_kws={'s': 1},
            ) 
            ax.set_xlabel('')
            ax.set_ylabel("")
            ax.tick_params(axis='x', pad=-3)  # Adjust pad for x-axis labels

            # set yticks 1 - 11
            yticks = range(1, 12)
            yticklabels = [str(i) if i in (1, 6, 11) else "" for i in yticks]
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)
            ax.tick_params(axis='y', pad=-2)  # Adjust pad for y-axis labels
            
            # ax.set_xlim(0, None)
            ax.set_ylim(0.5, 11.5)

            # set xticks based on attribute
            model_attributes = model_attributes.copy()
            model_attributes = [x for x in model_attributes if not np.isnan(x)]
            if attribute == "agonist length":
                ax.set_xticks(range(0, 500, 200))
                assert max(model_attributes) < 500
                assert min(model_attributes) > 0
            elif attribute == "pKi":
                ax.set_xticks(range(6, 12, 2))
                assert max(model_attributes) < 12
                assert min(model_attributes) > 6
            elif attribute == "gpcr selectivity":
                ax.set_xticks(range(0, 12, 5))
                assert max(model_attributes) < 12
                assert min(model_attributes) > 0
            # set a grid with opacity 0.5
            ax.grid(axis="y", linestyle="--", alpha=0.0)
            ax.grid(axis="x", linestyle="-", alpha=0.0)
            
            # add pvalue label
            # p_val_label = get_pval_label(p_val)
            # ax.text(1.0, 0.95, p_val_label,
            #         horizontalalignment='right', verticalalignment='top', transform=ax.transAxes,
            #         fontsize=18, fontweight='bold',color='black')
            
            # check if round by 2 decimals makes it 0.00, if so, write <0.01
            if round(p_val, 3) == 0.000:
                corr_qual = f"p<0.001"
            else:
                corr_qual = f"p≈{p_val:.3f}"

            fontweight = 'normal'
            if p_val < 0.05:
                # ax.title.set_bbox({
                #     'facecolor': 'lightgrey',
                #     'alpha': 0.8,
                #     'edgecolor': None,
                #     'pad': 1,  # Reduce padding
                #     'boxstyle': 'round,pad=0.1'  # Control box shrinkage
                # })
                # fontweight = 'bold'
                ax.set_title(corr_qual, fontsize=8, pad=0,loc='center', fontweight=fontweight,
                             # move to bottom
                             #y=0.8,
                              )
            else:
                ax.set_title(" ", fontsize=8, pad=0,loc='center', fontweight=fontweight)


    plt.savefig(plot_save_dir / 'merged.png', dpi=600)
    plt.savefig(plot_save_dir / 'merged.svg')
    plt.close()


def save_custom_cbar_with_opacity(plot_save_dir):
    # save colorbar separately
    fig, ax = plt.subplots(figsize=(2,0.75))
    # Load colormap
    cmap = plt.cm.get_cmap("coolwarm")  # Replace with your desired colormap
    # Convert colormap to an array and modify alpha
    colors = cmap(np.linspace(0, 1, cmap.N))  # Get RGBA values
    colors[:, -1] = 0.25  # Set alpha to 0.5
    # Create new transparent colormap
    cmap_transparent = mcolors.ListedColormap(colors)
    # Normalize color range
    norm = plt.Normalize(vmin=-0.5, vmax=0.5)
    plt.tight_layout()
    # add cmap ticks
    plt.cm.ScalarMappable(
        cmap=cmap_transparent, norm=norm
    ).set_array([])  # Create a mappable object
    cb = plt.colorbar(plt.cm.ScalarMappable(cmap=cmap_transparent, norm=norm), 
                 cax=ax,
                 # set ticks
                 ticks=[-0.5, -0.25, 0, 0.25, 0.50],
                 orientation='horizontal',
                 label='Spearman rank correlation',
                 shrink=0.5,
                 # height to width ratio
                 aspect=0.5,
    )
    # shrink
    cb.ax.tick_params(labelsize=8)
    cb.set_label('Spearman rank correlation', fontsize=8)
    cb.ax.xaxis.set_label_position('top')
    # total size of colorbar should be reduced
    plt.tight_layout()
    # set horizontal aspect ratio
    cb.ax.set_aspect(0.025)
    # rotate x-ticks
    cb.ax.set_yticklabels(cb.ax.get_yticklabels(), rotation=90)
    # set vertical aspect ratio
    # cb.ax.set_aspect(0.5, adjustable='box')

    plt.savefig(plot_save_dir / 'colorbar.png', dpi=600)
    plt.savefig(plot_save_dir / 'colorbar.svg')


def get_pval_label(p_val):
    if p_val < 0.001:
        return "***"
    elif p_val < 0.01:
        return "**"
    elif p_val < 0.05:
        return "*"
    else:
        return ""


def plot_correlation_heatmap(correlation_df, plot_p):
    script_dir = pathlib.Path(__file__).parent.absolute()
    plot_path = plot_p
    fig, ax = plt.subplots(figsize=(6, 4))

    cols = correlation_df.columns
    stats = ['rho', 'p_val', 'count']
    
    # Split the tuple values into separate columns for easier access
    for col in cols:
        for stat in stats:
            correlation_df[col + "_" + stat] = correlation_df[col].apply(lambda x: x[stats.index(stat)])
    
    # Remove original tuple columns
    correlation_df = correlation_df.drop(columns=cols)
    
    # Extract rho and p-value columns
    rho = correlation_df[[col + "_rho" for col in cols]]
    pvals = correlation_df[[col + "_p_val" for col in cols]]

    # Annotate heatmap with rho values and significance stars
    annotations = rho.copy()

    for i in range(rho.shape[0]):  # rows
        for j in range(rho.shape[1]):  # columns
            rho_val = rho.iloc[i, j]
            p_val = pvals.iloc[i, j]
            star_label = get_pval_label(p_val)
            # Annotate with rho value and p-value stars
            full_label = f"{rho_val:.2f}{star_label}"
            annotations.iloc[i, j] = full_label

    # max and min corr
    max_corr = rho.max().max()
    min_corr = rho.min().min()
    outer = max(abs(max_corr), abs(min_corr))

    # order models in a logical way
    model_order = ['AF2 (no templates)', 'AF2 (no templates) LIS', 'Peptriever']
    other_models = [m for m in correlation_df.index if m not in model_order]
    model_order.extend(other_models)
    rho = rho.loc[model_order]
    annotations = annotations.loc[model_order]    

    # order attributes in a logical way
    attribute_order = ['agonist length_rho', 
                       'agonist msa depth_rho',
                       'agonist selectivity_rho',
                       'pKi_rho', 
                       'N-term length_rho',
                       'gpcr selectivity_rho',]
    other_attributes = [a for a in rho.columns if a not in attribute_order]
    attribute_order.extend(other_attributes)
    rho = rho[attribute_order]
    annotations = annotations[attribute_order]

    sns.set_context("paper")
    sns.set_style("whitegrid")
    font = 'helvetica'
    plt.rcParams["font.family"] = font
    plt.rcParams.update({"font.size": 10})

    sns.heatmap(
        rho,
        cmap="coolwarm",
        ax=ax,
        annot=annotations,  # Now pass the formatted annotations
        annot_kws={"size": 8},
        xticklabels=True,
        yticklabels=True,
        fmt='', # disable format to use custom annotations without errors
        vmin=-outer,
        vmax=outer,
        # format nicely for paper
        square=True,
        cbar=True,
        # shrink cbar
        cbar_kws={"shrink": 0.5, "label": "Spearman rank correlation"},
        linewidths=0.5,
        linecolor='gray',
    )
    
    plt.title("Correlation between peptide characteristics and model rankings")
    # Rotate y-ticks for better readability
    plt.yticks(rotation=0)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    plt.savefig(plot_path)
    plt.savefig(plot_path.with_suffix(".png"), dpi=600)
    plt.close()
    return correlation_df


def main(models_to_keep, attributes_to_keep, plot_p):
    attributes = get_attributes()
    attributes = attributes[attributes_to_keep]
    rankings = load_rankings()
    rankings = rankings[rankings["Model"].isin(models_to_keep)]

    # models to keep
    correlation_df = create_correlation_df(attributes, rankings)
    

    print("APPLYING P-VAL CORRECTION")
    correlation_df = apply_pval_correction(correlation_df)

    plot_merged_correlation_overview(correlation_df, plot_p, attributes, rankings)

    # keep only models to keep
    correlation_df = correlation_df.loc[models_to_keep]
    # plot_correlation_heatmap(correlation_df, plot_p)

    # to csv
    script_dir = pathlib.Path(__file__).parent.absolute()
    correlation_df.to_csv(script_dir / "peptide_correlation_characteristics.csv")

    models = correlation_df.index 
    attributes = correlation_df.columns
    attributes = sorted(attributes)
    print(','.join(attributes))
    for m in models:
        print(m, end=',')
        for a in sorted(attributes):
            rho, p_val, n_gpcrs = correlation_df.loc[m, a]
            print(f'{rho},{p_val}', end=',')
        print("")
    #                             agonist length  ...                                     N-term length
    # AF2 (no templates)       (0.24687015266979925, 0.005910457810487032, 123)  ...  (-0.07952563609671996, 0.38192090669073486, 123)
    
    



if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.absolute()
    sns.set_style("whitegrid")
    sns.set_context("paper")
    # helvetica font
    # plt.rcParams["font.family"] = "Helvetica"
    # default font size is 10
    plt.rcParams.update({"font.size": 8})
    plt.rcParams.update({"axes.labelsize": 8})
    plt.rcParams.update({"xtick.labelsize": 8})
    plt.rcParams.update({"ytick.labelsize": 8})
    plt.rcParams.update({"legend.fontsize": 8})
    plt.rcParams.update({"legend.title_fontsize": 8})
    plt.rcParams.update({"axes.titlesize": 8})

    save_custom_cbar_with_opacity(script_dir / 'ranking_vs_peptide_characteristics')

    main(models_to_keep = ["AF2 (no templates)",
                           "AF2 (no templates) LIS",
                           "Chai-1",
                           "AF3",
                           "AF3 LIS",
                           "RF-AA",
                           "Peptriever",
                          ],
        attributes_to_keep=["agonist length", 
                            # "agonist msa depth", 
                            # "agonist selectivity", 
                            "pKi",
                            # "N-term length",
                            "gpcr selectivity"],
        plot_p = script_dir / "peptide_correlation_characteristics.svg"
        )
    
    # 
    # corr_plot_peptriever_vs_af2(plot_p=script_dir / "peptide_correlation_characteristics_peptriever_vs_af2.svg")