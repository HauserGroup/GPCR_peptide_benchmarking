"""
./models/<identifier>/*summary_confidences.json
"""
import pandas as pd
import numpy as np
import json 
import pathlib
import glob


def read_scores_json(json_p):
    with open(json_p) as f:
        data = json.load(f)
    return data


def get_metrics(json_data):
    """
    """
    iptm = json_data["iptm"] # 0.64,
    ptm = json_data["ptm"] # 0.76,
    ranking_score = json_data["ranking_score"] # 0.78
    return iptm, ptm, ranking_score


def get_identifier_from_conf_path(conf_path):
    parent = pathlib.Path(conf_path).parent.name
    # split on "no_templates"
    return parent.split("_no_templates")[0]


def main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    confidence_files = glob.glob(f"{script_dir}/models/**/*summary_confidences.json", recursive=True)
    identifiers = [get_identifier_from_conf_path(f) for f in confidence_files]
    scores = [read_scores_json(f) for f in confidence_files]
    assert len(identifiers) == len(scores), "Mismatch in number of identifiers and scores"

    # pack into pandas df
    df = pd.DataFrame()
    df["identifier"] = identifiers
    df["scores"] = scores
    df["iptm"] = df["scores"].apply(lambda x: x["iptm"])
    df["ptm"] = df["scores"].apply(lambda x: x["ptm"])
    df["ranking_score"] = df["scores"].apply(lambda x: x["ranking_score"])
    # remove scores column
    df = df.drop(columns=["scores"])
    
    df.to_csv(script_dir / 'scores.csv', index=False)


if __name__ == "__main__":
    main()
