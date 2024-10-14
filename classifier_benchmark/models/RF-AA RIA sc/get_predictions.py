import pathlib
import pandas as pd 

def run():
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'benchmark_RF-AA.csv'
    df = pd.read_csv(df)
    df['identifier'] = df['description'].apply(lambda x: x.rpartition('_')[0])
    
    # use sc_value as the InteractionProbability
    new_df = df[['identifier', 'sc_value']]
    new_df.columns = ['identifier', 'InteractionProbability']
    
    # save the new_df to ./predictions.csv
    new_df.to_csv(script_dir / 'predictions.csv', index=False)

    # also save one where we use 'per_residue_energy_int' as the InteractionProbability
    # invert it so higher is better
    new_df = df.copy()
    new_df = new_df[['identifier', 'per_residue_energy_int']]
    new_df['InteractionProbability'] = new_df['per_residue_energy_int'] * -1
    new_df = new_df[['identifier', 'InteractionProbability']]
    new_df.to_csv(script_dir / 'predictions_per_residue_energy_int.csv', index=False)



if __name__ == '__main__':
    run()
