# Directive Phase 28 (v3.7.0) — Institutionalization of ADR-004 (3-File Memory Protocol & Gateway Report Standard)

**Target Role:** `cline.executor`  
**Sender Role:** `system.master_architect`  
**Communication Vector:** `vertical`  
**Performative:** `inform`  
**Topic:** `directive:phase28`  
**System Version:** v3.7.0 — Phase 28  
**Date:** 2026-11-11  
**Budget Limit:** $0.00 (Pure Open-Source & Local Hardware Stack)  

---

### 1. Executive Intent & Objective

The objective of **Phase 28** is to permanently eradicate operational noise, micro-management over code syntax, and the "broken telephone" bottleneck between the Master Architect (Gemini Notebook) and the Execution Engineer (Cline).

This directive institutionalizes **ADR-004 (3-File Memory Protocol & Git Synchronization Standard)** across the Discovery Engine repository. Under this standard, Cline operates fully autonomously during directive execution and consolidates all execution telemetry into a standardized gateway report within **`PROJECT_STATE.md`**, followed by automated local Git state persistence.

---

### 2. Architectural Changes & Standards (ADR-004)

Cline must implement and enforce **ADR-004** with the following three core pillars:

#### Pillar A: Single Source of Truth — 3-File Memory Architecture
* **`PROJECT_SPEC.md` (Static — System Specification)**: Contains immutable constraints ($0.00 budget, AMD CPU hardware bounds, prompting protocols, DoD, ADRs). Updated ONLY when architecture or stack rules change.
* **`PROJECT_CONTEXT.md` (Semi-Dynamic — Master Data Plane)**: Contains RDF graph topology, schema locations, triple normalization rules, and inter-node message routing. Updated when data schemas or routes change.
* **`PROJECT_STATE.md` (Dynamic — Control Plane & Gateway Report)**: Contains global health metrics, node registry, execution history, and the active operational gateway state. Updated after EVERY directive execution.

#### Pillar B: Standardized Gateway Report Block
Cline MUST create and maintain a prominent block at the very top of **`PROJECT_STATE.md`**:

```markdown
## 🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)
- **Дата та час**: YYYY-MM-DD HH:MM
- **Фаза**: Phase 28 — COMPLETE
- **Шина повідомлень (Message ID)**: msg_20261111_121119 (status: completed)
- **Виконані дії**:
  1. [x] Впроваджено ADR-004 у PROJECT_SPEC.md та PROJECT_STATE.md
  2. [x] Створено/оновлено кореневі файли специфікації та стану
  3. [x] Збережено docs/STARTPOINT_META_PROMPT.md
  4. [x] Виконано локальний комміт стану через Git
- **Результати перевірок (Validation & Tests)**:
  - py_compile: PASSED (exit_code: 0)
  - bus_manager.py status check: PASSED
  - E2E smoke tests: PASSED
- **Змінені / створені файли**:
  - PROJECT_SPEC.md (додано ADR-004, v3.7.0)
  - PROJECT_STATE.md (оновлено до v3.7.0, додано Gateway Report)
  - PROJECT_CONTEXT.md (синхронізовано до v3.7.0)
  - docs/STARTPOINT_META_PROMPT.md (створено)
- **Відомі блокери / проблеми**: Відсутні (0 errors)
```

#### Pillar C: Git State Persistence Protocol
After completing all execution tasks and updating the 3 memory files, Cline must execute:
1. `git add PROJECT_SPEC.md PROJECT_CONTEXT.md PROJECT_STATE.md docs/ Bridge/`
2. `git commit -m "feat(phase-28): institutionalize ADR-004 3-file memory protocol & gateway report"`
3. If a remote repository (`git remote`) is attached, run `git push`; if not, retain the commit in local Git history cleanly.

---

### 3. Step-by-Step Execution Plan for Cline

1. **Read & Verify Current State**:
   * Inspect `PROJECT_STATE.md` and `PROJECT_CONTEXT.md`.
   * Verify that `Bridge/bus_manager.py` is operational and mark message `msg_20261111_121119` (or active phase 27/28 message) as `completed`.

2. **Deploy / Update `PROJECT_SPEC.md` (v3.7.0)**:
   * Ensure `PROJECT_SPEC.md` exists in the project root.
   * Add **ADR-004** to Section 5 (Architecture Decision Records).
   * Confirm all hardware bounds (AMD Ryzen 5 5625U, 16GB RAM, CPU-mode, $0.00 budget) and transactional prompting protocols are fully specified.

3. **Synchronize `PROJECT_CONTEXT.md` (v3.7.0)**:
   * Update header version to `v3.7.0 — Phase 28`.
   * Confirm cross-node data flows and Universal JSONL Message Bus definitions (`Bridge/messages.jsonl`).

4. **Synchronize `PROJECT_STATE.md` (v3.7.0)**:
   * Insert the `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block at the top.
   * Log Phase 28 in the Execution History table.
   * Update system readiness to 🟢 100% Core & Governance Synchronized.

5. **Generate `docs/STARTPOINT_META_PROMPT.md`**:
   * Save the strict anti-anthropomorphism and anti-sycophancy meta-prompt to `docs/STARTPOINT_META_PROMPT.md` for fast initialization of clean chat sessions.

6. **Validation & Git Persistence**:
   * Run `python -m py_compile Bridge/bus_manager.py`.
   * Execute `python Bridge/bus_manager.py status` (or list pending).
   * Run `git add .` and `git commit -m "feat(phase-28): institutionalize ADR-004 3-file memory protocol & gateway report"`.
   * Save execution report to `Bridge/out/execution_reports/report_phase28_v3.7.0_[TIMESTAMP].md`.

---

### 4. Definition of Done (DoD)

- [ ] `PROJECT_SPEC.md` contains ADR-004 and is present at project root.
- [ ] `PROJECT_STATE.md` starts with `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)`.
- [ ] `docs/STARTPOINT_META_PROMPT.md` is saved on disk.
- [ ] `Bridge/messages.jsonl` message status is set to `completed`.
- [ ] All Python files pass `py_compile` with `exit_code: 0`.
- [ ] Local Git commit executed successfully.
