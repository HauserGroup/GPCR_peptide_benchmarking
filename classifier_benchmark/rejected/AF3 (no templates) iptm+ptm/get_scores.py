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
    df = pd.read_csv(script_dir / 'scores.csv')
    # ipTM + pTM=0.8×pTM+0.2×ipTM
    iptm_vals = []
    for i, row in df.iterrows():
        df.loc[i, 'iptm+ptm'] = row['ptm'] * 0.8 + 0.2 * row['iptm']
        print(i)
    df.to_csv(script_dir / 'predictions.csv')


if __name__ == "__main__":
    main()
