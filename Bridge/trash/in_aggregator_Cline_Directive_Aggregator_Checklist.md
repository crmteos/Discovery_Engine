# TASK DIRECTIVE: Deploy Aggregator Operational Plan & Checklist
**Target Subsystem:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** AGGREGATOR_OPERATIONAL_PROTOCOL.md
**Budget Constraint:** $0.00 (Pure Local Hardware Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
Deploy a localized operational checklist (`AGGREGATOR_CHECKLIST.md`) inside `05_Knowledge_Aggregator/` to govern and track data ingestion, JSON template validation, RDF triple normalization, and channel execution logs independently from the core engine.

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Phase 1: Operational Checklist File Creation
Create `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md` with the following initial structure:

```markdown
# 05_Knowledge_Aggregator — Operational Plan & Checklist
#### Subsystem Scope & Target Directory
`C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`

--------------------------------------------------------------------------------

#### 📋 Phase 1: Ingestion Infrastructure & Schema Audit
- [x] **Subsystem Isolation:** Dedicated `AGGREGATOR_STATE.md` initialized.
- [x] **Channel Architecture:** Sub-channels `Bridge/in/aggregator/` and `Bridge/out/aggregator_reports/` configured.
- [ ] **Schema Contract Validation:** Audit JSON templates (`cognitive_model_template.json`, `analogy_template.json`, `concept_scheme_template.json`) for entity/relation invariants.
- [ ] **Intake Handler Health Check:** Test run `intake_processor.py` on sample drafts to verify schema validation and RDF envelope conversion.

--------------------------------------------------------------------------------

#### 📋 Phase 2: OSINT Data Stream Ingestion
- [ ] **Raw Cognitive Models Intake:** Deposit and validate cognitive model drafts in `Intake_Queue/raw_cognitive_models/`.
- [ ] **Structural Analogies Intake:** Process cross-domain mapping schemes in `Intake_Queue/structural_analogies/`.
- [ ] **Conceptual Schemes Intake:** Maintain domain concepts in `Intake_Queue/conceptual_schemes/`.

--------------------------------------------------------------------------------

#### 📋 Phase 3: Triple Normalization & Gate Output
- [ ] **RDF Envelope Verification:** Ensure output files in `Processed_Gate/normalized_triples/` carry `"status": "NORMALIZED"`.
- [ ] **Zero-Hallucination Audit:** Verify that 100% of generated triples trace back to valid intake sources.
- [ ] **Core Handoff Readiness:** Confirm normalized triples are formatted for seamless ingestion into `01_Formal_Core`.

--------------------------------------------------------------------------------

#### 📋 Phase 4: Execution & Logging
- [ ] **Log Storage:** Record intake summary reports to `Bridge/out/aggregator_reports/report_intake_[TIMESTAMP].md`.
- [ ] **Local Metrics Sync:** Update `AGGREGATOR_STATE.md` with processed file counts and queue metrics.
```

##### Phase 2: Verification & Test Execution
1. Verify `05_Knowledge_Aggregator/intake_processor.py` by running:
   `python 05_Knowledge_Aggregator/intake_processor.py`
2. Confirm normalized output generation in `Processed_Gate/normalized_triples/`.
3. Save the verification log to `Bridge/out/aggregator_reports/report_checklist_init_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Compliance & Verification Checklist
* [ ] `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md` created.
* [ ] Initial test run of `intake_processor.py` executed cleanly.
* [ ] Execution report deposited into `Bridge/out/aggregator_reports/`.
* [ ] Zero external API calls ($0.00 budget maintained).
