# ENGINEERING DIRECTIVE: Phase 33 (v4.2.0)
**System:** Discovery Engine — Autonomous Knowledge Infrastructure
**Target Component:** Node 05 (Knowledge Aggregator) + Node 00 (Ollama Gateway Integration)
**Execution Mode:** Single-Prompt Gateway Protocol (Stateless Autonomous Execution)
**Budget Limit:** $0.00 (Strict Zero-Budget Local Stack)
**Baseline Version:** v4.1.0 / Phase 32

---

## 1. Executive Summary & Objective
Phase 33 focuses on binding the local Ollama LLM Gateway (`00_Project_Interface/src/ollama_gateway.py`) directly into **Node 05 (`05_Knowledge_Aggregator/src/intake_processor.py`)**. 

Currently, `intake_processor.py` processes pre-structured JSON drafts. Under Phase 33, it will gain automated NLP RDF Triple Extraction capabilities using local LLM inference (fallback chain: `qwen2.5-coder:14b` -> `llama3.1:8b` -> `qwen2.5:7b`), converting unstructured text into W3C PROV-O / SKOS compliant RDF triplets with SHACL shape validation.

---

## 2. Scope of Work (Pillars A - D)

### Pillar A: Ollama LLM Binding in Intake Processor
1. Update `05_Knowledge_Aggregator/src/intake_processor.py`:
   - Add `--llm-extract` CLI mode.
   - Import `ollama_gateway.py` from `00_Project_Interface/src/`.
   - Implement structured JSON prompt template forcing LLM to output valid RDF triplets (`subject`, `predicate`, `object`, `graph_context`).
   - Add graceful offline fallback: if Ollama server is unreachable, log warning and skip LLM stage without throwing unhandled exceptions.

### Pillar B: Validation & Integration Test
1. Create `tests/integration/test_aggregator_ollama_binding.py`:
   - Test end-to-end extraction pipeline with sample unstructured text.
   - Verify `py_compile` on all modified files (`exit_code: 0`).
   - Run `--test` mode verifying zero-crash operation both with online Ollama and offline fallback.

### Pillar C: 3-File Memory Protocol Update (v4.2.0)
1. Synchronize Memory Triad:
   - **`PROJECT_SPEC.md`**: Update version header to `v4.2.0 / Phase 33`. Add Node 05 Ollama Extraction specification to Architecture.
   - **`PROJECT_CONTEXT.md`**: Update version header to `v4.2.0 / Phase 33`. Add NLP Intake Pipeline topology to Section 5.
   - **`PROJECT_STATE.md`**: Update version header to `v4.2.0 / Phase 33`. Update `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block with Phase 33 details and tests. Ensure `Current Phase:` text field matches Gateway Report.

### Pillar D: Automation & Persistence
1. Run `python scripts/sync_gdrive.py` to mirror updated files to Google Drive.
2. Execute local Git commit:
   `git add PROJECT_SPEC.md PROJECT_CONTEXT.md PROJECT_STATE.md 05_Knowledge_Aggregator/ tests/`
   `git commit -m "feat(phase-33): bind ollama gateway to node 05 intake processor for automated rdf extraction"`
3. Push to GitHub: `git push origin main`.

---

## 3. Definition of Done (DoD)
- [ ] `intake_processor.py` contains `--llm-extract` mode with `ollama_gateway.py` integration
- [ ] `tests/integration/test_aggregator_ollama_binding.py` passes with `exit_code: 0`
- [ ] `py_compile` passes for all modified scripts
- [ ] `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` updated to `v4.2.0 / Phase 33`
- [ ] `PROJECT_STATE.md` contains updated `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)`
- [ ] `scripts/sync_gdrive.py` executed successfully
- [ ] Git commit and `git push origin main` completed successfully
