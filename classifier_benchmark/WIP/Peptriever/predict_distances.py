""" For each GPCR chain, predict the distance to the peptide of the classifier dataset.
"""
from predict import get_model_and_tokenizer, get_distance

import pandas as pd
import numpy as np
import pathlib
import logging


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).resolve().parent
    chain_info = pd.read_csv(script_dir / "gpcr_info.csv")
    classifier_p = "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    classifier_df = pd.read_csv(pathlib.Path(classifier_p))
    model, tokenizer = get_model_and_tokenizer()
    out_p = script_dir / "distances.csv"
    log_p = out_p.with_suffix(".log")
    logging.basicConfig(filename=log_p, level=logging.INFO, format="%(asctime)s - %(message)s",
                        filemode="w")
    # for complex
    complex_distances = {}
    for i, row in classifier_df.iterrows():
        gpcr_id = row["Target ID"]
        peptide_id = row["Decoy ID"]
        identifier = f"{gpcr_id}___{peptide_id}"
        peptide_sequence = row["Ligand Sequence"]
        chain_rows = chain_info[chain_info["GPCR"] == gpcr_id]
        logging.info(f"Predicting for {identifier}")
        
        # for chain
        chain_predictions = {}
        for j, chain_row in chain_rows.iterrows():
            chain_type = chain_row["Chain"]
            chain_sequence = chain_row["Sequence"]
            try:
                distance = get_distance(peptide_sequence, chain_sequence, model, tokenizer)
            except RuntimeError as e:
                logging.error(f"Error for {identifier} with chain {chain_type}: {e}")
                distance = np.nan

            chain_predictions[chain_type] = distance

        # save for complex
        complex_distances[identifier] = chain_predictions
    
    # save
    out_df = pd.DataFrame(complex_distances).T
    out_df.to_csv(out_p, index=True)
