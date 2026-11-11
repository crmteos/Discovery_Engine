# DIRECTIVE: Phase 20.1 Cleanup (v2.9.1) — Node 05 File Consolidation & Legacy Cleanup

**Issuer:** system.master_architect (Gemini)  
**Target Executor:** cline.executor (Cline Execution Engineer)  
**Target Node:** 05_Knowledge_Aggregator  
**Version:** v2.9.1  
**Protocol:** Single-Prompt Gateway Protocol  

---

### 1. Objective & Architectural Rationale

During the verification of Phase 20 (v2.9.0), a audit revealed five legacy/fragmented Markdown files in `05_Knowledge_Aggregator/` and root that remain unintegrated into the official **2-File Notebook Context Standard**:
1. `CLI_COMPLETION.md` (root) — CLI intake protocol specification.
2. `05_Knowledge_Aggregator/AGGREGATOR_STATE.md` — Fragmented local state duplicate.
3. `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md` — Hanging validation checklist.
4. `05_Knowledge_Aggregator/AGGREGATOR_OPERATIONAL_PROTOCOL.md` — Hanging operational instructions.
5. `05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_AGGREGATOR.md` — Hanging role instruction file.

To uphold the strict **2-File Notebook Context Standard** (Control Plane vs Data Plane) for Node 05 and eliminate context clutter, all relevant logic from these 5 files must be merged into the two canonical interfaces, and the redundant source files must be removed.

---

### 2. Required Tasks

#### Task 1: Consolidated Control Plane Interface
Integrate `INSTRUCTIONS_ROLE_AGGREGATOR.md`, `AGGREGATOR_OPERATIONAL_PROTOCOL.md`, `AGGREGATOR_CHECKLIST.md`, and `AGGREGATOR_STATE.md` into a single, comprehensive architectural passport:
* **Target File:** `05_Knowledge_Aggregator/NOTEBOOK_PASSPORT_AGGREGATOR.md`
* **Contents to Include:**
  - Role Passport & Identity (`aggregator.architect` & `aggregator.osint_analyst`)
  - Operational Protocol & Rules of Engagement
  - System Readiness Checklist
  - Local Node State & Metrics History

#### Task 2: Consolidated Data Plane Interface
Integrate `CLI_COMPLETION.md` and intake specifications into the domain context file:
* **Target File:** `05_Knowledge_Aggregator/CONTEXT_DOMAIN_AGGREGATOR.md`
* **Contents to Include:**
  - CLI Intake Completion Protocols (`CLI_COMPLETION.md` content)
  - Intake Queue Template Schemas (`Intake_Queue/templates/*.json`)
  - RDF Triple Normalization Rules & SKOS/PROV-O Mappings

#### Task 3: File System Cleanup
After verifying that all content has been merged into the 2 canonical interfaces, remove the legacy files:
* Remove `CLI_COMPLETION.md` from workspace root.
* Remove `05_Knowledge_Aggregator/AGGREGATOR_STATE.md`.
* Remove `05_Knowledge_Aggregator/AGGREGATOR_CHECKLIST.md`.
* Remove `05_Knowledge_Aggregator/AGGREGATOR_OPERATIONAL_PROTOCOL.md`.
* Remove `05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_AGGREGATOR.md`.

#### Task 4: Governance & Manifest Synchronization
* Update `system_manifest.json` sub-component file registry for Node 05 to reflect the clean 2-file structure.
* Update `PROJECT_STATE.md` Execution History with Phase 20.1 cleanup record.

---

### 3. Verification & Acceptance Criteria

1. `05_Knowledge_Aggregator/` contains ONLY `NOTEBOOK_PASSPORT_AGGREGATOR.md` and `CONTEXT_DOMAIN_AGGREGATOR.md` plus `schemas/` and `src/`.
2. Legacy files `CLI_COMPLETION.md`, `AGGREGATOR_STATE.md`, `AGGREGATOR_CHECKLIST.md`, `AGGREGATOR_OPERATIONAL_PROTOCOL.md`, `INSTRUCTIONS_ROLE_AGGREGATOR.md` no longer exist on disk.
3. `json.load()` on `system_manifest.json` passes with exit_code: 0.
4. `python test_e2e_pipeline.py` passes all 4 stages with exit_code: 0.
5. Execution report generated at `Bridge/out/execution_reports/report_phase20_cleanup_v2.9.1_[TIMESTAMP].md`.
