import pathlib
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import logging

from sklearn.metrics import roc_curve, auc
from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values

# add "."
import sys

sys.path.append(".")
from colors import COLOR


def create_roc(invalid_identifiers, plot_p, log_p,
               models_to_plot,
               label_missing=True, disable_labels=False):
    """
    valid_identifiers: list of str, identifiers to keep. Remove other ones
    """
    # settings
    script_dir = pathlib.Path(__file__).parent
    model_dir = script_dir / "models"
    identifier_col = "identifier"
    score_col = "InteractionProbability"

    # run
    logging.basicConfig(filename=log_p, level=logging.INFO, filemode="w")
    models = get_models(model_dir)
    # remove models with 'APPRAISE' or 'LIS' in name
    models = [(name, df) for name, df in models if name in models_to_plot]

    ground_truth = get_ground_truth_df()
    # filter invalid identifiers
    ground_truth = ground_truth[~ground_truth[identifier_col].isin(invalid_identifiers)]
    number_positives = len(ground_truth[ground_truth["Acts as agonist"] == 1])
    number_negatives = len(ground_truth[ground_truth["Acts as agonist"] == 0])

    # set sns style
    sns.set_context("paper")
    sns.set_style("whitegrid") 
    fig, ax = plt.subplots(figsize=(3.55, 3.55))
    
    # grid with opacity
    plt.grid()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.grid(axis="x", linestyle="--", alpha=0.5)

    # iterate over models
    for model_name, prediction_df in models:
        logging.info(f"Processing model {model_name}")
        logging.info(f"Number of predictions: {len(prediction_df)}")
        nan_count = len(prediction_df) - len(prediction_df.dropna(subset=[score_col]))
        prediction_df = prediction_df.dropna(subset=[score_col])
        logging.info(f"Number of dropped NaNs in predictions: {nan_count}")
        # lastly, remove the identifiers that are not used in this evaluation
        prediction_df = prediction_df[
            ~prediction_df[identifier_col].isin(invalid_identifiers)
        ]
        logging.info(f"Number of predictions after filtering: {len(prediction_df)}")

        y_pred = prediction_df[score_col].to_numpy()
        y_true = get_ground_truth_values(ground_truth, prediction_df[identifier_col])
        
        if len(y_pred) != len(ground_truth):
            logging.warning(
                f"Number of predictions ({len(y_pred)}) does not match the number of ground truth values ({len(ground_truth)})"
            )

        # keep only valid predictions
        # calculate ROC curve
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        label = f"{model_name},\nAUC = {roc_auc:.2f}"
        
        missing_values = len(ground_truth) - len(y_pred)
        if missing_values > 0 and label_missing:
            label += f" ({missing_values} missing)"
        color = COLOR.get(model_name, "black")

        sns.lineplot(
            x=fpr,
            y=tpr,
            label=label,
            color=color,
            ax=ax,
            # marker="o",
            # markersize=4,
            # width 2
            linewidth=1,
            # dashes
            linestyle="-",
            # other styles
            # add variabilty to the line
            errorbar=None,
        )
    plt.xlim(0, 1.01)
    plt.ylim(0, 1.01)
    plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=12)
    plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=12)


    # make plot informative
    ax.plot([0, 1], [0, 1], color="black", lw=1, linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
    # ax.set_xlim([0.0, 1.0])
    # ax.set_ylim([0.0, 1.0])
    plt.title(
        f"Classifier performance\n n={len(ground_truth)}, ({number_positives} +, {number_negatives} -)"
    )

    # sort legend on AUC
    handles, labels = ax.get_legend_handles_labels()
    get_auc = lambda x: float(x.split("AUC = ")[1].split(" ")[0])
    labels, handles = zip(
        *sorted(zip(labels, handles), key=lambda x: get_auc(x[0]), reverse=True)
    )
    ax.legend(handles, labels,
              # place legend outside of plot (right)
              # bbox_to_anchor=(1.05, 1),
       loc="lower right",
        fontsize=8,
        title_fontsize=10,
        # tight layout
        bbox_to_anchor=(1.0, 0.0),
        # shrink legend
        borderaxespad=0,
        # shrink space between legend items
        labelspacing=0.2,
    )
    
    # disable labels
    if disable_labels:
        plt.title("")
        ax.set_xlabel("")
        ax.set_ylabel("")

    # set xticks as every 0.1, but labels every 0.2
    ax.set_xticks(np.arange(0, 1.1, 0.1))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    xticks_labels = []
    yticks_labels = []
    for i in range(0, 11, 1):
        if i % 2 == 0:
            xticks_labels.append(str(i / 10))
            yticks_labels.append(str(i / 10))
        else:
            xticks_labels.append("")
            yticks_labels.append("")
    ax.set_xticklabels(xticks_labels, fontsize=12)
    ax.set_yticklabels(yticks_labels, fontsize=12)

    # add xticks for every 0.1
    # plt.xticks(np.arange(0, 1.1, 0.1))
    # plt.yticks(np.arange(0, 1.1, 0.1))


    # remove the legend
    if disable_labels:
        plt.legend().remove()
    # use helvetica font
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontname("Helvetica")
        item.set_fontsize(8)

    # ensure the roc plot is square
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()

    print("saving to ", plot_p)
    # adjust so plot is total height
    plt.savefig(plot_p.with_suffix('.png'), dpi=300)
    plt.savefig(plot_p.with_suffix('.svg'))
    logging.info(f"Wrote ROC curve to {plot_p} (png and svg)")


def main(models_to_plot):
    ground_truth = get_ground_truth_df()
    script_dir = pathlib.Path(__file__).parent

    # set sns style
    sns.set_style("whitegrid")
    sns.set_context("notebook")
    
    # create roc for all
    create_roc(
        models_to_plot=models_to_plot,
        invalid_identifiers=[],
        plot_p=script_dir / "plots/roc_all.svg",
        log_p=script_dir / "plots/roc_all.log",
        disable_labels=False,
        label_missing=False,
    )

    # create roc WITHOUT similar decoys
    similar_identifiers = list()
    for i, row in ground_truth.iterrows():
        if row["Decoy Type"] == "Similar":
            similar_identifiers.append(row["identifier"])
    create_roc(
        models_to_plot=models_to_plot,
        invalid_identifiers=similar_identifiers,
        plot_p=script_dir / "plots/roc_no_similar.png",
        log_p=script_dir / "plots/roc_no_similar.log",
    )

    # create roc for ONLY most dissimilar. 
    # Use AF3 as reference as decoys were redefined in step 2
    for m, pred in get_models(script_dir / "models"):
        if "AF3_server" in m:
            af3_server_identifiers = list(pred["identifier"])
            break
    # add missing identifier to af3 (trfr_human), which is missing it's principal agonist
    af3_server_identifiers.append("trfr_human___2139")

    all_identifiers = list(ground_truth["identifier"])
    not_included = list(set(all_identifiers) - set(af3_server_identifiers))
    # print which type the identifiers are
    for i, row in ground_truth.iterrows():
        if row["identifier"] not in not_included:
            print(row["Decoy Type"], row["identifier"], row['Decoy Rank'])

    create_roc(
        models_to_plot=models_to_plot,
        invalid_identifiers=not_included,
        plot_p=script_dir / "plots/roc_most_dissimilar.svg",
        log_p=script_dir / "plots/roc_most_dissimilar.log",
        label_missing=False,
        disable_labels=False,
    )



if __name__ == "__main__":
    models_to_plot = ["AF3",
                      # "AF3_server",
                      "AF3 (no templates) iptm+ptm",
                      "AF3 (no templates)",
                      "AF2 (no templates)",
                      "AF2",
                      "RF-AA (no templates)",
                      "RF-AA",
                      "Neuralplexer",
                      "D-SCRIPT",
                      "ESMFold",
                      "Peptriever",
                      "Chai-1"
    ]
    main(models_to_plot)
