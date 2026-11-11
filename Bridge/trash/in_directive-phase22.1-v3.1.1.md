# Directive Phase 22.1 — Legacy Artifact Analysis & Bridge Deep Cleanup (v3.1.1)

**Issuer:** system.master_architect (Gemini)  
**Executor:** cline.executor (Cline Execution Engineer)  
**Target Version:** v3.1.1  
**Communication Vector:** vertical  

---

## Task Overview

### 1. Environment Specs Audit & Integration
- Inspect `Bridge/out/ENVIRONMENT_SPECS.md`.
- Verify that hardware/environment telemetry logic is cleanly integrated into `scripts/` (e.g., `scripts/bus_status.py` or `scripts/system_telemetry.py`).
- Ensure relevant hardware environment specs (CPU, RAM, GPU, Ollama model specifications) are recorded in `PROJECT_CONTEXT.md` (Data Plane).
- Move `Bridge/out/ENVIRONMENT_SPECS.md` to `Bridge/trash/`.

### 2. Legacy Directives & Reports Deep Audit
- Perform a thorough audit of all legacy `.md` files in `Bridge/in/` (including `in/core/`, `in/aggregator/`, etc.) and `Bridge/out/` (including `out/execution_reports/`, `out/aggregator_reports/`, etc.).
- Analyze the text of these directives and reports to detect any unfulfilled requirements, roadmap ideas, or architectural concepts that were proposed but never implemented in the current v3.1.0 codebase.
- If any unfulfilled ideas or backlog items are found, extract and document them in `docs/UNIMPLEMENTED_IDEAS.md`. If all features are 100% implemented, record a empty/clear backlog confirmation in `docs/UNIMPLEMENTED_IDEAS.md`.
- Move all analyzed legacy directive files and report files to `Bridge/trash/` (leaving `Bridge/in/` and `Bridge/out/` clean, while preserving active bus runtime files like `messages.jsonl`).

### 3. Manifest & Master State Synchronization
- Upgrade `system_manifest.json` version to `3.1.1`.
- Upgrade `PROJECT_STATE.md` to `v3.1.1` and append Phase 22.1 under Execution History.

### 4. Verification Protocol
- Run `python scripts/bus_status.py`
- Run `json.load()` on `system_manifest.json`
- Run `tomllib.load()` on `pyproject.toml`
- Run `python tests/e2e/test_e2e_pipeline.py` -> must exit with code `0`
- Post transaction outcome to `Bridge/messages.jsonl` with status `completed`
- Save report to `Bridge/out/execution_reports/report_phase22.1_v3.1.1_[TIMESTAMP].md`
