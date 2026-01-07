#!/bin/bash
#SBATCH -A DBS25005                # project allocation code
#SBATCH --job-name=dlc_gpu
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu-a100       # GPU partition
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=00:15:00            # 1.5 hours for 25 videos (analyze ~52 min)
#SBATCH --mem=16G

# --- Variables ---
export CONFIG_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/config.yaml"
export CONDA_ENV="$SCRATCH/miniconda3/envs/dlcfix"
export DEVICE="cuda:0"
export EPOCHS=200
export SHUFFLE=3
export TRAININGSETINDEX=0
export VIDEOS="$WORK/Black-FoodOnly-Atanu-2026-01-06/videos/*.mp4"
export SNAPSHOT_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/dlc-models-pytorch/iteration-3/DLC-Black-LightOnlyDec13-trainset95shuffle3/train/snapshot-best-230.pt"
export TASK="analyze"  # Options: train, evaluate, analyze, all

echo "Job started on $(hostname) at $(date)"

# Initialize environment
source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

# Control thread usage for OpenMP/MKL
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Using python: $(which python)"

# Check GPU status before task
echo "GPU status before task:"
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

# Change to the project directory to ensure outputs are saved correctly
cd "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13"

# Run DeepLabCut pipeline
python "$WORK/Black-FoodOnly-Atanu-2026-01-06/scripts/dlc_pipeline.py"

# Check GPU status after task
echo "GPU status after task:"
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo "Job completed at $(date)"