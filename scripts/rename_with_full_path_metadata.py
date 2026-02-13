#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import argparse

def rename_with_full_path_metadata(file_path, dry_run=False):
    # Get absolute path (keep drive letter)
    path = Path(file_path)
    full_path = path.resolve()
    # Split extension
    base = str(full_path.parent / full_path.stem)
    ext = full_path.suffix
    # Replace ALL non-alphanumeric characters (spaces, slashes, punctuation, etc.) with '_'
    sanitized = re.sub(r'[^A-Za-z0-9]+', '_', base)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    new_name = f"{sanitized}{ext.lower()}"
    # Save in the same directory as the original file
    dir_name = path.parent
    new_full_path = dir_name / new_name
    
    if dry_run:
        print(f"[DRY RUN] Would rename:")
        print(f"  Original: {file_path}")
        print(f"  New filename: {new_name}")
        print(f"  Full path: {new_full_path}")
    else:
        print(f"Original: {file_path}")
        print(f"New filename: {new_name}")
        print(f"Renamed to: {new_full_path}")
        path.rename(new_full_path)

def rename_all_in_folder(folder_path, extensions=None, dry_run=False):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv']
    folder = Path(folder_path)
    for file_path in folder.rglob('*'):
        if file_path.is_file() and any(file_path.suffix.lower() == ext for ext in extensions):
            try:
                rename_with_full_path_metadata(file_path, dry_run=dry_run)
            except Exception as e:
                print(f"Failed to rename {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Rename files with full path metadata encoded in the filename.'
    )
    parser.add_argument(
        'path',
        help='File or folder path to rename'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without actually renaming files'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        default=['.mp4', '.avi', '.mov', '.mkv'],
        help='File extensions to process (default: .mp4 .avi .mov .mkv)'
    )
    
    args = parser.parse_args()
    
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path does not exist: {args.path}")
        sys.exit(1)
    
    if args.dry_run:
        print("=== DRY RUN MODE - No files will be renamed ===\n")
    
    if path.is_dir():
        rename_all_in_folder(args.path, extensions=args.extensions, dry_run=args.dry_run)
    else:
        rename_with_full_path_metadata(args.path, dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n=== DRY RUN COMPLETE - No changes were made ===")