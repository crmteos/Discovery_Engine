# Directive Phase 20.2 — v2.9.2: Master Directives Path, Master Context File & Project Trash Standard

**Issuer:** system.master_architect (Gemini)  
**Executor:** cline.executor (Cline Execution Engineer)  
**Target Version:** v2.9.2  
**Timestamp:** 2026-11-10  
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)

---

### 1. Objective & Scope

This directive executes three crucial architectural fixes and standards for the Discovery Engine:

1. **Master Directive Path Standardisation**: Fix the root directive path. Master Architect (`system.master_architect`) directives are saved to `Bridge/in/` (not `Bridge/in/core/`). Update all governance specs, manifest entries, and scripts accordingly.
2. **Master Context Domain Deployment (`PROJECT_CONTEXT.md`)**: Create `PROJECT_CONTEXT.md` at the project root to complete the Dual-Vertical 2-File Standard for the Master Architect:
   - `PROJECT_STATE.md` → Control Plane (Master Governance, Node Registry, System Metrics)
   - `PROJECT_CONTEXT.md` → Data Plane (Master Knowledge Domain, RDF Graph Topology, Ingestion Standards)
3. **Project Trash Bin Standard (`Bridge/trash/`)**: Implement a non-destructive file lifecycle management standard. Create `Bridge/trash/` and mandate moving obsolete/executed directives, temporary `.py` scripts, and broken/outdated `.json` files into `Bridge/trash/` instead of hard deletion (`rm`/`unlink`).

---

### 2. Task Execution Plan

#### Task 1: Master Directive Path Alignment (`Bridge/in/`)
- Update `system_manifest.json` and `PROJECT_STATE.md` to declare `Bridge/in/` as the primary directive folder for `system.master_architect`.
- Deprecate `Bridge/in/core/` references for Master Architect directives.

#### Task 2: Creation of `PROJECT_CONTEXT.md` (Master Data Plane)
- Deploy `PROJECT_CONTEXT.md` at project root `/workspace/PROJECT_CONTEXT.md`.
- Move data-plane domain knowledge, global RDF graph topology, triple normalization rules, and cross-node data flow definitions into `PROJECT_CONTEXT.md`.
- Confirm Master Architect Notebook pair:
  1. `PROJECT_STATE.md` (Control Plane)
  2. `PROJECT_CONTEXT.md` (Data Plane)

#### Task 3: Deployment of Project Trash Bin (`Bridge/trash/`)
- Create `Bridge/trash/` directory.
- Update `system_manifest.json` under governance rules to enforce `trash_bin_policy`: all deprecated files, executed directives, and temporary scripts must be moved to `Bridge/trash/` (e.g. `Bridge/trash/directive-phase18-v2.7.0.md`).
- Move the following executed directive files into `Bridge/trash/`:
  - `Bridge/in/core/directive-phase18-v2.7.0.md` → `Bridge/trash/`
  - `Bridge/in/core/directive-phase19-v2.8.0.md` → `Bridge/trash/`
  - `Bridge/in/core/directive-phase20-v2.9.0.md` → `Bridge/trash/`
  - `Bridge/in/core/directive-phase20-cleanup-v2.9.1.md` → `Bridge/trash/`
- Clean any stray temporary Python scripts or broken draft JSONs into `Bridge/trash/`.

#### Task 4: Manifest & Master State Synchronization (v2.9.2)
- Upgrade `system_manifest.json` to version **2.9.2**:
  - Register `PROJECT_CONTEXT.md` under master governance artifacts.
  - Register `Bridge/trash/` directory under system storage layout.
  - Update `system.master_architect` directive input path to `Bridge/in/`.
- Synchronize `PROJECT_STATE.md` to version **v2.9.2**:
  - Update header metrics to `Phase 20.2 v2.9.2`.
  - Record Phase 20.2 in Execution History.
  - Add Project Trash Bin policy and Master Context Domain specifications.

---

### 3. Verification & Acceptance Criteria

| # | Criterion | Verification Command | Expected Outcome |
|---|---|---|---|
| 1 | Master Context File Created | `test -f PROJECT_CONTEXT.md` | `exit_code: 0` |
| 2 | Trash Bin Directory Deployed | `test -d Bridge/trash/` | `exit_code: 0` |
| 3 | Executed Directives Moved to Trash | `ls Bridge/trash/` | Contains `directive-phase18-v2.7.0.md`, etc. |
| 4 | Manifest JSON Validation | `python3 -c "import json; json.load(open('system_manifest.json'))"` | `PASSED` |
| 5 | E2E Pipeline Verification | `python3 test_e2e_pipeline.py` | `exit_code: 0` (4/4 stages OK) |
| 6 | Execution Report Saved | Check `Bridge/out/execution_reports/` | Report `report_phase20.2_v2.9.2_[TIMESTAMP].md` saved |

---

### 4. Single-Prompt Execution Command for Cline

```bash
# Step 1: Post directive to bus
python Bridge/bus_manager.py --post --sender system.master_architect --receiver cline.executor --vector vertical --performative task_request --topic directive-phase20.2-v2.9.2 --payload-file Bridge/in/directive-phase20.2-v2.9.2.md

# Step 2: Read directive and execute Tasks 1-4
# Step 3: Update bus message status to completed and output execution report
```
