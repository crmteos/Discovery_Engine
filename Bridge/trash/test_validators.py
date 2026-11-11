import json
from pathlib import Path
from datetime import datetime

# Import validators from intake_processor
import sys
sys.path.insert(0, "05_Knowledge_Aggregator")
from intake_processor import _validate_image_metadata, _validate_video_index

# Test image_metadata validator
img_path = "05_Knowledge_Aggregator/Intake_Queue/image_metadata/image_metadata.json"
with open(img_path, "r") as f:
    img_data = json.load(f)
img_errors = _validate_image_metadata(img_data)
print(f"Image metadata errors: {img_errors}")

# Test video_index validator
vid_path = "05_Knowledge_Aggregator/Intake_Queue/video_index/video_index.json"
with open(vid_path, "r") as f:
    vid_data = json.load(f)
vid_errors = _validate_video_index(vid_data)
print(f"Video index errors: {vid_errors}")