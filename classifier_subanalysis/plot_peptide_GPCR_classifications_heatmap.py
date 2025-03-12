"""
Create figure with 3 subplots. Each subplot is for one of the classes.
Each subplot contains the distribution of agonist ranks.
Use a barplot, with rank 1 to 11 on the x-axis and the count on the y-axis.
"""

import pathlib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from parse_predictions import (
    get_models,
    get_ground_truth_df,
    get_ground_truth_values,
    get_gpcr_class,
)
import sys
from plot_enrichment import get_peptide_protein_GPCRs
from plot_peptide_correlation_characteristics_heatmap import get_pval_label
from class_unseen_mannwhitneyu import mannwhitneyu_is_greater
from statsmodels.stats.multitest import multipletests

# append "."
sys.path.append(".")
from colors import COLOR


def get_principal_agonist_identifiers(ground_truth):
    """ """
    # get the principal agonist identifiers

    return ground_truth[ground_truth["Decoy Type"] == "Principal Agonist"][
        "identifier"
    ].values


def get_rankings_from_df(df, agonists):
    """
    df: pandas.DataFrame
        with columns "identifier" and "InteractionProbability"
    agonists: list
        list of agonist identifiers

    returns: {"gpcr" <str> : rank <int>}
    """
    # sort by "InteractionProbability"
    df = df.sort_values("InteractionProbability", ascending=False)
    gpcrs = df["Target ID"].unique()

    # for each gpcr, get the RELATIVE ranking of the agonists
    rankings = {}
    for gpcr in gpcrs:
        # get rows for this gpcr (should be 11 rows)
        gpcr_df = df[df["Target ID"] == gpcr]
        # iterate over the rows and find the first agonist
        for relative_i, (i, row) in enumerate(gpcr_df.iterrows()):
            if row["identifier"] in agonists:
                rankings[gpcr] = relative_i + 1
                break

    return rankings


def get_plot_df(models, agonists, gpcr_to_class_dict):
    """
    models: list of tuples (model_name, pred_df)
    agonists: list of agonist identifiers
    gpcr_to_class_dict: dict, mapping gpcr to class
    """
    # plot df will store all rankings per model
    plot_df = pd.DataFrame(columns=["Model", "GPCR", "AgonistRank"])
    for model_name, pred_df in models:
        # add info to prediction df required for plotting
        pred_df["Target ID"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["Target ID"].apply(lambda x: gpcr_to_class_dict[x])

        # keep only relevant class and agonists
        rankings = get_rankings_from_df(pred_df, agonists)
        rankings_df = pd.DataFrame(
            {
                "Model": model_name,
                "GPCR": list(rankings.keys()),
                "AgonistRank": list(rankings.values()),
            }
        )
        rankings_df["Class"] = rankings_df["GPCR"].apply(
            lambda x: gpcr_to_class_dict[x]
        )
        plot_df = pd.concat([plot_df, rankings_df])

    return plot_df



def get_all_plot_df():
    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir.parent / "classifier_benchmark/models")
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}
    agonists = get_principal_agonist_identifiers(ground_truth)
    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    all_plot_df["Class"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_class_dict[x])
    return all_plot_df



def apply_p_val_correction(stat_df):
    """ Per group, apply p-value correction using Benjamini-Hochberg
            group                   model    stat     p_val
    0    Class      AF2 (no templates)   910.0  0.139311
    1    Class  AF2 (no templates) LIS   871.5  0.204087
    2    Class                     AF3   880.0  0.194790
    3    Class                 AF3 LIS   891.5  0.150189
    4    Class                  Chai-1  1058.0  0.013713
    """
    # apply p-value correction per group
    groups = stat_df["group"].unique()
    for group in groups:
        group_df = stat_df[stat_df["group"] == group]
        p_vals = group_df["p_val"]
        _, p_vals_corrected, _, _ = multipletests(p_vals,
                                                  # bonferroni
                                                  method='bonferroni')
        
        stat_df.loc[stat_df["group"] == group, "p_val_corrected"] = p_vals_corrected
       
        
    return stat_df



