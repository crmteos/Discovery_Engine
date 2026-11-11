# SINGLE-PROMPT DIRECTIVE: Phase 31 (v4.0.0)
**System Architecture & Memory Synchronization Protocol**

---

### METADATA
* **Directive ID:** `directive-phase31-v4.0.0`
* **Target Version:** `v4.0.0`
* **Phase:** `Phase 31`
* **Date:** `2026-11-11`
* **Sender:** `system.master_architect`
* **Receiver:** `cline.executor`
* **Communication Vector:** `vertical`
* **Performative:** `inform`
* **Topic:** `directive:phase31`
* **Budget Limit:** `$0.00`

---

## 1. МЕТА ФАЗИ (OBJECTIVES)

1. **Усунення текстової розбіжності у `PROJECT_STATE.md`**:
   - Поле `Current Phase:` під заголовком метрик має бути розгороджене та синхронізоване з блоком `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` (Phase 31 / v4.0.0).

2. **Автоматизація синхронізації з Google Drive (Drive Mirroring Script)**:
   - Створити утиліту `scripts/sync_gdrive.py` (або `scripts/sync_memory_files.py`), яка копіює канонічні 3 файли пам'яті (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`) до локальної папки синхронізації Google Drive (наприклад, `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine` або шляху Google Drive, якщо такий задано/визначено в середовищі).
   - Додати виклики цієї синхронізації в автоматичний пост-виконавчий крок Кліна при завершенні кожної фази (після `git push`).

3. **Синхронізація Тріади Пам'яті (v4.0.0)**:
   - Оновити версії у `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md` та `PROJECT_STATE.md` до **v4.0.0 / Phase 31**.
   - Оновити блок `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)` у верхній частині `PROJECT_STATE.md`.

4. **Git Commit & Push**:
   - Зафіксувати всі зміни у локальному репозиторії та зробити `git push origin main`.

---

## 2. ВИМОГИ ДО РЕАЛІЗАЦІЇ (PILLARS)

### Pillar A: Корекція `PROJECT_STATE.md`
- Перевірити та синхронізувати значення полів:
  * `VERSION: v4.0.0`
  * `PHASE: Phase 31`
  * `Current Phase: Phase 31 — State Synchronization & Google Drive Auto-Sync Script (v4.0.0)...`

### Pillar B: Автоматичний скрипт синхронізації `scripts/sync_gdrive.py`
- Створити `scripts/sync_gdrive.py`, який:
  1. Знаходить канонічні `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md` у корені проекту.
  2. Визначає локальний шлях Google Drive / локальної папки синхронізації (із захистом від помилок, якщо шлях відсутній).
  3. Копіює 3 файли для забезпечення 100% відповідності між GitHub-репозиторієм та Google Drive.
  4. Проходить перевірку `python -m py_compile scripts/sync_gdrive.py` з `exit_code: 0`.

### Pillar C: Повний цикл Git & Bus
1. Зареєструвати та виконати публікацію в шину `Bridge/bus_manager.py`:
   ```bash
   python Bridge/bus_manager.py post \
     --sender system.master_architect \
     --receiver cline.executor \
     --vector vertical \
     --performative inform \
     --topic directive:phase31 \
     --payload-file Bridge/in/directive-phase31-v4.0.0.json
   ```
2. Виконати комміт та пуш:
   ```bash
   git add .
   git commit -m "feat(phase-31): fix state current phase text & add gdrive sync script"
   git push origin main
   ```
3. Перевести статус повідомлення на `completed`.

---

## 3. CRITERIA FOR DEFINITION OF DONE (DoD)
- [ ] `Current Phase:` у `PROJECT_STATE.md` строго відповідає блоку `GATEWAY REPORT` (Phase 31 / v4.0.0).
- [ ] `scripts/sync_gdrive.py` реалізовано та перевірено (`exit_code: 0`).
- [ ] Усі 3 файли пам'яті синхронізовано до версії **v4.0.0 / Phase 31**.
- [ ] Здійснено `git commit` та успішний `git push` до GitHub `https://github.com/crmteos/Discovery_Engine.git`.
- [ ] Бюджет виконання: **$0.00**.
