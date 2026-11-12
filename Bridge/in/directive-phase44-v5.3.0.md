# ІНЖЕНЕРНА ДИРЕКТИВА: Phase 44 (v5.3.0)
**Проект**: Discovery Engine — Суверенне ШІ-ядро з детермінованою пам'яттю  
**Тема**: Enterprise Switcher & Data Residency (EU/US) у `google_ai_gateway.py`  
**Бюджетний ліміт**: $0.00 (з підтримкою регіональної ізоляції та оффлайн-фолбеку)  
**Стандарт**: Node Envelope Structure v2.7.0+, W3C PROV-O, Single-Prompt Gateway Protocol (ADR-0003)

---

## 1. МЕТА ТА КОНТЕКСТ (Phase 44)

Розпочинаємо **Етап 4: Enterprise-масштабування & Agent Search**.

Метою фази **Phase 44 (v5.3.0)** є розширення модуля `00_Project_Interface/src/google_ai_gateway.py` для підтримки прапорця `--enterprise` (`enterprise=True`). Це забезпечує прозорий перехід від безкоштовного розробницького Google AI Studio (Gemini Developer API) до корпоративного **Vertex AI (Gemini Enterprise Agent Platform)** із підтримкою:
1. Автоматичної автентифікації через GCP Application Default Credentials (ADC) / Service Account.
2. Параметра **Data Residency (`location`)** (наприклад, `europe-west1` для ЄС або `us-central1` для США).
3. Збереження суворого оффлайн-фолбеку до `ollama_gateway.py` ($0.00 budget) у разі відсутності авторизації або збоїв мережі.

---

## 2. СПЕЦИФІКАЦІЯ ЗАВДАНЬ

### Завдання 1: Оновлення `00_Project_Interface/src/google_ai_gateway.py`
* Додати підтримку аргументів CLI та конфігураційних змінних:
  * `--enterprise` / `VERTEX_AI_ENABLED=true`
  * `--location` / `VERTEX_LOCATION` (за замовчуванням `europe-west1`)
  * `GCP_PROJECT_ID`
* При підключенні прапорця `--enterprise`:
  * Перемикати SDK-клієнт `google-genai` на авторизацію через Vertex AI (`vertexai=True`, `project=GCP_PROJECT_ID`, `location=VERTEX_LOCATION`).
* Якщо змінні оточення не вказані — забезпечити беззбійне падіння на `google-ai-studio` або локальний `ollama_gateway.py` (`exit_code: 0`).

### Завдання 2: Інтеграційне тестування `tests/integration/test_enterprise_gateway.py`
* Створити тест `tests/integration/test_enterprise_gateway.py` для перевірки:
  * Синтаксичної коректності (`py_compile`).
  * Ініціалізації розширених параметрів `enterprise` та `location`.
  * Граційного оффлайн-фолбеку без випадання винятків (`exit_code: 0`).

### Завдання 3: Оновлення Тріади Пам'яті (v5.3.0 / Phase 44)
* **`PROJECT_SPEC.md`**: Оновити версію до `v5.3.0 / Phase 44`, зафіксувати підтримку Enterprise Switcher & Data Residency.
* **`PROJECT_CONTEXT.md`**: Додати опис конфігурації Vertex AI / Data Residency (EU/US).
* **`PROJECT_STATE.md`**: Сформувати блок `🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)`, оновити поля `VERSION: v5.3.0` та `PHASE: Phase 44`.

### Завдання 4: Синхронізація та Git-автоматизація
* Виконати `python scripts/sync_gdrive.py`.
* Запустити `scripts/jules_code_health.py --sync-state`.
* Виконати `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)

1. [ ] Модуль `google_ai_gateway.py` підтримує `--enterprise` та `--location` (EU/US).
2. [ ] Створено `tests/integration/test_enterprise_gateway.py`, що успішно проходить з `exit_code: 0`.
3. [ ] Тріаду пам'яті (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`) оновлено до `v5.3.0 / Phase 44`.
4. [ ] Скрипт `scripts/sync_gdrive.py` виконано без помилок.
5. [ ] Зміни зафіксовано у git та виконано `git push origin main`.

---

**Затверджено системним архітектором Gemini Notebook.**  
*Версія: v5.3.0 | Фаза: Phase 44 | Дата: 2026-11-12*
