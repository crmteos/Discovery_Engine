# DIRECTIVE_PHASE18_v2.7.0: System Architecture Refactoring & Node 00 Deployment

**Issuer:** `system.master_architect` (Gemini)  
**Recipient:** `cline.executor` (Cline Execution Engineer)  
**Target Version:** v2.7.0  
**Phase:** Phase 18 — Architecture & Dual-Vertical Standardization  
**Execution Standard:** Zero-Budget, Production-Grade (Zero Mocks), Stateless Autonomous Session  

---

## 1. Context & Objectives

During the evolution of the system from a single-node setup to a 3-node pipeline, local `bridge/in/` and `bridge/out/` subdirectories accumulated inside individual nodes (`01_Formal_Core`, `05_Knowledge_Aggregator`, `06_Formalized_Model`). This created architectural collisions, context pollution, and version drift in `PROJECT_STATE.md`.

**Phase 18 Directive Goals:**
1. Upgrade `system_manifest.json` to **v2.7.0** with explicit Dual-Vertical Architecture definitions (Control Plane vs Data Plane).
2. Deploy **`00_Project_Interface`** (Dashboard Node) for unified cross-node architecture and context inspection.
3. Remove legacy node-level `bridge/in/` and `bridge/out/` folders, standardizing all inter-node and inter-role communications on the transactional Message Bus (`Bridge/bus_manager.py` & `Bridge/messages.jsonl`).
4. Update `PROJECT_STATE.md` to synchronize all version markers to **v2.7.0**.

---

## 2. Detailed Task Breakdown

### Task 1: Upgrade `system_manifest.json` to v2.7.0
* Update system manifest `version` to `"2.7.0"`.
* Register new node `00_Project_Interface` under `node_registry`:
  * Path: `00_Project_Interface/`
  * Sub-components: `schemas/`, `src/`
  * Status: `🟢 Active`
* Register new role `interface.operator` in `role_capability_registry`:
  * Allowed communication vectors: `interface_to_master`, `interface_to_bus`, `interface_to_nodes`
  * MCP Tool Spec: workspace inspection, execution reporting, architecture visualization.
* Remove legacy node-specific `bridge/in` and `bridge/out` path bindings from `01_Formal_Core`, `05_Knowledge_Aggregator`, and `06_Formalized_Model` registries. All communication must route via `Bridge/bus_manager.py`.

### Task 2: Physical Deployment of `00_Project_Interface`
* Create directory structure:
  * `00_Project_Interface/schemas/`
  * `00_Project_Interface/src/`
* Implement **`00_Project_Interface/src/architecture_view.py`**:
  * Inspects `system_manifest.json`, `Bridge/messages.jsonl`, `Bridge/messages_dlq.jsonl`, and `PROJECT_STATE.md`.
  * Outputs CLI diagnostic summary of system health, active nodes, bus transactions, and DLQ status.
  * Supports `--test` flag returning `exit_code: 0` on clean state.
* Implement **`00_Project_Interface/src/context_view.py`**:
  * Inspects knowledge graph state, normalized triple counts in `05_Knowledge_Aggregator/Processed_Gate/normalized_triples/`, OWL shapes in `01_Formal_Core`, and assembled target models in `06_Formalized_Model`.
  * Supports `--test` flag returning `exit_code: 0`.

### Task 3: Node-Level Legacy Bridge Cleanup
* Remove nested `bridge/in/` and `bridge/out/` directories from `01_Formal_Core/`, `05_Knowledge_Aggregator/`, and `06_Formalized_Model/`.
* Preserve central `Bridge/` root directory (`Bridge/bus_manager.py`, `Bridge/messages.jsonl`, `Bridge/in/core/`, `Bridge/out/execution_reports/`).

### Task 4: Master State Synchronization (`PROJECT_STATE.md`)
* Update header metrics and current phase to **Phase 18 v2.7.0**.
* Update all version references in tables (Tier 1 Governance, Central Manifest, Node Envelope Structure) from `v2.2.0` / `v2.6.0` to `v2.7.0`.
* Record Phase 18 completion entry under Execution History.

---

## 3. Verification & Acceptance Criteria

1. `python -m py_compile 00_Project_Interface/src/architecture_view.py` -> `exit_code: 0`
2. `python -m py_compile 00_Project_Interface/src/context_view.py` -> `exit_code: 0`
3. `python 00_Project_Interface/src/architecture_view.py --test` -> `exit_code: 0`
4. `python test_e2e_pipeline.py` -> `exit_code: 0`
5. `json.load()` validation on `system_manifest.json` -> `PASSED`
6. Execution report saved to `Bridge/out/execution_reports/report_phase18_v2.7.0_[TIMESTAMP].md`.

---
*Directive issued by Gemini Master Architect for immediate execution by Cline Execution Engineer.*
