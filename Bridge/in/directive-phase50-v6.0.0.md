# SYSTEM DIRECTIVE: PHASE 50 — DUAL-STREAM ELEPHANT ARCHITECTURE REFACTORING (v6.0.0)

**Header Metadata:**
* **Directive ID**: `directive-phase50-v6.0.0`
* **Sender**: `system.master_architect`
* **Receiver**: `cline.executor`
* **Target Nodes**: `06_Formalized_Model`, `05_Knowledge_Aggregator`, `01_Formal_Core`
* **System Version**: `v6.0.0` (Phase 50)
* **Budget Limit**: `$0.00` (Pure Open-Source Stack / Local Execution)
* **Timestamp**: `2026-11-12T11:25:00Z`

---

## 1. МЕТА ТА КОНЦЕПТУАЛЬНА АРХІТЕКТУРА ("СЛІПЦІ ТА СЛОН")
Основна мета Фази 50 — перебудова Discovery Engine з прямолінійного конвертера даних на **систему подвійної інтерпретації контексту (Dual-Variant Context Interpretation)**.

Один і той самий сирий потік даних від `NARROW_EXTRACTOR` має розщеплюватися на два автономні когнітивні канали:
1. **Потік А (Антропоморфно-декадний ракурс)**: Прямий текст, десяткова логарифмічна основа ($\log_{10}$), стандартний часовий параметр ($t$). Проходить через `ZERO_HALLUCINATION_AUDITOR` ➔ `KNOWLEDGE_WEAVER` (Канал А).
2. **Потік Б (Аксіоматично-модульований ракурс)**: Передається в ізольований модуль `AXIOMATIC_TRANSFORMER`. Модуль застосовує ключі з локальної папки `06_Formalized_Model/keys/` (PDF, MD, текстові методики) як **модулюючий сигнал**, переводить шкали в двійкову основу ($\log_2$) та трансформує час у частотний спектр LT-системи ➔ `KNOWLEDGE_WEAVER_B` (Канал Б).

**Формальне Математичне Ядро (Вузол 01)** отримує **два паралельні потоки (Канал А та Канал Б)** як дві різні когнітивні проєкції одного "Слона", проводить крос-матричну кореляцію та топологічний аналіз (TDA), виявляючи незмінний інваріант об'єктивної істини.

---

## 2. СПЕЦИФІКАЦІЯ РОБІТ ТА АРТЕФАКТИ

### Task 1: Створення папки ключів та модулюючого `AXIOMATIC_TRANSFORMER`
* **Шляхи артефактів**:
  * Папка ключів: `06_Formalized_Model/keys/`
  * Файл ключа за замовчуванням: `06_Formalized_Model/keys/LT_system_basis_key.md`
  * Трансформер: `06_Formalized_Model/src/axiomatic_transformer.py`
* **Вимоги до коду**:
  * `AxiomaticTransformer` відкриває та зчитує модулюючі сигнали з папки `keys/`.
  * Приймає сирий потік від `NARROW_EXTRACTOR` і будує аксіоматично-перетворений Потік Б ($\log_{10} \to \log_2$, заміна часового параметра $t$ на частотну суперпозицію).
  * Зберігає W3C PROV-O походження фактів (`provo_lineage.py`).

### Task 2: Реалізація двоканального `KNOWLEDGE_WEAVER`
* **Шлях артефакту**: `05_Knowledge_Aggregator/src/knowledge_weaver.py`
* **Вимоги до коду**:
  * Створення методу `weave_dual_streams(stream_a: dict, stream_b: dict) -> DualStreamEnvelope`.
  * Гарантія збереження метаданих про те, що Потік А та Потік Б походять від єдиної первинної бази даних `NARROW_EXTRACTOR`.

### Task 3: Інваріантне Порівняння у Формальному Ядрі (Вузол 01)
* **Шлях артефакту**: `01_Formal_Core/src/pure_tda_engine.py` та `01_Formal_Core/src/formal_core_gateway.py`
* **Вимоги до коду**:
  * Реалізація методу `extract_context_invariant(dual_envelope: DualStreamEnvelope) -> InvariantElephantResult`.
  * Порівняння топологічних інваріантів Бетті ($H_0, H_1$) двох потоків та обчислення коефіцієнта об'єктивного інваріанта ("Слона").

### Task 4: Інтеграційний тест
* **Шлях артефакту**: `tests/integration/test_dual_stream_elephant_architecture.py`
* **Покриття тесту**:
  * Симуляція збору даних `NARROW_EXTRACTOR`.
  * Розщеплення на Потік А та Потік Б (із застосуванням файлу ключів з `06_Formalized_Model/keys/`).
  * Передача у `FormalCoreGateway` та валідація отримання об'єктивного інваріанта.
  * Перевірка `assert exit_code == 0`.

### Task 5: Оновлення Пам'яті та Синхронізація (v6.0.0)
1. Оновити шапки та блоки версій у `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md` та `PROJECT_STATE.md` до **v6.0.0 / Phase 50**.
2. Запустити `python scripts/sync_gdrive.py`.
3. Виконати `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)
1. Створено структуру папки `06_Formalized_Model/keys/` з тестовим модулюючим файлом ключа.
2. Інтеграційний тест `tests/integration/test_dual_stream_elephant_architecture.py` виконується зі статусом `PASSED` (`exit_code: 0`).
3. Ядро (Вузол 01) приймає 2 паралельні інтерпретації одного контексту та обчислює інваріант.
4. Тріаду пам'яті оновлено до **v6.0.0 / Phase 50**, виконано `sync_gdrive.py` та `git push origin main`.
