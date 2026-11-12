# SYSTEM DIRECTIVE: PHASE 49 — W3C SHACL 1.2 PROFILING & PROV-O LINEAGE (v5.8.0)

**Header Metadata:**
* **Directive ID**: `directive-phase49-v5.8.0`
* **Sender**: `system.master_architect`
* **Receiver**: `cline.executor`
* **Target Node**: `06_Formalized_Model` & `05_Knowledge_Aggregator`
* **System Version**: `v5.8.0` (Phase 49)
* **Budget Limit**: `$0.00` (Pure Open-Source Stack / Local Execution)
* **Timestamp**: `2026-11-12T10:00:00Z`

---

## 1. МЕТА ТА КОНТЕКСТ
Завершити розгортання Комплекту системної документації для Вузлів 01 та 06 шляхом впровадження декларативної валідації онтологічних графів фактів за стандартом **W3C SHACL 1.2** та наскрізної системи аудиту походження даних **W3C PROV-O Lineage Engine**.

---

## 2. СПЕЦИФІКАЦІЯ РОБІТ ТА АРТЕФАКТИ

### Task 1: Декларативний валідатор SHACL 1.2
* **Шлях артефакту**: `06_Formalized_Model/src/shacl_validator.py`
* **Вимоги до коду**:
  * Реалізація класу `SHACLValidator` з суворою валідацією RDF-триплетів та Formal Projection графових моделей проти SHACL shapes.
  * Декларативна перевірка обов'язкових полів (`subject`, `predicate`, `object`, `prov:wasDerivedFrom`).
  * Pure Python фолбек без залучення зовнішніх платних API.

### Task 2: Двигун походження фактів W3C PROV-O Lineage
* **Шлях артефакту**: `06_Formalized_Model/src/provo_lineage.py`
* **Вимоги до коду**:
  * Реалізація класу `PROVOLineageAuditor` для генерації та валідації PROV-O графів походження фактів (`prov:Entity`, `prov:Activity`, `prov:Agent`, `prov:wasDerivedFrom`, `prov:wasGeneratedBy`).
  * Забезпечення наскрізного аудиту трансформації фактів: **Джерело ➔ Вузол 05 (Extract) ➔ Вузол 06 (Project) ➔ Вузол 01 (Math Transformation)**.

### Task 3: Інтеграційний тест
* **Шлях артефакту**: `tests/integration/test_shacl_provo_lineage.py`
* **Покриття тесту**:
  * Перевірка валідації коректних та некоректних RDF-графів через `SHACLValidator`.
  * Валідація генерації ланцюжка PROV-O метаданих для аксіоматичних трансформацій (`assert exit_code == 0`).

### Task 4: Синхронізація Пам'яті та Репозиторію (v5.8.0)
1. Оновити шапки та блоки версії у тріаді пам'яті до **`v5.8.0 / Phase 49`**:
   * `PROJECT_SPEC.md`
   * `PROJECT_CONTEXT.md`
   * `PROJECT_STATE.md`
2. Запустити `python scripts/sync_gdrive.py`.
3. Виконати `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)
1. Всі нові та модифіковані файли проходять синтаксичну перевірку: `python -m py_compile`.
2. Інтеграційне тестування `python tests/integration/test_shacl_provo_lineage.py` виконується зі статусом `PASSED` (`exit_code: 0`).
3. Потрійна пам'ять оновлена до **v5.8.0**, синхронізована з Google Drive та вивантажена в GitHub.
4. Дотримано суворого ліміту бюджету **$0.00**.
