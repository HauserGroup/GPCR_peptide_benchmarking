#!/bin/bash -l
#SBATCH --qos=cpu
#SBATCH --partition=cpu_jobs                                        
#SBATCH --job-name AF_LIS
#SBATCH --mem=20G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1             
#SBATCH --nodes=1   
#SBATCH --output=/projects/ilfgrid/people/pqh443/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/subanalyses/%j_out.txt
#SBATCH --error=/projects/ilfgrid/people/pqh443/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/subanalyses/%j_err.txt

log_path="/projects/ilfgrid/people/pqh443/Git_projects/GPCR_peptide_benchmarking/structure_benchmark_data/subanalyses"
module load miniconda
source activate /projects/ilfgrid/apps/alphafold-2.3.1/AF2.3.1_cuda11.8_conda_env
cd $log_path
python calculate_lis.py

# Rename logs
mv ${log_path}/${SLURM_JOB_ID}_out.txt ${log_path}/AF_LIS_log_out.txt
mv ${log_path}/${SLURM_JOB_ID}_err.txt ${log_path}/AF_LIS_log_err.txt
