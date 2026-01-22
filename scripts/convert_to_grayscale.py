
import os
import glob
import subprocess

def convert_to_grayscale_ffmpeg(input_path, output_path):
    cmd = [
        "ffmpeg",
        "-y",  # overwrite output
        "-i", input_path,
        "-vf", "format=gray,eq=contrast=1.1:brightness=0.1",  # Grayscale with contrast reduction and brightness reduction
        "-c:v", "libx264",  # Re-encode with H.264 for better quality
        "-preset", "medium",  # Balance speed/quality
        "-crf", "20",  # High quality (lower = better, 18-23 range)
        output_path
    ]
    subprocess.run(cmd, check=True)

def batch_convert_ffmpeg(input_dir, output_dir, ext="mp4"):
    os.makedirs(output_dir, exist_ok=True)
    for file in glob.glob(os.path.join(input_dir, f"*.{ext}")):
        filename = os.path.basename(file)
        output_file = os.path.join(output_dir, f"{filename}")
        print(f"Converting {file} -> {output_file}")
        convert_to_grayscale_ffmpeg(file, output_file)

if __name__ == "__main__":
    # Example usage: Convert videos from "videos" to "videos_gray" in the project root
    batch_convert_ffmpeg("videos", "videos_gray", ext="mp4")