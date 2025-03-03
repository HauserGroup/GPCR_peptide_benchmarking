import pandas as pd
from scipy.stats import wilcoxon
import itertools
from statsmodels.stats.multitest import multipletests
import os
import numpy as np

file_dir = os.path.dirname(__file__)
repo_name = "GPCR_peptide_benchmarking"
index = file_dir.find(repo_name)
repo_dir = file_dir[:index + len(repo_name)]

def round_to_significant_digits(number, significant_digits=3):
    if pd.isnull(number) or not isinstance(number, (int, float)):
        return number
    if number == 0:
        return 0
    else:
        return round(number, significant_digits - int(np.floor(np.log10(abs(number)))) - 1)

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

def get_significance(data, variable, model_col='model', pdb_col='pdb'):
    # Order dataframe by model and then by PDB code
    data = data.sort_values(by=[model_col, pdb_col])

    # Perform pairwise Wilcoxon signed-rank tests between all models
    results = []
    for model1, model2 in itertools.combinations(data[model_col].unique(), 2):
        # Get subset of data for each model
        var1 = data[data[model_col] == model1][[variable, pdb_col, model_col]].dropna()
        var2 = data[data[model_col] == model2][[variable, pdb_col, model_col]].dropna()

        # Merge the two subsets on PDB code
        merged = var1.merge(var2, on=pdb_col, suffixes=(f'_{model1}', f'_{model2}'))

        if merged.shape[0] < 2:
            # Skip if there are not enough data points for the test
            continue

        try:
            stat, p_value = wilcoxon(merged[f'{variable}_{model1}'], merged[f'{variable}_{model2}'])
        except ValueError:
            # Skip this pair if Wilcoxon test fails
            continue

        # Calculate averages and standard errors
        avg_1 = var1[variable].mean()
        se_1 = var1[variable].sem()
        avg_2 = var2[variable].mean()
        se_2 = var2[variable].sem()

        results.append((model1, model2, avg_1, se_1, avg_2, se_2, stat, p_value))

    # Create a DataFrame from the results
    results_df = pd.DataFrame(results, columns=[
        'Model1', 'Model2', f'Model1_Avg_{variable}', f'Model1_SE_{variable}', 
        f'Model2_Avg_{variable}', f'Model2_SE_{variable}', 'Statistic', 'P-value'
    ])

    # Apply Benjamini-Hochberg correction and add corrected p-values to the DataFrame
    if not results_df.empty:
        _, corrected_p_values, _, _ = multipletests(results_df['P-value'], method='fdr_bh')
        results_df['Corrected P-value'] = corrected_p_values

        # Round the p-values and apply the function to create a new column with significance stars
        results_df['P-value'] = results_df['P-value'].apply(lambda x: round(x, 10))
        results_df['Corrected P-value'] = results_df['Corrected P-value'].apply(lambda x: round(x, 10))
        results_df['Significance'] = results_df['Corrected P-value'].apply(significance_stars)

        # Apply function to all numeric columns in the DataFrame
        for col in results_df.columns:
            results_df[col] = results_df[col].apply(lambda x: round_to_significant_digits(x, 4) if pd.to_numeric(x, errors='coerce') is not None else x)

        # Save the results to a CSV file
        results_df.to_csv(f'{repo_dir}/structure_benchmark_data/wilcoxon_results_{variable}.csv', index=False)
    else:
        print(f"No valid comparisons for {variable}")

# Read DockQ data
dockq_path = f"{repo_dir}/structure_benchmark_data/DockQ_results.csv"
data = pd.read_csv(dockq_path)

# Merge with RMSD data and rename model names
rmsd_path = f"{repo_dir}/structure_benchmark_data/subanalyses/receptor_rmsds.csv"
rmsd_df = pd.read_csv(rmsd_path)
data = data.merge(rmsd_df, on=["pdb", "model"])
data["model"] = data["model"].replace({
    "RFAA_no_templates": "RF-AA (no templates)",
    "RFAA": "RF-AA",
    "AF2_no_templates": "AF2 (no templates)",
    "Chai-1_no_MSAs": "Chai-1 (no MSAs)"
})

# Perform Wilcoxon signed-rank tests for DockQ scores
get_significance(data, 'DockQ')

# Perform Wilcoxon signed-rank tests for receptor RMSD values
get_significance(data, 'rmsd')