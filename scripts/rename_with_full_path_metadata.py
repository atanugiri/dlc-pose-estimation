import os
import re
import sys

def rename_with_full_path_metadata(file_path):
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
    print(f"Original: {file_path}")
    print(f"New filename: {new_name}")
    print(f"Renamed to: {new_full_path}")
    os.rename(file_path, new_full_path)

def rename_all_in_folder(folder_path, extensions=None):
    if extensions is None:
        extensions = ['.mp4', '.avi', '.mov', '.mkv']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    rename_with_full_path_metadata(file_path)
                except Exception as e:
                    print(f"Failed to rename {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_with_full_path_metadata.py <file_path or folder_path>")
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            rename_all_in_folder(path)
        else:
            rename_with_full_path_metadata(path)