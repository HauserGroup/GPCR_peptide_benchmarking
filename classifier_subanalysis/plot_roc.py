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


def create_roc(invalid_identifiers, plot_p, log_p):
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
    models = [(name, df) for name, df in models if name in MODELS_TO_INCLUDE]

    all_model_identifiers = set()
    for n, m in models:
        # print if 'InteractionProbability' value is nan
        for v in m['identifier'].values:
            all_model_identifiers.add(v)

    for n, m in models:
        for v in all_model_identifiers:
            if v not in m['identifier'].values:
                print(f'{n} missing {v}')

    ground_truth = get_ground_truth_df()
    # filter invalid identifiers
    ground_truth = ground_truth[~ground_truth[identifier_col].isin(invalid_identifiers)]
    number_positives = len(ground_truth[ground_truth["Acts as agonist"] == 1])
    number_negatives = len(ground_truth[ground_truth["Acts as agonist"] == 0])

    # empty fig
    fig, ax = plt.subplots(1, 1, figsize=(5, 5))

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

        # calculate ROC curve
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        label = f"{model_name}, AUC = {roc_auc:.2f}"
        missing_values = len(ground_truth) - len(y_pred)
        if missing_values > 0:
            label += f" ({missing_values} missing)"
        color = COLOR.get(model_name, "black")

        sns.lineplot(
            x=fpr,
            y=tpr,
            label=label,
            # color=color,
            ax=ax,
            # marker="o",
            # markersize=4,
            # markers=True,
            errorbar=None,
        )

    # make plot informative
    ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend(loc="lower right")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.0])
    plt.title(
        f"Classifier performance\n n={len(ground_truth)}, ({number_positives} +, {number_negatives} -)"
    )

    # sort legend on AUC
    handles, labels = ax.get_legend_handles_labels()
    get_auc = lambda x: float(x.split("AUC = ")[1].split(" ")[0])
    labels, handles = zip(
        *sorted(zip(labels, handles), key=lambda x: get_auc(x[0]), reverse=True)
    )
    ax.legend(handles, labels, loc="lower right")

    # adjust legend font dict
    for text in ax.get_legend().get_texts():
        text.set_fontsize("small")
    plt.savefig(plot_p)
    logging.info(f"Wrote ROC curve to {plot_p}")
    # also save as png
    plt.savefig(plot_p.with_suffix(".png"), dpi=600)
    plt.close()



def main():
    ground_truth = get_ground_truth_df()
    script_dir = pathlib.Path(__file__).parent
    # gpcr,name,accession,receptor_class,receptor_family,ligand_type,subfamily,endogenous_ligands,species
    gpcr_df = pd.read_csv(script_dir / "gpcr_list_human_pep_prot_ligand.csv")

    # create roc for all
    create_roc(
        invalid_identifiers=[],
        plot_p=script_dir / "plots/roc_all.svg",
        log_p=script_dir / "plots/roc_all.log",
    )

    # create roc WITHOUT similar decoys
    similar_identifiers = list()
    for i, row in ground_truth.iterrows():
        if row["Decoy Type"] == "Similar":
            similar_identifiers.append(row["identifier"])
    create_roc(
        invalid_identifiers=similar_identifiers,
        plot_p=script_dir / "plots/roc_no_similar.svg",
        log_p=script_dir / "plots/roc_no_similar.log",
    )

    # create roc for ONLY most dissimilar
    not_included = list()
    for i, row in ground_truth.iterrows():
        if row["Decoy Type"] == "Similar":
            not_included.append(row["identifier"])
        elif row["Decoy Rank"] > 0:
            not_included.append(row["identifier"])

    create_roc(
        invalid_identifiers=not_included,
        plot_p=script_dir / "plots/roc_most_dissimilar.svg",
        log_p=script_dir / "plots/roc_most_dissimilar.log",
    )

    # split into peptide vs protein interface.
    peptide_receptors = gpcr_df[gpcr_df['ligand_type'] == 'Peptide receptors']['gpcr'].values
    peptide_receptors = [i.lower().strip() for i in peptide_receptors]
    receptor_to_class = gpcr_df.set_index('gpcr')['receptor_class'].to_dict()
    if 'hrh4_human' not in receptor_to_class:
        receptor_to_class['hrh4_human'] = 'Class A (Rhodopsin)'
    all_identifiers = ground_truth['identifier'].unique()
    peptide_identifiers = list()
    other_identifiers = list()
    for i in all_identifiers:
        i = str(i).strip().lower()
        i_gpcr = i.split("___")[0].lower()
        if i_gpcr in peptide_receptors:
            peptide_identifiers.append(i)
        else:
            other_identifiers.append(i)
    # report counts of class for peptide_identifiers and other_identifiers
    peptide_identifiers_gpcrs = [i.split("___")[0] for i in peptide_identifiers]
    other_identifiers_gpcrs = [i.split("___")[0] for i in other_identifiers]
    peptide_identifiers_classes = [receptor_to_class[i] for i in peptide_identifiers_gpcrs]
    other_identifiers_classes = [receptor_to_class[i] for i in other_identifiers_gpcrs]
    print("Peptide identifiers:")
    print(pd.Series(peptide_identifiers_classes).value_counts())
    print("Other identifiers:")
    print(pd.Series(other_identifiers_classes).value_counts())

    # plot roc for peptide
    create_roc(
        invalid_identifiers=other_identifiers,
        plot_p=script_dir / "plots/roc_peptide.svg",
        log_p=script_dir / "plots/roc_peptide.log",
    )

    # plot roc for other
    create_roc(
        invalid_identifiers=peptide_identifiers,
        plot_p=script_dir / "plots/roc_other.svg",
        log_p=script_dir / "plots/roc_other.log",
    )


if __name__ == "__main__":
    # MODELS_TO_INCLUDE = ['AF2 (no templates)', 'AF3_local', "RF-AA"]
    MODELS_TO_INCLUDE = ["AF3_local", 
                         "AF3_local DeepRank-GNN-esm",
                         

                         "AF3_local (no templates) DeepRank-GNN-esm",

                         "AF2 (no templates)", 
                         "AF2 (no templates) DeepRank-GNN-esm",
                         "AF2 LIS (no templates)",
                         "AF2 (no templates) GNN-DOVE",

                         "RF-AA",
                         "RFAA (no templates) DeepRank-GNN-esm",
    ]
    main()
