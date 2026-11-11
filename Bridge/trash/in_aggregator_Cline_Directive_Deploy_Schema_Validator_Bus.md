# TASK DIRECTIVE: Deploy Schema Validator & Transactional Message Bus
**Target Subsystem:** C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** NOTEBOOK_PASSPORT_AGGREGATOR.md v2.6.0 & AGGREGATOR_OPERATIONAL_PROTOCOL.md
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
Deploy `schema_validator.py` and `bus_manager.py` to enforce strict W3C PROV-O and W3C SKOS data standards, implement SHA256 idempotency keying, and enable append-only transactional logging to `Bridge/messages.jsonl` under Node 05 isolation rules.

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Deploy & Configure schema_validator.py
1. Create/update `05_Knowledge_Aggregator/schema_validator.py`.
2. Implement schema validation for incoming JSON drafts (`cognitive_model_template.json`, `analogy_template.json`, `concept_scheme_template.json`).
3. Enforce mandatory W3C PROV-O metadata validation:
   - `prov:wasAttributedTo` (non-null string)
   - `prov:generatedAtTime` (ISO 8601 UTC string with `Z` suffix)
   - `prov:hadPrimarySource` (valid source path)
   - `confidence_score` (float in range `[0.0, 1.0]`)
4. Enforce mandatory W3C SKOS relationship checks for concept schemes (`skos:broader`, `skos:narrower`, `skos:related`).
5. Ensure script returns `exit_code: 0` for compliant schemas and non-zero with diagnostic output for non-compliant schemas.

##### Task 2: Deploy & Configure bus_manager.py
1. Create/update `Bridge/bus_manager.py` (or `05_Knowledge_Aggregator/bus_manager.py` with bus interface).
2. Establish append-only transactional writing to `Bridge/messages.jsonl`.
3. Implement SHA256 idempotency key calculation for every record to prevent duplicate entries.
4. Support transaction payloads for `submit_task` (`data_type: concept_scheme` / `cognitive_model`) and `status_update`.

##### Task 3: Integration Testing & Verification
1. Run syntax verification:
   - `python -m py_compile 05_Knowledge_Aggregator/schema_validator.py`
   - `python -m py_compile Bridge/bus_manager.py`
2. Perform a end-to-end smoke test:
   - Validate an intake draft using `schema_validator.py`.
   - Write a validated record to `Bridge/messages.jsonl` via `bus_manager.py`.
3. Save the execution log report to `Bridge/out/aggregator_reports/report_validator_bus_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `schema_validator.py` deployed and returning `exit_code: 0` on valid schemas.
* [ ] PROV-O (`wasAttributedTo`, `generatedAtTime`, `hadPrimarySource`, `confidence_score`) and SKOS fields strictly validated.
* [ ] `bus_manager.py` configured as sole writer to `Bridge/messages.jsonl` with SHA256 idempotency keys.
* [ ] Smoke test executed cleanly without external API calls ($0.00 budget).
* [ ] Execution report saved to `Bridge/out/aggregator_reports/`.
