# Cline Directive: Resilience, Governance & Semantic Safety Architecture (v2.5.0)

**Target System:** Discovery Engine Framework  
**Architectural Upgrade:** v2.4.0 ➔ v2.5.0  
**Scope:** Integration of Zylos EDA, Logic Inc & FME Industry Standards for Multi-Agent Governance  
**Governance Constraints:** BUDGET: $0.00 | Stateless Autonomous Sessions | Production-Grade Zero-Hallucination

---

## 🏛️ Executive Summary & Objectives

Ця майстер-директива санкціонує перехід системи `Discovery Engine` на **v2.5.0 Resilience, Governance & Semantic Safety Standard**. 

Мета оновлення — впровадження 5 фундаментальних промислових паттернів побудови автономних багатоагентних систем для усунення «сліпих плям», захисту від нескінченних зациклень, забезпечення ідемпотентності та збереження жорсткого операторського контролю над критичними вузлами.

---

## 🎯 5 Фундаментальних Інженерних Паттернів (v2.5.0)

### 1. Dead Letter Queue (DLQ) & Error Triage (`Bridge/messages_dlq.jsonl`)
* **Механіка:** Будь-яке повідомлення з малформованим payload, збійним синтаксисом або недійсним паспортом ролі НЕ видаляється і не блокує головний потік `Bridge/messages.jsonl`.
* **Тріаж помилок у `bus_manager.py`:**
  * **Retryable:** Тимчасова помилка середовища ➔ автоматичний повтор з запізненням (backoff).
  * **Permanent:** Критичне порушення контракту чи схем ➔ переміщення у `Bridge/messages_dlq.jsonl` з полями `dlq_reason`, `error_type` та `timestamp`.

### 2. Idempotency Key & Deduplication Store (`Bridge/.idempotency_store.json`)
* **Механіка:** Будь-яка попередня дія, що викликає побічні ефекти (запис файлів, виконання аналізу), отримує унікальний Idempotency Key: `hash(sender + task_id + action_type)`.
* **Перевірка:** Перед виконанням `bus_manager.py` перевіряє `.idempotency_store.json`. Якщо дія за цим ключем вже позначена як `completed`, повторний побічний ефект блокується, і повертається кешований результат.

### 3. Circuit Breakers & Cascade Control (`max_hops` <= 3)
* **Механіка:** Усі діагональні та горизонтальні комунікаційні ланцюжки мають ліміт вкладеності.
* **Забіжник:** Кожне створене або перенаправлене повідомлення збільшує лічильник `hop_count`. Якщо `hop_count > max_hops` (за замовчуванням `3`), `bus_manager.py` перериває каскад, переводить статус у `circuit_broken` та надсилає сповіщення Оператору.

### 4. Semantic Verification Gate (Додаткова семантична перевірка)
* **Механіка:** Окрім перевірки синтаксису через JSON-схему (Draft 7), `bus_manager.py` запускає Python-перевірку семантичних інваріантів:
  * Для графів/онтологій: перевірка зв'язності та відсутності замкнених циклів через `NetworkX`.
  * Для логічних/математичних тверджень: перевірка непротиріччя через `SymPy`.

### 5. Human-in-the-Loop (HITL) Workflow
* **Механіка:** Підтримка перформатива `human_approval_required`.
* **Поведінка:** При досягненні критичних фаз (наприклад, збірка цільової моделі у `06_Formalized_Model`) задача переходить у стан `awaiting_human_approval`. Скрипти зупиняють виконання до моменту появи підтверджувального запису від `user.operator` у `Bridge/messages.jsonl`.

---

## 🛠️ Завдання для Кліна (Execution Engineer)

1. **Оновлення `system_manifest.json` (до v2.5.0):**
   * Оновити версію маніфесту на `2.5.0`.
   * Додати блок `resilience_governance` з налаштуваннями DLQ, Idempotency, Circuit Breakers (`max_hops: 3`), Semantic Gates та HITL.

2. **Модернізація `Bridge/bus_manager.py`:**
   * Додати методи обробки DLQ (`post_to_dlq()`).
   * Додати підтримку перевірки та запису ідемпотентних ключів у `Bridge/.idempotency_store.json`.
   * Впровадити перевірку `hop_count <= max_hops`.
   * Додати семантичний валідатор `validate_semantic_invariants()`.
   * Додати підтримку перформатива `human_approval_required`.

3. **Оновлення `PROJECT_STATE.md`:**
   * Фіксувати Milestone **Phase 14: Resilience & Governance Architecture v2.5.0 Deployed**.

4. **Тестування та Верифікація:**
   * Провести `py_compile` для оновлених скриптів.
   * Виконати дим-тест розширеного `bus_manager.py`: симуляція спроби некоректного повідомлення (маршрутизація в DLQ), повторного запиту (перевірка ідемпотентності) та зациклення (`circuit_breaker`).

5. **Звітність:**
   * Зберегти підсумковий звіт у `Bridge/out/execution_reports/report_resilience_governance_v2.5.0_[TIMESTAMP].md`.

---

**Розробка:** System Architect (Gemini Notebook)  
**Дата:** 2026-11-08
