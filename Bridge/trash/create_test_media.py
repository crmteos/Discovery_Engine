#!/usr/bin/env python3
"""Create test media stub files for media extractors."""
import os
from pathlib import Path

# Create test image stub (SVG)
images_dir = Path("05_Knowledge_Aggregator/Intake_Queue/media/images")
images_dir.mkdir(parents=True, exist_ok=True)

svg_content = b"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="1920" height="1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="white"/>
  <circle cx="960" cy="540" r="100" fill="blue"/>
  <text x="960" y="540" font-family="Arial" font-size="24" fill="white">Sample Diagram</text>
</svg>"""

(images_dir / "sample_diagram.png").write_bytes(svg_content)
print(f"Created test image: {images_dir / 'sample_diagram.png'}")

# Create test video stub (binary placeholder)
videos_dir = Path("05_Knowledge_Aggregator/Intake_Queue/media/videos")
videos_dir.mkdir(parents=True, exist_ok=True)

video_content = b"FAKE_MP4_FILE_CONTENT_FOR_TESTING_MEDIA_EXTRACTOR_PROCESSING"
(videos_dir / "sample_lecture.mp4").write_bytes(video_content)
print(f"Created test video: {videos_dir / 'sample_lecture.mp4'}")

print("Test media files created successfully.")