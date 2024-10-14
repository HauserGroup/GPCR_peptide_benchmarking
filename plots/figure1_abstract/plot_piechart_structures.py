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

    # class A is green
    colors = ["#115185", "#478347", "#A676D6"]

    # make colors 50% transparent
    new_colors=[]
    for c in colors:
        c = sns.set_hls_values(c, l=0.5)
        new_colors.append(c)
    colors = new_colors


    # piechart
    plt.figure(figsize=(4, 4))
    plt.pie(
        class_distribution,
        labels=class_distribution.index,
        autopct=lambda p: '{:.0f}'.format(p * sum(class_distribution) / 100),  # Display count values
        labeldistance=1.2,  # Adjust label distance for clarity
        startangle=90,  # Standardize orientation
        counterclock=False,  # Ensure clockwise ordering for consistency
        colors=colors,  # Use predefined color palette for visualization
        textprops={'fontsize': 12},  # Increase font size for better readability
        wedgeprops={'edgecolor': 'black'},  # Define edge color for visual separation
        # more scientific
        pctdistance=0.85,  # Adjust percentage distance for better alignment
    )
    plt.axis('equal')  # Maintain aspect ratio for a more accurate pie chart representation

    
    plt.title("Complexes per class\n\n",
                 fontsize=16)
    plt.tight_layout()
    # increase labels
    for text in plt.gca().texts:
        text.set_fontsize(15)
    save_path = script_dir / "class_distribution_piechart.svg"
    plt.savefig(save_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    run_main()
