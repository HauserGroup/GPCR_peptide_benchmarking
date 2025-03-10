""" """

import pathlib
import pandas
import numpy as np


def get_identifier_from_saved_folder(s:pathlib.Path):
    return s.name


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'predictions_all.csv'
    df = pandas.read_csv(df)

    # add identifier
    col = 'saved folder'
    # get identifier, which is the dir of the 'saved folder' path
    df['saved folder'] = df['saved folder'].apply(pathlib.Path)
    df['identifier'] = df['saved folder'].apply(get_identifier_from_saved_folder)
    print(df)

    # rename LIS to 'InteractionProbability'
    df['InteractionProbability'] = df["LIS"]
    print(df)

    df.to_csv(script_dir / 'predictions.csv')
    



    