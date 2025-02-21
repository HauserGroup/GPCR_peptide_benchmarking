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
    structural_benchmark_df = pd.read_csv(f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/3f_known_structures_benchmark_2021-09-30_updated.csv")

    # Make directory for output yamls
    os.makedirs(f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/RFAA_configs/", exist_ok=True)

    # Loop over the dataframe and make the complex jsons
    for index, row in structural_benchmark_df.iterrows():
        
        # With templates
        job_name = row["pdb"] 
        output_path = f"/projects/ilfgrid/people/pqh443/structural_benchmark_updated/RFAA/{job_name}"
        output_yaml = f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/RFAA_configs/{job_name}.yaml"
        loader_params = {"n_templ": 4}
        protein_inputs = {
            "A": {"fasta_file": f"/projects/ilfgrid/people/pqh443/Git_projects/structure_benchmark_data/updated_data_Feb2025/fastas/receptors/{row['pdb']}_receptor.fasta"},
            "B": {"fasta_file": f"/projects/ilfgrid/people/pqh443/Git_projects/structure_benchmark_data/updated_data_Feb2025/fastas/ligands/{row['pdb']}_ligand.fasta"}
        }
        create_yaml(job_name, output_path, loader_params, protein_inputs, output_yaml)

        # Without templates
        job_name = row["pdb"] + "_no_templates"
        output_path = f"/projects/ilfgrid/people/pqh443/structural_benchmark_updated/RFAA_no_templates/{job_name}"
        output_yaml = f"{repo_dir}/structure_benchmark_data/updated_data_Feb2025/RFAA_configs/{job_name}.yaml"
        loader_params = {"n_templ": 0}
        protein_inputs = {
            "A": {"fasta_file": f"/projects/ilfgrid/people/pqh443/Git_projects/structure_benchmark_data/updated_data_Feb2025/fastas/receptors/{row['pdb']}_receptor.fasta"},
            "B": {"fasta_file": f"/projects/ilfgrid/people/pqh443/Git_projects/structure_benchmark_data/updated_data_Feb2025/fastas/ligands/{row['pdb']}_ligand.fasta"}
        }
        create_yaml(job_name, output_path, loader_params, protein_inputs, output_yaml)
