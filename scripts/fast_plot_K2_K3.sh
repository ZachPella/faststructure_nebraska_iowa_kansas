#!/bin/bash
#SBATCH --partition=guest
#SBATCH --job-name=faststructure_plot_K2_K3
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=00:30:00
#SBATCH --output=plot_K2_K3.out
#SBATCH --error=plot_K2_K3.err

# 1. Load the faststructure module
module load faststructure/1.0

# 2. Set the backend to 'Agg' to prevent the DISPLAY error
export MPLBACKEND=Agg

# 3. Define the path to the fastStructure plotting utility
DISTRICT_SCRIPT='/util/opt/anaconda/deployed-conda-envs/packages/faststructure/envs/faststructure-1.0/bin/distruct.py'

# 4. Plot K=2
echo "Plotting results for K=2"
K_TO_PLOT=2
INPUT_BASE="faststructure_K${K_TO_PLOT}"
OUTPUT_PDF="Admixture_Plot_K${K_TO_PLOT}.pdf"

/util/opt/anaconda/deployed-conda-envs/packages/faststructure/envs/faststructure-1.0/bin/distruct.py \
    --input=${INPUT_BASE} \
    --output=${OUTPUT_PDF} \
    -K ${K_TO_PLOT}

echo "K=2 plot finished. Output file: $(pwd)/${OUTPUT_PDF}"

# 5. Plot K=3
echo "Plotting results for K=3"
K_TO_PLOT=3
INPUT_BASE="faststructure_K${K_TO_PLOT}"
OUTPUT_PDF="Admixture_Plot_K${K_TO_PLOT}.pdf"

/util/opt/anaconda/deployed-conda-envs/packages/faststructure/envs/faststructure-1.0/bin/distruct.py \
    --input=${INPUT_BASE} \
    --output=${OUTPUT_PDF} \
    -K ${K_TO_PLOT}

echo "K=3 plot finished. Output file: $(pwd)/${OUTPUT_PDF}"

echo "All plots complete!"
