"""
lineplot
 y-axis = percent agonists in scores
 x-axis = number of samples chosen (out of 11 per GPCR)
"""

import sys
import pathlib

# add "."
SCRIPT_DIR = pathlib.Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))
sys.path.append(str(SCRIPT_DIR.parent))
sys.path.append(str(SCRIPT_DIR.parent.parent))
sys.path.append('.')

from parse_predictions import (
    get_ground_truth_df,
    get_ground_truth_values,
    get_gpcr_class,
)
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


from colors import COLOR
from plot_heatmap_combined import apply_first_pick_to_predictions


def get_models_ria():
    """
    should be a list of tuples.
    ("name of model", pd.DataFrame)
        where the DataFrame has columns:
            "identifier" - the identifier of the ligand
            "InteractionProbability" - the probability of interaction

    """
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'benchmark_RF-AA.csv'
    df = pd.read_csv(df)

    #    total_score  complex_normalized  dG_cross  ...  side2_normalized  side2_score              description
    # 0          0.0               8.610  1544.387  ...            40.433      808.669  npy2r_human___1152_0001
    # 1          0.0              15.226  3410.164  ...            38.446     1730.050    ccr4_human___798_0001

    df['identifier'] = df['description'].apply(lambda x: x.rpartition('_')[0])
    # each column is a model
    columns = list(df.columns)
    useful_cols = 'total_score,complex_normalized,dG_cross,dG_cross/dSASAx100,dG_separated,dG_separated/dSASAx100,dSASA_hphobic,dSASA_int,dSASA_polar,delta_unsatHbonds,hbond_E_fraction,hbonds_int,nres_all,nres_int,packstat,per_residue_energy_int,sc_value,side1_normalized,side1_score,side2_normalized,side2_score,description,identifier'
    useful_cols = useful_cols.split(',')
    useful_cols.remove('description')
    # only keep if in useful_cols
    columns = [c for c in columns if c in useful_cols]
    df = df[columns]

    # invert the columns for some, so higher val is better complex
    # ['total_score', 'complex_normalized', 'dG_cross', 'dG_cross/dSASAx100', 'dG_separated', 'dG_separated/dSASAx100'
    # 'dSASA_hphobic', 'dSASA_int', 'dSASA_polar', 'delta_unsatHbonds', 'hbond_E_fraction', 'hbonds_int', 'nres_all', 'nres_int', 'packstat', 'per_residue_energy_int', 'sc_value', 'side1_normalized', 'side1_score', 'side2_normalized', 'side2_score']
    columns_to_invert = ['dG_cross', 'dG_cross/dSASAx100', 'dG_separated', 'dG_separated/dSASAx100',
                         'per_residue_energy_int', 'hbond_E_fraction',
                         'side1_score', 'side2_score', 'side1_normalized', 'side2_normalized', 'complex_normalized']
    
    for col in columns_to_invert:
        new_col = f'{col}_(inverted)'
        df[new_col] = df[col].apply(lambda x: x * -1)
        columns.append(new_col)
        columns.remove(col)

    out = []
    for col in columns:
        # create a new df with only the identifier and the 'InteractionProbability'
        new_df = df[['identifier', col]]
        new_df.columns = ['identifier', 'InteractionProbability']
        out.append((col, new_df))

    # remove ''identifier' metric
    out = [m for m in out if m[0] != 'identifier']

    return out


