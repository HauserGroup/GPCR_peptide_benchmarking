#!/bin/bash -l
#SBATCH --qos=cpu
#SBATCH --partition=cpu_jobs                                         
#SBATCH --job-name APPRAISE_1on1
#SBATCH --mem=20G
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=2          
#SBATCH --nodes=2
#SBATCH --output=/projects/ilfgrid/data/Luuk/APPRAISE_results/logs/wp1_%j_out.txt
#SBATCH --error=/projects/ilfgrid/data/Luuk/APPRAISE_results/logs/wp1_%j_err.txt

# activate the conda environment
# source /projects/ilfgrid/data/Luuk/custom_conda/conda/bin/activate
conda activate /projects/ilfgrid/data/Luuk/Luuk_env/luuk_conda_env

cd /projects/ilfgrid/data/Luuk/APPRAISE

TXT_WITH_PDBS=$1
BASE_OUTPUT_DIR=$2
echo "TXT $TXT_WITH_PDBS"
echo "Base out $BASE_OUTPUT_DIR"
# iterate over each subdirectory in the output directory and echo the name
while read -r PDB_FILE; do
    
    PDB_PARENT_NAME=$(basename "$PDB_FILE" .pdb)

    # define the out dir
    OUT_DIR="$BASE_OUTPUT_DIR/$PDB_PARENT_NAME"
    echo "   Output directory: $OUT_DIR"
    # run the APPRAISE script
    python run_appraise.py -p $PDB_FILE -o $OUT_DIR
    echo "   Done processing $PDB_FILE"


done < "$TXT_WITH_PDBS"
