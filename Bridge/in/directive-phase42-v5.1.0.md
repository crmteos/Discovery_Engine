# 📜 ІНЖЕНЕРНА ДИРЕКТИВА: PHASE 42 (v5.1.0)
**Проект:** Discovery Engine  
**Модуль:** CI/CD & Automated Code Health (`scripts/jules_code_health.py`)  
**Дата:** 2026-11-12  
**Статус:** READY FOR AUTONOMOUS EXECUTION  

---

## 🎯 МЕТА ФАЗИ
Реалізувати автономний модуль автоматизованого тестування та санітизації кодової бази **`scripts/jules_code_health.py`** (нахтнений агентом Jules), який автоматично аналізує покриття тестами (`pytest-cov`), виявляє кодові анти-патерни ("code smells") та забезпечує детерміновану санітизацію без залучення розробника і без порушення бюджетного ліміту **$0.00**.

---

## 📋 ПЕРЕЛІК ЗАВДАНЬ (DEFINITION OF DONE)

### 1. Реалізація модуля `scripts/jules_code_health.py`
- Створити CLI-скрипт `scripts/jules_code_health.py` із підтримкою параметрів `--check`, `--sanitize` та `--report`.
- Впровадити автоматичну перевірку покриття тестами через `pytest` для всіх вихідних модулів у `00_Project_Interface`, `05_Knowledge_Aggregator`, `06_Formalized_Model`.
- Забезпечити перевірку відсутності галюцинованих пакетів та виявлення недоглянутих `TODO` / `FIXME` у кодовій базі.
- Додати автономне збереження звіту в `logs/code_health_report.json`.
- Забезпечити 100% оффлайн-режим із кодом повернення `exit_code: 0`.

### 2. Інтеграційний тест `tests/integration/test_jules_code_health.py`
- Створити тест, що перевіряє санітизатор `scripts/jules_code_health.py` у режимі `--check`.
- Гарантувати підтвердження `exit_code: 0` та валідність згенерованого JSON-звіту.

### 3. Оновлення Тріади Пам'яті (v5.1.0 / Phase 42)
- **`PROJECT_SPEC.md`**: Оновити версію до `v5.1.0 / Phase 42`, додати правило про автоматичний санітизинг коду.
- **`PROJECT_CONTEXT.md`**: Оновити версію системи до `v5.1.0 / Phase 42`, додати опис модуля `jules_code_health.py`.
- **`PROJECT_STATE.md`**: Оновити поля `VERSION=v5.1.0`, `PHASE=42`, сформувати новий **GATEWAY REPORT Phase 42**.

### 4. Автоматична Синхронізація та Git-вивантаження
- Виконати `python scripts/sync_gdrive.py` для автоматичного оновлення Google Drive.
- Виконати `git commit` та `git push origin main` у приватний репозиторій GitHub.

---

## ⚡ ІНСТРУКЦІЯ ДЛЯ СИНГЛ-ПРОМПТ ПРОТОКОЛУ (CLINE)
```bash
Оброби директиву Bridge/in/directive-phase42-v5.1.0.md. Реалізуй scripts/jules_code_health.py та tests/integration/test_jules_code_health.py, онови 3 файли пам'яті до v5.1.0, запусти sync_gdrive.py та виконай git push origin main. Працюй повністю автономно.
```
