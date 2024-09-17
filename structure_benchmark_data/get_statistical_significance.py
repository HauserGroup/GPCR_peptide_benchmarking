import pandas as pd
from scipy.stats import wilcoxon
import itertools
from statsmodels.stats.multitest import multipletests
import os 
# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
folder_name = file_dir.split('/')[-1]

repo_name = "GPRC_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Make model names more readable
data["model"] = data["model"].replace("RFAA_no_templates", "RF-AA (no templates)")
data["model"] = data["model"].replace("RFAA", "RF-AA")
data["model"] = data["model"].replace("AF2_no_templates", "AF2 (no templates)")
data["model"] = data["model"].replace("Chai-1_no_MSAs", "Chai-1 (no MSAs)")

# Prepare a list to store Wilcoxon test results
wilcoxon_results = []
models = data['model'].unique()

# Order dataframe by model and then by PDB code
data = data.sort_values(by=['model', 'pdb'])

# Perform pairwise Wilcoxon signed-rank tests between all models
for model1, model2 in itertools.combinations(models, 2):

    # Get subset of data for each model
    dockq1 = data[data['model'] == model1][['DockQ', 'pdb', 'model']]
    dockq2 = data[data['model'] == model2][['DockQ', 'pdb', 'model']]
    # Merge the two subsets on PDB code
    merged = dockq1.merge(dockq2, on='pdb', suffixes=(f'_{model1}', f'_{model2}'))
    stat, p_value = wilcoxon(merged[f'DockQ_{model1}'], merged[f'DockQ_{model2}'])
    wilcoxon_results.append((model1, model2, stat, p_value))

# Create a DataFrame from the results
wilcoxon_results_df = pd.DataFrame(wilcoxon_results, columns=['Model1', 'Model2', 'Statistic', 'P-value'])

# Apply Benjamini-Hochberg correction
_, corrected_p_values, _, _ = multipletests(wilcoxon_results_df['P-value'], method='fdr_bh')

# Add corrected p-values to the DataFrame
wilcoxon_results_df['Corrected P-value'] = corrected_p_values

# Round the p-values to 4 numbers
wilcoxon_results_df['P-value'] = wilcoxon_results_df['P-value'].apply(lambda x: round(x, 10) if x < 1 else round(x, 3))
wilcoxon_results_df['Corrected P-value'] = wilcoxon_results_df['Corrected P-value'].apply(lambda x: round(x, 10) if x < 1 else round(x, 3))

# Define a function to assign significance stars based on p-value
def significance_stars(p):
    if p < 0.0001:
        return '****'
    elif p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'ns'



# Apply the function to create a new column with significance stars
wilcoxon_results_df['Significance'] = wilcoxon_results_df['Corrected P-value'].apply(significance_stars)

# Save the results to a CSV file
wilcoxon_results_df.to_csv(f'{repo_dir}/structure_benchmark_data/wilcoxon_results.csv', index=False)

