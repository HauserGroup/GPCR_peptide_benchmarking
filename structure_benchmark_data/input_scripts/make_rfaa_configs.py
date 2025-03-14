# Script to make RF-AA configs for the structural benchmark (with and without templates)
import yaml
import os 
import pandas as pd 

def create_yaml(job_name, output_path, loader_params, protein_inputs, output_yaml):
    data = {
        "defaults": ["base"],
        "job_name": job_name,
        "output_path": output_path
    }
    
    with open(output_yaml, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, width=100)

    with open(output_yaml, "w") as file:
        yaml.dump(data, file, default_flow_style=False, sort_keys=False, width=100)
        file.write("\n")
        yaml.dump({"loader_params": loader_params}, file, default_flow_style=False, sort_keys=False, width=100)
        file.write("\n")
        yaml.dump({"protein_inputs": protein_inputs}, file, default_flow_style=False, sort_keys=False, width=100)


if __name__ == "__main__":
    # Get the directory of the current file and build the path to the repository directory
    file_dir = os.path.dirname(__file__)
    repo_name = "GPCR_peptide_benchmarking"
    index = file_dir.find(repo_name)
    repo_dir = file_dir[:index + len(repo_name)]

    # Load the classifier benchmark dataset
    structural_benchmark_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/structural_benchmark_dataset.csv")

    # Make directory for output yamls
    yaml_dir = f"{repo_dir}/structure_benchmark_data/fastas/RFAA_configs/"
    os.makedirs(yaml_dir, exist_ok=True)

    # Path to git repo on cluster
    ilf_path = "/projects/ilfgrid/people/pqh443/Git_projects/GPCR_peptide_benchmarking"
    output_dir = "/projects/ilfgrid/people/pqh443/structural_benchmark_updated"

    # Loop over the dataframe and make the complex jsons
    for index, row in structural_benchmark_df.iterrows():
        
        # With templates
        job_name = row["pdb"] 
        output_path = f"{output_dir}/RFAA/{job_name}"
        output_yaml = f"{yaml_dir}/{job_name}.yaml"
        loader_params = {"n_templ": 4}
        protein_inputs = {
            "A": {"fasta_file": f"{ilf_path}/structure_benchmark_data/fastas/receptors/{row['pdb']}_receptor.fasta"},
            "B": {"fasta_file": f"{ilf_path}/structure_benchmark_data/fastas/ligands/{row['pdb']}_ligand.fasta"}
        }
        create_yaml(job_name, output_path, loader_params, protein_inputs, output_yaml)

        # Without templates
        job_name = row["pdb"] + "_no_templates"
        output_path = f"{output_dir}/RFAA_no_templates/{job_name}"
        output_yaml = f"{yaml_dir}/{job_name}.yaml"
        loader_params = {"n_templ": 0}
        protein_inputs = {
            "A": {"fasta_file": f"{ilf_path}/structure_benchmark_data/fastas/receptors/{row['pdb']}_receptor.fasta"},
            "B": {"fasta_file": f"{ilf_path}/structure_benchmark_data/fastas/ligands/{row['pdb']}_ligand.fasta"}
        }
        create_yaml(job_name, output_path, loader_params, protein_inputs, output_yaml)
