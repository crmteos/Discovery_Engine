# Phase Directive: Phase 36 — Context Caching Integration in `google_ai_gateway.py` (v4.5.0)

**Target System Version:** v4.5.0  
**Phase Identifier:** Phase 36 — COMPLETE  
**Execution Mode:** Single-Prompt Autonomous Execution (Cline)  
**Budget Limit:** $0.00 (Zero-Budget Operational Standard / Free Tier & Local Offloading)  
**Memory & Sync Standard:** 3-File Memory Protocol + Drive Sync Gateway (ADR-0004, ADR-0005)  
**Target Repository:** `https://github.com/crmteos/Discovery_Engine.git` (main)

---

### 1. Objective & Scope

In accordance with the Google AI System Integration Roadmap (Stage 1: Inference Hybridization & Token Optimization), **Phase 36** focuses on implementing **Context Caching** within `00_Project_Interface/src/google_ai_gateway.py` using the `google-genai` SDK (v2.24.0+).

By caching static, heavy specification contexts (`PROJECT_SPEC.md` and `PROJECT_CONTEXT.md`) directly via Gemini's Context Caching feature, the system minimizes input token consumption by ~90% during multi-turn LLM reasoning sessions while enforcing immutable system governance prompts.

---

### 2. Detailed Technical Requirements

1. **Context Caching Implementation in `00_Project_Interface/src/google_ai_gateway.py`**:
   - Add context caching support via `google-genai` SDK (`client.caches.create` / `CachedContent`).
   - Construct static cache targets combining `PROJECT_SPEC.md` and `PROJECT_CONTEXT.md` with TTL management (e.g., 5-minute to 1-hour TTL).
   - Pass cached content references to model call configurations (`config=types.GenerateContentConfig(cached_content=...)`).
   - Implement graceful fallback: if API key is missing, network is offline, or caching fails, fall back smoothly to standard prompt injection or local Ollama without crashing (`exit_code: 0`).
   - Add CLI flag `--cache-stats` to report active cache metadata and status.

2. **Integration Testing (`tests/integration/test_context_caching.py`)**:
   - Implement integration test `tests/integration/test_context_caching.py`.
   - Verify cache initialization, token reduction metrics handling, and fallback behavior when offline/unauthenticated.
   - Run `py_compile` on all modified Python files (`exit_code: 0`).

3. **3-File Memory Synchronization (v4.5.0)**:
   - Synchronize `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` to **v4.5.0 / Phase 36**.
   - Update `PROJECT_STATE.md` header, metrics, and top `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block.
   - Ensure `Current Phase:` text field under Header Metrics matches Phase 36 / v4.5.0 exactly.

4. **Automation & Git Push**:
   - Execute `python scripts/sync_gdrive.py` to mirror the updated memory triad to Google Drive.
   - Commit changes: `git commit -m "feat(phase-36): implement context caching in google_ai_gateway, update memory tribe to v4.5.0"`.
   - Push to remote: `git push origin main`.

---

### 3. Execution Protocol for Cline

Execute all tasks fully autonomously:
1. Update `00_Project_Interface/src/google_ai_gateway.py` with Context Caching.
2. Create and run `tests/integration/test_context_caching.py`.
3. Perform `py_compile` syntax validation across modified files.
4. Update `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md` to **v4.5.0**.
5. Run `python scripts/sync_gdrive.py`.
6. Perform `git commit` and `git push origin main`.
7. Output Gateway Report summary upon completion.
