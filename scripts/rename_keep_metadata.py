import os
import re
import argparse


def extract_metadata(filename):
    base = os.path.splitext(filename)[0]
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
    dir_name = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1]
    new_base = extract_metadata(filename)
    new_name = f"{new_base}{ext}"
    new_full_path = os.path.join(dir_name, new_name)
    print(f"Original: {file_path}")
    print(f"New filename: {new_name}")
    print(f"Renamed to: {new_full_path}")
    # Skip renaming if the filename is already the desired one
    if os.path.abspath(file_path) == os.path.abspath(new_full_path):
        print("Already named correctly; skipping")
        return
    if dry_run:
        print("Dry-run: would rename (no changes made)")
        return
    os.rename(file_path, new_full_path)


def batch_rename_keep_metadata(folder_path, extensions=None, dry_run=False):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    rename_keep_metadata(file_path, dry_run=dry_run)
                except Exception as e:
                    print(f"Failed to rename {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Rename files keeping metadata after date.')
    parser.add_argument('path', help='File or folder path')
    parser.add_argument('-n', '--dry-run', action='store_true', help='Show changes without renaming')
    args = parser.parse_args()

    path = args.path
    if os.path.isdir(path):
        batch_rename_keep_metadata(path, dry_run=args.dry_run)
    else:
        rename_keep_metadata(path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
