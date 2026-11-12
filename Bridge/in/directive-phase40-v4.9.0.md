# Directive Phase 40 — v4.9.0
**Target System**: Discovery Engine Core Framework  
**Phase**: 40  
**Version**: v4.9.0  
**Budget Constraint**: $0.00 (Zero-Budget Enforcement)  
**Governance Standard**: Dual-Vertical 2-File Standard (ADR-0001), 3-File Memory Protocol & Drive Sync Gateway (ADR-0005)

---

## 1. Executive Summary & Objective

Phase 40 completes **Stage 2 (Firebase Genkit Orchestration)** of the system expansion roadmap. The objective of Phase 40 is to integrate **Genkit Telemetry & Tracing** and establish the **Genkit Developer UI CLI Launcher** within Node 00 (`00_Project_Interface`). This grants full visual inspection over agent execution flows, tool calls, and prompt latency without incurring third-party SaaS logging costs ($0.00 enforcement).

---

## 2. Core Requirements & Task Breakdown

### Task 1: Genkit Tracing & Telemetry Module
- Create `00_Project_Interface/src/genkit_tracer.py`:
  - Implements local telemetry logging and trace collection for Genkit flows running across Node 05 (`Knowledge Aggregator`) and Node 06 (`Formalized Model`).
  - Supports offline file-based trace dumps (`logs/genkit_traces.jsonl`) with graceful fallback when Genkit CLI UI is not running.
  - Ensures compliance with zero-network air-gap standards ($0.00 budget).

### Task 2: Genkit Developer UI Launcher Script
- Create `scripts/start_genkit_ui.py`:
  - Command-line utility to invoke `npx genkit start` or launch the local trace viewer.
  - Includes `--check-deps` flag to verify local Node.js/npx availability without failing build pipelines when absent.

### Task 3: Integration Testing
- Create `tests/integration/test_genkit_tracing.py`:
  - Verifies that `genkit_tracer.py` records flow executions, prompt inputs/outputs, and latency metrics correctly.
  - Validates `py_compile` syntax and ensures execution returns `exit_code: 0`.

### Task 4: Memory Triad & Git Synchronization (v4.9.0)
- Update headers and status blocks in:
  - `PROJECT_SPEC.md` -> Version: v4.9.0 / Phase 40
  - `PROJECT_CONTEXT.md` -> Version: v4.9.0 / Phase 40
  - `PROJECT_STATE.md` -> Version: v4.9.0 / Phase 40 (Log Phase 39 and Phase 40 completion in Gateway Report)
- Execute `python scripts/sync_gdrive.py`.
- Execute `git commit -m "feat(phase40): integrate Genkit Developer UI tracing and launcher v4.9.0"` and `git push origin main`.

---

## 3. Definition of Done (DoD)

1. `00_Project_Interface/src/genkit_tracer.py` implemented with offline trace handling.
2. `scripts/start_genkit_ui.py` implemented and verified.
3. `tests/integration/test_genkit_tracing.py` passes with `exit_code: 0`.
4. All 3 memory files updated to **v4.9.0**.
5. `sync_gdrive.py` executed successfully.
6. `git push origin main` confirmed.
