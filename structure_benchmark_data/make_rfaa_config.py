import pandas as pd
import os
import yaml
from pathlib import Path

def make_rosetta_yaml(job_name, output_path, config_path, protein_inputs, na_inputs, sm_inputs, n_templ = 4):
    '''
    Function to make a YAML file for a RoseTTAFold job with given name, output path, and inputs
    job_name: Name of the job
    output_path: Path to the output directory
    protein_inputs: List of paths to protein fasta files (named as A, B, C, ...)
    na_inputs: List of paths to nucleic acid fasta files (named as A, B, C, ...)
    sm_inputs: List of paths to small molecule files (named as A, B, C, ...)
    '''

    # Start the YAML file with the defaults and job name
    yaml = f"""defaults:\n  - base\njob_name: "{job_name}"\noutput_path: "{output_path}"\n"""

    # Add template information to the YAML file
    yaml += f"\nloader_params:\n  n_templ: {n_templ}\n"
    
    # List of letters from A to Z - used to name the inputs
    letters = [chr(i) for i in range(65, 91)]
    c = 0

    # Add the inputs to the YAML file
    if protein_inputs:
        yaml += "\nprotein_inputs:\n"
        for protein_input in protein_inputs:
            yaml += f"""  {letters[c]}:\n    fasta_file: {protein_input}\n"""
            c += 1
    
    if na_inputs:
        yaml += "\nna_inputs:\n"
        for na_input in na_inputs:
            yaml += f"""  {letters[c]}:\n    fasta: {na_input}\n    input_type: "dna"\n"""
            c += 1

    if sm_inputs:
        yaml += "\nsm_inputs:\n"
        for sm_input in sm_inputs:
            yaml += f"""  {letters[c]}:\n    input: {sm_input}\n    input_type: "{sm_input.split('.')[-1]}"\n"""
            c += 1

    # Save yaml to config path
    config_dir = os.path.dirname(config_path)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    with open(config_path, "w") as f:
        f.write(yaml)

# Load the benchmark set
benchmark_set = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/3f_known_structures_benchmark_2021-09-30.csv"
benchmark_set = pd.read_csv(benchmark_set)

# Get list of already modelled structures
df_old = pd.read_csv('/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data/DockQ_results.csv')
old_pdbs = df_old['pdb'].tolist()

for index, row in benchmark_set.iterrows():

    # Skip structures that have already been modelled
    if row['pdb'] in old_pdbs:
        continue

    # Make a folder for the configs
    config_folder = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/RFAA_configs"
    os.makedirs(config_folder, exist_ok=True)

    # Path to the ILF directory
    ilf_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark"
    fasta_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark_data"

    # Protein inputs
    job_name = f"{row['pdb']}"
    output_path = f"{ilf_path}/RFAA_chain/{job_name}"
    protein_inputs = [f"{fasta_path}/fastas/receptors/{row['pdb']}_receptor.fasta", f"{fasta_path}/fastas/ligands/{row['pdb']}_ligand.fasta"]
    config_path = f"{config_folder}/chain/{job_name}.yaml"
    #make_rosetta_yaml(job_name, output_path, config_path, protein_inputs, None, None)
    
    config_path_no_templates = f"{config_folder}/chain_no_templates/{job_name}_no_templates.yaml"
    output_path = f"{ilf_path}/RFAA_chain_no_templates/{job_name}"
    #make_rosetta_yaml(job_name + "_no_templates", output_path + "_no_templates", config_path_no_templates, protein_inputs, None, None, 0)

    # Small molecule inputs
    job_name = f"{row['pdb']}_sm"
    output_path = f"{ilf_path}/RFAA_sm{job_name}"
    protein_inputs = [f"{fasta_path}/fastas/receptors/{row['pdb']}_receptor.fasta"]
    sm_inputs = [f"{fasta_path}/sdfs/{row['pdb']}_ligand.sdf"]
    config_path = f"{config_folder}/sm/{job_name}.yaml"
    #make_rosetta_yaml(job_name, output_path, config_path, protein_inputs, None, sm_inputs)
    
    config_path_no_templates = f"{config_folder}/sm_no_templates/{job_name}_no_templates.yaml"
    output_path = f"{ilf_path}/RFAA_sm_no_templates/{job_name}"
    #make_rosetta_yaml(job_name + "_no_templates", output_path + "_no_templates", config_path_no_templates, protein_inputs, None, sm_inputs, 0)

# List .yaml files in a folder where name contains "_sm"
def list_sm_yaml_files(folder):
    '''
    Function to list all YAML files in a folder where the name contains "_sm"
    '''
    folder = Path(folder)
    yaml_files = [f for f in folder.iterdir() if f.is_file() and f.suffix == ".yaml" and "_sm" in f.name]
    return yaml_files

def link_rfaa_msas(config_path, msa_db_path):
    
    # Load the YAML file
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    # Path to Rosetta MSA database
    msa_db_path = Path(msa_db_path)

    # Read job name and output path from YAML 
    output_path = data["output_path"]
    job_name = data["job_name"]

    # Loop through protein inputs and link the fasta files to the target path
    for key in data["protein_inputs"].keys():
        
        # Path to the sequence file
        seq_path = data["protein_inputs"][key]["fasta_file"]
        target_path = f"{output_path}/{job_name}/{key}/"
        target_path = Path(target_path)

        # Make sure the target path exists
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # Parse protein name
        protein_name = seq_path.split("/")[-1].split(".")[0]
        protein_name = protein_name.split("_")[0]
        
        # Paths to required MSA files
        out_a3m = msa_db_path / protein_name / protein_name / key / "t000_.msa0.a3m"
        out_atab = msa_db_path / protein_name / protein_name / key / "t000_.atab"
        out_hhr = msa_db_path / protein_name / protein_name / key / "t000_.hhr"

        # Link file to target path
        os.symlink(out_a3m, target_path / "t000_.msa0.a3m")
        os.symlink(out_atab, target_path / "t000_.atab")
        os.symlink(out_hhr, target_path / "t000_.hhr")  

        #print(out_a3m, target_path / "t000_.msa0.a3m")
        #print(out_atab, target_path / "t000_.atab")
        #print(out_hhr, target_path / "t000_.hhr")  

        # Check if out_a3m exist
        if not os.path.exists(out_a3m):
            print(f"{out_a3m} does not exist")

        if not os.path.exists(out_atab):
            print(f"{out_atab} does not exist")

        if not os.path.exists(out_hhr):
            print(f"{out_hhr} does not exist")


msa_db_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/RFAA_chain"

# List yaml files in a folder
yaml_folder = "/projects/ilfgrid/people/pqh443/Git_projects/GPRC_peptide_benchmarking/structure_benchmark/RFAA_configs/chain_no_templates"

# List yaml files
yaml_files = os.listdir(yaml_folder)
yaml_files = [f"{yaml_folder}/{f}" for f in yaml_files if f.endswith(".yaml") ]
print(yaml_files)
for yaml_file in yaml_files:
    link_rfaa_msas(yaml_file, msa_db_path)
