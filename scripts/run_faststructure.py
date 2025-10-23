#!/bin/bash
#SBATCH --partition=guest
#SBATCH --job-name=FastStr_K1-10
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=10G
#SBATCH --time=1-00:00:00
#SBATCH --array=1-10
#SBATCH --output=faststructure_K%a.out
#SBATCH --error=faststructure_K%a.err

WORKING_DIR=/work/fauverlab/zachpella/structure_no_threader_but_k10_r10_our_data_only/faststructure_files
OUTDIR=${WORKING_DIR}/faststructure_results
INPUT_FILE=${WORKING_DIR}/input_for_faststructure

mkdir -p ${OUTDIR}
cd ${WORKING_DIR}

K=${SLURM_ARRAY_TASK_ID}
SEED=$((29092025 + K))

echo "Starting fastStructure run on $HOSTNAME"
echo "K value: ${K}, Task ID: ${SLURM_ARRAY_TASK_ID}, Seed: ${SEED}"
echo "Input file: ${INPUT_FILE}"

# --- Execution ---
module load faststructure/1.0

/util/opt/anaconda/deployed-conda-envs/packages/faststructure/envs/faststructure-1.0/bin/structure.py \
    -K ${K} \
    --input=${INPUT_FILE} \
    --output=${OUTDIR}/faststructure_K${K} \
    --format=str \
    --seed=${SEED} \
    --full

echo "Finished K=${K}"
echo "Output files: ${OUTDIR}/faststructure_K${K}.${K}.*"
