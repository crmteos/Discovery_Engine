# DIRECTIVE: Phase 34 (v4.3.0) — OSINT Search & AI Grounding Intake Adapter

**TARGET VERSION:** v4.3.0  
**TARGET PHASE:** Phase 34  
**MODULE:** 05_Knowledge_Aggregator & 00_Project_Interface  
**EXECUTION MODE:** Autonomous Single-Prompt Gateway Execution  
**BUDGET LIMIT:** $0.00 (Zero-Budget Open-Source & Local Fallback Stack)

---

## 1. Context & Baseline
Phase 33 (v4.2.0) successfully integrated `--llm-extract` into `intake_processor.py` bound to `ollama_gateway.py`.
Phase 34 focuses on implementing the OSINT Search & AI Grounding Intake Adapter (`05_Knowledge_Aggregator/src/search_intake_adapter.py`) to ingest search results, web overviews, and grounded web sources directly into the RDF normalization pipeline.

---

## 2. Key Requirements & Architecture

### A. Search & AI Grounding Intake Adapter (`search_intake_adapter.py`)
- Implement `05_Knowledge_Aggregator/src/search_intake_adapter.py`.
- Support query intake from role `aggregator.osint_analyst`.
- Use zero-cost search fetching (e.g. `duckduckgo_search` / open web search wrappers / standard HTTP requests with graceful offline fallback).
- Convert search results and web summaries into structured JSON intake drafts (`Intake_Queue/drafts/`) containing text summaries and source URLs.
- Pass generated drafts to `intake_processor.py` for triple normalization, automatically adding `prov:wasDerivedFrom` and `skos:Concept` metadata.

### B. Offline & Resilience Fallback
- If internet connection is unavailable or search API returns an error/rate-limit (HTTP 429), fall back gracefully to offline processing of pre-existing `Intake_Queue/` drafts without raising uncaught exceptions (`exit_code: 0` with diagnostic warning).

### C. Automated Testing (`tests/integration/test_search_intake_adapter.py`)
- Create integration test `tests/integration/test_search_intake_adapter.py`.
- Verify query handling, draft creation, schema validation, and graceful offline fallback mode.
- Ensure `python -m py_compile` passes for all modified and created Python files with `exit_code: 0`.

---

## 3. Memory Triad & State Synchronization (v4.3.0)

1. **PROJECT_SPEC.md**:
   - Update header to `v4.3.0 / Phase 34`.
   - Register OSINT Search & AI Grounding Intake Adapter in Module 05 specification.
   - Synchronize DoD to v4.3.0.

2. **PROJECT_CONTEXT.md**:
   - Update header to `v4.3.0 / Phase 34`.
   - Add Section 11: OSINT Search & Grounding Intake Topology & Flow.

3. **PROJECT_STATE.md**:
   - Update header metrics to `VERSION: v4.3.0 | PHASE: Phase 34`.
   - Update top block `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` to Phase 34 — COMPLETE.
   - Synchronize `Current Phase:` text field below metrics to match Gateway Report.
   - Log Phase 34 in Execution History.

---

## 4. Synchronization & Git Operations

1. Run Google Drive Sync Script:
   ```bash
   python scripts/sync_gdrive.py
   ```
2. Git Commit & Push:
   ```bash
   git add PROJECT_SPEC.md PROJECT_CONTEXT.md PROJECT_STATE.md 05_Knowledge_Aggregator/ tests/
   git commit -m "feat(phase-34): implement osint search & ai grounding intake adapter"
   git push origin main
   ```

---

## 5. Definition of Done (DoD) Checklist
- [ ] `search_intake_adapter.py` created and syntax verified (`py_compile`).
- [ ] `test_search_intake_adapter.py` passes with `exit_code: 0` (including offline fallback).
- [ ] `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md` synchronized to v4.3.0.
- [ ] `PROJECT_STATE.md` starts with updated `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` and matching `Current Phase:` field.
- [ ] `python scripts/sync_gdrive.py` executed successfully.
- [ ] `git commit` and `git push origin main` completed.
- [ ] Budget remains exactly $0.00.
