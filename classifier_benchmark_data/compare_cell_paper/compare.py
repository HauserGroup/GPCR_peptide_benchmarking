import pandas as pd
import pathlib
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

def run_main():
    script_dir = pathlib.Path(__file__).parent.absolute()
    
    # Read the 'HumanGPCRLigands' sheet
    old_file = script_dir / "mmc1.xlsx"
    old = pd.read_excel(old_file, sheet_name='HumanGPCRLigands')
    old_pa = old[old['type'] == 'Peptide']
    old_pa_set = set(old_pa["EntryName"].unique())
    print(f"Number of GPCRs in 'old': {len(old_pa_set)}")
    
    # Read the new file
    new_file = script_dir.parent / 'output/6_interactions_with_decoys.csv'
    new = pd.read_csv(new_file)
    new_pa = new[new['Acts as agonist'] == True]
    new_pa_set = set(new_pa['Original Target'].unique())
    print(f"Number of GPCRs in 'new': {len(new_pa_set)}")
    
    # Plot Venn diagram
    venn = venn2([old_pa_set, new_pa_set], ('Cell paper', 'New'))
    
    # Annotate the subsets with the actual GPCR names
    venn.get_label_by_id('10').set_text('\n'.join(sorted(old_pa_set - new_pa_set)))
    venn.get_label_by_id('01').set_text('\n'.join(sorted(new_pa_set - old_pa_set)))
    # venn.get_label_by_id('11').set_text('\n'.join(sorted(old_pa_set & new_pa_set)))
    
    # Add a title and display the plot
    plt.title("Venn Diagram of GPCRs")
    plt.savefig(script_dir / "venn_diagram.png", dpi=300)

if __name__ == "__main__":
    run_main()
