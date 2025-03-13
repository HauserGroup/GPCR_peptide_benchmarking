#!/bin/bash -l
#SBATCH --qos=cpu
#SBATCH --partition=cpu_jobs                                         
#SBATCH --job-name DeepRank_GNN_esm
#SBATCH --mem=32G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8  
#SBATCH --nodes=1   
#SBATCH --output=/projects/ilfgrid/apps/DeepRank/logs/jobs/%j_out.txt
#SBATCH --error=/projects/ilfgrid/apps/DeepRank/logs/jobs/%j_err.txt

# Usage check
if [ $# -ne 2 ]; then
    echo "Usage: $0 <pdb_list.txt> <output_dir>"
    echo "Example: $0 pdb_list.txt /projects/ilfgrid/apps/DeepRank/results"
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
ENV_PATH="/projects/ilfgrid/apps/DeepRank/DeepRank_GNN_esm_env"
APP_DIR="/projects/ilfgrid/apps/DeepRank/DeepRank-GNN-esm"
# Set working directory to APP_DIR
cd $APP_DIR
# Load Conda Environment
echo "Loading Conda environment: $ENV_PATH"
module load miniconda
source /opt/software/miniconda/py39_23.1/etc/profile.d/conda.sh
conda activate $ENV_PATH
# Optimize CPU threading
export OMP_NUM_THREADS=8
export CUDA_VISIBLE_DEVICES=""  # Prevents CUDA-related errors in a CPU environment
unset PYTHONPATH  # Ensures correct environment use
unset PIP_HOME
unset PIP_TARGET
unset PIP_PREFIX
unset PYTHONUSERBASE
export PYTHONNOUSERSITE=1  # Prevents using ~/.local/lib/pythonX.Y/site-packages
# Verify Conda activation
echo ">> Activated Conda environment: $(which python)"


# iterate over each PDB file in the list
while read -r PDB_FILE; do
    # Ensure PDB file exists
    if [ ! -f "$PDB_FILE" ]; then
        echo "Error: PDB file not found: $PDB_FILE"
        continue
    fi
    echo "=============================================="
    echo "Processing PDB file: $PDB_FILE"
    # Get (only the) parent directory name
    PDB_PARENT_NAME=$(basename $(dirname "$PDB_FILE"))
    # Create output directory
    PDB_OUT_DIR="$OUTPUT_DIR/$PDB_PARENT_NAME"
    mkdir -p "$PDB_OUT_DIR"

    # Get the first 2 chains automatically
    echo "   Detecting chains from PDB file..."
    CHAINS=$(grep '^ATOM' "$PDB_FILE" | awk '{print $5}' | sort | uniq | tr -d ' ' | tr -d '\n')
    if [ ${#CHAINS} -lt 2 ]; then
        echo "Error: Could not detect two chains in PDB file."
        exit 1
    fi
    CHAIN1=${CHAINS:0:1}
    CHAIN2=${CHAINS:1:1}
    echo "   Detected Chains: $CHAIN1, $CHAIN2"

    # # Run DeepRank-GNN-esm Prediction
    echo "   Running DeepRank-GNN-esm..."
    # deeprank-gnn-esm-predict "$PDB_FILE" "$CHAIN1" "$CHAIN2" "$PRETRAINED_MODEL"
    deeprank-gnn-esm-predict "$PDB_FILE" "$CHAIN1" "$CHAIN2" --output_dir "$PDB_OUT_DIR"
    echo "   Output saved to: $PDB_OUT_DIR"
    echo "=============================================="

done < "$PDB_LIST"

echo "All PDB files processed."

