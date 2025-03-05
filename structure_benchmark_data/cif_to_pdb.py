import os
import glob 
import numpy as np 
import pandas as pd

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
cif_dir = f"{repo_dir}/structure_benchmark_data/cifs"
pdb_dir = f"{repo_dir}/structure_benchmark_data/pdbs"

# Convert all cif files to pdb files
for cif_file in os.listdir(cif_dir):
    if cif_file.endswith(".cif"):
        pdb_file = cif_file.replace(".cif", ".pdb")
        cif_file = f"{cif_dir}/{cif_file}"
        pdb_file = f"{pdb_dir}/{pdb_file}"
        cif_to_pdb(cif_file, pdb_file)

# Convert AF3 models to pdb files
AF3_server_path = f"{repo_dir}/structure_benchmark/AF3_server"

AF3_models = glob.glob(f"{AF3_server_path}/*/*_model_0.cif")

# List all _model_0.cif files in the AF3 server directory
for cif_file in AF3_models:
    pdb_id = cif_file.split("/")[-2].upper()
    pdb_file = f"{AF3_server_path}/{pdb_id}.pdb"
    cif_to_pdb(cif_file, pdb_file)

# Convert AF3 models to pdb files
AF3_path = f"{repo_dir}/structure_benchmark/AF3"

AF3_models = glob.glob(f"{AF3_path}/*/*_model.cif")
for cif_file in AF3_models:
    pdb_id = cif_file.split("/")[-2].upper()
    pdb_file = f"{AF3_path}/{pdb_id}.pdb"
    #print(pdb_file, cif_file)
    cif_to_pdb(cif_file, pdb_file)

# Convert AF3 models to pdb files
AF3_no_templates_path = f"{repo_dir}/structure_benchmark/AF3_no_templates"
AF3_models = glob.glob(f"{AF3_no_templates_path}/*/*_model.cif")
for cif_file in AF3_models:
    pdb_id = cif_file.split("/")[-2].upper().replace("_NO_TEMPLATES", "")
    pdb_file = f"{AF3_no_templates_path}/{pdb_id}.pdb"
    cif_to_pdb(cif_file, pdb_file)

# Read npz files from folder
npz_dir = f"{repo_dir}/structure_benchmark/Chai-1/"
npz_files = glob.glob(f"{npz_dir}/*/*.npz")
npz_scores = []
for npz_file in npz_files:
    model_id = npz_file.split("/")[-2]
    model_name = npz_file.split("/")[-1]
    # Read npz file
    npz = np.load(npz_file)
    # To dictionary
    npz_dict = dict(npz)
    agg_score = npz_dict["aggregate_score"].item()
    ptm = npz_dict["ptm"].item()
    iptm = npz_dict["iptm"].item()
    npz_scores.append([model_id, model_name, agg_score, ptm, iptm])

chai_results_df = pd.DataFrame(npz_scores, columns=["model_id", "model_name", "aggregate_score", "ptm", "iptm"])
chai_results_df = chai_results_df.sort_values(["model_id", "iptm"], ascending=[True, False])
chai_results_df = chai_results_df.drop_duplicates(subset="model_id", keep="first")

print("\n\n\nChai:\n")
chai_dir = f"{repo_dir}/structure_benchmark/Chai-1"
for index, row in chai_results_df.iterrows():
    model_id = row["model_id"]
    idx = row["model_name"].split("_")[-1].replace(".npz", "")
    model_name = f"pred.model_idx_{idx}.cif"
    cif_file = f"{chai_dir}/{model_id}/{model_name}"
    pdb_file = f"{chai_dir}/{model_id}.pdb"
    cif_to_pdb(cif_file, pdb_file)