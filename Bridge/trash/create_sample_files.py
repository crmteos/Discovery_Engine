import os
import json

# Create directories
os.makedirs("05_Knowledge_Aggregator/Intake_Queue/image_metadata", exist_ok=True)
os.makedirs("05_Knowledge_Aggregator/Intake_Queue/video_index", exist_ok=True)

# Create sample image_metadata.json
image_metadata_sample = {
    "image_id": "IMG_001",
    "source_path_or_url": "Intake_Queue/media/images/sample_diagram.png",
    "extracted_concepts": [
        {
            "concept_name": "Visual_Entity_Alpha",
            "definition": "Key structural element extracted from image diagram",
            "bounding_box": [100, 150, 400, 350]
        }
    ],
    "visual_keys": ["legend_symbol_01", "flowchart_node_beta"],
    "prov": {
        "wasAttributedTo": "aggregator.osint_analyst",
        "generatedAtTime": "2026-11-08T23:30:00Z",
        "hadPrimarySource": "05_Knowledge_Aggregator/Intake_Queue/media/images/sample_diagram.png"
    },
    "confidence_score": 0.95,
    "skos": {
        "broader": "CS::VisualData::v1",
        "narrower": [],
        "related": ["CS::DiagramAnalysis::v1"]
    }
}

with open("05_Knowledge_Aggregator/Intake_Queue/image_metadata/sample.json", "w", encoding="utf-8") as f:
    json.dump(image_metadata_sample, f, indent=2, ensure_ascii=False)

# Create sample video_index.json
video_index_sample = {
    "video_id": "VID_INDEX_001",
    "source_path_or_url": "C:\\Media\\Lectures\\Topology_Lecture_01.mp4",
    "title": "Topological Data Analysis Foundations",
    "duration_seconds": 3600,
    "temporal_chunks": [
        {
            "chunk_id": "chunk_001",
            "timestamp_start": "00:05:10",
            "timestamp_end": "00:12:45",
            "transcript_segment": "Discussion of persistent homology and Betti numbers...",
            "extracted_entities": ["persistent_homology", "betti_number_k"],
            "visual_keys": ["keyframe_005m10s.png"]
        }
    ],
    "prov": {
        "wasAttributedTo": "aggregator.osint_analyst",
        "generatedAtTime": "2026-11-08T23:30:00Z",
        "hadPrimarySource": "C:\\Media\\Lectures\\Topology_Lecture_01.mp4"
    },
    "confidence_score": 0.90,
    "skos": {
        "broader": "CS::VideoIndex::v1",
        "narrower": [],
        "related": ["CS::TopologicalDataAnalysis::v1"]
    }
}

with open("05_Knowledge_Aggregator/Intake_Queue/video_index/sample.json", "w", encoding="utf-8") as f:
    json.dump(video_index_sample, f, indent=2, ensure_ascii=False)

print("Sample files created successfully")