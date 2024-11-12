import pathlib
import pandas as pd

def main():
    script_dir = pathlib.Path(__file__).parent
    result = script_dir / 'result_df.csv'
    res = pd.read_csv(result)

    # get identifier from 'saved folder' by splitting '/'
    res['identifier'] = res['saved folder'].apply(lambda x: x.split('/')[-1])
    out_p = script_dir / 'predictions.csv'
    # rename 'ipTM' to 'InteractionProbability'
    res.rename(columns={'ipTM': 'InteractionProbability'}, inplace=True)
    res.to_csv(out_p, index=False)

    # also, create AFM-LIS predictions
    out_p = script_dir / 'predictions_AFMLIS.csv'
    res.rename(columns={'InteractionProbability': 'ipTM'}, inplace=True)
    # rename 'LIS' to 'InteractionProbability'
    res.rename(columns={'LIS': 'InteractionProbability'}, inplace=True)
    res.to_csv(out_p, index=False)
    

if __name__ == "__main__":
    main()