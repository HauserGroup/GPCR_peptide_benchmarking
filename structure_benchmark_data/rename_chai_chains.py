import os
import pandas as pd

# Build the path to the pdb files
file_dir = os.path.dirname(__file__)
repo_name = "GPRC_peptide_benchmarking" 
repo_dir = file_dir.split(repo_name)[0] + repo_name

# Benchmark data path
structural_benchmark_path = f"{repo_dir}/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30_cleaned.csv"
structural_benchmark_df = pd.read_csv(structural_benchmark_path)
pdbs = set(structural_benchmark_df["pdb"].tolist())

def rename_chains_in_pdb(input_pdb, output_pdb):
    # Open the input PDB file for reading
    with open(input_pdb, 'r') as infile:
        # Open the output PDB file for writing
        with open(output_pdb, 'w') as outfile:
            # Loop over each line in the input PDB file
            for line in infile:
                # Only modify lines that start with 'ATOM' or 'HETATM'
                if line.startswith(('ATOM', 'HETATM')):
                    # Get the current chain identifier (which is in column 22, index 21 in the string)
                    chain_id = line[21]

                    # Rename chain B to A, and C to B
                    if chain_id == 'B':
                        line = line[:21] + 'A' + line[22:]
                    elif chain_id == 'C':
                        line = line[:21] + 'B' + line[22:]

                # Write the (potentially modified) line to the output file
                outfile.write(line)

# Fix Chai models to have AB suffix and change chain B to A and C to B
for model in pdbs:
    for chai_model in ["Chai-1", "Chai-1_no_MSAs"]:
        if "no_MSAs" in chai_model:
            model += "_no_MSAs"
        os.makedirs(f"{repo_dir}/structure_benchmark/{chai_model}/renamed_chains", exist_ok=True)
        input_pdb = f"{repo_dir}/structure_benchmark/{chai_model}/{model}.pdb"
        output_pdb = f"{repo_dir}/structure_benchmark/{chai_model}/renamed_chains/{model}.pdb"
        rename_chains_in_pdb(input_pdb, output_pdb)