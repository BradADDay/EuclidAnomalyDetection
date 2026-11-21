#!/bin/bash
# ==============================
# get_data.sh
# ==============================

#SBATCH --job-name=get_euclid_data
#SBATCH --partition=teach_cpu
#SBATCH --account=phys040684
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:0
#SBATCH --mem=100M

cd $SLURM_SUBMIT_DIR

bash get_data.sh -f download.txt
