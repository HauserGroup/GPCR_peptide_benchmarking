""" Plot a piechart displaying the class distribution of our filtered dataset.
"""
import pathlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
import logging


def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    main_dir = script_dir.parent.parent
    structure_dir = main_dir / "structure_benchmark_data"
    known_structs = structure_dir / "3f_known_structures_benchmark_2021-09-30_cleaned.csv"
    known_df = pd.read_csv(known_structs)

    # modify class to "(" -> "\n("
    known_df["class"] = known_df["class"].str.replace("(", "\n(")

    # plot class distribution
    class_distribution = known_df["class"].value_counts()

    # piechart
    plt.figure(figsize=(4, 4))
    plt.pie(class_distribution,
            labels=class_distribution.index,
            # count
            autopct = lambda p: '{:.0f}'.format(p * sum(class_distribution) / 100),
            # increase font size
            labeldistance=1.2,
            startangle=90,
            # reverse
            counterclock=False,
            colors=sns.color_palette("tab10"),
            textprops={'fontsize': 12},
            wedgeprops={'edgecolor': 'black'})
    plt.axis('equal')
    
    plt.title("Complexes per class\n\n",
                 fontsize=16)
    plt.tight_layout()
    # increase labels
    for text in plt.gca().texts:
        text.set_fontsize(15)
    save_path = script_dir / "class_distribution_piechart.png"
    plt.savefig(save_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    run_main()
