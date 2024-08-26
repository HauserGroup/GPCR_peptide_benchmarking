""" """

import pathlib
import pandas as pd
import sys
import matplotlib.pyplot as plt


SCRIPT_DIR = pathlib.Path(__file__).parent
sys.path.append(str(SCRIPT_DIR))
sys.path.append(str(SCRIPT_DIR.parent))
sys.path.append(str(SCRIPT_DIR.parent.parent))

from sklearn.metrics import roc_curve, auc
from parse_predictions import get_models, get_ground_truth_df, get_ground_truth_values


def get_subdir_name_from_path(p):
    p = pathlib.Path(p)
    return p.parts[-1]


def combine_p1_p2(p1_p, p2_p, combined_p, predictions_p):
    df1 = pd.read_csv(p1_p)
    df2 = pd.read_csv(p2_p)

    # concat and keep header of df1
    df = pd.concat([df1, df2], ignore_index=True)

    # add identifier column
    df["identifier"] = df["saved folder"].apply(get_subdir_name_from_path)

    # copy 'LIS' to 'InteractionProbability'
    df.to_csv(combined_p, index=False)

    df["InteractionProbability"] = df["LIS"]
    # group by identifier and take the max value of InteractionProbability
    df = df.groupby("identifier")["InteractionProbability"].max().reset_index()
    df.to_csv(predictions_p, index=False)


def mini_roc(df, score_cols, ground_truth, identifier_col, plot_p):
    """
    use all the score cols as an roc line
    """
    for score in score_cols:
        # subset df, to take the max value for score for each identifier
        plot_df = df.groupby(identifier_col)[score].max().reset_index()
        y_pred = plot_df[score].to_numpy()
        y_true = get_ground_truth_values(ground_truth, plot_df[identifier_col])
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{score} (area = {roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC, AF2 LIS with templates")
    plt.legend(loc="lower right")
    plt.savefig(plot_p, dpi=300)


def main():
    script_dir = pathlib.Path(__file__).parent
    # combine if not yet done
    combine_p = script_dir / "combined.csv"
    pred_p = script_dir / "predictions.csv"
    # if not combine_p.exists():
    combine_p1_p2(script_dir / "p1.csv", script_dir / "p2.csv", combine_p, pred_p)

    pred_df = pd.read_csv(combine_p)
    score_cols = ["LIS", "LIA", "ipTM", "Confidence", "pTM", "pLDDT"]
    ground_truth = get_ground_truth_df()
    identifier_col = "identifier"
    plot_p = script_dir / "roc.png"
    mini_roc(pred_df, score_cols, ground_truth, identifier_col, plot_p)


if __name__ == "__main__":
    main()
