A personal website for John Honda featuring ASCII art animation, music, and upcoming shows.

### ASCII Art Generation

The ASCII animation works by converting video frames to ASCII art. To create your own animation:

1. Place your video file as `input.mov` in the root directory
2. Run the Python script:

`python script.py`

The script will:

- Extract frames from the video
- Convert each frame to grayscale ASCII art
- Save frames as text files in `public/ascii_frames/`
- Generate 121 frames at 180 characters width

### Development

Start the development server:

`pnpm dev`

The site will be available at `http://localhost:4321`

### Technologies Used

- **Astro**: Static site generator
- **Python**: Video processing and ASCII conversion
- **OpenCV**: Computer vision library for frame extraction
- **Pillow**: Image processing
