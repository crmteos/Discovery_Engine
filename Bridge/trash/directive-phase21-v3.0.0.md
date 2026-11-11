# Directive Phase 21 (v3.0.0) — Architectural Standardization & Workspace Layout Refactoring

**Issuer:** system.master_architect (Gemini)  
**Executor:** cline.executor (Cline Execution Engineer)  
**Target Version:** v3.0.0  
**Communication Channel:** Bridge/in/ (Primary Directive Gateway)  
**Bus Performative:** task_request  

---

## 1. Objective & Scope

The purpose of Phase 21 (v3.0.0) is to transition the **Discovery Engine** repository into a fully standardized, production-grade project layout adhering to modern software engineering best practices (PEP 518/621, ADR architecture records, isolated testing suites, and dedicated maintenance scripting).

This upgrade implements four structural enhancements:
1. **Architecture Decision Records (`docs/adr/`)**: Establish a permanent decision log.
2. **Isolated Test Hierarchy (`tests/`)**: Reorganize test suites out of the root directory.
3. **Project Metadata & Packaging (`pyproject.toml`)**: Centralize project configurations and dependencies.
4. **Maintenance Utility Suite (`scripts/`)**: Isolate operational tools from the core codebase.

---

## 2. Detailed Task Breakdown

### Task 1 — Architecture Decision Records (`docs/adr/`)
* Create directory: `docs/adr/`
* Deploy initial ADR documents:
  * `docs/adr/0001-dual-vertical-standard.md`: Document the isolation of Control Plane (Governance) and Data Plane (Domain Knowledge).
  * `docs/adr/0002-trash-bin-policy.md`: Document the non-destructive disposal protocol using `Bridge/trash/`.
  * `docs/adr/0003-single-prompt-gateway-protocol.md`: Document the 4-step execution workflow and single-prompt automation interface.

### Task 2 — Test Suite Reorganization (`tests/`)
* Create directory structure:
  * `tests/unit/`
  * `tests/integration/`
  * `tests/e2e/`
* Move `test_e2e_pipeline.py` from root to `tests/e2e/test_e2e_pipeline.py`.
* Ensure import paths in `test_e2e_pipeline.py` are adjusted so execution from root (`python tests/e2e/test_e2e_pipeline.py`) runs with `exit_code: 0`.

### Task 3 — Centralized Packaging Configuration (`pyproject.toml`)
* Create `pyproject.toml` in the project root containing:
  * Standard `[build-system]` table using setuptools.
  * `[project]` metadata (name: `discovery-engine`, version: `3.0.0`, description, python_requires: `>=3.12`).
  * `[project.dependencies]` detailing required packages (`networkx`, `sympy`, `rdflib`, `dspy-ai`, `torch`, `requests`).
  * `[tool.pytest.ini_options]` specifying `testpaths = ["tests"]`.

### Task 4 — Maintenance Utility Suite (`scripts/`)
* Create directory: `scripts/`
* Create helper scripts:
  * `scripts/clean_trash.py`: Operational script to manage/purge `Bridge/trash/` if needed.
  * `scripts/bus_status.py`: Operational CLI shortcut to inspect `Bridge/messages.jsonl` and `Bridge/messages_dlq.jsonl`.

### Task 5 — System Manifest Upgrade (`system_manifest.json`)
* Upgrade manifest version: `"version": "3.0.0"`.
* Register new directories: `docs/adr/`, `tests/`, `scripts/`, `pyproject.toml`.
* Verify manifest validity with `json.load()`.

### Task 6 — Master State Synchronization (`PROJECT_STATE.md`)
* Update header metrics: `Phase 21 — Architectural Standardization v3.0.0`.
* Update Tier 1 Governance and Directory Layout tables to reflect v3.0.0.
* Record Phase 21 milestone details in Execution History.

---

## 3. Verification & Acceptance Criteria

| # | Criterion | Verification Command | Expected Output |
|---|-----------|----------------------|-----------------|
| 1 | Manifest Integrity | `python -c "import json; json.load(open('system_manifest.json'))"` | PASSED (valid JSON) |
| 2 | Syntax Validation | `python -m py_compile tests/e2e/test_e2e_pipeline.py scripts/clean_trash.py scripts/bus_status.py` | `exit_code: 0` |
| 3 | E2E Pipeline Verification | `python tests/e2e/test_e2e_pipeline.py` | `exit_code: 0` (4/4 stages PASSED) |
| 4 | ADR Documentation | `ls docs/adr/` | `0001-...md`, `0002-...md`, `0003-...md` present |
| 5 | Packaging Metadata | `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"` | PASSED (valid TOML) |
| 6 | Execution Report | Save to `Bridge/out/execution_reports/report_phase21_v3.0.0_[TIMESTAMP].md` | File written & synced |

---

## 4. Post-Execution Protocol

Upon completing all tasks:
1. Update bus message status to `completed` in `Bridge/messages.jsonl`.
2. Generate execution report `Bridge/out/execution_reports/report_phase21_v3.0.0_[TIMESTAMP].md`.
