# Cline Directive: Physical Architectural Refactoring to 3-Tier Multi-Agent Standard (v2.1.0)

## 🎯 Мета директиви
Здійснити повний фізичний та логічний рефакторинг проєкту `Discovery_Engine` відповідно до стандартів **Agentic OS**, **Anthropic Multi-Agent Reference Architecture** та **Domain-Driven Design (DDD / Bounded Contexts)**.

Зафіксувати **Трирівневий Фізичний Паттерн Ізоляції** у `PROJECT_STATE.md` та транслювати його у `system_manifest.json` та локальні контейнери кожного вузла.

---

## 🏛️ Стандарт трирівневої ізоляції

1. **Рівень 1 (Master Governance & Manifest):**
   - `PROJECT_STATE.md` у корені проєкту — єдине джерело істини про архітектуру та стан.
   - `system_manifest.json` (v2.1.0) — системний реєстр маршрутів, ролей та JSON-схем.
2. **Рівень 2 (Node Container & Universal Envelope):**
   - Кожен із 3 вузлів (`05_Knowledge_Aggregator`, `01_Formal_Core`, `06_Formalized_Model`) має уніфіковану конвертну структуру:
     - `bridge/in/` (вхідні директиви)
     - `bridge/out/` (звіти та логи)
     - `schemas/` (JSON-контракти)
     - `src/` (код та реалізація)
3. **Рівень 3 (Core Sub-module Encapsulation):**
   - Усі суб-модулі Ядра (`01_Formal_Ontologies`, `02_NeuroSymbolic_Bridge`, `03_Multimodal_Interface`, `04_Discovery_Engine`) повністю переміщуються всередину `01_Formal_Core/src/`.

---

## 📋 Завдання для виконання (Task List)

### Крок 1 — Оновлення `PROJECT_STATE.md`
- Додати розділ **"Multi-Agent Agentic OS & DDD Bounded Context Standard"**.
- Зафіксувати 3-рівневу структуру та правила трансляції стану на рівні вузлів.

### Крок 2 — Фізичне перегрупування директорій
- Створити `01_Formal_Core/src/` (якщо відсутня).
- Фізично перемістити папки:
  - `01_Formal_Ontologies` ➔ `01_Formal_Core/src/01_Formal_Ontologies`
  - `02_NeuroSymbolic_Bridge` ➔ `01_Formal_Core/src/02_NeuroSymbolic_Bridge`
  - `03_Multimodal_Interface` ➔ `01_Formal_Core/src/03_Multimodal_Interface`
  - `04_Discovery_Engine` ➔ `01_Formal_Core/src/04_Discovery_Engine`
- Створити уніфіковані envelope-папки у `05_Knowledge_Aggregator` та `06_Formalized_Model` (`schemas/`, `src/`).

### Крок 3 — Оновлення `system_manifest.json` (v2.1.0)
- Оновити шляхи до всіх суб-компонентів Ядра у маніфесті.
- Зафіксувати правила взаємодії між вузлами.

### Крок 4 — Оновлення шляхів імпорту в Python
- Всі тестові та виконні скрипти (`test_e2e_pipeline.py`, `intake_processor.py` тощо) оновити з урахуванням нової фізичної структури (`01_Formal_Core/src/...`).
- Провести `py_compile` для всіх ключових Python-файлів.
- Запустити `test_e2e_pipeline.py` та пересвідчитись, що всі 4 етапи працюють із `exit_code: 0`.

### Крок 5 — Звітність
- Зберегти підсумковий звіт у `Bridge/out/execution_reports/report_physical_refactor_[TIMESTAMP].md`.

---

## 🔒 Непорушні обмеження
- **BUDGET_LIMIT:** $0.00 (Pure Open-Source & Local Hardware Stack)
- **EXECUTION_MODE:** Stateless Autonomous Sessions