def run_main():
    """ """
    
    script_dir = pathlib.Path(__file__).parent
    models = get_models_ria()

    unique_models = list([m[0] for m in models])
    plot_p = script_dir / "enrichment.svg"
    ground_truth = get_ground_truth_df()

    gpcrs = ground_truth["identifier"].apply(lambda x: x.split("___")[0]).unique()
    gpcr_to_class = {g: get_gpcr_class(g) for g in gpcrs}
    agonist_identifiers = ground_truth[ground_truth["Acts as agonist"] == 1][
        "identifier"
    ].values

    # remove AF3 from models
    models = [m for m in models if m[0] != "AF3"]

    for model_name, pred_df in models:
        pred_df["gpcr"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        pred_df["class"] = pred_df["gpcr"].apply(lambda x: gpcr_to_class[x])
        pred_df["is_agonist"] = pred_df["identifier"].apply(
            lambda x: x in agonist_identifiers
        )
        pred_df = pred_df.sort_values(["class", "gpcr"])

    plot_df = pd.DataFrame(
        columns=["model", "keep_top_n", "pa_count", "decoy_count", "total_pa"]
    )
    for keep_top_n in range(1, 12):
        for model_name, pred_df in models:
            # print stats if keep_top_n == 1
            if keep_top_n == 1:
                pa_count = pred_df[pred_df["is_agonist"]].shape[0]
                decoy_count = pred_df[~pred_df["is_agonist"]].shape[0]
                total_pa = pred_df["is_agonist"].sum()
                print(
                    f"Model: {model_name}, PA count: {pa_count}, Decoy count: {decoy_count}, Total PA: {total_pa}"
                )

            # sort
            filter_df = pred_df.sort_values(
                ["class", "gpcr", "InteractionProbability"],
                ascending=[True, True, False],
            )
            # keep top n
            filter_df = filter_df.groupby(["class", "gpcr"]).head(keep_top_n)
            pa_count = filter_df[filter_df["is_agonist"]].shape[0]
            decoy_count = filter_df[~filter_df["is_agonist"]].shape[0]
            total_pa = pred_df["is_agonist"].sum()
            row_df = pd.DataFrame(
                {
                    "model": model_name,
                    "keep_top_n": keep_top_n,
                    "pa_count": pa_count,
                    "decoy_count": decoy_count,
                    "total_pa": total_pa,
                },
                index=[0],
            )
            plot_df = pd.concat([plot_df, row_df], ignore_index=True)

    # calculate 'pa_retained' and 'decoy_retained'
    plot_df["pa_retained"] = plot_df["pa_count"] / plot_df["total_pa"]
    plot_df["decoy_retained"] = plot_df["decoy_count"] / (
        plot_df["pa_count"] + plot_df["decoy_count"]
    )
    
    # calculate area under curve for each
    auc_dict = {}
    for model_name in plot_df["model"].unique():
        model_df = plot_df[plot_df["model"] == model_name]
        auc_pa = model_df["pa_retained"].sum() / 11
        auc_decoy = model_df["decoy_retained"].sum() / 11
        auc_dict[model_name] = {"pa": auc_pa, "decoy": auc_decoy}
    
    # plot
    sns.set_context("paper")
    sns.set_style("whitegrid") 
    # two subplots, 1 for curve and 1 for legend
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))
    ax = axes[0]

    # automatically use diverse colors and styles for the lineplot
    sns.lineplot(
        x="keep_top_n",
        y="pa_retained",
        hue="model",
        data=plot_df,
        style="model",
        markers=True,
        dashes=False,
        ax=ax,
        # marker size
        markersize=8,
        # color palette for colorblind and with large number of categories
        palette="tab20",
    )

    # add label to the left of x == 1
    # for model_name in plot_df["model"].unique():
    #     model_df = plot_df[plot_df["model"] == model_name]
    #     pa_retained = model_df[model_df["keep_top_n"] == 1]["pa_retained"].values[0]
    #     ax.text(
    #         1,
    #         pa_retained,
    #         model_name,
    #         fontsize=6,
    #         ha="right",
    #         va="center",
    #         color=COLOR.get(model_name, "black"),
    #     )

    # plt.legend(title="Model", loc="lower right", fontsize=11, title_fontsize=12,
    #            markerscale=1.5, ncol=2, bbox_to_anchor=(1.5, 1), borderaxespad=0.)

    # plot dashed line at random performance
    random_performance_yvals = 1 / 11 * plot_df["keep_top_n"]
    ax.plot(
        plot_df["keep_top_n"],
        random_performance_yvals,
        linestyle="--",
        color="black",
        label="Random",
        # opacity
        alpha=0.5,
        # width = 2
        linewidth=1,
    )

    # save
    # set active axis
    plt.sca(ax)
    plt.xlim(0.8, 11.2)
    plt.ylim(0, 1.01)
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # sort legend on number of samples chosen
    handles, labels = ax.get_legend_handles_labels()
    plot_df = plot_df[plot_df["keep_top_n"] == 1]
    # add auc to labels
    labels = [f"{l} (AUC: {auc_dict[l]['pa']:.2f})" for l in labels if l in auc_dict]
 
    # disable labels (add in illustrator)
    plt.xlabel("Top n peptides selected")
    plt.ylabel("Agonists retained ratio")
    plt.title("Performance of RoseTTAInterfaceAnalyzer\nmetrics on GPCR agonist prediction")


    # remove legend from ax[0]
    ax.get_legend().remove()

    # plot legend on ax[1]
    ax = axes[1]
    plt.sca(ax)
    ax.axis("off")
    ax.legend(handles, labels, title="", loc="upper right", fontsize=8,
              markerscale=1.5,
              # center right
                bbox_to_anchor=(1.0, 1.2),
                # remove padding
                borderaxespad=0,
                # reduce size between handles
                columnspacing=0.2,
                # reduce size between rows
                labelspacing=0.2,
    )

    plt.tight_layout()
    plt.savefig(plot_p)
    print(f"Saved plot to {plot_p}")


if __name__ == "__main__":
    run_main()
