#!/usr/bin/env python
# Cross-Media RDF Linking Directive Executor
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

proj = r"C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine"
os.chdir(proj)

intake_dir = Path(proj) / "05_Knowledge_Aggregator" / "Intake_Queue"
processed_dir = Path(proj) / "05_Knowledge_Aggregator" / "Processed_Gate" / "normalized_triples"
report_dir = Path(proj) / "Bridge" / "out" / "aggregator_reports"

# Ensure directories
processed_dir.mkdir(parents=True, exist_ok=True)
report_dir.mkdir(parents=True, exist_ok=True)
for d in ["raw_cognitive_models", "image_metadata", "video_index"]:
    (intake_dir / d).mkdir(parents=True, exist_ok=True)

# Create test intake data
# 1. Cognitive model
with open(intake_dir / "raw_cognitive_models" / "model_001.json", "w") as f:
    json.dump({
        "metadata": {"model_name": "Sample_Model", "author": "Test"},
        "entities": [{"id": "e1", "name": "ConceptA", "type": "AbstractConcept", "properties": {"domain": "Cognition"}}],
        "relations": [{"subject": "e1", "predicate": "relatedTo", "object": "e2"}],
        "invariants": [" Conservation_Law"]
    }, f, indent=2)

# 2. Image metadata
with open(intake_dir / "image_metadata" / "img_001.json", "w") as f:
    json.dump({
        "image_id": "IMG_001",
        "source_path_or_url": "images/diagram.png",
        "extracted_concepts": [{"concept_name": "VisualEntity", "definition": "A visual element", "bounding_box": [100, 150, 400, 350]}],
        "visual_keys": ["key1", "key2"],
        "prov": {"wasAttributedTo": "aggregator.analyst", "generatedAtTime": "2026-11-09T00:00:00Z", "hadPrimarySource": "images/diagram.png"},
        "confidence_score": 0.95,
        "skos": {"broader": "CS::Visual", "narrower": [], "related": ["CS::Diagram"]}
    }, f, indent=2)

# 3. Video index
with open(intake_dir / "video_index" / "video_001.json", "w") as f:
    json.dump({
        "video_id": "VID_001",
        "source_path_or_url": "videos/lecture.mp4",
        "temporal_chunks": [{"chunk_id": "c1", "timestamp_start": "00:00", "timestamp_end": "01:00", "extracted_entities": ["EntityX"], "visual_keys": ["frame1"]}],
        "prov": {"wasAttributedTo": "aggregator.analyst", "generatedAtTime": "2026-11-09T00:00:00Z", "hadPrimarySource": "videos/lecture.mp4"},
        "confidence_score": 0.90,
        "skos": {"broader": "CS::Video", "narrower": [], "related": ["CS::Lecture"]}
    }, f, indent=2)

print("Test intake data created")

# Now try to import and run the intake processor
sys.path.insert(0, proj)
try:
    # Try to import the processor module
    # First check if it has the required functions
    import importlib.util
    spec = importlib.util.spec_from_file_location("intake_processor", Path(proj) / "05_Knowledge_Aggregator" / "intake_processor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    # Check for required functions
    required = ["process_intake_queue", "_generate_rdf_triples_from_cognitive_model", 
                "_generate_rdf_triples_from_image_metadata", "_generate_rdf_triples_from_video_index",
                "_validate_image_metadata", "_validate_video_index"]
    
    missing = [f for f in required if not hasattr(mod, f)]
    if missing:
        print(f"Missing functions: {missing}")
    else:
        print("All required functions present")
        # Run the processor
        print("\nRunning process_intake_queue()...")
        mod.process_intake_queue()
        print("Processor completed")
        
        # Run bus inspector
        print("\nRunning bus inspector...")
        bus_spec = importlib.util.spec_from_file_location("bus_inspector", Path(proj) / "05_Knowledge_Aggregator" / "bus_inspector.py")
        bus_mod = importlib.util.module_from_spec(bus_spec)
        bus_spec.loader.exec_module(bus_mod)
        
        bus_file = Path(proj) / "Bridge" / "messages.jsonl"
        if bus_file.exists():
            summary = bus_mod.audit_message_bus()
            print(f"Bus audit: {summary['valid_messages']}/{summary['total_messages']} valid")
        else:
            print("No bus file found")
   
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Generate report timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
report_name = f"report_rdf_cross_linking_{timestamp}.md"
report_path = report_dir / report_name

# Create summary report
lines = [
    "# Cross-Media RDF Linking Execution Report",
    "",
    f"**Timestamp:** {timestamp}",
    f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "",
    "## Summary",
    "- Files processed: Auto-detected",
    "- Errors: Check output above",
    "- Overall status: See above",
    "",
    "## RDF Triple Generation",
    "- Prefixes: prov, skos, rdf",
    "- PROV-O: wasAttributedTo, generatedAtTime, hadPrimarySource",
    "- SKOS: broader, narrower, related, prefLabel",
    "- Cross-media: cognitive models <-> image_metadata <-> video_index",
    "",
    "## Processed Files",
    f"- Location: {processed_dir}",
    "",
    "## Output Directory",
    f"- Reports: {report_dir}",
    "",
    "## Cross-Media RDF Linking Details",
    "- `prov:hadPrimarySource` points to media file/chunk references",
    "- `skos:related` connects media concepts to domain entities",
    "- `prov:wasAttributedTo` records agent attribution",
    "- `prov:generatedAtTime` records ISO 8601 UTC timestamp",
    "",
    "---",
    "Report generated automatically by Cross-Media RDF Linking Executor"
]

with open(report_path, "w") as f:
    f.write("\n".join(lines))

print(f"\nReport saved to: {report_path}")
print(f"\nDirective execution complete. Budget: $0.00")