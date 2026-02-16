#!/usr/bin/env python3
from pathlib import Path

cwd = Path(__file__).parent.resolve()
print(f"Current working directory: {cwd}")
data_dir = cwd.parent / "Black-ToyLight-Atanu-2026-01-22" / "videos"
print(f"Data directory: {data_dir}")

if not data_dir.exists():
    print(f"Data directory does not exist: {data_dir}")
    exit(1)
else:
    print(f"Data directory exists: {data_dir}")
mp4_videos = sorted([f for f in data_dir.iterdir() if f.is_file() and f.suffix == ".mp4"])
first_five = [str(f) for f in mp4_videos[:5]]
# print("First 5 sorted .mp4 videos:")
for idx, v in enumerate(mp4_videos):
    file_path = Path(str(v))
    print(f"{idx}. {file_path.name}")