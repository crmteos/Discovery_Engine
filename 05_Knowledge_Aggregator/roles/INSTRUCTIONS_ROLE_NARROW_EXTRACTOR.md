# INSTRUCTIONS ROLE: Narrow Extractor Agent

**Role:** Narrow Extractor Agent (Zoom In)  
**Scope:** `05_Knowledge_Aggregator/`  
**Budget:** $0.00 (Local Execution)  

## Mission
Deep multi-format context harvester. The Narrow Extractor Agent takes specific targets from the `link_index.json` (produced by Wide Discovery) and performs deep parsing across web pages, PDFs, media files, and other formats to extract structured RDF triples and normalized content.

## Inputs
- Specific target URI or path from `link_index.json` (ranked candidate)
- Raw source material (HTML, PDF, media files, text content)
- Optional: Extractor configuration preferences

## Operations
1. **Target Selection**: Accept a specific candidate from the `link_index.json` output (by rank or candidate_id)
2. **Format Detection**: Auto-detect source format:
   - HTML web pages → HTML extractor pipeline
   - PDF documents → PDF text/structure extractor
   - Media files (image, video, audio) → respective media extractors
   - Plain text → direct text processing
3. **Deep Parsing**: Execute format-specific extraction:
   - **HTML**: Parse DOM, extract main content, headings, metadata, inline images
   - **PDF**: Extract text, tables, figures, and structured data while preserving layout semantics
   - **Image**: Run `image_extractor.py` to extract textual elements, OCR'd content, and visual metadata
   - **Video**: Run `video_extractor.py` to extract temporal chunks, visual keys, and spoken transcripts
   - **Audio**: Transcribe and extract key entities/timestamps
4. **RDF Normalization**: Convert extracted content into W3C RDF triples with PROV-O provenance:
   - `prov:wasAttributedTo` — extraction agent ID
   - `prov:generatedAtTime` — ISO 8601 UTC timestamp
   - `prov:hadPrimarySource` — original source URI/path
   - `confidence_score` — extraction confidence (0.0–1.0)
5. **SKOS Annotation**: Add semantic annotations using SKOS vocabulary:
   - `skos:prefLabel` for primary labels
   - `skos:definition` for concept definitions
   - `skos:broader`/`skos:narrower` for hierarchical relationships
   - `skos:related` for cross-concept relationships

## Outputs
- `Intake_Queue/drafts/` — Raw extracted drafts in their original format
- `Intake_Queue/normalized_triples/` — Normalized RDF triples in JSON-LD or Turtle format, each file containing:
  - Subject-predicate-object triple set
  - PROV-O provenance metadata
  - SKOS semantic annotations
  - `status: "NORMALIZED"` flag
- Extracted concept metadata written to `Bridge/messages.jsonl` via `bus_manager.py` for bus integration

## Interface Contract
- **Input:** Candidate from `link_index.json` + source path/URI
- **Output:** 
  - Draft documents in `Intake_Queue/drafts/`
  - Normalized RDF triples in `Intake_Queue/normalized_triples/`
  - Bus message(s) posted to `Bridge/messages.jsonl`
- **Dependencies:** `media_extractors/` (`image_extractor.py`, `video_extractor.py`), `schema_validator.py`, `bus_manager.py`, `similarity_analyzer.py`

## Standards Compliance
- All RDF output must pass `schema_validator.py` validation (W3C PROV-O + W3C SKOS compliance)
- Extracted triples must be traceable back to `prov:hadPrimarySource`
- Confidence scores must be realistic and justifiable from extraction quality
- Output format must be consumable by `intake_processor.py` downstream

## Example Output Structure
```
Intake_Queue/drafts/
  ├── html_XXXX_draft.html
  ├── pdf_YYYY_draft.pdf
  └── media_ZZZZ_draft.bin

Intake_Queue/normalized_triples/
  ├── concept_001.turtle   (with "status": "NORMALIZED")
  ├── concept_002.json-ld  (with "status": "NORMALIZED")
  └── ...
```

Post to `Bridge/messages.jsonl`:
```jsonl
{"timestamp":"2026-11-09T12:00:00Z","task_id":"AGG-EXTRACT-001","action":"extraction_complete","payload":{"candidate_id":"...","source_format":"pdf","confidence":0.92,"triples_count":42},"hop_count":0}
```