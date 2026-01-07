#!/bin/bash
#SBATCH -A DBS25005                # project allocation code
#SBATCH --job-name=dlc_cpu
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=normal         # CPU partition (no GPU cost)
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8          # More CPUs for video encoding
#SBATCH --time=00:30:00            # 30 min for filter+label (25 videos ~15 min)
#SBATCH --mem=16G

# --- Variables ---
export CONFIG_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/config.yaml"
export CONDA_ENV="$SCRATCH/miniconda3/envs/dlcfix"
export DEVICE="cpu"                # Force CPU (no GPU on this partition)
export SHUFFLE=3
export TRAININGSETINDEX=0
export VIDEOS="$WORK/Black-FoodOnly-Atanu-2026-01-06/videos/*.mp4"
export TASK="filter"               # Options: filter, label_video

echo "Job started on $(hostname) at $(date)"

# Initialize environment
source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

# Control thread usage for OpenMP/MKL
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Using python: $(which python)"

# Change to the project directory to ensure outputs are saved correctly
cd "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13"

# Run DeepLabCut pipeline
python "$WORK/Black-ToyOnly/scripts/dlc_pipeline.py"

echo "Job completed at $(date)"