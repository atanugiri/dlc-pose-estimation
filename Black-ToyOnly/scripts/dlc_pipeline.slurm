#!/bin/bash
#SBATCH -A DBS25005                # project allocation code
#SBATCH --job-name=dlc_pipeline
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --partition=gpu-a100       # Use the A100 GPU partition
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --time=02:00:00
#SBATCH --mem=32G

# --- Variables ---
CONFIG_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/config.yaml"
CONDA_ENV="$SCRATCH/miniconda3/envs/dlcfix"
DEVICE="cuda:0"
EPOCHS=200
SHUFFLE=1
TRAININGSETINDEX=0
VIDEOS="$WORK/Black-ToyOnly/videos/*.mp4"
SNAPSHOT_PATH="$WORK/DLC-Black-LightOnly-Atanu-2025-12-13/dlc-models-pytorch/iteration-1/DLC-Black-LightOnlyDec13-trainset95shuffle1/train/snapshot-best-060.pt"
TASK="analyze"  # Options: train, evaluate, analyze, filter, label_video
echo "Job started on $(hostname) at $(date)"

# Initialize environment
source $SCRATCH/miniconda3/etc/profile.d/conda.sh
conda activate "$CONDA_ENV"

echo "Using python: $(which python)"

# Check GPU status before task
echo "GPU status before task:"
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader,nounits

# Change to the project directory to ensure outputs are saved correctly
cd "$WORK/DLC-Black-LightOnly-Atanu-2025-12-13"

# Run DeepLabCut
python <<EOF
import deeplabcut
import glob
videos = glob.glob("$VIDEOS")
videos = videos[:2]  # Uncomment to process only first two videos for testing

if "$TASK" == "train":
    deeplabcut.train_network(
        "$CONFIG_PATH",
        shuffle=$SHUFFLE,
        trainingsetindex=$TRAININGSETINDEX,
        device="$DEVICE",
        max_snapshots_to_keep=5,
        displayiters=100,
        save_epochs=5,
        epochs=$EPOCHS,
        batch_size=8,
        snapshot_path="$SNAPSHOT_PATH"
    )
elif "$TASK" == "evaluate":
    deeplabcut.evaluate_network(
        "$CONFIG_PATH",
        Shuffles=[1,2,3],
        trainingsetindex=$TRAININGSETINDEX,
        gputouse="$DEVICE",
        plotting=True
    )
elif "$TASK" == "analyze":
    deeplabcut.analyze_videos(
        "$CONFIG_PATH",
        videos=videos,
        shuffle=$SHUFFLE,
        trainingsetindex=$TRAININGSETINDEX,
        gputouse="$DEVICE"
    )
elif "$TASK" == "filter":
    deeplabcut.filterpredictions(
        config="$CONFIG_PATH",
        video=videos,
        shuffle=$SHUFFLE,
        save_as_csv=False
    )
elif "$TASK" == "label_video":
    deeplabcut.create_labeled_video(
        config="$CONFIG_PATH",
        videos=videos,
        shuffle=$SHUFFLE,
        filtered=True
    )
else:
    print("Invalid TASK. Set TASK to: train, evaluate, analyze, filter, or label_video")
EOF

# Check GPU status after task
echo "GPU status after task:"
nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader,nounits

echo "Job completed at $(date)"
