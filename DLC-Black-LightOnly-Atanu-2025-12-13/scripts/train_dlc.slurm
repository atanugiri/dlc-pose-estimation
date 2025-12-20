#!/bin/bash
#SBATCH -A DBS25005                # project allocation code
#SBATCH --job-name=dlc_train
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu-a100       # Use the A100 GPU partition
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --time=08:00:00
#SBATCH --mem=64G

# --- Variables ---
CONFIG_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/config.yaml"
CONDA_ENV="$SCRATCH/miniconda3/envs/dlcfix"
DEVICE="cuda:0"
EPOCHS=500
SHUFFLE=1
TRAININGSETINDEX=0

echo "Job started on $(hostname) at $(date)"

# Initialize environment
source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

echo "Using python: $(which python)"

# Change to the project directory to ensure outputs are saved correctly
cd "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13"

# Run DeepLabCut
python <<EOF
import deeplabcut

# deeplabcut.train_network(
#     "$CONFIG_PATH",
#     shuffle=$SHUFFLE,
#     trainingsetindex=$TRAININGSETINDEX,
#     device="$DEVICE",
#     max_snapshots_to_keep=5,
#     displayiters=100,
#     save_epochs=5,
#     epochs=$EPOCHS,
#     batch_size=8,
#     snapshot_path="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/dlc-models-pytorch/iteration-0/DLC-Black-LightOnlyDec13-trainset95shuffle1/train/snapshot-best-050.pt"
# )

deeplabcut.evaluate_network(
    "$CONFIG_PATH",
    Shuffles=[$SHUFFLE],
    trainingsetindex=$TRAININGSETINDEX,
    gputouse="$DEVICE",
    plotting=True
)

# deeplabcut.analyze_videos(
#     "$CONFIG_PATH",
#     ["$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Navy.mp4", 
#     "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Tan.mp4"],
#     shuffle=$SHUFFLE,
#     trainingsetindex=$TRAININGSETINDEX,
#     gputouse="$DEVICE",
# )

# deeplabcut.filterpredictions(
#     "$CONFIG_PATH",
#     ["$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Navy.mp4", 
#     "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Tan.mp4"]
# )

# deeplabcut.create_labeled_video(
#     "$CONFIG_PATH",
#     ["$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Navy.mp4", 
#     "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/videos/LightOnly_11_18_24_S4P_Tan.mp4"],
#     filtered=True
# )
EOF
echo "Job completed at $(date)"