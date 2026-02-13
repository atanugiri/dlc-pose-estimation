#!/usr/bin/env python3
from pathlib import Path
import re
import argparse


def extract_metadata(filename):
    path = Path(filename)
    base = path.stem
    match = re.search(r'(\d+_\d+_\d+_.*)', base)
    if match:
        metadata = match.group(1)
        # Pad the date pattern to two digits each (MM_DD_YY)
        def pad_date(m):
            month, day, year = m.groups()
            return f"{month.zfill(2)}_{day.zfill(2)}_{year.zfill(2)}_"
        metadata = re.sub(r'^(\d+)_(\d+)_(\d+)_', pad_date, metadata)
        # Remove underscore before 'None' if followed by digits (None_4 -> None4)
        metadata = re.sub(r'None_(\d+)', r'None\1', metadata)
        # Remove underscore before 'Trial' if followed by digits (Trial_2 -> Trial2)
        metadata = re.sub(r'Trial_(\d+)$', r'Trial\1', metadata)
        return metadata
    else:
        return base


def rename_keep_metadata(file_path, dry_run=False):
    path = Path(file_path)
    dir_name = path.parent
    filename = path.name
    ext = path.suffix
    new_base = extract_metadata(filename)
    new_name = f"{new_base}{ext}"
    new_full_path = dir_name / new_name
    print(f"Original: {file_path}")
    print(f"New filename: {new_name}")
    print(f"Renamed to: {new_full_path}")
    # Skip renaming if the filename is already the desired one
    if path.resolve() == new_full_path.resolve():
        print("Already named correctly; skipping")
        return
    if dry_run:
        print("Dry-run: would rename (no changes made)")
        return
    path.rename(new_full_path)


def batch_rename_keep_metadata(folder_path, extensions=None, dry_run=False):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv']
    folder = Path(folder_path)
    for file_path in folder.rglob('*'):
        if file_path.is_file() and any(file_path.suffix.lower() == ext for ext in extensions):
            try:
                rename_keep_metadata(file_path, dry_run=dry_run)
            except Exception as e:
                print(f"Failed to rename {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Rename files keeping metadata after date.')
    parser.add_argument('path', help='File or folder path')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Show changes without renaming')
    args = parser.parse_args()

    path = Path(args.path)
    if path.is_dir():
        batch_rename_keep_metadata(path, dry_run=args.dry_run)
    else:
        rename_keep_metadata(path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
