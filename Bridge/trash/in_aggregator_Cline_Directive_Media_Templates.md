# TASK DIRECTIVE: Deploy Image Metadata & Video Indexing Templates
**Target Directory:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** `AGGREGATOR_OPERATIONAL_PROTOCOL.md` & `NOTEBOOK_PASSPORT_AGGREGATOR.md` (v2.6.0)
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
Expand the ingestion capabilities of Subsystem 05 (`05_Knowledge_Aggregator`) to support multi-modal knowledge ingestion (visual knowledge keys and external video indexing) by deploying two new W3C PROV-O / SKOS compliant intake JSON templates into `Intake_Queue/templates/`.

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Create `image_metadata_template.json`
Deploy file to `05_Knowledge_Aggregator/Intake_Queue/templates/image_metadata_template.json`:
```json
{
  "image_id": "IMG_001",
  "file_path": "Intake_Queue/media/images/sample_diagram.png",
  "dimensions": {
    "width": 1920,
    "height": 1080
  },
  "format": "PNG",
  "extracted_concepts": [
    {
      "concept_name": "Visual_Entity_Alpha",
      "definition": "Key structural element extracted from image diagram",
      "bounding_box": [100, 150, 400, 350]
    }
  ],
  "visual_keys": [
    "legend_symbol_01",
    "flowchart_node_beta"
  ],
  "prov": {
    "wasAttributedTo": "aggregator.osint_analyst",
    "generatedAtTime": "2026-11-08T23:30:00Z",
    "hadPrimarySource": "05_Knowledge_Aggregator/Intake_Queue/media/images/sample_diagram.png",
    "confidence_score": 0.95
  },
  "skos": {
    "broader": "CS::VisualData::v1",
    "narrower": [],
    "related": ["CS::DiagramAnalysis::v1"]
  }
}
```

##### Task 2: Create `video_index_template.json`
Deploy file to `05_Knowledge_Aggregator/Intake_Queue/templates/video_index_template.json`:
```json
{
  "video_id": "VID_INDEX_001",
  "source_url_or_path": "C:\\Media\\Lectures\\Topology_Lecture_01.mp4",
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
    "hadPrimarySource": "C:\\Media\\Lectures\\Topology_Lecture_01.mp4",
    "confidence_score": 0.90
  },
  "skos": {
    "broader": "CS::VideoIndex::v1",
    "narrower": [],
    "related": ["CS::TopologicalDataAnalysis::v1"]
  }
}
```

##### Task 3: Pipeline Integration & Verification
1. Ensure `Intake_Queue/media/images/` directory exists.
2. Run syntax and schema validation smoke test using `schema_validator.py` and `intake_processor.py`.
3. Save execution report to `Bridge/out/aggregator_reports/report_media_templates_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `image_metadata_template.json` deployed and schema valid.
* [ ] `video_index_template.json` deployed and schema valid.
* [ ] W3C PROV-O & SKOS compliance verified.
* [ ] Execution report saved to `Bridge/out/aggregator_reports/`.
