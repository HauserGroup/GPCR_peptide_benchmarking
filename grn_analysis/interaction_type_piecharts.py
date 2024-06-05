import os 
import sys
import pandas as pd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from get_chosen_grns import get_chosen_grns

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]
repo_dir = file_dir.replace(f'/{folder_name}', '')
plot_dir = f'{file_dir}/plots'
interaction_csv_path = f'{file_dir}/interactions.csv'

# Get the top-level directory
top_level_dir = os.path.abspath(os.path.join(file_dir, '..'))
sys.path.append(top_level_dir)
from colors import * 

# Font path
font_path = f'{repo_dir}/Aptos.ttf'
font_prop = fm.FontProperties(fname=font_path)

def plot_piechart(df, column, output_path = "", title = "", fontprop = ""):

    # Make a pie chart of df column
    x = df[column].value_counts()

    # Make plot bigger
    plt.figure(figsize=(16,7))

    # Get total number of values in column
    total = sum(x)

    # Edit labels - include percentage
    labels = [ f"{i} ({round(int(i)/total*100, 2)} %)" if int(i) > 30 else "" for i in x ]

    # Make a pie chart without labels but add legend
    plt.pie(x, labels = labels)
    plt.legend(labels = x.index, loc="center left", bbox_to_anchor=(1.1, 0, 0.5, 1), prop=fontprop)
    plt.title(title, fontsize = 20, fontweight = 'bold', fontproperties=fontprop)

    # Update font of the pie chart labels
    for text in plt.gca().texts:
        text.set_fontproperties(fontprop)
        
    if output_path != "":
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi = 600) 
    else:
        plt.show()
    plt.close()

# Read in the interactions data
interactions_df = pd.read_csv(interaction_csv_path)

# Plot the interaction types for all generic residue positions
plot_piechart(interactions_df, "interaction_type", output_path=f'{plot_dir}/interaction_types.png', title = "Interaction types of interacting generic residue positions", fontprop = font_prop)

# Plot the interaction types for the chosen generic residue numbers
chosen_grns, _, _ = get_chosen_grns(f"{file_dir}/grn_frequencies.csv", interaction_csv_path)
interactions_chosen_grns = interactions_df[interactions_df["generic_residue_number_a"].isin(chosen_grns)]
plot_piechart(interactions_chosen_grns, "interaction_type", output_path=f"{plot_dir}/interaction_types_chosen_grns.png", title = "Interaction types of the chosen generic residue numbers", fontprop = font_prop)