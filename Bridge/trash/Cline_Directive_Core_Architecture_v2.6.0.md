# Cline Directive: Formal Core Architecture & Rigor Upgrade (v2.6.0)

**Target System:** `Discovery_Engine` / `01_Formal_Core` (Modules 01–04)  
**Standard Version:** v2.6.0 (W3C SHACL + DSPy Assertions + CAS SymPy Prover + Vietoris-Rips TDA + OpenTelemetry GenAI)  
**Budget:** $0.00 (Pure Open-Source & Local Hardware Stack)  
**Execution Mode:** Autonomous Execution Agent (Cline)  

---

## 🎯 OBJECTIVE & SYSTEM PURPOSE

Оновити обчислювальні та математичні модулі **Математичного Ядра (`01_Formal_Core`)** до версії **v2.6.0**, інтегрувавши 5 фундаментальних промислових стандартів:

1. **W3C SHACL (Shapes Constraint Language):** Декларативна валідація онтологій та RDF-графів знань.
2. **DSPy Assertions & Dynamic Backtracking:** Автоматичний самокорекційний нейро-символьний місток без зовнішніх платнових API.
3. **CAS SymPy Theorem & Invariant Prover:** Канонізація алгебраїчних формул та перевірка здійснимості інваріантів.
4. **Vietoris-Rips Persistent Homology ($H_0, H_1$):** Автоматичний вимір компонентів зв'язності та топологічних прогалин знань.
5. **OpenTelemetry GenAI Semantic Conventions:** Широкий семантичний логінг обчислювальних кроків Ядра в `Bridge/messages.jsonl`.

---

## 📋 STEP-BY-STEP EXECUTION INSTRUCTIONS

### Step 1: Update `system_manifest.json` to v2.6.0
* Оновити глобальний конфіг у корені до версії `2.6.0`.
* Додати блок `formal_core_standards`:
```json
"formal_core_standards": {
  "w3c_shacl": {
    "enabled": true,
    "schema_dir": "01_Formal_Core/schemas/shacl/"
  },
  "dspy_guardrails": {
    "enabled": true,
    "backtracking": true
  },
  "sympy_cas_prover": {
    "enabled": true,
    "canonical_simplification": true
  },
  "vietoris_rips_tda": {
    "enabled": true,
    "homology_dimensions": ["H0", "H1"]
  },
  "opentelemetry_genai": {
    "enabled": true,
    "telemetry_bus": "Bridge/messages.jsonl"
  }
}
```

### Step 2: Implement Core Modules Upgrades in `01_Formal_Core/src/`

1. **`01_Formal_Ontologies` & `Knowledge_Graphs` (W3C SHACL Validator):**
   * Створити `01_Formal_Core/src/01_Formal_Ontologies/shacl_validator.py`.
   * Реалізувати базову перевірку графів `rdflib` на відповідність базовим SHACL-формам (типи вузлів, наявність URI, відсутність циклів-пастка).

2. **`02_NeuroSymbolic_Bridge` (DSPy Assertions):**
   * Модернізувати `01_Formal_Core/src/02_NeuroSymbolic_Bridge/Grounding_Validators/axiom_checker.py` та `dspy_signatures.py`.
   * Додати підтримку `dspy.Assert()` для логічних умов та автоматичного підсказування при виявленні суперечностей з аксіомами `universe_base.ttl`.

3. **`Symbolic_AI` (CAS Theorem & Invariant Prover):**
   * Створити `01_Formal_Core/src/Symbolic_AI/sympy_cas_prover.py`.
   * Реалізувати функції `verify_invariant(expr_str)` та `check_satisfiability(clauses)`, що виконують `sympy.sympify()` та `sympy.satisfiable()` для перевірки математичної несуперечливості.

4. **`04_Discovery_Engine` (Vietoris-Rips Persistent Homology $H_0, H_1$):**
   * Модернізувати `01_Formal_Core/src/04_Discovery_Engine/Topological_Data_Analysis/tda_gap_finder.py`.
   * Додати обчислення Betti numbers: $b_0$ (компоненти зв'язності) та $b_1$ (топологічні дірки). Формувати підсумкову гіпотезу `HYPOTHESIS_UNIFIED_CORE_001` із зазначенням чисел Бетті.

### Step 3: OpenTelemetry GenAI Logging Integration
* У `Bridge/bus_manager.py` або локальних скриптах Ядра реалізувати функцію `log_core_telemetry(step_name, metrics, status)`, яка дописує семантичний лог у `Bridge/messages.jsonl` за стандартом OpenTelemetry.

### Step 4: Verification & E2E Testing
1. Виконати `py_compile` для всіх створених та модифікованих Python-файлів у `01_Formal_Core/src/`.
2. Запустити `python3 test_e2e_pipeline.py`.
3. Переконатися, що всі 4 етапи завершуються з `exit_code: 0`.

### Step 5: Update Project State & Execution Report
1. Оновити `PROJECT_STATE.md` (фіксація Phase 15, Core Standards v2.6.0).
2. Зберегти підсумковий звіт у `Bridge/out/execution_reports/report_core_architecture_v2.6.0_[TIMESTAMP].md`.

---

## 🛑 NON-NEGOTIABLE CONSTRAINTS
- **BUDGET_LIMIT:** $0.00 (Жодних платнових API / Тільки локальний CPU стек).
- **STATELESS SESSIONS:** Весь стан оновлюється у `PROJECT_STATE.md` та `system_manifest.json`.
- **ZERO HALLUCINATION:** Будь-яке твердження має бути заземлене через SHACL, SymPy або TDA.
