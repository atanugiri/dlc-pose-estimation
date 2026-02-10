#!/usr/bin/env python3
"""
Split video files into 4 quadrants based on animal names in filename.

Expected filename format:
    Prefix_Animal1_Animal2_Animal3_Animal4[_TrialN or _Trial_N].mp4
    Examples: 
        - ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial1.mp4
        - ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial_1.mp4
        - ChocolateMilk_07_01_24_S3Y_1_2_3_4.mp4 (digit names supported)

Output format:
    Prefix_AnimalName[_TrialN or _Trial_N].mp4
    Examples:
        - ChocolateMilk_07_01_24_S3Y_Teal_Trial1.mp4
        - ChocolateMilk_07_01_24_S3Y_Orange_Trial_1.mp4
        - ChocolateMilk_07_01_24_S3Y_1.mp4

Quadrant mapping:
    - top_left: Animal1
    - top_right: Animal2
    - bottom_left: Animal3
    - bottom_right: Animal4
"""

import os
import re
import argparse
import subprocess
from pathlib import Path


def parse_filename(filename):
    """
    Parse the video filename to extract prefix and animal names.
    
    Args:
        filename: Base filename without extension
        
    Returns:
        tuple: (prefix, animals_list, trial_suffix) or (None, None, None) if no match
    """
    # Pattern: Prefix_Animal1_Animal2_Animal3_Animal4[_TrialN or _Trial_N]
    # Note: Trial suffix is optional and supports both formats: Trial1 or Trial_1
    # Animal names can be words or digits (e.g., "Teal", "1", "2", etc.)
    
    # First, check for and extract the trial suffix if present
    # Support both Trial1 and Trial_1 formats by making the underscore optional
    trial_match = re.search(r'_(Trial_?\d+)$', filename)
    if trial_match:
        trial_suffix = trial_match.group(1)
        # Remove trial suffix from filename for further parsing
        filename_without_trial = filename[:trial_match.start()]
    else:
        trial_suffix = ""
        filename_without_trial = filename
    
    # Now parse the remaining part: Prefix_Animal1_Animal2_Animal3_Animal4
    # \w+ matches word characters (letters, digits, underscores)
    # This works for animal names like "Teal", "1", "2", "None4", etc.
    match = re.match(r"^(.*)_(\w+_\w+_\w+_\w+)$", filename_without_trial)
    
    if not match:
        return None, None, None
    
    prefix = match.group(1)
    animal_block = match.group(2)
    animals = animal_block.split("_")
    
    return prefix, animals, trial_suffix


