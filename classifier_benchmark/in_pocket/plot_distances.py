import pathlib
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from itertools import combinations
from scipy.stats import ttest_rel


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = pd.read_csv(script_dir / "distances.csv")
    plot_p = script_dir / "distances.svg"
    # model,identifier,shortest_distance,agonist
    # ESMFold,vipr2_human___1152,6.243615627288818,True
    # ESMFold,ccr6_human___2257,34.36741638183594,False

    # plot all 'shortest_distance' for each 'model'
    sns.set_theme()
    sns.set_context("paper")
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="model", y="shortest_distance", hue="agonist")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_p)
    plt.close()


if __name__ == "__main__":
    run_main()
