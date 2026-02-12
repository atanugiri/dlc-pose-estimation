#!/usr/bin/env python3
import os
import re
import sys
import argparse

def rename_with_full_path_metadata(file_path, dry_run=False):
    # Get absolute path (keep drive letter)
    full_path = os.path.abspath(file_path)
    # Split extension
    base, ext = os.path.splitext(full_path)
    # Replace ALL non-alphanumeric characters (spaces, slashes, punctuation, etc.) with '_'
    sanitized = re.sub(r'[^A-Za-z0-9]+', '_', base)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    new_name = f"{sanitized}{ext.lower()}"
    # Save in the same directory as the original file
    dir_name = os.path.dirname(file_path)
    new_full_path = os.path.join(dir_name, new_name)
    
    if dry_run:
        print(f"[DRY RUN] Would rename:")
        print(f"  Original: {file_path}")
        print(f"  New filename: {new_name}")
        print(f"  Full path: {new_full_path}")
    else:
        print(f"Original: {file_path}")
        print(f"New filename: {new_name}")
        print(f"Renamed to: {new_full_path}")
        os.rename(file_path, new_full_path)

def rename_all_in_folder(folder_path, extensions=None, dry_run=False):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
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
    
    if not os.path.exists(args.path):
        print(f"Error: Path does not exist: {args.path}")
        sys.exit(1)
    
    if args.dry_run:
        print("=== DRY RUN MODE - No files will be renamed ===\n")
    
    if os.path.isdir(args.path):
        rename_all_in_folder(args.path, extensions=args.extensions, dry_run=args.dry_run)
    else:
        rename_with_full_path_metadata(args.path, dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n=== DRY RUN COMPLETE - No changes were made ===")