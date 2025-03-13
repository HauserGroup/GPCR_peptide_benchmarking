"""
Parse all model data, only save best pdbs for storage.
"""
import pathlib
import pandas as pd 
import json 
import glob
import matplotlib.pyplot as plt
import seaborn as sns


def get_confidences_for_model_dir(model_dir : pathlib.Path):
    conf_files = model_dir.glob("*summary_confidences*.json")
    conf_files = list(conf_files)
    conf_files = sorted(conf_files)

    # load all as json
    confidences = []
    for conf_file in conf_files:
        with open(conf_file, 'r') as f:
            confidences.append(json.load(f))
    return confidences


def get_iptm_from_confidence(conf : json):
    """
    Get the IPTM from a confidence json.
    """
    return conf['iptm']


def get_best_pdb_p_from_dir(model_dir):
    """
    fold_ackr1_human_758_full_data_0.json
    ***
    fold_ackr1_human_758_full_data_4.json

    fold_ackr1_human_758_model_0.cif
    ***
    fold_ackr1_human_758_model_4.cif

    fold_ackr1_human_758_summary_confidences_0.json
    ***
    fold_ackr1_human_758_summary_confidences_4.json
    """
    confidences = get_confidences_for_model_dir(model_dir)
    iptms = [get_iptm_from_confidence(x) for x in confidences]
    # index of best iptm
    best_iptm = iptms.index(max(iptms))
    best_model = model_dir / f'{model_dir.name}_model_{best_iptm}.cif'
    return best_model


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    models = script_dir / 'models'
    model_dirs = [x for x in models.iterdir() if x.is_dir()]
    identifiers = [x.name.replace("fold_", "") for x in model_dirs]
    identifiers = [x.replace("human_", "human___") for x in identifiers]

 
    # confidences are now a list of jsons, need to get the IPTM from all
    df = pd.DataFrame()
    df['identifier'] = identifiers
    df['best_pdb'] = [get_best_pdb_p_from_dir(x) for x in model_dirs]
    df = df.sort_values('identifier')
    
    # out dir
    out_dir = script_dir / 'best_models'
    out_dir.mkdir(exist_ok=True)

    # copy best pdbs to out dir. Name them "{identifier}.cif"
    for i, row in df.iterrows():
        identifier = row['identifier']
        best_pdb = row['best_pdb']
        out_p = out_dir / f'{identifier}.cif'
        best_pdb.rename(out_p)
        print(f"Moved {best_pdb} to {out_p}")
        
