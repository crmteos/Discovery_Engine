# PHASE DIRECTIVE: Phase 37 (v4.6.0)
## Dynamic Provider Switcher & Hybrid LLM Extraction in Intake Processor

### Metadata & Governance
* **Target Version:** v4.6.0
* **Phase:** Phase 37 — COMPLETE DUAL-PROVIDER FALLBACK IN INTAKE PROCESSOR
* **Budget Limit:** $0.00 (Pure Open-Source & Free Tier Google AI Studio API)
* **Architecture Standard:** 3-File Memory Protocol (ADR-0004), Drive Sync Gateway (ADR-0005)

---

### Objectives
1. **Dynamic Provider Selection in `intake_processor.py`**:
   * Update `05_Knowledge_Aggregator/src/intake_processor.py` to support `--provider {auto,ollama,google}`.
   * In `auto` mode: Attempt extraction via `google_ai_gateway.py` (utilizing Context Caching for zero-latency structured RDF generation). If `GEMINI_API_KEY` is missing or offline, gracefully fallback to `ollama_gateway.py` (`qwen2.5-coder:14b` -> `llama3.1:8b` -> `qwen2.5:7b`).
   * Preserve 100% W3C PROV-O and SKOS compliance for extracted triples.

2. **Integration Verification**:
   * Create `tests/integration/test_intake_hybrid_provider.py` to test `--provider auto`, `--provider ollama`, and `--provider google` with mock/offline fallback validation.
   * Run `python3 -m py_compile` on all modified files.

3. **Memory Synchronization & Telemetry**:
   * Synchronize `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` to **v4.6.0 / Phase 37**.
   * Run `python scripts/sync_gdrive.py` to update Google Drive copies.
   * Perform `git commit -m "feat(phase-37): implement dynamic hybrid provider switcher in intake_processor"` and `git push origin main`.

---

### Acceptance Criteria
- [ ] `05_Knowledge_Aggregator/src/intake_processor.py` implements `--provider` flag with seamless fallback.
- [ ] `tests/integration/test_intake_hybrid_provider.py` passes with exit code 0.
- [ ] Memory tribe updated to v4.6.0 and synced via `sync_gdrive.py`.
- [ ] Git repository pushed to `origin/main`.
