# DIRECTIVE_PHASE19_v2.8.0 — AnythingLLM GUI Gateway Integration & REST API Bridge

**Issuer:** `system.master_architect` (Gemini System Architect)  
**Target:** `cline.executor` (Cline Execution Engineer)  
**Phase:** Phase 19 — AnythingLLM GUI Gateway Integration  
**Target Version:** v2.8.0  
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)  
**Status:** DIRECTIVE_ISSUED  

---

## 1. Context & Objective

Following the completion of Phase 18 (Dual-Vertical Architecture v2.7.0 and `00_Project_Interface` deployment), the system requires a primary user-facing Graphical User Interface (GUI). The user has selected **AnythingLLM** (running locally on Windows/localhost) as the operator desktop workspace.

Phase 19 establishes the gateway bridge between the AnythingLLM REST API (`http://localhost:3001/api/v1`) and the central Message Bus (`Bridge/bus_manager.py`).

---

## 2. Required Tasks

### Task 1 — AnythingLLM Configuration & Contract Specification
* Inspect `01_Formal_Core/src/02_NeuroSymbolic_Bridge/Local_RAG_Config/anythingllm_bridge.json` and deploy an operational schema contract to `00_Project_Interface/schemas/anythingllm_gateway_schema.json`.
* Define API endpoint bindings for AnythingLLM:
  * Health/Ping: `GET http://localhost:3001/api/v1/auth` (or `/ping`)
  * Workspaces: `GET /api/v1/workspaces`
  * Document Upload / Ingestion: `POST /api/v1/workspace/{slug}/update-embeddings`
  * Chat Execution: `POST /api/v1/workspace/{slug}/chat`

### Task 2 — Implementation of `anythingllm_gateway.py`
* Implement `00_Project_Interface/src/anythingllm_gateway.py`.
* Requirements:
  * Support `--test` flag: Runs diagnostic validation of local API connectivity (or fallback mock ping if offline) and outputs structured status with `exit_code: 0`.
  * Support `--sync-workspace`: Fetches active workspaces and posts document intake directives into `Bridge/messages.jsonl` for Node 05 (`aggregator.architect`).
  * Support `--send-chat`: Packages user prompts or synthesized models into AnythingLLM chat payload format.
  * Robust exception handling: Graceful fallback when AnythingLLM server is not actively running.

### Task 3 — System Manifest & Master State Upgrade (v2.8.0)
* Upgrade `system_manifest.json` version string to `"2.8.0"`.
* Register `anythingllm_gateway.py` under Node `00_Project_Interface` artifacts in `system_manifest.json`.
* Register new communication vectors if required (`interface_to_anythingllm`).
* Update `PROJECT_STATE.md`:
  * Header metrics to Phase 19 v2.8.0.
  * Append Phase 19 record under Execution History.

---

## 3. Verification & Acceptance Criteria

| # | Criterion | Expected Result |
|---|-----------|-----------------|
| 1 | Syntax Check | `python -m py_compile 00_Project_Interface/src/anythingllm_gateway.py` -> exit_code 0 |
| 2 | Gateway Test | `python 00_Project_Interface/src/anythingllm_gateway.py --test` -> exit_code 0 |
| 3 | Pipeline Integrity | `python test_e2e_pipeline.py` -> exit_code 0 |
| 4 | Manifest Integrity | `json.load()` validation on `system_manifest.json` -> PASSED |
| 5 | Execution Report | Saved to `Bridge/out/execution_reports/report_phase19_v2.8.0_[TIMESTAMP].md` |

---

## 4. Execution Protocol

1. Read `PROJECT_STATE.md` and `system_manifest.json`.
2. Implement `00_Project_Interface/schemas/anythingllm_gateway_schema.json` and `00_Project_Interface/src/anythingllm_gateway.py`.
3. Verify all code with `py_compile` and `--test`.
4. Update `system_manifest.json` to v2.8.0 and record Phase 19 in `PROJECT_STATE.md`.
5. Post completion status to `Bridge/messages.jsonl` and write execution report.
