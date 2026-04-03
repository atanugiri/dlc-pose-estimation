#!/bin/bash
#SBATCH --job-name=dlc_gpu
#SBATCH --output=/work/agiri/logs/%x-%j.out
#SBATCH --error=/work/agiri/logs/%x-%j.err
#SBATCH --partition=dgx
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=3:00:00
#SBATCH --mem=16G

set -euo pipefail

mkdir -p "$WORK/logs"
mkdir -p "$WORK/.cache"
mkdir -p "$WORK/pip-cache"
mkdir -p "$WORK/mplconfig"
mkdir -p "$WORK/tmp"
mkdir -p "$WORK/home_fake"

export CONFIG_PATH="$WORK/ElevatedMaze-Atanu-2026-03-25/config.yaml"
export CONDA_ENV="$HOME/miniconda3/envs/DEEPLABCUT"
export DEVICE="cuda:0"
export EPOCHS=200
export SHUFFLE=3
export TRAININGSETINDEX=0
export VIDEOS="$WORK/ElevatedMaze-Atanu-2026-03-25/stitched_video.mp4"
export SNAPSHOT_PATH="$WORK/ElevatedMaze-Atanu-2026-03-25/dlc-models-pytorch/iteration-3/ElevatedMazeMar25-trainset95shuffle3/train/snapshot-best-790.pt"
export TASK="evaluate" # Options: train, evaluate, analyze, all

echo "Job started on $(hostname) at $(date)"

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"

export PIP_CACHE_DIR="$WORK/pip-cache"
export XDG_CACHE_HOME="$WORK/.cache"
export MPLCONFIGDIR="$WORK/mplconfig"
export TMPDIR="$WORK/tmp"
export TMP="$WORK/tmp"
export TEMP="$WORK/tmp"
export HOME="$WORK/home_fake"

export OMP_NUM_THREADS="$SLURM_CPUS_PER_TASK"
export MKL_NUM_THREADS="$SLURM_CPUS_PER_TASK"

cd "$WORK/ElevatedMaze-Atanu-2026-03-25"

echo "Using python: $(which python)"
echo "PWD=$(pwd)"
echo "HOME=$HOME"
echo "XDG_CACHE_HOME=$XDG_CACHE_HOME"
echo "PIP_CACHE_DIR=$PIP_CACHE_DIR"
echo "TMPDIR=$TMPDIR"
echo "MPLCONFIGDIR=$MPLCONFIGDIR"

echo "GPU status before task:"
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

python "$WORK/scripts/dlc_pipeline.py"

echo "GPU status after task:"
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo "Job completed at $(date)"