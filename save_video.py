import cv2
import os
from pathlib import Path
from tqdm import tqdm

# Directory containing images
img_dir = Path("samples/CAM_BACK_RIGHT")
# Output video path
output_path = "cam_back_right_video.mp4"

# Get sorted list of image files (assuming .png, change if needed)
img_files = sorted([f for f in img_dir.iterdir() if f.suffix.lower() in [".png", ".jpg", ".jpeg"]])

if not img_files:
    raise RuntimeError("No images found in samples/CAM_BACK_RIGHT")

# Read the first image to get frame size
frame = cv2.imread(str(img_files[0]))
height, width, layers = frame.shape

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = 24  # Change as needed
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# Add tqdm to track progress
for img_file in tqdm(img_files, desc="Processing images"):
    img = cv2.imread(str(img_file))
    if img is None:
        print(f"Warning: Could not read {img_file}")
        continue
    out.write(img)

out.release()
print(f"Video saved to {output_path}")