# Architectural Directive — Phase 24 (v3.3.0)
**Directive ID:** directive-phase24-v3.3.0  
**Phase:** Phase 24 — Live Observability Bus Dashboard & AnythingLLM Visualizer Integration  
**Target System Version:** v3.3.0  
**Issuer:** system.master_architect  
**Executor:** cline.executor  
**Target Node:** Node 00 (00_Project_Interface) & Central Bridge  
**Status:** PROPOSED / PENDING EXECUTION  

---

## 1. Context & Rationale
System v3.2.1 established bidirectional live REST API connectivity with AnythingLLM workspace `Discovery_Engine`. To achieve full operational transparency and deliver continuous observability into AnythingLLM, Node 00 (`00_Project_Interface`) requires a dedicated **Live Observability Bus Dashboard (`bus_dashboard.py`)**. This component will process real-time transaction logs from `Bridge/messages.jsonl`, generate visual topology matrices, and feed status dashboards directly into AnythingLLM.

---

## 2. Phase 24 Scope & Technical Requirements

### Task 1: Create Live Bus Dashboard (`00_Project_Interface/src/bus_dashboard.py`)
1. **Transaction Stream Parser**:
   - Parse `Bridge/messages.jsonl` and calculate key metrics:
     - Message states: `pending`, `in_progress`, `completed`, `failed`, `dlq`.
     - Communication vector traffic matrix (e.g. `interface_to_aggregator`, `aggregator_to_core`, `vertical`).
     - Processing latency per actor role (`system.master_architect`, `aggregator.architect`, `core.tda_engineer`, `model.builder`, `interface.operator`).
2. **Dashboard Renderers**:
   - **CLI Mode (`--cli`)**: Rich terminal status matrix.
   - **Markdown Dashboard Export (`--export-md`)**: Generate structured Markdown dashboard (`BUS_OBSERVABILITY_DASHBOARD.md`) containing tables, vector stats, and Mermaid diagram code block representation of system state.
   - **SVG Topology Generator (`--export-svg`)**: Render an architectural node/bus topology graph SVG (`system_topology.svg`) displaying node statuses and active traffic.

### Task 2: Gateway Visualizer Sync Integration
1. Extend `00_Project_Interface/src/anythingllm_gateway.py` with `--sync-dashboard`:
   - Automatically push generated `BUS_OBSERVABILITY_DASHBOARD.md` and topology graphs to AnythingLLM workspace `Discovery_Engine` via REST API.
   - Ensure seamless fallback if AnythingLLM API is unreachable.

### Task 3: Update Node 00 Interface Specifications
1. **`00_Project_Interface/NOTEBOOK_PASSPORT_INTERFACE.md`**:
   - Register `bus_dashboard.py` under Node 00 MCP tools and operational CLI flags.
2. **`00_Project_Interface/CONTEXT_DOMAIN_INTERFACE.md`**:
   - Add schemas for observability metrics and topology graph descriptors.

### Task 4: Governance & Manifest Synchronization
1. Update `system_manifest.json` version `3.2.1` → `3.3.0`. Register `bus_dashboard.py` tool entry and observability schemas.
2. Update `PROJECT_STATE.md` header metrics and log Phase 24 milestone.
3. Record architectural decision in `docs/adr/0005-live-bus-dashboard-and-anythingllm-visualizers.md`.

---

## 3. Verification Criteria
1. **Syntax & Compilation**: `python -m py_compile 00_Project_Interface/src/bus_dashboard.py` exits with `0`.
2. **Dashboard Execution**:
   - `python 00_Project_Interface/src/bus_dashboard.py --cli` returns structured execution metrics with exit code `0`.
   - `python 00_Project_Interface/src/bus_dashboard.py --export-md` produces valid Markdown with Mermaid graph.
3. **Gateway Visualizer Test**:
   - `python 00_Project_Interface/src/anythingllm_gateway.py --test --api-key AC2DW6K-E5T4QV7-PWHYFTG-E8KXP50 --workspace Discovery_Engine` passes with `status: online`.
4. **Manifest & Pipeline Integrity**:
   - `json.load()` on `system_manifest.json` passes.
   - `tomllib.load()` on `pyproject.toml` passes.
   - `python tests/e2e/test_e2e_pipeline.py` passes all 4 stages with exit code `0`.

---

## 4. Execution Output Protocol
Upon completion, register directive status as `completed` on `Bridge/messages.jsonl` and generate execution report at:
`Bridge/out/execution_reports/report_phase24_v3.3.0_[TIMESTAMP].md`
