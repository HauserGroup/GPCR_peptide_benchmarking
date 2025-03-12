import pandas as pd 
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr, friedmanchisquare

def get_df():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = pd.read_csv(script_dir / "a_all_predictions.csv")
    return df

def plot_correlation():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = get_df()

    comparisons = [
        ("AF3", "AF3 (no templates)"),
        ("RF-AA", "RF-AA (no templates)"),
        ("AF2", "AF2 (no templates)"),
    ]
    
    fig, axes = plt.subplots(1, 3, figsize=(8, 5), sharey=False)
    
    spearman_results = []
    
    for i, (with_templates, without_templates) in enumerate(comparisons):
        subset = df[df["model"].isin([with_templates, without_templates])]
        pivoted = subset.pivot(index="identifier", columns="model", values="InteractionProbability")
        
        if pivoted.isna().sum().sum() > 0:
            print(f"Warning: Missing values detected for {with_templates} vs {without_templates}")
            pivoted = pivoted.dropna()
        
        if not pivoted.empty:
            rho, p_value = spearmanr(pivoted[with_templates], pivoted[without_templates])
            spearman_results.append((with_templates, without_templates, rho, p_value))
            
            sns.scatterplot(x=pivoted[with_templates], y=pivoted[without_templates], ax=axes[i])
            # show p-value as scientific notation
            if p_value < 0.001:
                p_value_label = "<0.001"
            else:
                p_value_label = f"{p_value:.3f}"
            axes[i].set_title(f"{with_templates} vs {without_templates}\nSpearman: {rho:.2f}, p={p_value_label}")
            axes[i].set_xlabel("With templates")
            if i == 0:
                axes[i].set_ylabel("Without templates")
            # make sure the aspect ratio is 1:1
            axes[i].set_aspect('equal')
        else:
            print(f"Skipping {with_templates} vs {without_templates} due to lack of data.")
    
    plt.tight_layout()
    plt.savefig(script_dir / 'b_correlation.png', dpi=600)
    plt.savefig(script_dir / 'b_correlation.svg')


def run_friedman_tests():
    df = get_df()
    for (m1, m2) in [
        ("AF3", "AF3 (no templates)"),
        ("RF-AA", "RF-AA (no templates)"),
        ("AF2", "AF2 (no templates)"),
    ]:
        subset = df[df["model"].isin([m1, m2])]
        pivoted = subset.pivot(index="identifier", columns="model", values="InteractionProbability")
        if pivoted.isna().sum().sum() > 0:
            print(f"Warning: Missing values detected for {m1} vs {m2}")
            pivoted = pivoted.dropna()
        
        if not pivoted.empty:
            statistic, p_value = friedmanchisquare(pivoted[m1], pivoted[m2])
            print(f"Friedman test for {m1} vs {m2}: p={p_value:.2f}")
        else:
            print(f"Skipping {m1} vs {m2} due to lack of data.")


def permutation_test(n_permutations=10000):
    """ Run a permutation test instead of Spearman correlation test. """
    df = get_df()
    np.random.seed(42)  # Ensuring reproducibility

    comparisons = [
        ("AF3", "AF3 (no templates)"),
        ("RF-AA", "RF-AA (no templates)"),
        ("AF2", "AF2 (no templates)"),
    ]

    for with_templates, without_templates in comparisons:
        subset = df[df["model"].isin([with_templates, without_templates])]
        pivoted = subset.pivot(index="identifier", columns="model", values="InteractionProbability")
        
        if pivoted.isna().sum().sum() > 0:
            print(f"Warning: Missing values detected for {with_templates} vs {without_templates}")
            pivoted = pivoted.dropna()
        
        if not pivoted.empty:
            # Compute observed Spearman correlation
            observed_rho, _ = spearmanr(pivoted[with_templates], pivoted[without_templates])

            # Generate null distribution by permuting labels
            permuted_rhos = []
            for _ in range(n_permutations):
                shuffled_values = np.random.permutation(pivoted[without_templates].values)
                permuted_rho, _ = spearmanr(pivoted[with_templates], shuffled_values)
                permuted_rhos.append(permuted_rho)

            # Compute p-value (two-tailed test)
            permuted_rhos = np.array(permuted_rhos)
            p_value = (np.sum(np.abs(permuted_rhos) >= np.abs(observed_rho)) + 1) / (n_permutations + 1)

            print(f"Permutation test for {with_templates} vs {without_templates}:")
            print(f"Observed Spearman rho: {observed_rho:.2f}, p={p_value:.9f}")
        else:
            print(f"Skipping {with_templates} vs {without_templates} due to lack of data.")


if __name__ == "__main__":
    sns.set_style("whitegrid")
    sns.set_context("paper")    
    
    plot_correlation()
    # run_friedman_tests()
    permutation_test()
