# Check which structures are missing from the new dataset

import os
import pandas as pd

# Load the updated dataset and get included PDB codes
df = pd.read_csv('/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30.csv')
pdb_codes = df['pdb'].tolist()
folder = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark"
models = ["AF2", "AF2_no_templates", "RFAA_sm", "RFAA_chain_no_templates", "RFAA_chain", "neuralplexer_chain", "ESMFold", "RFAA_sm", "RFAA_sm_no_templates"]

# Remove structures that are not in the new dataset
for model in models:
    for path in os.listdir(f'{folder}/{model}/'):
        pdb_code = path.split('.')[0].split('_')[0].upper()
        if pdb_code not in pdb_codes and path.endswith('.pdb'):
            if os.path.exists(f'{folder}/{model}/{path}'):
                os.remove(f'{folder}/{model}/{path}')

# Save a text file with the missing structures
af2_models = os.listdir(f'{folder}/{models[0]}/')

df_old = pd.read_csv('/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results.csv')
old_pdbs = df_old['pdb'].tolist()
missing_structures = [pdb_code for pdb_code in pdb_codes if pdb_code not in old_pdbs]
with open('/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/missing_structures.txt', 'w') as f:
    for pdb_code in missing_structures:
        f.write(f'{pdb_code}\n')
