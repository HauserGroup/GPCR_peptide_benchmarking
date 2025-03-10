import pathlib
import pandas as pd 

def run():
    script_dir = pathlib.Path(__file__).parent
    df = script_dir / 'benchmark_AF2_no_templates.csv'
    df = pd.read_csv(df)
    df['identifier'] = df['description'].apply(lambda x: x.rpartition('_')[0])
    # use sc_value as the InteractionProbability
    new_df = df[['identifier', 'sc_value']]
    new_df.columns = ['identifier', 'InteractionProbability']
    
    # save the new_df to ./predictions.csv
    new_df.to_csv(script_dir / 'predictions.csv', index=False)


if __name__ == '__main__':
    run()
