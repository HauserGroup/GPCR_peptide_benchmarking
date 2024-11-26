import numpy as np
import pandas as pd
import pathlib 
from scipy.stats import mannwhitneyu
import itertools


from plot_class_comparison_new import get_all_plot_df


def mannwhitneyu_is_greater(ranks0, ranks1):
    """ Perform Mann-Whitney U test to compare the performance of the models.
    Does not require the ranks to be paired.
    Also does not require same length of ranks0 and ranks1.

    Test if ranks0 are significantly higher than ranks1. 

    ranks0: a list of integers, where each integer represents the rank of the agonist
    ranks1: a list of integers, where each integer represents the rank of the agonist
    """
    # assert there are no 0 values
    assert 0 not in ranks0, "ranks0 cannot contain 0 values"
    assert 0 not in ranks1, "ranks1 cannot contain 0 values"
    
    # calculate if ranks0 are significantly higher than ranks1, return p-value and statistic
    statistic, p = mannwhitneyu(ranks0, ranks1, alternative='greater')
    return statistic, p


def main():
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


if __name__ == "__main__":
    main()

    