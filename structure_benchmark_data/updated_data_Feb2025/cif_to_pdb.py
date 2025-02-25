import os
# Helper script to produce pymol command line commands to convert cif files to pdb files
# Used mainly for large input files that cannot be downloaded from the RCSB website and AF3 models

def cif_to_pdb(cif_file, pdb_file):
    if not os.path.exists(pdb_file):
        command = f'pymol -c -d "load {cif_file}; save {pdb_file}; quit"'
        print(command)

# Get directory where the current script is located
script_dir = os.path.dirname(os.path.realpath(__file__))
folder_name = script_dir.split('/')[-1]
repo_name = "GPCR_peptide_benchmarking"
index = script_dir.find(repo_name)
repo_dir = script_dir[:index + len(repo_name)]

# Input and output directories
cif_dir = f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/cifs"
pdb_dir = f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/pdbs"

# Convert all cif files to pdb files
for cif_file in os.listdir(cif_dir):
    if cif_file.endswith(".cif"):
        pdb_file = cif_file.replace(".cif", ".pdb")
        cif_file = f"{cif_dir}/{cif_file}"
        pdb_file = f"{pdb_dir}/{pdb_file}"
        cif_to_pdb(cif_file, pdb_file)
