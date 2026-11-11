# DIRECTIVE_PHASE20_v2.9.0: Notebook Context Standardization & Single-Prompt Gateway Protocol

**Phase:** Phase 20 — Notebook Context Standardization & Single-Prompt Gateway Protocol Formalization  
**Target Version:** v2.9.0  
**Issuer:** system.master_architect (Gemini)  
**Executor:** cline.executor (Cline Execution Engineer)  
**Target Modules:** `system_manifest.json`, `PROJECT_STATE.md`, `00_Project_Interface/`, `01_Formal_Core/`, `05_Knowledge_Aggregator/`, `06_Formalized_Model/`  
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)

---

## 1. Context & Objectives

In Phase 19 (v2.8.0), the AnythingLLM GUI Gateway (`anythingllm_gateway.py`) was successfully deployed and integrated into `00_Project_Interface`.

However, an architectural inefficiency remains across notebook environments:
1. **Context Pollution in Node Notebooks**: Node 05 (Knowledge Aggregator) currently has 10 unorganized source files attached, mixing architectural governance with raw context data.
2. **Lack of Uniform Gateway Protocol**: The 4-step Single-Prompt Gateway Protocol (Gemini Directive → User Save → Single Prompt in Cline VS Code → Bus Completion & Report Return) needs to be formally embedded into the system manifest and all node passports.

**Phase 20 Objective**: Formalize the **Single-Prompt Gateway Protocol** and enforce the **Strict 2-File Notebook Context Standard** across all nodes (Node 00, 01, 05, 06), consolidating Node 05's 10 files into 2 clean interfaces (`NOTEBOOK_PASSPORT_*` and `CONTEXT_DOMAIN_*`), while keeping Master Architect at 1 file (`PROJECT_STATE.md`).

---

## 2. Technical Tasks & Work Breakdown

### Task 1 — Manifest Upgrade & Protocol Formalization (`system_manifest.json`)
1. Set `"version": "2.9.0"`.
2. Add `single_prompt_gateway_protocol` specification under `system_governance`:
   - Step 1: Architect generates `directive-phaseXX-vX.Y.Z.md` in Studio.
   - Step 2: Gateway Operator saves to `Bridge/in/core/directive-phaseXX-vX.Y.Z.md`.
   - Step 3: Gateway Operator executes Single-Prompt in Cline session (runs `bus_manager.py --post` via `--payload-file` + task execution).
   - Step 4: Cline executes, updates message status to `completed`, saves execution report to `Bridge/out/execution_reports/`, and returns summary.
3. Add `notebook_context_standard` rule:
   - Master Architect (Root Notebook): Exactly 1 file (`PROJECT_STATE.md`).
   - Node Orchestrators (Nodes 00, 01, 05, 06): Exactly 2 files per notebook (`NOTEBOOK_PASSPORT_[NODE].md` for Architectural Control Plane + `CONTEXT_DOMAIN_[NODE].md` for Data Plane).

### Task 2 — Physical Deployment of 2-File Node Interfaces
Deploy/standardize the following 2-file pairs for all node directories:

1. **Node 05 (`05_Knowledge_Aggregator/`)**:
   - `05_Knowledge_Aggregator/NOTEBOOK_PASSPORT_AGGREGATOR.md` — Architectural Interface (role passport, PROV-O/SKOS rules, bus JSON schemas).
   - `05_Knowledge_Aggregator/CONTEXT_DOMAIN_AGGREGATOR.md` — Contextual Data Domain (consolidating raw intake templates, RDF triple normalization schemas, and ingestion rules).
2. **Node 00 (`00_Project_Interface/`)**:
   - `00_Project_Interface/NOTEBOOK_PASSPORT_INTERFACE.md` — Architectural Interface (role `interface.operator`, AnythingLLM REST API specs, CLI `--payload-file` protocol).
   - `00_Project_Interface/CONTEXT_DOMAIN_INTERFACE.md` — Contextual Data Domain (AnythingLLM workspace sync schemas, dashboard telemetry structures).
3. **Node 01 (`01_Formal_Core/`)**:
   - `01_Formal_Core/NOTEBOOK_PASSPORT_CORE.md` — Architectural Interface (SHACL shapes, SymPy CAS Prover rules, DSPy backtracking assertions).
   - `01_Formal_Core/CONTEXT_DOMAIN_CORE.md` — Contextual Data Domain (mathematical invariants, TDA Betti H0/H1 definitions, ontology TTL base files).
4. **Node 06 (`06_Formalized_Model/`)**:
   - `06_Formalized_Model/NOTEBOOK_PASSPORT_MODEL.md` — Architectural Interface (ISO 42010 3-view specs, W3C OWL 2 DL validation rules).
   - `06_Formalized_Model/CONTEXT_DOMAIN_MODEL.md` — Contextual Data Domain (OpenAPI 3.1 & JSON-LD 1.1 exporter specifications).

### Task 3 — Master State Synchronization (`PROJECT_STATE.md`)
1. Update Header Metrics to Phase 20 v2.9.0.
2. Update Tier 1 Governance, Node Envelope, and System Health tables to v2.9.0.
3. Append Phase 19 (v2.8.0) and Phase 20 (v2.9.0) complete milestones to Execution History.
4. Document the Single-Prompt Gateway Protocol and 2-File Notebook Context Standard in governance sections.

---

## 3. Acceptance & Verification Criteria

| # | Criterion | Verification Command / Check |
|---|-----------|------------------------------|
| 1 | Manifest v2.9.0 Integrity | `json.load()` on `system_manifest.json` -> PASSED |
| 2 | Node 05 Passport Consolidation | `05_Knowledge_Aggregator/NOTEBOOK_PASSPORT_AGGREGATOR.md` and `CONTEXT_DOMAIN_AGGREGATOR.md` created & verified |
| 3 | All Node Passports Deployed | All 4 nodes (00, 01, 05, 06) have pair (`NOTEBOOK_PASSPORT_*.md` + `CONTEXT_DOMAIN_*.md`) |
| 4 | Master State Sync | `PROJECT_STATE.md` updated to v2.9.0 with Phase 19 & 20 recorded |
| 5 | E2E Pipeline Verification | `python test_e2e_pipeline.py` -> exit_code: 0 (all 4 stages OK) |
| 6 | Execution Report | Saved to `Bridge/out/execution_reports/report_phase20_v2.9.0_[TIMESTAMP].md` |

---

**End of Directive directive-phase20-v2.9.0**
