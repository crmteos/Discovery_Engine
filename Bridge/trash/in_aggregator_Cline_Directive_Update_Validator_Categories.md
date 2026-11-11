# TASK DIRECTIVE: Register Image Metadata & Video Index Categories in Schema Validator
**Target Subsystem:** C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** AGGREGATOR_OPERATIONAL_PROTOCOL.md
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
Register two new intake categories (`image_metadata` and `video_index`) in `05_Knowledge_Aggregator/schema_validator.py` contract mapping so that incoming media templates are validated against their dedicated schemas rather than falling back to `cognitive_model`.

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Update schema_validator.py Category Mapping & Contracts
1. Edit `05_Knowledge_Aggregator/schema_validator.py`:
   - Add `image_metadata` to the category detection and contract map.
     - Required root fields / contract: `image_id` (or `id`), `source_path_or_url`, `extracted_concepts`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `prov:hadPrimarySource`, `confidence_score`.
   - Add `video_index` to the category detection and contract map.
     - Required root fields / contract: `video_id` (or `id`), `source_path_or_url`, `temporal_chunks`, `prov:wasAttributedTo`, `prov:generatedAtTime`, `prov:hadPrimarySource`, `confidence_score`.

##### Task 2: Re-run Validation Smoke Test
1. Execute:
   - `python schema_validator.py --file Intake_Queue/templates/image_metadata_template.json --category auto`
   - `python schema_validator.py --file Intake_Queue/templates/video_index_template.json --category auto`
2. Confirm both return `exit_code: 0` (Valid Schema) with correct category detection (`image_metadata` and `video_index`).

##### Task 3: Update Execution Report
1. Append test results to `Bridge/out/aggregator_reports/report_media_templates_20261109_093928.md` confirming `RESULT: ✅ Schema-valid` for both categories.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `schema_validator.py` explicitly recognizes `image_metadata` and `video_index`.
* [ ] Both templates pass validation with `exit_code: 0`.
* [ ] `report_media_templates_20261109_093928.md` updated with passing status.
