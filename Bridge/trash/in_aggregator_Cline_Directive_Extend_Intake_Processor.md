# TASK DIRECTIVE: Extend Intake Processor for Media Categories & E2E Verification
**Target Subsystem:** C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** AGGREGATOR_OPERATIONAL_PROTOCOL.md
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
1. Extend `05_Knowledge_Aggregator/intake_processor.py` to support ingestion and normalization of the newly registered media categories (`image_metadata` and `video_index`).
2. Execute an End-to-End pipeline verification test using sample intake drafts to confirm seamless execution: `Intake_Queue/` -> `schema_validator.py` -> `intake_processor.py` -> `Processed_Gate/normalized_triples/` -> `Bridge/messages.jsonl` (via `bus_manager.py`).

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Update intake_processor.py
- Update `05_Knowledge_Aggregator/intake_processor.py` to scan and handle media intake categories (`image_metadata` and `video_index`) alongside existing categories (`raw_cognitive_models`, `structural_analogies`, `conceptual_schemes`).
- Ensure normalized output wrappers in `Processed_Gate/normalized_triples/` preserve W3C PROV-O and SKOS compliance attributes.
- Integrate transactional logging to `Bridge/messages.jsonl` via `bus_manager.py`.

##### Task 2: Pipeline End-to-End Smoke Test
- Create sample ingestion drafts for `image_metadata` and `video_index` in `Intake_Queue/`.
- Run `python 05_Knowledge_Aggregator/intake_processor.py`.
- Verify:
  - `schema_validator.py` validates drafts with `exit_code: 0`.
  - Normalized JSON files are generated in `Processed_Gate/normalized_triples/`.
  - Transactional event records are appended to `Bridge/messages.jsonl` with SHA256 idempotency keys.

##### Task 3: Reporting
- Save execution report to `Bridge/out/aggregator_reports/report_intake_processor_e2e_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `intake_processor.py` updated and passes `python -m py_compile`.
* [ ] Both `image_metadata` and `video_index` correctly processed into `Processed_Gate/`.
* [ ] Transactional messages logged to `Bridge/messages.jsonl` via `bus_manager.py`.
* [ ] Report saved in `Bridge/out/aggregator_reports/`.
