"""
For AF2, RF-AA, and AF3 classifiers,
Load the prediction data for later correlation.
"""
import pandas as pd
import pathlib


def main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    model_dir = script_dir.parent / "models"

    af3_df = pd.read_csv(model_dir / "AF3/predictions.csv")
    af3_df['model'] = 'AF3'
    af3_no_tp_df = pd.read_csv(model_dir / "AF3 (no templates)/predictions.csv")
    af3_no_tp_df['model'] = 'AF3 (no templates)'
    rf_aa_df = pd.read_csv(model_dir / "RF-AA/predictions.csv")
    rf_aa_df['model'] = 'RF-AA'
    rf_aa_no_tp_df = pd.read_csv(model_dir / "RF-AA (no templates)/predictions.csv")
    rf_aa_no_tp_df['model'] = 'RF-AA (no templates)'
    af2_df = pd.read_csv(model_dir / "AF2/predictions.csv")
    af2_df['model'] = 'AF2'
    af2_no_tp_df = pd.read_csv(model_dir / "AF2 (no templates)/predictions.csv")
    af2_no_tp_df['model'] = 'AF2 (no templates)'

    # concat
    df = pd.concat([af3_df, af3_no_tp_df, rf_aa_df, rf_aa_no_tp_df, af2_df, af2_no_tp_df])
    # only keep "identifier" and "InteractionProbability"
    df = df[['identifier', 'InteractionProbability', 'model']]
    df.to_csv(script_dir / "a_all_predictions.csv", index=False)


if __name__ == "__main__":
    main()
