# SYSTEM DIRECTIVE: PHASE 46 — SINGLE-PROMPT STUDIO GATEWAY RULE & TYPED GENKIT BRIDGING (v5.5.0)

**Header Metadata:**
* **Directive ID**: `directive-phase46-v5.5.0`
* **Sender**: `system.master_architect` (Gemini Notebook)
* **Receiver**: `cline.executor` (Cline AI in VS Code)
* **Target Nodes**: `00_Project_Interface`, `05_Knowledge_Aggregator`, `01_Formal_Core`, `06_Formalized_Model`
* **System Version**: `v5.5.0` (Phase 46)
* **Budget Limit**: `$0.00` (Pure Open-Source Stack / Free Limits)
* **Timestamp**: `2026-11-12T08:30:00Z`

---

## 1. МЕТА ТА КОНТЕКСТ

1. **Системна фіксація правила Studio & Cline Protocol**: Закріпити в `PROJECT_SPEC.md` (ADR-0003), `PROJECT_STATE.md` та `docs/STARTPOINT_META_PROMPT.md` незмінне системне правило:
   - Архітектор (Gemini Notebook) публікує всі інженерні директиви у вигляді `.md` артефактів у **панель Studio**, а не в код-блоки чату.
   - Директиви призначені виключно для виконання **ШІ Кліном (Cline AI у VS Code)**, а не для ручного виконання людиною-оператором.
   - Людина виконує роль **Gateway Operator**: зберігає артефакт директиви зі Studio у `Bridge/in/` та передає Кліну єдину Single-Prompt команду.

2. **Старт Фази 46 із нового комплекту системної документації (Вузли 01 та 06)**:
   - Побудова типізованого мосту на базі **Firebase Genkit Python SDK**, **Dotprompt** та **Pydantic v2** для вилучення RDF-триплетів знань без відхилень від схем та галюцинацій (Вузол 05 / 00).

---

## 2. СПЕЦИФІКАЦІЯ РОБІТ ТА АРТЕФАКТИ

### Task 1: Закріплення правила Studio & Single-Prompt Gateway у Пам'яті Проекту
* **Файли для оновлення**: `PROJECT_SPEC.md` (ADR-0003), `PROJECT_STATE.md` (Governance Standards), `docs/STARTPOINT_META_PROMPT.md`.
* **Вимоги**:
  1. Оновити ADR-0003 та Governance Standards з чітким формулюванням 4-крокового протоколу:
     - **Step 1 (Architect - Gemini Notebook)**: Створює інженерну директиву `directive-phaseXX-vX.Y.Z.md` як артефакт у панелі Studio.
     - **Step 2 (Gateway Operator - Human User)**: Зберігає файл директиви зі Studio у `Bridge/in/directive-phaseXX-vX.Y.Z.md`.
     - **Step 3 (Gateway Operator / Execution Engineer)**: Передає єдину Single-Prompt команду Кліну у VS Code.
     - **Step 4 (Execution Engineer - Cline AI)**: Обробляє директиву, реєструє в шині через `bus_manager.py --post`, реалізує код, проганяє тести, оновлює тріаду пам'яті (`PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md`), виконує `python scripts/sync_gdrive.py` та робить `git push origin main`.
  2. Зафіксувати, що цей протокол є **обов'язковим незмінним стандартом** для всіх наступних сесій і блокнотів.

### Task 2: Створення Dotprompt-шаблону вилучення RDF-триплетів
* **Шлях артефакту**: `05_Knowledge_Aggregator/prompts/rdf_extraction.prompt`
* **Вимоги до вмісту**:
  * YAML frontmatter: `model: googleai/gemini-2.5-flash`, `temperature: 0.0`, `maxOutputTokens: 2048`.
  * Визначення `input.schema.raw_text` та `output.format: json`.
  * Застереження про нульове використання фактів поза наданим текстом `{{raw_text}}` (Zero Hallucination Rule).

### Task 3: Реалізація типізованого мосту Genkit Python SDK
* **Шлях артефакту**: `05_Knowledge_Aggregator/src/genkit_typed_bridge.py`
* **Вимоги до коду**:
  * Pydantic v2 моделі:
    * `RDFTripleModel`: `subject` (str), `predicate` (str), `object` (str), `graph_context` (str = "main_graph").
    * `ExtractionResponse`: `triples` (list[RDFTripleModel]).
  * Async Genkit Flow `extract_rdf_triples_flow(raw_text: str) -> ExtractionResponse`.
  * Гібридний оффлайн-резерв: при відсутності мережі чи API-ключа здійснювати перемикання на локальний Ollama API / Pure Python parser (`exit_code: 0`).

### Task 4: Інтеграційний тест та Синхронізація (v5.5.0)
* **Шлях артефакту**: `tests/integration/test_genkit_typed_bridge.py`
* **Покриття**:
  * Перевірка створення Pydantic-моделей та валідації JSON-схеми.
  * Перевірка оффлайн-фолбеку та нульового виходу (`assert exit_code == 0`).
* **Синхронізація**:
  * Оновити тріаду пам'яті до **v5.5.0 / Phase 46**.
  * Виконати `python scripts/sync_gdrive.py` для оновлення Google Drive.
  * Виконати `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)
1. `PROJECT_SPEC.md` (ADR-0003), `PROJECT_STATE.md` та `docs/STARTPOINT_META_PROMPT.md` оновлено з жорсткою фіксацією ролей Studio Artifact & Single-Prompt Protocol.
2. `rdf_extraction.prompt` та `genkit_typed_bridge.py` реалізовано та перевірено `python -m py_compile`.
3. `tests/integration/test_genkit_typed_bridge.py` пройдено з `exit_code: 0`.
4. Пам'ять синхронізовано до `v5.5.0 / Phase 46`, `sync_gdrive.py` виконано, комміт вивантажено на GitHub (`git push origin main`).
