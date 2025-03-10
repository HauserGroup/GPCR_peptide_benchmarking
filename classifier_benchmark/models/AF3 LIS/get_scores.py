""" Get InteractionProbability by:
- sorting on identifier and on iptm
- taking the LIS value of the top model per identified (based on iptm)
- save as predictions.csv with LIS -> InteractionProbability
"""
import pandas as pd 
import pathlib


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'AF3_LIS_merged.csv'
    df = pd.read_csv(df)
    # rename 'folder_name' to 'identifier'
    df.rename(columns={'folder_name': 'identifier'}, inplace=True)
    print(df)

    # sort on identifier and on iptm
    df = df.sort_values(['identifier', 'iptm'], ascending=[True, False])
    print(df)
    # only keep rows if protein_1,protein_2 == 1,2
    df = df[(df['protein_1'] == 1) & (df['protein_2'] == 2)]
    print(df)

    # take the LIS value of the top model per identified (based on iptm)
    new_df = df.groupby('identifier').first().reset_index()
    new_df.to_csv(script_dir / 'AF3_best_iptm_per_identifier.csv', index=False)


    # save as predictions.csv with iptm -> InteractionProbability
    new_df = new_df[['identifier', 'LIS']]
    new_df.columns = ['identifier', 'InteractionProbability']
    new_df.to_csv(script_dir / 'predictions.csv', index=False)

