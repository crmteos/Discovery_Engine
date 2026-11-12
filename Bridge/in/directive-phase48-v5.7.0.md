# SYSTEM DIRECTIVE: PHASE 48 — ISO/IEC/IEEE 42010:2022 METAMODEL & FORMAL PROJECTION OPERATOR (v5.7.0)

**Header Metadata:**
* **Directive ID**: `directive-phase48-v5.7.0`
* **Sender**: `system.master_architect`
* **Receiver**: `cline.executor`
* **Target Node**: `06_Formalized_Model` & `01_Formal_Core`
* **System Version**: `v5.7.0` (Phase 48)
* **Budget Limit**: `$0.00` (Pure Open-Source Stack / Zero Third-Party Paid API)
* **Standards Compliance**: ISO/IEC/IEEE 42010:2022, W3C PROV-O, ADR-0003, ADR-0011
* **Timestamp**: `2026-11-12T09:45:00Z`

---

## 1. МЕТА ТА КОНТЕКСТ

Після оптимізації математичного ядра (Вузол 01: TDA & Basis Transformer у Фазі 47), Фаза 48 інтегрує **`AXIOMATIC_TRANSFORMER`** у **Вузол 06 (`Formalized Model`)** як **Formal Projection Operator** відповідно до стандарту **ISO/IEC/IEEE 42010:2022**.

Трансформатор бере канонічні RDF-факти з Вузла 05 (або шини `Bridge/messages.jsonl`), викликає математичні перетворення Вузла 01 (зміна логарифмічного базису $\log_{10} \to \log_2$, ДФТ-перетворення «часу» у частотну хвильову геометрію) і проектує їх у ізольовані ракурси моделі (Architecture Views/Viewpoints) без викривлення первинних знань джерела (збереження W3C PROV-O).

---

## 2. СПЕЦИФІКАЦІЯ РОБІТ ТА АРТЕФАКТИ

### Task 1: Розширення схем ISO 42010 у Вузлі 06
* **Шлях артефакту**: `06_Formalized_Model/src/schemas.py`
* **Вимоги до вмісту**:
  * Додати Pydantic v2 моделі:
    * `ArchitectureViewpointModel`: `viewpoint_id` (str), `concerns` (list[str]), `framing_axioms` (list[str]), `target_basis` (str = "log2_frequency").
    * `FormalProjectionRequest`: `source_graph_id` (str), `viewpoint` (ArchitectureViewpointModel), `transformation_rules` (list[str]).
    * `FormalProjectionResult`: `projected_graph_id` (str), `triples` (list[dict]), `provenance_chain` (list[str]), `betti_numbers` (dict[str, int]).

### Task 2: Реалізація `axiomatic_transformer.py` у Вузлі 06
* **Шлях артефакту**: `06_Formalized_Model/src/axiomatic_transformer.py`
* **Вимоги до коду**:
  * Клас `AxiomaticTransformer`:
    * Метод `project_viewpoint(request: FormalProjectionRequest) -> FormalProjectionResult`.
    * Інтеграція з `01_Formal_Core/src/basis_transformer.py` для обчислення двійкових логарифмів та ДФТ-спектрів.
    * Повна збереженість походження даних W3C PROV-O (оригінальні RDF-триплети залишаються незмінними в канонічному графі).
    * Підтримка оффлайн-резерву (\$0.00 budget) та `# type: ignore[import]` для безпечного статичного аналізу.

### Task 3: Інтеграційний тест
* **Шлях артефакту**: `tests/integration/test_axiomatic_transformer_iso42010.py`
* **Покриття тесту**:
  * Перевірка створення проєкцій Viewpoint за стандартом ISO/IEC/IEEE 42010:2022.
  * Валідація перерахунку фактів через двійковий базис $\log_2$ та ДФТ-спектр.
  * Перевірка незмінності первинного графу (W3C PROV-O lineage).
  * Нульовий статус помилок (`assert exit_code == 0`).

### Task 4: Оновлення Пам'яті Тріади до v5.7.0 / Phase 48
* **PROJECT_SPEC.md**: Оновлення шапки та розсув ADR-0005 до `v5.7.0 / Phase 48`.
* **PROJECT_CONTEXT.md**: Фіксація стандарту ISO 42010 Formal Projections у Вузлі 06.
* **PROJECT_STATE.md**: Реєстрація успішного виконання Phase 48.

### Task 5: Синхронізація та Git Push
1. Запуск `python scripts/sync_gdrive.py`.
2. Виконання `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)
1. Усі нові та модифіковані файли успішно проходять синтаксичний контроль (`python -m py_compile`).
2. Інтеграційний тест `python tests/integration/test_axiomatic_transformer_iso42010.py` виконується з результатом `PASSED` (`exit_code: 0`).
3. Дотримано суворого бюджетного ліміту `$0.00`.
4. Пам'ять проєкту оновлено до `v5.7.0`, вивантажено на Google Drive та в GitHub-репозиторій.
