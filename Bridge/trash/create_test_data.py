#!/usr/bin/env python3
import json, os
from pathlib import Path

project = r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine"
intake = Path(project) / "05_Knowledge_Aggregator" / "Intake_Queue"

for d in ["raw_cognitive_models", "image_metadata", "video_index"]:
    (intake / d).mkdir(parents=True, exist_ok=True)

# Cognitive model
with open(intake / "raw_cognitive_models" / "model_001.json", "w") as f:
    json.dump({"metadata": {"model_name": "M1"}, "entities": [{"id": "e1", "name": "C1", "type": "C", "properties": {}}], "relations": [{"subject": "e1", "predicate": "rel", "object": "e2"}], "invariants": ["inv1"]}, f, indent=2)

# Image metadata
with open(intake / "image_metadata" / "img_001.json", "w") as f:
    json.dump({"image_id": "IMG1", "source_path_or_url": "img.png", "extracted_concepts": [{"concept_name": "C1", "definition": "def"}], "prov": {"wasAttributedTo": "agg", "generatedAtTime": "2024-01-01T00:00:00Z", "hadPrimarySource": "img.png"}, "skos": {"broader": "b", "related": ["r"]}}, f, indent=2)

# Video index
with open(intake / "video_index" / "vid_001.json", "w") as f:
    json.dump({"video_id": "V1", "source_path_or_url": "vid.mp4", "temporal_chunks": [{"chunk_id": "c1", "timestamp_start": "00:00", "timestamp_end": "01:00", "extracted_entities": ["e1"], "visual_keys": ["v1"]}] , "prov": {"wasAttributedTo": "agg", "generatedAtTime": "2024-01-01T00:00:00Z", "hadPrimarySource": "vid.mp4"}, "skos": {"broader": "b", "related": ["r"]}}, f, indent=2)

print("Test data created")