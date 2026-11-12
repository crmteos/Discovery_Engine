# 🛠️ ENGINEERING DIRECTIVE: Phase 41 (v5.0.0)
**System Domain**: Discovery Engine — CI/CD & Automated Code Audit
**Target Version**: `v5.0.0` / Phase 41
**Governance Protocol**: Dual-Vertical 2-File Standard (ADR-0001) & Single-Prompt Protocol (ADR-0003)
**Execution Constraint**: Autonomous $0.00 Budget (Zero-Mock Requirement)

---

### 1. OBJECTIVE & CONTEXT
With Stage 2 (Firebase Genkit Orchestration, v4.9.0) successfully completed, we initiate **Stage 3: CI/CD Automation & Autonomous Oversight**.

Phase 41 implements **Gemini CLI GitHub Actions Integration for Automated Definition of Done (DoD) Auditing**. This workflow automatically evaluates incoming Pull Requests and code changes against `PROJECT_SPEC.md` constraints ($0.00 budget, pure Python fallbacks, zero-mock policy, W3C PROV-O compliance, and absence of hallucinated dependencies).

---

### 2. ARCHITECTURAL REQUIREMENTS & MODIFICATION TARGETS

#### Target A: `.github/workflows/gemini_dod_audit.yml`
1. Create a GitHub Actions workflow `.github/workflows/gemini_dod_audit.yml` triggered on `push` to `main` and `pull_request`.
2. Configure steps to install dependencies, run `pytest`, and execute the Gemini CLI DoD audit script.
3. Pass `GEMINI_API_KEY` as a secret if available, falling back gracefully to static rules audit if no key is present.

#### Target B: `scripts/gemini_cli_audit.py`
1. Create `scripts/gemini_cli_audit.py` that inspects recent git diffs or modified code.
2. Verify code against core invariants from `PROJECT_SPEC.md`:
   - No paid third-party API dependencies or non-standard packages.
   - Presence of graceful offline fallbacks (`exit_code: 0`).
   - W3C PROV-O metadata preservation in intake adapters.
3. Support standalone local execution: `python scripts/gemini_cli_audit.py --local` with `exit_code: 0`.

#### Target C: Integration Test & Verification
1. Create `tests/integration/test_gemini_cli_audit.py` to verify `gemini_cli_audit.py` functions correctly without errors.
2. Perform syntax validation via `py_compile`.

#### Target D: Memory & State Synchronization (v5.0.0)
1. Update headers in `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` to `v5.0.0 / Phase 41`.
2. Log Phase 41 completion under `PROJECT_STATE.md`.
3. Execute `python scripts/sync_gdrive.py` for Google Drive mirroring.
4. Perform `git commit -m "feat: Phase 41 (v5.0.0) Gemini CLI GitHub Actions DoD Audit"` and `git push origin main`.

---

### 3. DEFINITION OF DONE (DoD) CHECKLIST
- [ ] `.github/workflows/gemini_dod_audit.yml` created and validated.
- [ ] `scripts/gemini_cli_audit.py` implemented with offline fallback.
- [ ] `tests/integration/test_gemini_cli_audit.py` passes with `exit_code: 0`.
- [ ] Memory triad updated to `v5.0.0` / Phase 41.
- [ ] `scripts/sync_gdrive.py` executed successfully.
- [ ] `git push origin main` completed autonomously.
