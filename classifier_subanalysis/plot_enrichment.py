"""
lineplot
 y-axis = percent agonists in scores
 x-axis = number of samples chosen (out of 11 per GPCR)
"""

import sys
import pathlib
from parse_predictions import (
    get_ground_truth_df,
    get_ground_truth_values,
    get_gpcr_class,
    get_models,
)
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
import pandas as pd

from colors_subanalysis import COLOR, MARKER, STYLE

# add "."
sys.path.append(".")
from plot_heatmap_combined import apply_first_pick_to_predictions


def get_peptide_protein_GPCRs():
    script_dir = pathlib.Path(__file__).parent
    # gpcr,name,accession,receptor_class,receptor_family,ligand_type,subfamily,endogenous_ligands,species
    gpcr_df = pd.read_csv(script_dir / "gpcr_list_human_pep_prot_ligand.csv")
    ground_truth = get_ground_truth_df()

     # split into peptide vs protein interface.
    peptide_receptors = gpcr_df[gpcr_df['ligand_type'] == 'Peptide receptors']['gpcr'].values
    peptide_receptors = [i.lower().strip() for i in peptide_receptors]
    other_receptors = gpcr_df[gpcr_df['ligand_type'] != 'Peptide receptors']['gpcr'].values
    other_receptors = [i.lower().strip() for i in other_receptors]

    if not 'hrh4_human' in other_receptors:
        other_receptors.append('hrh4_human')
        
    # add 
    return peptide_receptors, other_receptors


def run_main(plot_p,
             only_GPCRs_without_complex=False,
             reject_models_with_substrings=[],
             gpcrs_to_reject = [],
             ):
    """ """
    rcParams['font.family'] = 'Helvetica'  # or use 'sans-serif' if Helvetica isn't available

    script_dir = pathlib.Path(__file__).parent
    models = get_models(script_dir.parent / "classifier_benchmark/models")
    if len(reject_models_with_substrings) > 0:
        models = [m for m in models if not any([r in m[0] for r in reject_models_with_substrings])]
    models = [m for m in models if m[0] in MODELS_TO_KEEP]

    # remove models with LIS or APPRAISE
    unique_models = list([m[0] for m in models])
    ground_truth = get_ground_truth_df()

    gpcrs = ground_truth["identifier"].apply(lambda x: x.split("___")[0]).unique()
    gpcr_to_class = {g: get_gpcr_class(g) for g in gpcrs}
    agonist_identifiers = ground_truth[ground_truth["Acts as agonist"] == 1][
        "identifier"
    ].values

    # read gpcr_no_complex.txt
    no_complex_txt = script_dir / 'gpcrs_no_complex.txt'
    no_complex = no_complex_txt.read_text().splitlines()

    # get gpcr, class, is_agonist
    new_models = []
    for model_name, pred_df in models:
        pred_df["gpcr"] = pred_df["identifier"].apply(lambda x: x.split("___")[0])
        if len(gpcrs_to_reject) > 0:
            print(f'Rejecting GPCRs: {len(gpcrs_to_reject)}')
            pred_df = pred_df[~pred_df["gpcr"].isin(gpcrs_to_reject)]

        pred_df["class"] = pred_df["gpcr"].apply(lambda x: gpcr_to_class[x])
        pred_df["is_agonist"] = pred_df["identifier"].apply(
            lambda x: x in agonist_identifiers
        )
        pred_df = pred_df.sort_values(["class", "gpcr"])
        # if filter to only GPCRs without complex
        if only_GPCRs_without_complex:
            # gpcrs without complex
            gpcrs_with_complex_count = pred_df[pred_df["gpcr"].isin(no_complex)].shape[0]
            print('Removing this many GPCRs with complex:', gpcrs_with_complex_count)
            pred_df = pred_df[~pred_df["gpcr"].isin(no_complex)]
        new_models.append((model_name, pred_df))
    models = new_models


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

    # plot
    sns.set_context("paper")
    sns.set_style("whitegrid") 
    fig, ax = plt.subplots(figsize=(2.25, 3))
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)
    
    # add marker to plot df so we can sort on marker and model, for legend
    plot_df['marker'] = plot_df['model'].apply(lambda x: MARKER.get(x, None))
    plot_df['color'] = plot_df['model'].apply(lambda x: COLOR.get(x, 'black'))
    plot_df = plot_df.sort_values(['model', 'marker'])

    colors = [COLOR.get(m, 'black') for m in plot_df["model"].unique()]
    markers = [MARKER.get(m, None) for m in plot_df["model"].unique()]
    markers = ['' if m is None else m for m in markers]

    # plot dashed line at random performance
    random_performance_yvals = 1 / 11 * plot_df["keep_top_n"].unique()
    # random perf line
    plt.plot(
        plot_df["keep_top_n"].unique(),
        random_performance_yvals,
        color="black",
        alpha=0.5,
        # dotted instead of dashes
        linestyle=":",
    )
    # plot lines with different styles
    for model_name, model_line_style in STYLE.items():
        model_df = plot_df[plot_df["model"] == model_name]
        sns.lineplot(
            data=model_df,
            x="keep_top_n",
            y="pa_retained",
            ax=ax,
            color=COLOR[model_name],
            linestyle=model_line_style,
            linewidth=1,
            alpha=0.5,
            legend=True,
        )
    # markers
    sns.scatterplot(
        data=plot_df,
        x="keep_top_n",
        y="pa_retained",
        ax=ax,
        # color for models
        hue="model",
        # markers for rescoring methods
        markers=markers,

        # use this one if the colors of markers should match the line colors
        # palette=colors,
        
        # use this one if the colors of markers should all be black
        palette={m: 'black' for m in plot_df["model"].unique()},
       
        style="model",
        # make markers same size
        s=25,
        # line opacity
        alpha=1.0,
        legend=False,
    )

    # save
    plt.xlim(0.8, 11.2)
    plt.ylim(0, 1.01)
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # reduce legend font size
    # zoom
    plt.xticks(range(1, 12))
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.tight_layout()

    # fontsize of x and y labels
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
 
    # disable labels (add in illustrator)
    plt.xlabel("")
    plt.ylabel("")
    plt.title("")
    
    # fix the legend.
    # first it should contain a line with the color of the base models
    # then it should contain the black markers for the rescoring methods
    model_names = plot_df["model"].unique()
    # sort on last word
    sorted_names = list(sorted(model_names, key=lambda x: x.replace(" (no templates)", "").split()[-1]))
    for model_name in model_names:
        # get the color of the model
        model_color = COLOR.get(model_name, 'black')
        # get the line style of the model
        model_line_style = STYLE.get(model_name, '--')
        # model marker
        model_marker = MARKER.get(model_name, None)
        # remove the (no templates) part and add a dagger symbol instead
        replacement = r'$^\dagger$'

        # TODO: FIX THIS
        model_name = model_name.replace(" (no templates)", replacement)
        if " " in model_name:
            model_name = model_name.partition(" ")[2]
        # add a line, with the marker of the model, style and color
        plt.plot([], [], color=model_color, linestyle=model_line_style, label=model_name,
                    marker=model_marker, 
                    # set marker color to black
                    markerfacecolor='black', markeredgecolor='black', markersize=5)
    
  
    plt.tight_layout()
    # for xticks and yticks
    legend = plt.legend(loc='lower right', fontsize=8)
    for text_object in ax.get_xticklabels() + ax.get_yticklabels() + legend.get_texts():
        text_object.set_fontname('Helvetica')
        text_object.set_fontsize(8)
        text_object.set_color('black')
        
    ax.tick_params(axis='x', pad=0)  # Adjust pad for x-axis labels
    ax.tick_params(axis='y', pad=0)  # Adjust pad for y-axis labels
    
    # no padding

    plt.savefig(plot_p)
    print(f"Saved plot to {plot_p}")

    # also save as png
    plot_png = plot_p.with_suffix(".png")
    plt.savefig(plot_png, dpi=300)
    plt.close()
    print(f"Saved plot to {plot_png}")


