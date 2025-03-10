import numpy as np
import pandas as pd
import pathlib 
from scipy.stats import mannwhitneyu
import itertools



def mannwhitneyu_is_greater(ranks0, ranks1):
    """ Perform Mann-Whitney U test to compare the performance of the models.
    Does not require the ranks to be paired.
    Also does not require same length of ranks0 and ranks1.

    Test if ranks0 are significantly higher than ranks1. 

    ranks0: a list of integers, where each integer represents the rank of the agonist
    ranks1: a list of integers, where each integer represents the rank of the agonist
    """
    # turn ranks0 into a list
    if not isinstance(ranks0, list):
        ranks0 = list(itertools.chain(ranks0))
    if not isinstance(ranks1, list):
        ranks1 = list(itertools.chain(ranks1))
    # print value count of ranks
    print(pd.Series(ranks1).value_counts(dropna=False))
    # assert there are no 0 values
    assert 0 not in ranks0, f"ranks0 cannot contain 0 values {pd.Series(ranks0).value_counts(dropna=False)}"
    assert 0 not in ranks1, f"ranks1 cannot contain 0 values {pd.Series(ranks1).value_counts(dropna=False)}"
    
    # calculate if ranks0 are significantly higher than ranks1, return p-value and statistic
    statistic, p = mannwhitneyu(ranks0, ranks1, alternative='greater')
    return statistic, p


def class_main():
    df = get_all_plot_df()
    # per model do test if class A > class B
    a = 'Class A (Rhodopsin)'
    b = 'Class B1 (Secretin)'
    models = df["Model"].unique()
    # models_to_test = ['AF2 (no templates)', 'AF2 LIS (no templates)', 'Peptriever']
    # models = [m for m in models if m in models_to_test]

    print("Model,Statistic,p-value (Class A > Class B)")
    for model in models:
        ranks_a = df[(df["Model"] == model) & (df["Class"] == a)]["AgonistRank"]
        ranks_a = ranks_a.to_list()
        ranks_b = df[(df["Model"] == model) & (df["Class"] == b)]["AgonistRank"]
        ranks_b = ranks_b.to_list()
        
        statistic, p = mannwhitneyu_is_greater(ranks_a, ranks_b)
        print(f"{model},{statistic},{p}")


def unseen_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = script_dir / 'plots/class_seen_unseen.csv'
    df = pd.read_csv(df)


    models = df["Model"].unique()
    print("Model,Statistic,p-value (Unseen > Seen)")
    for model in models:
        ranks_unseen = df[(df["Model"] == model) & (df["unseen"] == 'Unseen')]["AgonistRank"]
        ranks_unseen = ranks_unseen.to_list()
        ranks_seen = df[(df["Model"] == model) & (df["unseen"] == 'Seen')]["AgonistRank"]
        ranks_seen = ranks_seen.to_list()

        statistic, p = mannwhitneyu_is_greater(ranks_unseen, ranks_seen)
        print(f"{model},{statistic},{p}")



if __name__ == "__main__":
    class_main()
    unseen_main()
    

    