def run_main_barplot(plot_p, models_to_keep, gpcr_groups):
    """ """
    # load predictions
    script_dir = pathlib.Path(__file__).parent
    plot_p.parent.mkdir(parents=True, exist_ok=True)
    models = get_models(script_dir.parent / "classifier_benchmark/models")

    # load agonists
    ground_truth = get_ground_truth_df()
    gpcrs = ground_truth["Target ID"].unique()
    gpcr_to_class_dict = {g: get_gpcr_class(g) for g in gpcrs}

    agonists = get_principal_agonist_identifiers(ground_truth)
    gpcr_classes = ["Class A (Rhodopsin)", "Class B1 (Secretin)"] # , "Class F (Frizzled)"]
    gpcr_renamed = {k: k.split(" (")[0] for k in gpcr_classes}
    models = [(model_name, model_df) for model_name, model_df in models if model_name in models_to_keep]

    # combine dataframe
    all_plot_df =[get_plot_df([(model_name, model_df)], agonists, gpcr_to_class_dict) for model_name, model_df in models]
    all_plot_df = pd.concat(all_plot_df)
    # add class
    all_plot_df["Class"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_class_dict[x])
    all_plot_df['Model_class'] = all_plot_df['Model'] + ' ' + all_plot_df['Class']
    # add family
    peptide_receptors, other_receptors = get_peptide_protein_GPCRs()
    gpcr_to_family = {g: "Peptide" for g in peptide_receptors}
    gpcr_to_family.update({g: "Protein" for g in other_receptors})
    all_plot_df["Family"] = all_plot_df["GPCR"].apply(lambda x: gpcr_to_family[x])
    # add seen/unseen
    unseen_gpcrs = pd.read_csv(script_dir / "gpcrs_no_complex_before_2021-09-30.txt")
    unseen_gpcrs = unseen_gpcrs.values.flatten()
    gpcr_is_unseen = dict()
    for g in gpcrs:
        if g in unseen_gpcrs:
            gpcr_is_unseen[g] = "Unseen"
        else:
            gpcr_is_unseen[g] = "Seen"
    all_plot_df["Unseen"] = all_plot_df["GPCR"].apply(lambda x: gpcr_is_unseen[x])


    # TODO: fix
    fig, axes = plt.subplots(
                             len(models_to_keep),
                             len(gpcr_groups),
                             figsize=(1*len(gpcr_groups), 4.5),
                             # share y-axis
                             sharey=True,
                             # reduce padding
                             gridspec_kw={'wspace': 0.25, 'hspace': 0.1,
                                          'left': 0.05, 'right': 0.95, 'top': 0.95, 'bottom': 0.05},
                             # share x axis per row
                             sharex='col',
                             constrained_layout=True,
    )
    stats = list()
    for gpcr_group_i, gpcr_group in enumerate(gpcr_groups):
        for model_i, model in enumerate(sorted(models_to_keep)):
            ax = axes[model_i, gpcr_group_i]
            # get only the data for this model
            model_df = all_plot_df[all_plot_df["Model"] == model]
            if model_i == 0:
                print(model_df[gpcr_group].value_counts())
            if gpcr_group == "Class":
                model_df = model_df[model_df["Class"].isin(gpcr_classes)]
            # sort by class
            model_df = model_df.sort_values(gpcr_group)
            model_color = "black"
            if "AF2 (no templates)" in model:
                model_color = COLOR["AF2 (no templates)"]
            elif "AF2" in model:
                model_color = COLOR["AF2"]
            elif "AF3 (no templates)" in model:
                model_color = COLOR["AF3 (no templates)"]
            elif "AF3" in model:
                model_color = COLOR["AF3"]
            elif "Chai-1 (no templates)" in model:
                model_color = COLOR["Chai-1 (no templates)"]
            elif "Chai-1" in model:
                model_color = COLOR["Chai-1"]
            else:
                model_color = COLOR.get(model, "black")

            # stripplot uses jitter. Set seed for reproducibility
            np.random.seed(42)
            sns.stripplot(
                x=gpcr_group,
                y="AgonistRank",
                data=model_df,
                ax=ax,
                color=model_color,
                size=1.25,
                alpha=1.0,
                dodge=True,
                # set behind barplot
                zorder=1,
                # spread wider
                jitter=0.25,
            )
            # plot
            sns.barplot(
                x=gpcr_group,
                y="AgonistRank",
                data=model_df,
                ax=ax,
                linewidth=0.5,
                # add error bars
                capsize=0.25,
                errwidth=1,
                errcolor="black",
                color = model_color,
                alpha=0.5,
                # no label
                # inner = None,
                # scale="count",
                # crop at min (0) and max(11)
                # cut=0,
            )

            # set yticks 1 - 11
            yticks = range(1, 12)
            yticklabels = [str(i) if i in (1, 6, 11) else "" for i in yticks]
            ax.set_yticks(yticks)
            ax.set_yticklabels(yticklabels)
            ax.tick_params(axis='y', pad=-2)  # Adjust pad for y-axis labels
            ax.set_ylim(0.5, 11.5)
            ax.tick_params(axis='x', pad=-3)  # Adjust pad for x-axis labels

            # set a grid with opacity 0.5
            ax.grid(axis="y", linestyle="--", alpha=0.0)
            ax.grid(axis="x", linestyle="-", alpha=0.0)
            # get mean difference A-B
            mean_rank_dict = model_df.groupby(gpcr_group)["AgonistRank"].mean().to_dict()
            if gpcr_group == "Class":
                ax.set_title(f"Δx̄(A-B1)={mean_rank_dict[gpcr_classes[0]] - mean_rank_dict[gpcr_classes[1]]:.2f}", fontsize=8, pad=0, loc="center")
                ax.set_xticklabels([gpcr_renamed[g].replace("Class", "") for g in gpcr_classes])
                stat, p_val = mannwhitneyu_is_greater(model_df[model_df["Class"] == gpcr_classes[0]]["AgonistRank"],
                                                      model_df[model_df["Class"] == gpcr_classes[1]]["AgonistRank"])
            elif gpcr_group == "Family":
                ax.set_title(f"Δx̄(Prot-Pep)={mean_rank_dict['Protein'] - mean_rank_dict['Peptide']:.2f}", fontsize=8, pad=0, loc="center")
                ax.set_xticklabels(["Peptide", "Protein"])
                stat, p_val = mannwhitneyu_is_greater(model_df[model_df["Family"] == "Protein"]["AgonistRank"],
                                                        model_df[model_df["Family"] == "Peptide"]["AgonistRank"])
            elif gpcr_group == "Unseen":
                ax.set_title(f"Δx̄(unseen-seen)= {mean_rank_dict['Unseen'] - mean_rank_dict['Seen']:.2f}", fontsize=8, pad=0, loc="center")  
                ax.set_xticklabels(["Seen", "Unseen"])
                stat, p_val = mannwhitneyu_is_greater(model_df[model_df["Unseen"] == "Seen"]["AgonistRank"],
                                                        model_df[model_df["Unseen"] == "Unseen"]["AgonistRank"])
            else:
                raise NotImplementedError(f"Unknown gpcr_group {gpcr_group}")
            

            # store stat, pval in df
            stats.append((gpcr_group, model, stat, p_val))            
            ax.set_title(" ", fontsize=8, pad=0, loc="center")

    # now add p-value corrected stats
    stats = pd.DataFrame(stats, columns=["group", "model", "stat", "p_val"])
    stats = apply_p_val_correction(stats)
    # set 'Unseen,AF2 (no templates)' to a random number to see if the p-value correction works
    # stats.loc[(stats["group"] == "Unseen") & (stats["model"] == "AF2 (no templates)"), "p_val"] = 0.213
    # correct p-values per group
    for group_i, group in enumerate(gpcr_groups):
        for model_i, model in enumerate(sorted(models_to_keep)):
            ax = axes[model_i, group_i]
            p_val_corrected = stats[(stats["group"] == group) & (stats["model"] == model)]["p_val_corrected"]
            assert len(p_val_corrected) == 1
            p_val_corrected = p_val_corrected.values[0]
            
            text_type = "normal"
            # if <0.05, bol text
            # if p_val_corrected < 0.05:
            #     text_type = "bold"

            if round(p_val_corrected, 3) == 0.000:
                p_val_text = "p<0.001"
            else:
                p_val_text = f'p≈{p_val_corrected:.3f}'

            # p_val_label = get_pval_label(p_val)
            if p_val_corrected < 0.05:
                ax.set_title(p_val_text, fontsize=8, pad=0, loc="center", fontweight=text_type)
                p_val_label = get_pval_label(p_val_corrected)
                # ax.text(0.5,
                #         1.0, 
                #         p_val_label,
                #         horizontalalignment='center', # instead of center
                #         verticalalignment='top',
                #         transform=ax.transAxes,
                #         fontsize=18,
                #         # bold
                #         fontweight="bold",
                #         color='black')
            else:
                ax.set_title(" ", fontsize=8, pad=0, loc="center", fontweight=text_type)
            ax.set_xlabel("")
            ax.set_ylabel("")

    # save plot
    plt.savefig(plot_p)
    plt.savefig(plot_p.with_suffix(".png"), dpi=600)
    print("Saved plot to", plot_p)

    # save df
    all_plot_df.to_csv(plot_p.with_suffix(".csv"), index=False)
    print("Saved plot df to", plot_p.with_suffix(".csv"))

    # save stats
    stat_p = plot_p.parent / f'{plot_p.stem}_stats.csv'
    stats.to_csv(stat_p, index=False)
    # only corrected p-val
    corrected_pval_df = stats[["p_val_corrected"]]
    corrected_pval_df.to_csv(plot_p.parent / f'{plot_p.stem}_corrected_pval.csv', index=False)


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    sns.set(style="whitegrid")
    sns.set_context("paper")
    sns.set_palette("colorblind")
    # set default fontsize to 10
    plt.rcParams.update({"font.size": 8})
    # helvetica font
    # plt.rcParams["font.family"] = "Helvetica"
    # default font size is 10
    # plt.rcParams.update({"font.size": 8})
    # plt.rcParams.update({"axes.labelsize": 8})
    # plt.rcParams.update({"xtick.labelsize": 8})
    # plt.rcParams.update({"ytick.labelsize": 8})
    # plt.rcParams.update({"legend.fontsize": 8})
    # plt.rcParams.update({"legend.title_fontsize": 8})
    # plt.rcParams.update({"axes.titlesize": 8})

    models_to_keep = [
        "AF2 (no templates)",
        "AF2 (no templates) LIS",
        "Chai-1",
        "AF3",
        "AF3 LIS",
        "RF-AA",
        "Peptriever",
        ]
    
    run_main_barplot(plot_p = script_dir / "ranking_vs_receptor_classifications/barplot_GPCR_classifications.svg",
                     models_to_keep=models_to_keep,
                     gpcr_groups=["Class", "Unseen",  "Family"])
