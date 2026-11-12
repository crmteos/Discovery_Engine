# ENGINEERING DIRECTIVE: Phase 45 (v5.4.0)
**Module:** `00_Project_Interface` & Enterprise Data Connectors  
**Target Architecture:** Discovery Engine v5.4.0 (Enterprise Scaling & BigQuery Agent Search)  
**Governance Standard:** Dual-Vertical 2-File Standard (ADR-0001), Single-Prompt Gateway Protocol (ADR-0003), Zero-Dollar Budget ($0.00)

---

### EXECUTIVE SUMMARY & GOAL

Phase 45 completes **Stage 4 (Enterprise Scaling & Agent Search)** by implementing **BigQuery Agent Search & External Enterprise Memory Integration** in `00_Project_Interface/src/bigquery_agent_search.py`.

This module provides enterprise-grade data search capabilities across BigQuery tables and external vector indexes when `enterprise=True`, while enforcing a **100% strict offline fallback ($0.00 budget)** using local JSONL/SQLite indices when GCP BigQuery credentials or network connections are absent.

---

### SPECIFIC IMPLEMENTATION TASKS

#### Task 1: Enterprise BigQuery Agent Search (`00_Project_Interface/src/bigquery_agent_search.py`)
- Implement `bigquery_agent_search.py` supporting CLI flags: `--dataset`, `--query`, `--limit`, `--offline`, `--json`.
- Implement `BigQueryAgentSearch` class:
  - If `google-cloud-bigquery` / GCP environment is available and credentials exist, query enterprise datasets.
  - If offline or missing credentials, fallback gracefully to searching local knowledge bases (`Bridge/bus_manager.py` JSONL messages, node passports, or local RDF triples).
  - Preserve W3C PROV-O provenance metadata in search results.
  - Return `exit_code: 0` in all execution paths.

#### Task 2: Integration Testing (`tests/integration/test_bigquery_agent_search.py`)
- Create integration test `tests/integration/test_bigquery_agent_search.py`:
  - Test syntax validity (`py_compile`).
  - Test fallback execution mode (`--offline`).
  - Verify JSON structure and W3C PROV-O provenance preservation.
  - Enforce `exit_code: 0` for zero-mock fallback verification.

#### Task 3: Memory Triad Update (v5.4.0 / Phase 45)
- Update `PROJECT_SPEC.md`: Bump version header to `v5.4.0 / Phase 45`. Update System Architecture section with BigQuery Agent Search capability.
- Update `PROJECT_CONTEXT.md`: Bump version header to `v5.4.0 / Phase 45`. Register `bigquery_agent_search.py` under Node 00 interfaces.
- Update `PROJECT_STATE.md`: Bump version header to `v5.4.0 / Phase 45`. Log Phase 45 execution in the Master Execution Log & Gateway Report.

#### Task 4: Drive & Git Synchronization
- Run `python scripts/sync_gdrive.py` to synchronize all 3 memory files to Google Drive.
- Run `git add .`, `git commit -m "feat(phase45): implement bigquery agent search with offline fallback (v5.4.0)"`, and `git push origin main`.

---

### DEFINITION OF DONE (DoD) CHECKLIST

- [ ] `00_Project_Interface/src/bigquery_agent_search.py` implemented with offline fallback.
- [ ] `tests/integration/test_bigquery_agent_search.py` passes with `exit_code: 0`.
- [ ] Memory triad updated to `v5.4.0` / Phase 45.
- [ ] `scripts/sync_gdrive.py` executed successfully.
- [ ] `git push origin main` completed.
