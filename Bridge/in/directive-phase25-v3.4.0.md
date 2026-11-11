# Directive Phase 25 — Visual Patterns Engine & AnythingLLM Exporter Integration (v3.4.0)

**Header Metrics:** BUDGET: $0.00 | SESSION: Autonomous Clean State | SYSTEM READINESS: 🟢 100% Core Deployed  
**Sender:** `system.master_architect` (Gemini Notebook Master Architect)  
**Receiver:** `cline.executor` (Cline Execution Engineer)  
**Date:** 2026-11-10  
**Version:** v3.4.0  

---

### 1. Context & Objective
Following the approval of the **Visualization Patterns Handbook** (`visualization-patterns-handbook.md`), Phase 25 focuses on turning theoretical information design standards (Tufte, Few, Bertin, Cairo, Ware, Aigner, Rosenberg) into executable Python generators within Node 00 (`00_Project_Interface/src/visualizers/`) and integrating them with the AnythingLLM Gateway.

---

### 2. Required Tasks

#### Task 2.1: Deploy Visual Patterns Reference Document
* Copy/deploy the handbook to `docs/VISUALIZATION_PATTERNS.md` to establish an in-repository reference for all visualization generators.

#### Task 2.2: Implement Visual Generator Suite in `00_Project_Interface/src/visualizers/`
Create the dedicated package `00_Project_Interface/src/visualizers/` containing:
1. `__init__.py`: Package initialization and unified interface.
2. `executive_dashboard.py`: At-a-Glance Executive Bus Dashboard (Stephen Few 5-second rule, Tufte Data-to-Ink ratio). Reads `Bridge/messages.jsonl` and generates clean Mermaid KPI panels.
3. `timeline_visualizer.py`: Time-Oriented Phase Topology (Aigner/Rosenberg time data model). Visualizes Phase 0–25 evolution and ADR timeline.
4. `rdf_graph_visualizer.py`: Semantic Knowledge Network (Jacques Bertin semiology). Renders RDF triples from Node 05 (`05_Knowledge_Aggregator`) as Mermaid state/class diagrams or DOT graphs.
5. `tda_gap_visualizer.py`: TDA Betti Gap & Invariant Visualizer (Colin Ware preattentive perception, Alberto Cairo functional art). Visualizes Betti numbers ($H_0, H_1$), SymPy invariants, and detected knowledge gaps.
6. `iso42010_visualizer.py`: Visual Causality Architecture (Edward Tufte causal explanations). Renders ISO/IEC/IEEE 42010 3-view models (Structural, Behavioral, Ontological).
7. `adr_matrix_visualizer.py`: ADR & Interaction Map (David Sibbet visual meeting methods). Visualizes actor role dependencies and decision histories (ADR 0001–0006).

#### Task 2.3: Enhance AnythingLLM Gateway (`00_Project_Interface/src/anythingllm_gateway.py`)
* Add CLI flag `--export-visuals` / `--sync-all-visuals` to trigger all visualizers in `00_Project_Interface/src/visualizers/`, compile their Markdown/Mermaid outputs into a unified visual suite, and upload them to the `Discovery_Engine` Workspace via AnythingLLM REST API (`/v1/workspace/discovery_engine/update-embeddings` / document upload).

#### Task 2.4: Architectural Decision Record (ADR 0006)
* Create `docs/adr/0006-visualization-patterns-and-anythingllm-exporter.md` detailing the decision to adopt the 6-pattern visualization engine and AnythingLLM exporter.

#### Task 2.5: Synchronize System Manifest & State (v3.4.0)
* Upgrade `system_manifest.json` to version `3.4.0`, registering the new `00_Project_Interface/src/visualizers/` modules and visual export capabilities.
* Update `PROJECT_STATE.md` with Phase 25 status and header metrics.

---

### 3. Verification Criteria
1. `py_compile` exits with code `0` for all scripts under `00_Project_Interface/src/visualizers/`.
2. Execution of each visualizer script with `--export-md` produces valid Markdown containing Mermaid syntax.
3. Execution of `anythingllm_gateway.py --test --api-key AC2DW6K-E5T4QV7-PWHYFTG-E8KXP50 --workspace Discovery_Engine` verifies live API connectivity (`online`, HTTP 200).
4. `json.load()` on `system_manifest.json` and `tomllib.load()` on `pyproject.toml` pass without errors.
5. End-to-end integration benchmark `tests/e2e/test_e2e_pipeline.py` passes all 4 stages with `exit_code: 0`.

---

### 4. Completion Handoff
* Update the message status on `Bridge/messages.jsonl` to `completed`.
* Generate the execution report at `Bridge/out/execution_reports/report_phase25_v3.4.0_[TIMESTAMP].md`.
