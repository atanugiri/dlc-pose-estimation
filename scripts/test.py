from pathlib import Path

if __name__ == "__main__":
    test_folder = Path("/Users/atanugiri/Downloads/dlc-pose-estimation/Competition-task/Videos")
    for folder in sorted(test_folder.rglob("*")):
        if folder.is_dir() and any(folder.glob("*.mp4")):
            print(folder)