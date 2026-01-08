#!/bin/bash
#SBATCH -A DBS25005          # project allocation code for lonestar6
#SBATCH --job-name=dlc_gpu
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu-a100-dev       # GPU partition
## SBATCH --gres=gpu:1          # request 1 GPU only for punakha
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=0:15:00        # 2 hours for training
#SBATCH --mem=16G

# --- Variables ---
export CONFIG_PATH="$WORK/Black-FoodOnly-Atanu-2026-01-06/config.yaml"
export CONDA_ENV="$SCRATCH/miniconda3/envs/dlcfix"
export DEVICE="cuda:0"
export EPOCHS=200
export SHUFFLE=3
export TRAININGSETINDEX=0
export VIDEOS="$WORK/Black-FoodOnly-Atanu-2026-01-06/videos/*.mp4"
export SNAPSHOT_PATH="$WORK/Black-FoodOnly-Atanu-2026-01-06/dlc-models-pytorch/iteration-0/Black-FoodOnlyJan6-trainset95shuffle3/train/snapshot-best-320.pt"
export TASK="evaluate"  # Options: train, evaluate, analyze, all

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
cd "$WORK/Black-FoodOnly-Atanu-2026-01-06"

# Run DeepLabCut pipeline
python "$WORK/Black-FoodOnly-Atanu-2026-01-06/scripts/dlc_pipeline.py"

# Check GPU status after task
echo "GPU status after task:"
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo "Job completed at $(date)"