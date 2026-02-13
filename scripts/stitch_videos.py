#!/usr/bin/env python3
"""
Stitch (concatenate) all videos in a folder into a single output video using ffmpeg.
"""

from pathlib import Path
import subprocess
import tempfile
import argparse


def stitch_videos(input_folder, output_folder=None, output_name='stitched_video', ext='mp4',
                  fast_mode=False, target_width=None, target_height=None, target_fps=None):
    """
    Concatenate all videos in input_folder into a single video.
    
    Args:
        input_folder: Path to folder containing videos to stitch
        output_folder: Path to output folder (default: same as input_folder)
        output_name: Output filename without extension (default: 'stitched_video')
        ext: Video file extension to search for (default: 'mp4')
        fast_mode: Use -c copy (no re-encoding) - only if all videos match (default: False)
        target_width: Target width for re-encoding (default: use first video's width)
        target_height: Target height for re-encoding (default: use first video's height)
        target_fps: Target fps for re-encoding (default: use first video's fps)
    
    Returns:
        Path to the created output video
    """
    # Set output folder to input folder if not specified
    if output_folder is None:
        output_folder = input_folder
    
    input_path = Path(input_folder)
    output_path_dir = Path(output_folder)
    
    # Ensure output directory exists
    output_path_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all video files in input folder
    video_files = sorted(input_path.glob(f"*.{ext}"))
    
    if not video_files:
        raise ValueError(f"No .{ext} files found in {input_folder}")
    
    print(f"Found {len(video_files)} video(s) to stitch:")
    for i, video in enumerate(video_files, 1):
        print(f"  {i}. {video.name}")
    
    # Create output path
    output_path = output_path_dir / f"{output_name}.{ext}"
    
    # Create temporary file list for ffmpeg concat demuxer
    # This is the safest method that preserves quality
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        for video in video_files:
            # Use absolute paths and escape special characters
            abs_path = video.resolve()
            f.write(f"file '{abs_path}'\n")
        filelist_path = f.name
    
    try:
        # Build ffmpeg command based on mode
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output file
            "-f", "concat",
            "-safe", "0",
            "-i", filelist_path,
        ]
        
        if fast_mode:
            # Fast mode: copy streams without re-encoding
            print("\nUsing fast mode (-c copy) - assumes all videos have matching properties")
            cmd.extend(["-c", "copy"])
        else:
            # Re-encode mode: handle different resolutions, fps, codecs
            print("\nUsing re-encode mode (handles different resolutions/fps/codecs)")
            
            # Get properties from first video if not specified
            if target_width is None or target_height is None or target_fps is None:
                probe_cmd = [
                    "ffprobe", "-v", "error",
                    "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,r_frame_rate",
                    "-of", "csv=p=0",
                    str(video_files[0])
                ]
                result = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
                parts = result.stdout.strip().split(',')
                
                if target_width is None:
                    target_width = int(parts[0])
                if target_height is None:
                    target_height = int(parts[1])
                if target_fps is None:
                    # Parse fraction like "30/1" or "30000/1001"
                    fps_str = parts[2]
                    if '/' in fps_str:
                        num, den = fps_str.split('/')
                        target_fps = int(num) / int(den)
                    else:
                        target_fps = float(fps_str)
            
            print(f"  Target: {target_width}x{target_height} @ {target_fps:.2f}fps")
            
            # Add re-encoding parameters
            cmd.extend([
                "-vf", f"scale={target_width}:{target_height}",
                "-r", str(target_fps),
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",  # Good quality (lower = better, 18-28 range)
                "-pix_fmt", "yuv420p",  # Ensure compatibility
            ])
        
        cmd.append(str(output_path))
        
        print(f"\nStitching videos into: {output_path}")
        subprocess.run(cmd, check=True)
        print(f"✓ Successfully created {output_path}")
        
        return str(output_path)
        
    finally:
        # Clean up temporary file
        temp_path = Path(filelist_path)
        if temp_path.exists():
            temp_path.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Stitch (concatenate) all videos in a folder into a single video",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "input_folder",
        help="Path to folder containing videos to stitch"
    )
    parser.add_argument(
        "--output-folder", "-o",
        help="Path to output folder (default: same as input folder)"
    )
    parser.add_argument(
        "--output-name", "-n",
        default="stitched_video",
        help="Output filename without extension"
    )
    parser.add_argument(
        "--ext", "-e",
        default="mp4",
        help="Video file extension to search for"
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use fast mode (-c copy). Only works if all videos have identical codec/resolution/fps"
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Target width for re-encoding (default: use first video's width)"
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Target height for re-encoding (default: use first video's height)"
    )
    parser.add_argument(
        "--fps",
        type=float,
        help="Target fps for re-encoding (default: use first video's fps)"
    )
    
    args = parser.parse_args()
    
    try:
        stitch_videos(
            input_folder=args.input_folder,
            output_folder=args.output_folder,
            output_name=args.output_name,
            ext=args.ext,
            fast_mode=args.fast,
            target_width=args.width,
            target_height=args.height,
            target_fps=args.fps
        )
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
