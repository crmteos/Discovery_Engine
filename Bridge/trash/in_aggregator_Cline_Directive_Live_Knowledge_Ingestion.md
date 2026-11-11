# Directive: Live Knowledge Ingestion & E2E Core Readiness Test

## 1. Objective
Perform a complete end-to-end ingestion of a complex cognitive model cross-linked with image metadata and video indices, validating the entire Node 05 pipeline before formal core handoff.

## 2. Execution Steps
1. **Prepare Ingestion Drafts**: Create a comprehensive cognitive model draft in `Intake_Queue/raw_cognitive_models/`, associated image metadata in `Intake_Queue/image_metadata/`, and a video index in `Intake_Queue/video_index/`.
2. **Schema Validation**: Run `schema_validator.py` on all 3 drafts (verify `exit_code: 0` for all categories).
3. **Triple Normalization**: Run `intake_processor.py` to generate normalized W3C PROV-O / SKOS RDF triples in `Processed_Gate/normalized_triples/`.
4. **Transaction Logging**: Confirm that `bus_manager.py` appends SHA256-keyed event logs into `Bridge/messages.jsonl`.
5. **Bus Audit**: Execute `bus_inspector.py` to verify 100% message schema compliance and 0 errors.
6. **Execution Report**: Save the finalized audit report to `Bridge/out/aggregator_reports/report_live_ingestion_[TIMESTAMP].md`.

## 3. Constraints & Acceptance Criteria
- **Budget**: $0.00 (pure local execution).
- **Standards**: Full W3C PROV-O and SKOS compliance.
- **Exit Codes**: `0` across all pipeline stages.
