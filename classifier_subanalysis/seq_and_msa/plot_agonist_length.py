""" Plot agonist length distributions
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import sys


def get_agonist_len(s : str):
    return int(s.split("|")[1].split(":")[1])


def main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    df = pd.read_csv(script_dir / "combined.csv")
    print(df)    
    #               identifier  msa_dim0  msa_dim1  num_templates  num_alignments chain_lengths msa_seq_lengths
    # 0      cckar_human___864      2065       436              1            2065     1:428|2:8     1:1248|2:18
    
    # get the length of the agonists. Agonist is chain 2
    # 1:428|2:8 -> 8
    df["agonist_length"] = df["chain_lengths"].apply(get_agonist_len)
    
    # plot agonist len distribution
    sns.histplot(df["agonist_length"])
    plt.savefig(script_dir / "agonist_length_distribution.png")
    plt.close()

if __name__ == "__main__":
    main()
    print("Done.")