def process_video(input_path, output_dir, dry_run=False):
    """
    Process a single video file and split it into quadrants.
    
    Args:
        input_path: Path to input video file
        output_dir: Directory to save output videos
        dry_run: If True, only print what would be done without executing
        
    Returns:
        bool: True if successful, False otherwise
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    
    if not input_path.exists():
        print(f"ERROR: Input file does not exist: {input_path}")
        return False
    
    filename = input_path.name
    base_name = input_path.stem
    
    # Parse filename
    prefix, animals, trial_suffix = parse_filename(base_name)
    
    if prefix is None or animals is None:
        print(f"ERROR: Filename format not recognized: {filename}")
        print(f"Expected format: Prefix_Animal1_Animal2_Animal3_Animal4[_TrialN or _Trial_N].mp4")
        print(f"Examples: ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial1.mp4")
        print(f"          ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial_1.mp4")
        print(f"          ChocolateMilk_07_01_24_S3Y_1_2_3_4.mp4")
        return False
    
    if len(animals) != 4:
        print(f"ERROR: Expected 4 animal names, found {len(animals)}: {animals}")
        return False
    
    # Create output directory if it doesn't exist (unless dry run)
    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Quadrant configurations
    quadrant_labels = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
    crop_filters = {
        'top_left':     "crop=in_w/2:in_h/2:0:0",
        'top_right':    "crop=in_w/2:in_h/2:in_w/2:0",
        'bottom_left':  "crop=in_w/2:in_h/2:0:in_h/2",
        'bottom_right': "crop=in_w/2:in_h/2:in_w/2:in_h/2"
    }
    
    print(f"\nProcessing: {filename}")
    print(f"Prefix: {prefix}")
    print(f"Animals: {animals}")
    if trial_suffix:
        print(f"Trial: {trial_suffix}")
    print(f"Output directory: {output_dir}")
    
    success_count = 0
    
    for label, animal in zip(quadrant_labels, animals):
        # Skip if placeholder or empty
        if not animal or animal.lower() == 'none' or 'none' in animal.lower():
            print(f"  Skipping {label}: {animal} (placeholder)")
            continue
        
        # Build output filename: Prefix_Animal[_Trial].mp4
        if trial_suffix:
            output_filename = f"{prefix}_{animal}_{trial_suffix}.mp4"
        else:
            output_filename = f"{prefix}_{animal}.mp4"
        output_path = output_dir / output_filename
        
        command = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-filter:v", crop_filters[label],
            "-c:a", "copy",  # Copy audio without re-encoding
            str(output_path)
        ]
        
        if dry_run:
            print(f"  [DRY RUN] Would save {label} ({animal}) as: {output_filename}")
            print(f"    Command: {' '.join(command)}")
        else:
            print(f"  Saving {label} ({animal}) as: {output_filename}")
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )
                success_count += 1
            except subprocess.CalledProcessError as e:
                print(f"    ERROR: Failed to process {label}")
                print(f"    {e.stderr.decode()}")
                return False
    
    if dry_run:
        print(f"[DRY RUN] Completed processing: {filename}")
    else:
        print(f"Successfully created {success_count} video(s) from: {filename}")
    
    return True


def process_directory(input_dir, output_dir, dry_run=False):
    """
    Process all .mp4 files in a directory.
    
    Args:
        input_dir: Directory containing .mp4 files
        output_dir: Directory to save output videos
        dry_run: If True, only print what would be done
        
    Returns:
        tuple: (success_count, total_count)
    """
    input_dir = Path(input_dir)
    
    if not input_dir.is_dir():
        print(f"ERROR: Input directory does not exist: {input_dir}")
        return 0, 0
    
    mp4_files = list(input_dir.glob("*.mp4"))
    
    if not mp4_files:
        print(f"No .mp4 files found in: {input_dir}")
        return 0, 0
    
    print(f"Found {len(mp4_files)} video file(s) to process")
    
    success_count = 0
    for video_file in mp4_files:
        if process_video(video_file, output_dir, dry_run):
            success_count += 1
        print()  # Blank line between files
    
    return success_count, len(mp4_files)


def main():
    parser = argparse.ArgumentParser(
        description="Split video files into 4 quadrants based on animal names.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a single file
  python split_animal_videos.py input.mp4 -o output_dir
  
  # Process all videos in a directory
  python split_animal_videos.py input_dir/ -o output_dir -d
  
  # Dry run to see what would be done
  python split_animal_videos.py input.mp4 -o output_dir --dry-run

Expected filename format:
  Prefix_Animal1_Animal2_Animal3_Animal4[_TrialN or _Trial_N].mp4
  Examples: 
    - ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial1.mp4
    - ChocolateMilk_07_01_24_S3Y_Teal_Orange_Cyan_None4_Trial_1.mp4
    - ChocolateMilk_07_01_24_S3Y_1_2_3_4.mp4 (digit names)

Output filename format:
  Prefix_AnimalName[_TrialN or _Trial_N].mp4
  Examples:
    - ChocolateMilk_07_01_24_S3Y_Teal_Trial1.mp4
    - ChocolateMilk_07_01_24_S3Y_Orange_Trial_1.mp4
    - ChocolateMilk_07_01_24_S3Y_1.mp4
        """
    )
    
    parser.add_argument(
        "input",
        help="Input video file (.mp4) or directory containing video files"
    )
    
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output directory for split videos"
    )
    
    parser.add_argument(
        "-d", "--directory",
        action="store_true",
        help="Process all .mp4 files in the input directory"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually processing videos"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_path.exists():
        print(f"ERROR: Input path does not exist: {input_path}")
        return 1
    
    if args.dry_run:
        print("=" * 60)
        print("DRY RUN MODE - No files will be created")
        print("=" * 60)
    
    # Process directory or single file
    if args.directory or input_path.is_dir():
        success, total = process_directory(input_path, output_dir, args.dry_run)
        print("\n" + "=" * 60)
        print(f"Summary: Successfully processed {success}/{total} video(s)")
        print("=" * 60)
        return 0 if success == total else 1
    else:
        # Single file
        success = process_video(input_path, output_dir, args.dry_run)
        return 0 if success else 1


if __name__ == "__main__":
    exit(main())
