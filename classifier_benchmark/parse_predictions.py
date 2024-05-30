import pandas as pd
import numpy as np
import pathlib


def directory_to_model_name(directory_name : str) -> str:
    """
    # match color dictionary in colors.py
    {'Receptor': '#0b3d91', 'Ligand': '#f9aa43', 'Agonist': '#f9aa43', 'Dissimilar decoy': '#99231b', 
    'Similar decoy': '#c62d1f', 'NeuralPLexer': '#5b616b', 'ESMFold': '#478347', 'RF-AA': '#A676D6',
      'RF-AA (no templates)': '#7352BF', 'AF2': '#115185', 'AF2 (no templates)': '#008FD7', 
      'AF3': '#061f4a', 'Peptriever': '#aeb0b5', 'D-SCRIPT2': '#aeb0b5', 
      'Class A (Rhodopsin)': '#115185', 'Class B1 (Secretin)': '#478347', 
      'Class F (Frizzled)': '#A676D6', 'Other GPCRs': '#aeb0b5'}
    """
    dir_to_name = {
        "AF2_template_iptm+ptm" : "AF2",
        "AF2_template_LIS" : "AF2-LIS",
        "AF3" : "AF3",
        "DSCRIPT2_TTV1" : "D-SCRIPT2",
        "Neuralplexer_sm_lig_plddt" : "NeuralPLexer",
        "RFAA_no_template_pae_prot" : "RF-AA (no templates)",
        "RFAA_template_pae_prot" : "RF-AA",
    }
    if directory_name in dir_to_name:
        return dir_to_name[directory_name]
    else:
        return directory_name


def get_models(model_dir, identifier_column="identifier"):
    """Get the models in the model directory.

    returns a list of tuples with the model name and the prediction df.
    """
    models = []
    for model in model_dir.iterdir():
        if model.is_dir():
            # get name of model
            model_name = model.name
            print("Getting data for model", model_name)
            # get path to prediction csv
            prediction_csv = model / "predictions.csv"
            if not prediction_csv.exists():
                print(f"Predictions not found for {model_name}. Skipping...")
                continue
            # read df
            prediction_csv = pd.read_csv(prediction_csv)
            # check identifier column is unique
            assert prediction_csv[
                identifier_column
            ].is_unique, "Identifier column is not unique."
            # append list and df
            model_name = directory_to_model_name(model_name)
            models.append((model_name, prediction_csv))

    return models


def get_ground_truth_df():
    script_dir = pathlib.Path(__file__).parent
    ground_truth_p = (
        script_dir.parent
        / "classifier_benchmark_data/output/6_interactions_with_decoys.csv"
    )
    ground_truth = pd.read_csv(ground_truth_p)
    if "identifier" not in ground_truth.columns:
        ground_truth["identifier"] = (
            ground_truth["Target ID"] + "___" + ground_truth["Decoy ID"].astype(str)
        )
    return ground_truth


def get_ground_truth_values(
    ground_truth, identifiers, interaction_column="Acts as agonist"
):
    """Get the ground truth values for the identifier."""
    values = []
    for identifier in identifiers:
        if identifier not in ground_truth["identifier"].values:
            continue
        values.append(
            ground_truth.loc[
                ground_truth["identifier"] == identifier, interaction_column
            ].values[0]
        )
    return np.array(values)


def get_gpcr_class(gpcr_id):
    """
    5ht1a_human -> Class A (Rhodopsin)
    """
    # directory of this file
    file_dir = pathlib.Path(__file__).parent
    # path to the GPCR class file
    class_csv = file_dir / "gpcr_list_human.csv"
    df = pd.read_csv(class_csv)
    # get the class
    gpcr_class = df.loc[df["gpcr"] == gpcr_id, "receptor_class"].values
    return gpcr_class[0]
