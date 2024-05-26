import pathlib
import pandas as pd
import logging
import json


def find_best_alphafold3_score(af_dir: pathlib.Path):
    summary_jsons = list(af_dir.glob("*.json"))
    summary_jsons = [
        j for j in summary_jsons if str(j).endswith("_summary_confidences_0.json")
    ]

    return summary_jsons[0]


def get_relevant_af3_scores():
    return [
        "fraction_disordered",
        "has_clash",
        "iptm",
        "num_recycles",
        "ptm",
        "ranking_score",
    ]


def get_scores_from_af3_json(af3_json: pathlib.Path):
    summary_json = json.load(open(af3_json))
    scores = {}
    for score_col in get_relevant_af3_scores():
        scores[score_col] = summary_json[score_col]

    return scores


def get_scores():
    script_dir = pathlib.Path(__file__).parent
    out_p = script_dir / "predictions.csv"
    log_p = out_p.with_suffix(".log")

    model_dir = script_dir / "models"
    subdirs = [x for x in model_dir.iterdir() if x.is_dir()]
    # create df with cols
    out_df = pd.DataFrame(columns=["identifier"] + get_relevant_af3_scores())

    for s in subdirs:
        logging.info(f"Processing {s}")
        identifier = s.name
        identifier = identifier.partition("_")[2]
        identifier = identifier.replace("human_", "human___")

        summary = find_best_alphafold3_score(s)
        logging.info(f"Best score: {summary}")
        scores = get_scores_from_af3_json(summary)
        scores["identifier"] = identifier
        out_df = pd.concat([out_df, pd.DataFrame([scores])])

    # copy the iptm column to the an InteractionProbability column
    out_df["InteractionProbability"] = out_df["iptm"]
    # sort on identifier, then interaction probability
    out_df = out_df.sort_values(by=["identifier", "InteractionProbability"])

    out_df.to_csv(out_p, index=False)
    logging.info(f"Wrote predictions to {out_p}")


if __name__ == "__main__":
    get_scores()
