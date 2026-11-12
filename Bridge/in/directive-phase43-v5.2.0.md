# Directive Phase 43 (v5.2.0): Automated Test Coverage & Typing Audit Integration

**Directive ID:** `directive-phase43-v5.2.0`  
**Target Version:** `v5.2.0` | **Target Phase:** `Phase 43`  
**Sender:** `system.master_architect`  
**Recipient:** `cline.executor`  
**Budget:** `$0.00` (Pure Open-Source & Local Hardware Stack)

---

### 1. Objective & Architectural Context
Phase 43 concludes **Stage 3 (CI/CD Automation & Autonomous Oversight)** of the Discovery Engine roadmap. 

The goal of this phase is to integrate the `jules_code_health.py` suite directly into the GitHub Actions CI/CD pipeline and enable automated metrics synchronization into `PROJECT_STATE.md` via `--sync-state`. This ensures that test coverage, type checking, and code health scores are continuously audited in GitHub Actions and updated in the project state without manual developer intervention.

---

### 2. Required Tasks

#### Task 1: Extend `.github/workflows/gemini_dod_audit.yml`
* Extend `.github/workflows/gemini_dod_audit.yml` to include a step for running `python scripts/jules_code_health.py --check`.
* Ensure CI pipeline fails if code health or coverage falls below critical thresholds or if syntax/typing errors are detected.
* Preserve $0.00 budget and offline fallback capabilities.

#### Task 2: Implement `--sync-state` in `scripts/jules_code_health.py`
* Add `--sync-state` CLI flag to `scripts/jules_code_health.py`.
* When called with `--sync-state`, parse `logs/code_health_report.json` and update the Code Health & Verification metrics in `PROJECT_STATE.md`.
* Ensure clean file writing and zero corruption of `PROJECT_STATE.md`.

#### Task 3: Integration Test (`tests/integration/test_code_health_sync.py`)
* Implement `tests/integration/test_code_health_sync.py` to test `--check`, `--report`, and `--sync-state` execution.
* Ensure all tests pass with `exit_code: 0`.

#### Task 4: Memory Triad & Git Automation
1. **Update Memory Files**:
   * `PROJECT_SPEC.md` -> Update System Version to `v5.2.0` / `Phase 43`.
   * `PROJECT_CONTEXT.md` -> Update System Version to `v5.2.0` / `Phase 43`.
   * `PROJECT_STATE.md` -> Record Phase 43 completion, log metrics, update VERSION to `v5.2.0` / `Phase 43`.
2. **Execute Sync Script**:
   * Run `python scripts/sync_gdrive.py` to sync updated memory files to Google Drive.
3. **Git Commit & Push**:
   * Execute `git add .`, `git commit -m "feat(ci/cd): complete Phase 43 v5.2.0 automated test coverage and health audit integration"`, and `git push origin main`.

---

### 3. Definition of Done (DoD)
- [ ] `.github/workflows/gemini_dod_audit.yml` extended with `jules_code_health.py --check`.
- [ ] `scripts/jules_code_health.py --sync-state` implemented and verified.
- [ ] `tests/integration/test_code_health_sync.py` passes with `exit_code: 0`.
- [ ] Memory triad (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`) updated to `v5.2.0 / Phase 43`.
- [ ] `python scripts/sync_gdrive.py` executed successfully.
- [ ] `git push origin main` completed.
