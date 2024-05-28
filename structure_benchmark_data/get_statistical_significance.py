import pandas as pd
from scipy.stats import wilcoxon
import itertools
from statsmodels.stats.multitest import multipletests

dockq_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results_new.csv"
data = pd.read_csv(dockq_path)

# Prepare a list to store Wilcoxon test results
wilcoxon_results = []
models = data['model'].unique()

# Order dataframe by model and then by PDB code
data = data.sort_values(by=['model', 'pdb'])

# Perform pairwise Wilcoxon signed-rank tests between all models
for model1, model2 in itertools.combinations(models, 2):

    print(data[data['model'] == model1]["pdb"])
    print(data[data['model'] == model2]["pdb"])

    dockq1 = data[data['model'] == model1]['DockQ']
    dockq2 = data[data['model'] == model2]['DockQ']
    
    # Ensure the lengths of both series are equal for paired test
    min_length = min(len(dockq1), len(dockq2))
    dockq1 = dockq1.iloc[:min_length]
    dockq2 = dockq2.iloc[:min_length]

    stat, p_value = wilcoxon(dockq1, dockq2)
    wilcoxon_results.append((model1, model2, stat, p_value))

# Create a DataFrame from the results
wilcoxon_results_df = pd.DataFrame(wilcoxon_results, columns=['Model1', 'Model2', 'Statistic', 'P-value'])

# Apply Benjamini-Hochberg correction
_, corrected_p_values, _, _ = multipletests(wilcoxon_results_df['P-value'], method='fdr_bh')

# Add corrected p-values to the DataFrame
wilcoxon_results_df['Corrected P-value'] = corrected_p_values
print(wilcoxon_results_df.head())
