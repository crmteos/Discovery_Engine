#!/usr/bin/env python3
"""Part 1: Directive header and step 1"""
import os, json
from pathlib import Path

PROJECT = r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine"
os.chdir(PROJECT)

intake = Path(PROJECT)/"05_Knowledge_Aggregator"/"Intake_Queue"
for d in ["raw_cognitive_models","image_metadata","video_index"]:
    (intake/d).mkdir(parents=True, exist_ok=True)
with open(intake/"raw_cognitive_models"/"model_001.json","w") as f:
    json.dump({"metadata":{"model_name":"Sample_Model"},"entities":[{"id":"e1","name":"ConceptA","type":"AbstractConcept","properties":{"domain":"Cognition"}}],"relations":[{"subject":"e1","predicate":"relatedTo","object":"e2"}],"invariants":["Conservation_Law"]},f,indent=2)
with open(intake/"image_metadata"/"img_001.json","w") as f:
    json.dump({"image_id":"IMG_001","source_path_or_url":"images/diagram.png","extracted_concepts":[{"concept_name":"VisualEntity","definition":"A visual element","bounding_box":[100,150,400,350]}],"visual_keys":["key1","key2"],"prov":{"wasAttributedTo":"aggregator.osint_analyst","generatedAtTime":"2026-11-09T00:00:00Z","hadPrimarySource":"images/diagram.png"},"confidence_score":0.95,"skos":{"broader":"CS::Visual","narrower":[],"related":["CS::Diagram"]}},f,indent=2)
with open(intake/"video_index"/"video_001.json","w") as f:
    json.dump({"video_id":"VID_001","source_path_or_url":"videos/lecture.mp4","title":"Topological Data Analysis","duration_seconds":3600,"temporal_chunks":[{"chunk_id":"c1","timestamp_start":"00:05:10","timestamp_end":"00:12:45","extracted_entities":["persistent_homology","betti_number_k"],"visual_keys":["keyframe_005m10s.png"]}],"prov":{"wasAttributedTo":"aggregator.osint_analyst","generatedAtTime":"2026-11-09T00:00:00Z","hadPrimarySource":"videos/lecture.mp4"},"confidence_score":0.90,"skos":{"broader":"CS::VideoIndex","narrower":[],"related":["CS::TopologicalDataAnalysis"]}},f,indent=2)
print("Part 1: Test data created\n")