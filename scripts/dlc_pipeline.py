#!/usr/bin/env python3
import deeplabcut
import subprocess
import time
import sys
import os
import glob
from pathlib import Path

def nvidia_status(label):
    print(f"=== NVIDIA SMI: {label} ===")
    try:
        subprocess.call("nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits", shell=True)
    except Exception as e:
        print("nvidia-smi failed:", e)

def do_train(config, shuffle, trainingsetindex, device, epochs, snapshot_path):
    print("Starting train:", time.asctime())
    nvidia_status("before train")
    deeplabcut.train_network(
        config,
        shuffle=shuffle,
        trainingsetindex=trainingsetindex,
        device=device,
        max_snapshots_to_keep=1,
        displayiters=100,
        save_epochs=5,
        epochs=epochs,
        batch_size=8,
        snapshot_path=snapshot_path
    )
    nvidia_status("after train")
    print("Completed train:", time.asctime())

def do_evaluate(config, shuffles, trainingsetindex, device):
    print("Starting evaluate:", time.asctime())
    nvidia_status("before evaluate")
    deeplabcut.evaluate_network(
        config,
        Shuffles=shuffles,
        trainingsetindex=trainingsetindex,
        device=device,
        plotting=False
    )
    nvidia_status("after evaluate")
    print("Completed evaluate:", time.asctime())

def do_analyze(config, videos, shuffle, trainingsetindex, device):
    print("Starting analyze:", time.asctime())
    nvidia_status("before analyze")
    deeplabcut.analyze_videos(
        config,
        videos=videos,
        shuffle=shuffle,
        trainingsetindex=trainingsetindex,
        device=device,
        in_random_order=False
    )
    nvidia_status("after analyze")
    print("Completed analyze:", time.asctime())

def do_filter(config, videos, shuffle):
    print("Starting filter:", time.asctime())
    nvidia_status("before filter")
    deeplabcut.filterpredictions(
        config=config,
        video=videos,
        shuffle=shuffle,
        save_as_csv=False
    )
    nvidia_status("after filter")
    print("Completed filter:", time.asctime())

def do_label(config, videos, shuffle):
    print("Starting label_video:", time.asctime())
    nvidia_status("before label_video")
    deeplabcut.create_labeled_video(
        config=config,
        videos=videos,
        shuffle=shuffle,
        filtered=False,
        pcutoff=0.3
    )
    nvidia_status("after label_video")
    print("Completed label_video:", time.asctime())

def main():
    # Get parameters from environment variables
    config_path = os.environ.get("CONFIG_PATH")
    videos_pattern = os.environ.get("VIDEOS")
    shuffle = int(os.environ.get("SHUFFLE", 1))
    trainingsetindex = int(os.environ.get("TRAININGSETINDEX", 0))
    device = os.environ.get("DEVICE", "cuda:0")
    task = os.environ.get("TASK", "all")
    epochs = int(os.environ.get("EPOCHS", 200))
    snapshot_path = os.environ.get("SNAPSHOT_PATH", "")
    
    # Expand video pattern using glob (supports absolute and relative patterns)
    if not videos_pattern:
        print("No VIDEOS pattern provided in environment variable VIDEOS")
        sys.exit(1)
    # If user provided multiple paths, use them directly
    if " " in videos_pattern:
        videos = [str(Path(p)) for p in videos_pattern.split()]
    else:
        # fallback to glob pattern
        matches = glob.glob(videos_pattern)
        videos = sorted([str(Path(p)) for p in matches])
    if not videos:
        print(f"No videos found at: {videos_pattern}")
        sys.exit(1)

    # For testing: limit to first 2 videos (comment out for full run)
    selected_indices = [3,5,7]  #list(range(3))  # Example indices
    videos = [videos[i] for i in selected_indices]
    
    print(f"Found {len(videos)} videos")
    
    try:
        # convert config and snapshot paths to strings when present
        config_arg = str(Path(config_path)) if config_path else ""
        snapshot_arg = str(Path(snapshot_path)) if snapshot_path else ""

        if task == "all":
            do_analyze(config_arg, videos, shuffle, trainingsetindex, device)
           #  do_filter(config_path, videos, shuffle)
            do_label(config_arg, videos, shuffle)
        elif task == "train":
            do_train(config_arg, shuffle, trainingsetindex, device, epochs, snapshot_arg)
        elif task == "evaluate":
            do_evaluate(config_arg, [1, 2, 3], trainingsetindex, device)
        elif task == "analyze":
            do_analyze(config_arg, videos, shuffle, trainingsetindex, device)
        elif task == "filter":
            do_filter(config_arg, videos, shuffle)
        elif task == "label_video":
            do_label(config_arg, videos, shuffle)
        else:
            print("Invalid TASK. Set TASK to: train, evaluate, analyze, filter, label_video, or all")
            sys.exit(1)
    except Exception as e:
        print("Error during DLC pipeline:", e)
        raise

if __name__ == "__main__":
    main()
