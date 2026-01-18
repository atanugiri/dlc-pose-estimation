import os
from pathlib import Path

cwd = Path(__file__).parent.resolve()
print(f"Current working directory: {cwd}")
data_dir = cwd.parent / "Black-FoodLight-Atanu-2026-01-15" / "videos"
print(f"Data directory: {data_dir}")

if not data_dir.exists():
    print(f"Data directory does not exist: {data_dir}")
    exit(1)
else:
    print(f"Data directory exists: {data_dir}")

for v in sorted(data_dir.iterdir()):
    print(f"Found file: {v.name}")