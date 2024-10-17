""" Test if models perform significantly different better than random.
And test if re-scoring significantly improves the performance of the models.
"""
import numpy as np
import pandas as pd
import pathlib 
from scipy.stats import wilcoxon
import itertools


def load_rankings():
    script_dir = pathlib.Path(__file__).parent.absolute()
    rankings = pd.read_csv(script_dir / 'agonist_rankings.csv')
    return rankings


def wilcoxon_signed_rank_test(ranks0, ranks1):
    """ Perform Wilcoxon signed-rank test to compare the performance of the models

    Test if ranks0 are significantly higher than ranks1. 

    ranks0: a list of integers, where each integer represents the rank of the agonist
    ranks1: a list of integers, where each integer represents the rank of the agonist
    """
    # check equal length
    assert len(ranks0) == len(ranks1), "ranks0 and ranks1 must have the same length"

    # assert there are no 0 values
    assert 0 not in ranks0, "ranks0 cannot contain 0 values"
    assert 0 not in ranks1, "ranks1 cannot contain 0 values"

    n = len(ranks0)
    
    # calculate if ranks0 are significantly higher than ranks1, return p-value and statistic
    statistic, p = wilcoxon(ranks0, ranks1, alternative='greater')
    return statistic, p
    

def mean_random_ranking(n_scores, n_ranks):
    # Step 1: Determine approximately how many scores should be assigned to each rank
    base_count = n_scores // n_ranks  # This is 9 in your case (100 // 11)
    extra = n_scores % n_ranks        # This is the remainder, 1 in your case (100 % 11)
    
    # Step 2: Create an array where each rank has `base_count` scores
    counts = [base_count] * n_ranks
    
    # Step 3: Distribute the extra scores across some ranks
    for i in range(extra):
        counts[i] += 1  # Adding the extra score to the first `extra` ranks

    # Step 4: Create the ranks array based on the counts
    ranks = []
    for rank, count in enumerate(counts, start=1):
        ranks.extend([rank] * count)
    
    # Step 5: Shuffle the ranks randomly
    np.random.seed(0)
    np.random.shuffle(ranks)

    return ranks


def compared_to_random(compared_to_random_p):
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = load_rankings()
    possible_ranks = 11

    # Model, GPCR, AgonistRank, unseen, class
    models = df['Model'].unique()
    # all vs random
    with open(compared_to_random_p, 'w') as f:
        f.write('Model,Statistic,p-value,Number of GPCRs\n')

    for model in models:
        ranks = df[df['Model'] == model]['AgonistRank'].values
        gpcrs_ranked = len(ranks)
        random_ranks = mean_random_ranking(gpcrs_ranked, possible_ranks)
        stat, p = wilcoxon_signed_rank_test(random_ranks, ranks)

        with open(compared_to_random_p, 'a') as f:
            f.write(f'{model},{stat},{p},{gpcrs_ranked}\n')


def compare_all_vs_all(compared_all_vs_all_p):
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = load_rankings()
    compared_all_vs_all_p = script_dir / 'wilcoxon_compared_all_vs_all.csv'
    models = df['Model'].unique()

    with open(compared_all_vs_all_p, 'w') as f:
        f.write('Model1,Model2,Statistic,p-value,Number of GPCRs,Model2 is better (a=0.05)\n')

    # get all pairs of models, including different order
    model_combinations = list(itertools.combinations(models, 2))
    model_combinations += [(model2, model1) for model1, model2 in model_combinations]
    # drop self comparisons
    model_combinations = [pair for pair in model_combinations if pair[0] != pair[1]]

    for model1, model2 in model_combinations:
        model1_df = df[df['Model'] == model1].copy()
        model2_df = df[df['Model'] == model2].copy()
        shared_gpcrs = set(model1_df['GPCR']).intersection(set(model2_df['GPCR']))
        
        # fix df1 so that it only contains shared GPCRs between model1 and model2
        model1_df = model1_df[model1_df['GPCR'].isin(shared_gpcrs)]
        # fix df2 so that it only contains shared GPCRs between model1 and model2
        model2_df = model2_df[model2_df['GPCR'].isin(shared_gpcrs)]

        # set GPCR as index
        model1_df.set_index('GPCR', inplace=True)
        model2_df.set_index('GPCR', inplace=True)

        # reorder model2 index to match model1 index
        model2_df = model2_df.reindex(model1_df.index)

        ranks1 = model1_df['AgonistRank'].values
        ranks2 = model2_df['AgonistRank'].values

        stat, p = wilcoxon_signed_rank_test(ranks1, ranks2)
        model2_better = p < 0.05

        with open(compared_all_vs_all_p, 'a') as f:
            f.write(f'{model1},{model2},{stat},{p},{len(ranks1)},{model2_better}\n')


def compare_with_templates_without(all_vs_all_p, new_p):
    df = pd.read_csv(all_vs_all_p)
    model_names = df['Model1'].unique()
    
    no_templates_models = [model for model in model_names if '(no templates)' in model]
    templates_version = [m.replace(' (no templates)' , '') for m in no_templates_models]

    pairs = list(zip(no_templates_models, templates_version))
    # add in reverse order
    pairs += [(model2, model1) for model1, model2 in pairs]


    df['is_pair'] = df.apply(lambda x: (x['Model1'], x['Model2']) in pairs, axis=1)
    
    # drop if not pair
    df = df[df['is_pair']]
    df.drop(columns='is_pair', inplace=True)

    df.to_csv(new_p, index=False)
    

def compare_LIS_to_AF2(all_vs_all_p, new_p):
    """
    """
    df = pd.read_csv(all_vs_all_p)

    # only compare those that make sense (same structure, or 1m vs 5m)
    model_names = df['Model1'].unique()
    lis_1m_models = [model for model in model_names if 'LIS' in model and '1m' in model]
    lis_5m_models  = [m.replace(' 1m', '') for m in lis_1m_models]
    pairs_1m = list(zip(lis_1m_models, lis_5m_models))
  
    # now compare rescoring
    lis = [model for model in model_names if 'LIS' in model]
    af2 = [m.replace(' LIS', '') for m in lis]
    pairs_rescoring = list(zip(lis, af2))
    pairs_rescoring += [(model2, model1) for model1, model2 in pairs_rescoring]
    pairs = pairs_1m + pairs_rescoring

    df['is_pair'] = df.apply(lambda x: (x['Model1'], x['Model2']) in pairs, axis=1)
    
    # drop if not pair
    df = df[df['is_pair']]
    df.drop(columns='is_pair', inplace=True)

    df.to_csv(new_p, index=False)
    

if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).parent.absolute()
    
    compared_to_random(script_dir / 'wilcoxon_compared_to_random_p.csv')
    
    compare_all_vs_all(script_dir / 'wilcoxon_compared_all_vs_all.csv')

    compare_with_templates_without(script_dir / 'wilcoxon_compared_all_vs_all.csv',
                                   script_dir / 'wilcoxon_compare_templates.csv')   
    
    compare_LIS_to_AF2(script_dir / 'wilcoxon_compared_all_vs_all.csv',
                                   script_dir / 'wilcoxon_compare_AFM-LIS.csv')  