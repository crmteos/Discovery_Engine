# DIRECTIVE: Phase 23 (v3.2.0) — AnythingLLM Workspace Sync & Node 00 2-File Envelope Standardization

**Target Version:** v3.2.0  
**Issuer:** `system.master_architect` (Gemini Master Architect)  
**Recipient:** `cline.executor` (Cline Execution Engineer)  
**Primary Directive File Path:** `Bridge/in/directive-phase23-v3.2.0.md`  
**Execution Standard:** Zero-Budget ($0.00), Production-Grade Code, 2-File Envelope Isolation  

---

### 1. Objective & Scope
The objective of Phase 23 is to finalize the physical and logical integration of **Node 00 (`00_Project_Interface`)** as an official bidirectional 4th node in the system, enforce the **Universal 2-File Envelope Standard** (`NOTEBOOK_PASSPORT_INTERFACE.md` + `CONTEXT_DOMAIN_INTERFACE.md`), and enable live workspace synchronization and prompt-response routing between **AnythingLLM** (HTTP `127.0.0.1:3001/api/v1`) and the central transactional Message Bus (`Bridge/messages.jsonl`).

---

### 2. Task Breakdown

#### Task 1: Deploy Node 00 2-File Envelope
1. Create `00_Project_Interface/NOTEBOOK_PASSPORT_INTERFACE.md` (Control Plane):
   - Passport metadata, assigned role (`interface.operator`), agent card (allowed vectors: `interface_to_master`, `interface_to_bus`, `interface_to_nodes`, `interface_to_anythingllm`).
   - MCP tool definitions (`architecture_view.py`, `context_view.py`, `anythingllm_gateway.py`).
   - Single-Prompt Gateway Protocol & operational rules for Node 00.
2. Create `00_Project_Interface/CONTEXT_DOMAIN_INTERFACE.md` (Data Plane):
   - Specification of visual dashboards, workspace schemas, and data structures exchanged with AnythingLLM.
   - Event mapping for bidirectional telemetry (inbound intake requests vs. outbound formal model delivery).

#### Task 2: Enhance AnythingLLM Gateway (`00_Project_Interface/src/anythingllm_gateway.py`)
1. Implement full workspace synchronization (`--sync-workspace`):
   - Poll AnythingLLM API endpoint `/v1/workspaces`.
   - Parse active workspace document lists and post intake task requests (`task_request`) to `Bridge/messages.jsonl` for recipient `aggregator.architect` (Node 05).
2. Implement chat payload routing (`--send-chat`):
   - Package user prompts/responses from AnythingLLM chat threads into JSON messages.
   - Validate against `00_Project_Interface/schemas/anythingllm_gateway_schema.json`.
3. Preserve graceful offline fallback (`offline_fallback`) when AnythingLLM server is not actively running during `--test`.

#### Task 3: Update `system_manifest.json` to v3.2.0
1. Upgrade `"version"` field to `"3.2.0"`.
2. Ensure Node 00 entry in `"nodes"` explicitly lists `NOTEBOOK_PASSPORT_INTERFACE.md` and `CONTEXT_DOMAIN_INTERFACE.md` in envelope schema.
3. Verify `interface.operator` role capability registry, including allowed vectors and tools (`anythingllm_gateway.py`).

#### Task 4: Master State & Context Synchronization
1. Update `PROJECT_STATE.md`:
   - Header metrics version -> `v3.2.0`.
   - Add Phase 23 milestone to Execution History.
2. Update `PROJECT_CONTEXT.md`:
   - Add AnythingLLM Gateway REST API topology to Section 8.

---

### 3. Acceptance & Verification Criteria
1. `python -m py_compile 00_Project_Interface/src/anythingllm_gateway.py` -> exit_code 0.
2. `python 00_Project_Interface/src/anythingllm_gateway.py --test` -> exit_code 0.
3. `json.load()` on `system_manifest.json` -> PASSED.
4. `tomllib.load()` on `pyproject.toml` -> PASSED.
5. `python tests/e2e/test_e2e_pipeline.py` -> exit_code 0 (4/4 stages OK).
6. Execution report saved to `Bridge/out/execution_reports/report_phase23_v3.2.0_[TIMESTAMP].md`.
