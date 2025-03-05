#!/bin/bash -l
#SBATCH --qos=prio
#SBATCH --partition=priority
#SBATCH --job-name neuralplexer
#SBATCH --mem=40G
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --output=/projects/ilfgrid/people/pqh443/temp/logs/%j_out.txt
#SBATCH --error=/projects/ilfgrid/people/pqh443/temp/logs/%j_err.txt
#SBATCH --gres=gpu:a100:1

module load mamba

# Set the directory for mamba to store packages, avoiding the use of your home directory
export CONDA_PKGS_DIRS=/projects/ilfgrid/apps/neuralplexer_kcd635/.conda/pkgs
# Optionally, set the root prefix for mamba to fully isolate its operations (not always necessary)
export MAMBA_ROOT_PREFIX=/projects/ilfgrid/apps/neuralplexer_kcd635/mamba_root

# HARDCODED PATHS ========================================
INSTALL_DIR="/projects/ilfgrid/apps/neuralplexer_kcd635"
NP_DIR="${INSTALL_DIR}/NeuralPLexer"
ENV_DIR="${INSTALL_DIR}/mamba_env"
MODEL_P="/projects/ilfgrid/apps/neuralplexer_kcd635/data/neuralplexermodels_downstream_datasets_predictions/models/complex_structure_prediction.ckpt"
# ========================================================

# activate the conda environment
module load miniconda
conda activate "${ENV_DIR}"

# add the dir to the python path
export PYTHONPATH="${NP_DIR}:${PYTHONPATH}"
# add af_common too
export PYTHONPATH="${NP_DIR}/af_common:${PYTHONPATH}"
# add pytorch3d to the python path
# /projects/ilfgrid/apps/neuralplexer_kcd635/NeuralPLexer/pytorch3d
export PYTHONPATH="${NP_DIR}/pytorch3d:${PYTHONPATH}"

# Text file containing fasta paths as input
FASTA_FILE=$1

# Output folder
output_folder="/projects/ilfgrid/people/pqh443/structural_benchmark_updated/NeuralPLexer"

# Loop over the fasta path file
while IFS= read -r fasta_path; do
    start_time=$(date +%s)
    fasta_name=$(basename "$fasta_path" .fasta)
    receptor_seq=$(grep -A1 "_receptor" "$fasta_path" | tail -n1)
    ligand_seq=$(grep -A1 "_ligand" "$fasta_path" | tail -n1)

    # Create a folder for each fasta file
    mkdir -p "${output_folder}/${fasta_name}"
    echo -e "\n\n\nProcessing $fasta_name"
    echo -e "Receptor: $receptor_seq"
    echo -e "Ligand: $ligand_seq\n"

    # Launch the NeuralPLexer command
    /projects/ilfgrid/apps/neuralplexer_kcd635/mamba_env/bin/python '/projects/ilfgrid/apps/neuralplexer_kcd635/NeuralPLexer/neuralplexer/inference_patch.py' \
        --task 'batched_structure_sampling' \
        --sampler 'langevin_simulated_annealing' \
        --model-checkpoint '/projects/ilfgrid/apps/neuralplexer_kcd635/data/neuralplexermodels_downstream_datasets_predictions/models/complex_structure_prediction.ckpt' \
        --num-steps=40 \
        --chunk-size 4 \
        --n-samples 16 \
        --confidence \
        --input-receptor "${receptor_seq}|${ligand_seq}" \
        --out-path "${output_folder}/${fasta_name}"
    
    # Track the runtime in the log file
    end_time=$(date +%s)
    runtime=$((end_time - start_time))
    echo -e "Processed $fasta_name in $runtime seconds"
done < "$FASTA_FILE"

# Move log files to output folder
mv /projects/ilfgrid/people/pqh443/temp/logs/${SLURM_JOB_ID}_out.txt "${output_folder}/NeuralPLexer_log_out.txt"
mv /projects/ilfgrid/people/pqh443/temp/logs/${SLURM_JOB_ID}_err.txt "${output_folder}/NeuralPLexer_log_err.txt"

