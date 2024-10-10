import pathlib
import pandas as pd 

def run():
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'benchmark_AF2_no_templates.csv'
    df = pd.read_csv(df)
    df['identifier'] = df['description'].apply(lambda x: x.rpartition('_')[0])
    df = df.copy()
    # use per_residue_energy_int as the InteractionProbability
    df = df[['identifier', 'per_residue_energy_int']]
    # invert per_residue_energy_int
    df['InteractionProbability'] = df['per_residue_energy_int'] * -1

    df = df[['identifier', 'InteractionProbability']]
    # save the new_df to ./predictions.csv
    df.to_csv(script_dir / 'predictions.csv', index=False)


if __name__ == '__main__':
    run()
