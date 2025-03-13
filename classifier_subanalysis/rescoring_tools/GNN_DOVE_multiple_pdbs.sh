#!/bin/bash -l
#SBATCH --qos=prio
#SBATCH --partition=priority                                         
#SBATCH --job-name GNN_DOVE
#SBATCH --mem=20G
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1             
#SBATCH --nodes=1   
#SBATCH --output=/projects/ilfgrid/apps/DOVE/GNN_DOVE_logs/%j_out.txt
#SBATCH --error=/projects/ilfgrid/apps/DOVE/GNN_DOVE_logs/%j_err.txt
#SBATCH --gres=gpu:gtx1080:1

# Usage check
if [ $# -ne 2 ]; then
    echo "Usage: $0 <pdb_list.txt> <output_dir>"
    echo "Example: sbatch /projects/ilfgrid/apps/DOVE/GNN_DOVE_multiple_pdbs.sh /projects/ilfgrid/apps/DOVE/example/multiple.txt /projects/ilfgrid/apps/DOVE/example/multiple_out"
    exit 1
fi
# Input variables
PDB_LIST="$1"
OUTPUT_DIR="$2"
echo "PDB List: $PDB_LIST"
echo "Output Dir: $OUTPUT_DIR"
# validate input file
if [ ! -f "$PDB_LIST" ]; then
    echo "Error: PDB list file not found: $PDB_LIST"
    exit 1
fi
# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# HARDCODED SETTINGS
APP_DIR="/projects/ilfgrid/apps/DOVE/GNN_DOVE"
cd $APP_DIR
ENV_PATH="/projects/ilfgrid/apps/DOVE/GNN_DOVE_env"
# Load Conda Environment
echo "Loading Conda environment: $ENV_PATH"
module load miniconda
source /opt/software/miniconda/py39_23.1/etc/profile.d/conda.sh
conda activate $ENV_PATH
# unset user-specific Python settings
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
unset PYTHONPATH  # Ensures correct environment use
unset PIP_HOME
unset PIP_TARGET
unset PIP_PREFIX
unset PYTHONUSERBASE
export PYTHONNOUSERSITE=1  # Prevents using ~/.local/lib/pythonX.Y/site-packages

# Verify Conda activation
echo ">> Activated Conda environment: $(which python)"

# Get GPU number (required for multi-GPU systems)
GET_GPU_NUMBER=$(echo $CUDA_VISIBLE_DEVICES | cut -d',' -f1)
echo ">> Running on GPU: $GET_GPU_NUMBER"

while read -r PDB_FILE; do
    # Ensure PDB file exists
    if [ ! -f "$PDB_FILE" ]; then
        echo "Error: PDB file not found: $PDB_FILE"
        continue
    fi

    # Detect chain IDs, should be A (receptor), B (peptide)
    if [ -z "$CHAIN1" ] || [ -z "$CHAIN2" ]; then
        echo "Detecting chains from PDB file..."
        CHAINS=$(grep '^ATOM' "$PDB_FILE" | awk '{print $5}' | sort | uniq | tr -d ' ' | tr -d '\n')
        if [ ${#CHAINS} -lt 2 ]; then
            echo "Error: Could not detect two chains in PDB file."
            exit 1
        fi
        CHAIN1=${CHAINS:0:1}
        CHAIN2=${CHAINS:1:1}
        echo "Detected Chains: $CHAIN1, $CHAIN2"
    fi

    # set custom dir
    PDB_PARENT_NAME=$(basename $(dirname "$PDB_FILE"))
    # Create output directory
    PDB_OUT_DIR="$OUTPUT_DIR/$PDB_PARENT_NAME"
    mkdir -p "$PDB_OUT_DIR"

    # Run DeepRank-GNN-esm Prediction
    echo "Running GNN-DOVE prediction..."
    cd $PDB_OUT_DIR
    /projects/ilfgrid/apps/DOVE/GNN_DOVE_env/bin/python3 /projects/ilfgrid/apps/DOVE/GNN_DOVE/main.py --mode=0 -F $PDB_FILE --gpu=$GET_GPU_NUMBER --fold=5
    echo "Done: $PDB_FILE"
    echo "Saved to $PDB_OUT_DIR"

done < "$PDB_LIST"

