#!/bin/bash -l
#SBATCH --qos=normal
#SBATCH --partition=standard                                         
#SBATCH --job-name In_pocket
#SBATCH --mem=20G
#SBATCH --ntasks=20
#SBATCH --cpus-per-task=1             
#SBATCH --nodes=1   
#SBATCH --output=/projects/ilfgrid/data/Luuk/Classifier_models/script_logs/i_pocket_%j_out.txt
#SBATCH --error=/projects/ilfgrid/data/Luuk/Classifier_models/script_logs/i_pocket_%j_err.txt

# Print output for SLURM log file
echo -e ">> Running the following command:\n${0} ${@}\n"
echo -e ">> Start time:  $(date)"
echo -e "   Machine:     $(hostname)"
echo -e "   Directory:   $(pwd)"
echo -e "   GPU:         ${SLURM_JOB_GPUS}"
echo -e "   Slurm Array Task ID:  ${SLURM_ARRAY_TASK_ID}"


COMMAND="/projects/ilfgrid/apps/neuralplexer_kcd635/mamba_env/bin/python /projects/ilfgrid/data/Luuk/Classifier_models/rescore_scripts/in_pocket.py"
echo $COMMAND
$COMMAND

end=`date +%s`
runtime=$((end-start))
echo -e "\n>> Job finished at: $(date)"
echo -e "\n>> Runtime: $runtime s"