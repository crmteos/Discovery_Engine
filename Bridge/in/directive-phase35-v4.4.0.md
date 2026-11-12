# DIRECTIVE: Phase 35 (v4.4.0) — Google AI Gateway Integration & Dual-Provider Inference Engine

**Priority:** HIGH  
**Target Version:** `v4.4.0` | **Phase:** `Phase 35`  
**Execution Standard:** Single-Prompt Gateway Protocol (ADR-0003, ADR-0004, ADR-0005)  
**Budget Limit:** $0.00 (Google AI Studio Free Tier + Local Ollama Fallback)  

---

## 1. Objective & Scope

Institutionalize the **Dual-Provider Inference Engine** for the Discovery Engine by integrating the official `google-genai` SDK alongside the local `ollama_gateway.py`. This step enables free cloud inference via Google AI Studio (Gemini Flash models) with a zero-budget quota while maintaining 100% offline fallback capabilities via Ollama.

---

## 2. Detailed Technical Requirements

### 2.1. New Module: `00_Project_Interface/src/google_ai_gateway.py`
- Implement `google_ai_gateway.py` using `google-genai` Python SDK.
- Include environment variable resolution for `GEMINI_API_KEY`.
- Implement model selection chain: `gemini-2.5-flash` → `gemini-2.0-flash` → `gemini-1.5-flash`.
- Support standalone `--test` CLI mode:
  - If `GEMINI_API_KEY` is present: execute live API ping / generation test.
  - If `GEMINI_API_KEY` is missing or network fails: execute graceful fallback mode, log telemetry, and return `exit_code: 0`.

### 2.2. Integration Test: `tests/integration/test_google_ai_gateway.py`
- Verify liveness check, error handling, and fallback mechanics.
- Ensure `py_compile` syntax validation passes with `exit_code: 0`.

### 2.3. Memory Triad Synchronization (v4.4.0)
- **`PROJECT_SPEC.md`**: Update header metrics to `v4.4.0 / Phase 35`; add `google-genai` SDK and Dual Inference Gateway to Section 3 & DoD.
- **`PROJECT_CONTEXT.md`**: Synchronize version to `v4.4.0 / Phase 35`; update Topology Section to record Dual-Provider Inference routes (Ollama Local REST ↔ Google AI Studio API).
- **`PROJECT_STATE.md`**: Update header to `v4.4.0 / Phase 35`; insert `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block at top; ensure `Current Phase:` text field matches Phase 35; append Phase 35 to Execution History.

---

## 3. Automation & Verification Workflow

1. `python -m py_compile 00_Project_Interface/src/google_ai_gateway.py` (exit code: 0)
2. `python -m py_compile tests/integration/test_google_ai_gateway.py` (exit code: 0)
3. `python tests/integration/test_google_ai_gateway.py` (exit code: 0)
4. `python Bridge/bus_manager.py --post --payload-file ...` (post `directive:phase35` message `msg_20261112_phase35` and set status `completed`)
5. `python scripts/sync_gdrive.py` (synchronize 3 memory files to Google Drive)
6. `git add .` && `git commit -m "feat(phase-35): google ai gateway integration & dual-provider inference engine"` && `git push origin main`

---

## 4. Definition of Done (DoD)

- [ ] `00_Project_Interface/src/google_ai_gateway.py` created and verified with `--test` (`exit_code: 0`).
- [ ] `tests/integration/test_google_ai_gateway.py` created and passed (`exit_code: 0`).
- [ ] Memory triad (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`) synchronized to `v4.4.0`.
- [ ] `PROJECT_STATE.md` contains `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block at top.
- [ ] `scripts/sync_gdrive.py` executed successfully.
- [ ] Git commit and `git push origin main` executed successfully.