if __name__ == "__main__":
    # MODELS_TO_KEEP = ["AF3_local", "AF2 (no templates)", "RF-AA"]
    MODELS_TO_KEEP = [
                      "AF2 (no templates)", 
                      "AF2 (no templates) DeepRank-GNN-esm",
                      "AF2 (no templates) APPRAISE",
                      "AF2 (no templates) LIS",
                      "AF2 (no templates) GNN-DOVE",
                      "AF2 (no templates) RIA sc",
                      ]
    script_dir = pathlib.Path(__file__).parent
    plot_p = script_dir / "plots/rescoring_enrichment_AF2_plot.svg"
    run_main(plot_p)
    plot_p = script_dir / "plots/rescoring_enrichment_AF2_no_complex.svg"
    run_main(plot_p, only_GPCRs_without_complex=True)

    # run for AF3
    MODELS_TO_KEEP = ["AF3",
                      "AF3 DeepRank-GNN-esm",
                      "AF3 APPRAISE",
                      "AF3 LIS",
                      "AF3 RIA sc",
                      "AF3 GNN-DOVE",
                      ]
    plot_p = script_dir / "plots/rescoring_enrichment_AF3_plot.svg"
    run_main(plot_p)
    plot_p = script_dir / "plots/rescoring_enrichment_AF3_no_complex.svg"
    run_main(plot_p, only_GPCRs_without_complex=True)


    # run for Chai-1
    MODELS_TO_KEEP = ["Chai-1",
                      "Chai-1 DeepRank-GNN-esm",
                      "Chai-1 APPRAISE",
                      "Chai-1 LIS",
                      "Chai-1 RIA sc",
                      "Chai-1 GNN-DOVE",
                      ]
    plot_p = script_dir / "plots/rescoring_enrichment_Chai-1_plot.svg"
    run_main(plot_p)
    plot_p = script_dir / "plots/rescoring_enrichment_Chai-1_no_complex.svg"
    run_main(plot_p, only_GPCRs_without_complex=True)


    # run for RF-AA
    MODELS_TO_KEEP = ["RF-AA",
                      "RF-AA DeepRank-GNN-esm",
                      "RF-AA APPRAISE",
                      "RF-AA LIS",
                      "RF-AA RIA sc",
                      "RF-AA GNN-DOVE",
                      ]
    plot_p = script_dir / "plots/rescoring_enrichment_RF-AA_plot.svg"
    run_main(plot_p)
    plot_p = script_dir / "plots/rescoring_enrichment_RF-AA_no_complex.svg"
    run_main(plot_p, only_GPCRs_without_complex=True)
    


    # run for peptide vs protein interface
    # peptide_receptors, other_receptors = get_peptide_protein_GPCRs()
    # plot_p = script_dir / "plots/enrichment_plot_peptide_receptors.svg"
    # run_main(plot_p, gpcrs_to_reject=other_receptors)
    # plot_p = script_dir / "plots/enrichment_plot_other_receptors.svg"
    # run_main(plot_p, gpcrs_to_reject=peptide_receptors)

 