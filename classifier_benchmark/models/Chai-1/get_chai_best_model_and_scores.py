"""
Chai-1 predictions look like:
./models/<identifier>/pred.model_idx_0.cif
                      ....
                      pred.model_idx_4.cif

We want to get the best scores for 5 models. Get the best .cif. Then convert those to .pdb.
Scores are in the .out file.
"""
import os
import pathlib
import pandas as pd
import shutil
import logging

# convert to .pdb with biopython
from Bio.PDB import MMCIFParser
from Bio.PDB import PDBIO


def cif_to_pdb(cif_input, pdb_output):
    """
    Convert cif to pdb
    """
    cif_input = str(cif_input)
    pdb_output = str(pdb_output)

    parser = MMCIFParser()
    structure = parser.get_structure("structure", cif_input)
    io = PDBIO()
    io.set_structure(structure)
    io.save(pdb_output)


def yield_identifier_and_log_path():
    script_dir = pathlib.Path(__file__).parent
    model_dir = script_dir / "models"
    models = [d for d in model_dir.iterdir() if d.is_dir()]

    # assert there is 1 .out.txt
    for model in models:
        out_files = list(model.glob("*_out.txt"))
        if len(out_files) != 1:
            logging.warning(f'There should be 1 .out.txt file. Found {len(out_files)} for {model}')
            continue
        out_file = out_files[0]

        yield model.name, out_file



def get_scores_per_model_from_out_log(log_p):
    # Score=0.3783, writing output to /groups/scienceai/tronkko/chai-1/Classifier_Models/xcr1_human___2270/pred.model_idx_0.cif
    # Score=0.3690, writing output to /groups/scienceai/tronkko/chai-1/Classifier_Models/xcr1_human___2270/pred.model_idx_1.cif
    # Score=0.3718, writing output to /groups/scienceai/tronkko/chai-1/Classifier_Models/xcr1_human___2270/pred.model_idx_2.cif
    # Score=0.3735, writing output to /groups/scienceai/tronkko/chai-1/Classifier_Models/xcr1_human___2270/pred.model_idx_3.cif
    # Score=0.3755, writing output to /groups/scienceai/tronkko/chai-1/Classifier_Models/xcr1_human___2270/pred.model_idx_4.cif
    
    # get identifier from log_p (it is the parent directory)
    identifier = log_p.parent.name

    with open(log_p) as f:
        lines = f.readlines()

    score_lines = [line for line in lines if line.startswith("Score=")]
    assert len(score_lines) == 5, f"Expected 5 scores, got {len(score_lines)}"

    score_df = pd.DataFrame(columns=["identifier", "model_file_name", "score"])


    for idx, line in enumerate(score_lines):
        # get score and model from line
        score = line.split(",")[0].split("=")[1]
        assert score.replace(".", "").isnumeric(), f"Score is not numeric: {score}"
        score = float(score)
        # get name ('pred.model_idx_0.cif')
        model = line.rsplit("/")[-1].strip()
        score_df.loc[idx] = [identifier, model, score]
    


    return score_df


def main():
    """
    """
    script_dir = pathlib.Path(__file__).parent
    log_p = script_dir / "chai_best_model_and_scores.log"
    logging.basicConfig(filename=log_p, level=logging.INFO, filemode='w')
    identifiers, out_files = zip(*list(yield_identifier_and_log_path()))
    
    score_dataframes = [get_scores_per_model_from_out_log(out_file) for out_file in out_files]

    # concat all dataframes
    df = pd.concat(score_dataframes)
    # sort on identifier, then on score
    df = df.sort_values(by=["identifier", "score"], ascending=[True, False])
    df.to_csv(script_dir / 'All_scores.csv', index=False)

    # keep only best
    df = df.groupby("identifier").head(1)
    df.to_csv(script_dir / 'Best_scores.csv', index=False)
    # rename col
    df = df.rename(columns={"score": "InteractionProbability"})
    df.to_csv(script_dir / 'predictions.csv', index=False)

    # copy best models
    model_dir = script_dir / "models"
    best_model_dir = script_dir / "best_models"
    best_model_dir.mkdir(exist_ok=True)

    for i, row in df.iterrows():
        identifier = row["identifier"]
        model = row["model_file_name"]
        model_p = model_dir / identifier / model
  
        # save to pdb (not cif)
        pdb_out_p = best_model_dir / f"{identifier}.pdb"

        cif_to_pdb(model_p, pdb_out_p)
        logging.info(f"Saved {pdb_out_p}")


if __name__ == "__main__":
    main()