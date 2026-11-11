# Directive Phase 29 (v3.8.0) — E2E Pure Python Pipeline Benchmark & Ollama Gateway Binding

**Sender:** `system.master_architect`  
**Receiver:** `cline.executor`  
**Vector:** `vertical`  
**Performative:** `inform`  
**Topic:** `directive:phase29`  
**Date:** 2026-11-11  
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)  

---

### 1. Goal & Architectural Purpose
Phase 29 standardizes the end-to-end integration benchmark using the newly deployed Zero-Dependency Pure Python Engines (`pure_rdf_engine.py`, `pure_tda_engine.py`, `pure_symbolic_engine.py`) alongside local Ollama LLM REST binding, validating full offline operational capability under $0.00 budget governance.

---

### 2. Execution Pillars

#### Pillar A: Pure Python E2E Integration Benchmark
- Create/verify `tests/e2e/test_pure_e2e_pipeline.py` executing 4 stages:
  1. Knowledge Intake & Triple Normalization (`05_Knowledge_Aggregator`)
  2. Pure RDF Topology & Graph Construction (`pure_rdf_engine.py`)
  3. Pure TDA Gap & Invariant Extraction (`pure_tda_engine.py` — Betti H0/H1)
  4. Pure Symbolic Regression & Model Assembly (`pure_symbolic_engine.py` + `06_Formalized_Model`)
- Ensure all tests run in pure Python without external native C-dependencies.

#### Pillar B: Ollama Local REST Gateway Implementation
- Implement/verify `00_Project_Interface/src/ollama_gateway.py` with:
  - Liveness ping to local Ollama API
  - Model fallback chain (`qwen2.5-coder:14b` -> `llama3.1:8b` -> `qwen2.5:7b`)
  - Standalone `--test` CLI execution mode with graceful fallback if server is offline.

#### Pillar C: 3-File Memory Protocol (ADR-004) & Execution Report
- Perform `py_compile` syntax verification on all modified files (`exit_code: 0`).
- Execute `test_pure_e2e_pipeline.py` and verify `exit_code: 0`.
- Update `PROJECT_SPEC.md` (sync version to v3.8.0 / Phase 29).
- Update `PROJECT_CONTEXT.md` (sync version and REST endpoints).
- Update `PROJECT_STATE.md` with:
  - Top block: `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` (timestamp, test status, completed message ID).
  - Milestone log: Phase 29 — COMPLETE.
- Mark message status as `completed` on `Bridge/bus_manager.py`.
- Execute local Git commit:
  `git add PROJECT_SPEC.md PROJECT_CONTEXT.md PROJECT_STATE.md tests/ 00_Project_Interface/ Bridge/`
  `git commit -m "feat(phase-29): e2e pure python benchmark & ollama gateway binding"`

---

### 3. Definition of Done (DoD)
- [ ] `tests/e2e/test_pure_e2e_pipeline.py` runs with exit_code 0.
- [ ] `00_Project_Interface/src/ollama_gateway.py` passes `--test`.
- [ ] `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` synchronized to v3.8.0.
- [ ] `PROJECT_STATE.md` updated with `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ`.
- [ ] Local Git commit completed.
- [ ] Budget strictly preserved at $0.00.
