#!/bin/bash
#SBATCH --job-name=dlc_cpu
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=dgx         # CPU partition (no GPU cost)
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24          # More CPUs for video encoding
#SBATCH --time=00:30:00            # 30 min for filter+label (25 videos ~15 min)
#SBATCH --mem=16G

# --- Variables ---
export CONFIG_PATH="$WORK/Black-FoodLight-Atanu-2026-01-15/config.yaml"
export CONDA_ENV="$SCRATCH/miniconda3/envs/DEEPLABCUT"
export DEVICE="cpu"                # Force CPU (no GPU on this partition)
export SHUFFLE=3
export TRAININGSETINDEX=0
export VIDEOS="$WORK/Black-FoodLight-Atanu-2026-01-15/videos/*.mp4"
export SNAPSHOT_PATH="$WORK/Black-FoodLight-Atanu-2026-01-15/dlc-models-pytorch/\
iteration-3/Black-FoodLightDec13-trainset95shuffle3/train/snapshot-best-230.pt"
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
cd "$WORK/Black-FoodLight-Atanu-2026-01-15"

# Run DeepLabCut pipeline
python "$WORK/scripts/dlc_pipeline.py"

echo "Job completed at $(date)"