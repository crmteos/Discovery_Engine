# Directive Phase 22 (v3.1.0) — General Project File Audit, Refactoring & Clean Architecture

**Issuer:** system.master_architect (Gemini)  
**Executor:** cline.executor (Cline Execution Engineer)  
**Target System Version:** v3.1.0  
**Primary Directive Path:** `Bridge/in/directive-phase22-v3.1.0.md`  
**Governance Standard:** Dual-Vertical Control/Data Plane, Single-Prompt Gateway Protocol, Trash Bin Safeguard (`Bridge/trash/`)

---

## 1. Objective & Scope

Perform a **General Audit and Refactoring** across the entire `Discovery_Engine` codebase. Every file in the repository must be audited against our standardized v3.0.0 Feature-Based Isolation Layout to eliminate clutter, consolidate redundant context files, move misplaced artifacts to their canonical locations, and transfer obsolete files to `Bridge/trash/`.

---

## 2. Execution Tasks

### Task 1: Complete Directory Audit & Misplaced File Sweep
1. **Root Directory Cleanliness Audit**:
   * Inspect all files lingering in the project root (`Discovery_Engine/`).
   * Ensure ONLY canonical root governance files remain in the root directory:
     * `system_manifest.json`
     * `PROJECT_STATE.md`
     * `PROJECT_CONTEXT.md`
     * `pyproject.toml`
     * `README.md` (if present)
     * `.gitignore`
   * Move any standalone utility Python scripts to `scripts/` and any test scripts to `tests/`.

2. **Node Envelope Audit (Nodes 00, 01, 05, 06)**:
   * Verify that each node directory contains strictly:
     * `schemas/` (JSON/SHACL/OWL contracts)
     * `src/` (Encapsulated implementation Python code)
     * `NOTEBOOK_PASSPORT_[NODE].md` (Control Plane interface)
     * `CONTEXT_DOMAIN_[NODE].md` (Data Plane interface)
   * Consolidate any remaining fragmented markdown or text instruction files into `NOTEBOOK_PASSPORT_[NODE].md` or `CONTEXT_DOMAIN_[NODE].md`.

### Task 2: Trash Relocation & Sanitization (`Bridge/trash/`)
1. Scan for obsolete/temporary artifacts:
   * Completed directive markdown files in `Bridge/in/` (older than current phase).
   * Temporary execution scripts, residual test logs, broken `.json` files, and `.pyc` / `__pycache__` artifacts.
2. Relocate all obsolete/unneeded files to `Bridge/trash/` using `shutil.move` or `scripts/clean_trash.py`. **NEVER use hard deletion (`rm` / `unlink`)**.

### Task 3: Architectural Decision Record (ADR 0004)
Create `docs/adr/0004-general-file-audit-and-cleanup.md`:
* **Title**: ADR 0004: General Codebase Audit, File Standardization and Trash Archival.
* **Status**: Accepted.
* **Context**: Project growth led to residual files and minor layout drift.
* **Decision**: All nodes strictly enforce 2-file envelopes, root contains only core governance manifests, obsolete files are archived to `Bridge/trash/`.

### Task 4: Governance & Manifest Upgrade (v3.1.0)
1. Update `system_manifest.json` to version `"3.1.0"`:
   * Record Phase 22 audit milestone and updated file inventory.
2. Update `PROJECT_STATE.md` to version **v3.1.0**:
   * Record Phase 22 under Execution History.
   * Update header metrics and System Readiness.

---

## 3. Verification & Acceptance Criteria

1. **Root & Node Cleanliness**: No misplaced `.py`, `.md`, or `.json` files in project root or node roots.
2. **Node Envelope Enforcement**: Nodes 00, 01, 05, 06 each contain strictly 2 markdown interface files (`NOTEBOOK_PASSPORT` + `CONTEXT_DOMAIN`).
3. **ADR 0004 Deployed**: `docs/adr/0004-general-file-audit-and-cleanup.md` exists and is valid Markdown.
4. **Bus Status Check**: `python scripts/bus_status.py` executes with `exit_code: 0`.
5. **E2E Pipeline Test**: `python tests/e2e/test_e2e_pipeline.py` passes all 4 stages with `exit_code: 0`.
6. **Manifest Integrity**: `json.load()` on `system_manifest.json` and `tomllib.load()` on `pyproject.toml` pass without errors.
7. **Execution Report**: Report saved to `Bridge/out/execution_reports/report_phase22_v3.1.0_[TIMESTAMP].md`.

---
*End of Directive Phase 22 (v3.1.0)*
