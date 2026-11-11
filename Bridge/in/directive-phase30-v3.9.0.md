# DIRECTIVE-PHASE30-V3.9.0: GitHub Repository Mirroring & Canonical URL Binding

**Phase:** Phase 30 — GitHub Repository Mirroring & Absolute Canonical URL Binding  
**System Version:** v3.9.0  
**Date:** 2026-11-11  
**Sender:** system.master_architect  
**Receiver:** cline.executor  
**Vector:** vertical  
**Performative:** inform  
**Topic:** directive:phase30  

---

### 1. Executive Summary & Context
With the successful initialization of the GitHub remote repository (`https://github.com/crmteos/Discovery_Engine.git`), Phase 30 establishes absolute canonical URL binding for the 3-File Memory Architecture (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`). This guarantees transparent synchronization between local disk memory, GitHub remote origin, and Master Architect context inspection.

---

### 2. Operational Tasks for Execution Engineer (Cline)

#### Task 1: Canonical GitHub URL Header Binding
In each of the three root memory files, insert/update the explicit canonical GitHub URL mirror in the top metadata block:

1. **`PROJECT_CONTEXT.md`**:
   - Canonical Mirror URL: `https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_CONTEXT.md`
   - Synchronize header version: `v3.9.0 — Phase 30` (Date: `2026-11-11`).

2. **`PROJECT_SPEC.md`**:
   - Canonical Mirror URL: `https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_SPEC.md`
   - Update Section 2 (Hardware & Repository Specs): Add `Remote Repository: https://github.com/crmteos/Discovery_Engine.git`.
   - Update Section 5 (ADR-004): Reference absolute GitHub mirror URLs as primary remote endpoints.
   - Synchronize header version: `v3.9.0 / Phase 30`.

3. **`PROJECT_STATE.md`**:
   - Canonical Mirror URL: `https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_STATE.md`
   - Synchronize header version: `v3.9.0 / Phase 30`.

#### Task 2: Gateway Report Update in `PROJECT_STATE.md`
Replace the top `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` block with the Phase 30 completion status:

```markdown
#### 🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)
* **Дата та час**: 2026-11-11
* **Фаза**: Phase 30 — COMPLETE
* **Шина повідомлень (Message ID)**: msg_20261111_phase30 (status: completed)
* **Виконані дії**:
    1. [x] Прописано канонічні GitHub URLs дзеркал у заголовки PROJECT_SPEC.md, PROJECT_CONTEXT.md, PROJECT_STATE.md
    2. [x] Оновлено телеметрію та конфігурацію GitHub у PROJECT_SPEC.md та PROJECT_CONTEXT.md
    3. [x] Перевірено роботу транзакційної шини Bridge/bus_manager.py та py_compile синтаксис
    4. [x] Виконано гібридну синхронізацію: локальний git commit + git push u origin main
* **Результати перевірок (Validation & Tests)**:
    * py_compile: PASSED (exit_code: 0)
    * Git Remote Push: PASSED (origin/main synchronized)
    * bus_manager.py: PASSED (status completed)
* **Змінені / створені файли**:
    * PROJECT_SPEC.md (v3.9.0)
    * PROJECT_CONTEXT.md (v3.9.0)
    * PROJECT_STATE.md (v3.9.0)
* **Відомі блокери / проблеми**: Відсутні (0 errors)
```

#### Task 3: Git Commit and Remote Push
Execute clean synchronization commands:
```powershell
git add PROJECT_SPEC.md PROJECT_CONTEXT.md PROJECT_STATE.md docs/ Bridge/
git commit -m "feat(phase-30): bind canonical github urls & sync memory state v3.9.0"
git push -u origin main
```

---

### 3. Master Architect Self-Instruction Protocol (System Guardrail)

**System Instruction for Master Architect (Gemini Notebook):**
> Upon any new turn or session activation, Master Architect MUST automatically read `/workspace/knowledge/PROJECT_STATE.md` (specifically the `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ` block) to parse system status and recent execution metrics prior to responding. Master Architect shall never prompt the user for state verification or micro-management details.

---

### 4. Definition of Done (DoD)
- [ ] All 3 root memory files contain their explicit GitHub canonical mirror URLs in headers.
- [ ] `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, and `PROJECT_STATE.md` are synchronized to `v3.9.0 / Phase 30`.
- [ ] `PROJECT_STATE.md` contains the updated Phase 30 Gateway Report.
- [ ] `git push -u origin main` completes successfully with `exit_code: 0`.
- [ ] All modified Python scripts pass `py_compile` checks with `exit_code: 0`.
