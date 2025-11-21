import os
import cv2
from PIL import Image
import json  # Add this import for JSON functionality

# ================= CONFIG =================
VIDEO_PATH = "input.mov"         # your video file
OUTPUT_FOLDER = "ascii_frames"   # where ASCII frames will be saved
NUM_FRAMES = 120                 # target number of frames
NEW_WIDTH = 180                   # width of ASCII art
ASCII_CHARS = "▓▒░johnda "       # dark -> light
# =========================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def resize_image(image, new_width=80):
    height, width = image.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 compensates for character height
    return cv2.resize(image, (new_width, new_height))

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def pixels_to_ascii(image):
    pixels = image.flatten().astype(int)  # convert from uint8 to int
    n_chars = len(ASCII_CHARS)
    chars = [ASCII_CHARS[pixel * (n_chars - 1) // 255] for pixel in pixels]
    return "".join(chars)

def image_to_ascii(image, width=80):
    image = resize_image(image, width)
    image = grayscale(image)
    ascii_str = pixels_to_ascii(image)
    lines = [ascii_str[i:i+image.shape[1]] for i in range(0, len(ascii_str), image.shape[1])]
    return "\n".join(lines)

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_interval = max(1, total_frames // NUM_FRAMES)

frame_idx = 0
saved_idx = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    if frame_idx % frame_interval == 0:
        ascii_art = image_to_ascii(frame, NEW_WIDTH)
        out_path = os.path.join(OUTPUT_FOLDER, f"frame_{saved_idx:03d}.txt")
        with open(out_path, "w") as f:
            f.write(ascii_art)
        saved_idx += 1
    
    frame_idx += 1

cap.release()
print(f"Saved {saved_idx} ASCII frames to '{OUTPUT_FOLDER}'")

# Compile all frames into a single JSON file
frames = []
for i in range(saved_idx):
    frame_path = os.path.join(OUTPUT_FOLDER, f"frame_{i:03d}.txt")
    with open(frame_path, "r") as f:
        frames.append(f.read())

# Save as JSON array
json_path = "ascii_compiled.json"
with open(json_path, "w") as f:
    json.dump(frames, f)

print(f"Compiled {len(frames)} frames into '{json_path}'")