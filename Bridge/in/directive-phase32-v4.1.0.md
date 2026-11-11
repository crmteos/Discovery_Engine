# Directive Phase 32 (v4.1.0) — Institutionalization of ADR-0005 & Startpoint Meta-Prompt Protocol

## Metadata
- **Directive ID:** `directive-phase32-v4.1.0`
- **Sender:** `system.master_architect`
- **Receiver:** `cline.executor`
- **Vector:** `vertical`
- **Performative:** `request`
- **Topic:** `directive:phase32`
- **Version:** `v4.1.0`
- **Baseline Phase:** `Phase 31 (v4.0.0)`
- **Target Phase:** `Phase 32 (v4.1.0)`
- **Execution Mode:** `Stateless Autonomous Session (Zero Micro-management)`
- **Budget Constraint:** `$0.00`

---

## 1. Executive Summary & Context

Phase 32 institutionalizes **ADR-0005 (Private Repository & Drive Sync Gateway Protocol)** and finalizes the **Seed & Handover Protocol** for `docs/STARTPOINT_META_PROMPT.md`.

This architecture decouples source code persistence from the AI Architect's memory window:
1. **GitHub (Private Repository):** Primary Version Control System for code, diffs, history, and raw project files.
2. **Google Drive Synced Folder:** Automated live gateway for Gemini Notebook containing **ONLY** the 3 canonical memory files (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`) updated via `scripts/sync_gdrive.py`.
3. **Anti-Noise Guardrail:** Prohibits dumping raw code, vendor files, or unstructured text to Google Drive to prevent RoPE context dispersion and attention degradation in LLM long-context windows.

---

## 2. Pillar Tasks & Requirements

### Pillar A: ADR-0005 Institutionalization (`PROJECT_SPEC.md`)
- Add **ADR-0005 (Private Repository & Drive Sync Gateway Protocol)** to Section 5 of `PROJECT_SPEC.md`.
- Define the rules for:
  - Private GitHub storage for code.
  - 3-File Drive Sync Gateway for Notebook state.
  - Strict exclusion of raw code/vendor files from the Drive Sync scope.
- Synchronize header to `v4.1.0 / Phase 32`.

### Pillar B: Startpoint Meta-Prompt Update (`docs/STARTPOINT_META_PROMPT.md`)
- Update `docs/STARTPOINT_META_PROMPT.md` to reflect the **Seed & Handover Protocol**:
  1. User feeds `STARTPOINT_META_PROMPT.md` (or `PROJECT_STATE.md`) into a new Notebook session.
  2. Notebook auto-detects system state (`v4.1.0`) and requests attaching the live `PROJECT_STATE.md` from Google Drive.
  3. User detaches the static seed file; Notebook runs continuously on the auto-synced Drive source.

### Pillar C: Memory Tribe & Gateway Report Synchronization (`PROJECT_STATE.md` & `PROJECT_CONTEXT.md`)
- Update `PROJECT_STATE.md` with top block `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` for Phase 32 (v4.1.0).
- Ensure `Current Phase:` text field directly mirrors the Gateway Report block.
- Execute `python scripts/sync_gdrive.py` post-execution.
- Execute local Git commit and `git push -u origin main`.

---

## 3. Definition of Done (DoD)

- [ ] `PROJECT_SPEC.md` contains **ADR-0005** and header `v4.1.0 / Phase 32`.
- [ ] `docs/STARTPOINT_META_PROMPT.md` updated with Seed & Handover Protocol.
- [ ] `PROJECT_STATE.md` starts with `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` (v4.1.0) and `Current Phase:` field is synchronized.
- [ ] `scripts/sync_gdrive.py` executed cleanly with `exit_code: 0`.
- [ ] `git commit` & `git push` to `https://github.com/crmteos/Discovery_Engine.git` completed successfully.
- [ ] Budget remains strictly `$0.00`.
