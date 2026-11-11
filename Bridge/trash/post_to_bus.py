#!/usr/bin/env python3
"""Post media extractor results to the message bus."""
import json
import sys
import os
from pathlib import Path

# Add Bridge directory to path for bus_manager import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Bridge"))

from bus_manager import post_to_bus

WORKSPACE = Path(__file__).resolve().parent.parent

# Image metadata message
img_msg = {
    "timestamp": "2026-11-09T11:35:00Z",
    "task_id": "TASK_AGG_IMG_001",
    "action": "media_extract",
    "payload": {
        "media_type": "image",
        "image_id": "sample_diagram",
        "exit_code": 0,
        "confidence_score": 0.95
    },
    "hop_count": 0,
    "idempotency_key": None
}

# Video index message
vid_msg = {
    "timestamp": "2026-11-09T11:35:10Z",
    "task_id": "TASK_AGG_VID_001",
    "action": "media_extract",
    "payload": {
        "media_type": "video",
        "video_id": "sample_lecture",
        "exit_code": 0,
        "confidence_score": 0.90
    },
    "hop_count": 0,
    "idempotency_key": None
}

print("Posting image metadata to bus...")
post_to_bus(img_msg)

print("Posting video index to bus...")
post_to_bus(vid_msg)

print("Done posting to bus.")