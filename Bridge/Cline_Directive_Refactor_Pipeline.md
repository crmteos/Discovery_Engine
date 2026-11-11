# Master Architecture Directive: 3-Node Actor Pipeline & System Manifest Refactoring

**Target Audience:** Execution Engineer (Cline)  
**Execution Context:** Local Windows System (`Discovery_Engine` repository)  
**Governance:** Zero-Budget ($0.00), Stateless Autonomous Sessions, Contract-First Architecture  

---

## 🏛️ Executive Architectural Summary

Ця директива виконує глобальний архітектурний рефакторинг проєкту з метою **100% ізоляції контекстних полів** між трьома автономними вузлами (Блокнотами):

1. **Node 05 (`05_Knowledge_Aggregator`)**: Зовнішній інтаке-вузол (Оркестрація OSINT, когнітивні карти, метафори).
2. **Node 01 (`01_Formal_Core` + 02–04)**: Математичне Ядро (RDF/OWL ontologies, DSPy bridge, Multimodal interface, TDA Discovery Engine).
3. **Node 06 (`06_Formalized_Model`)**: Фінальна формалізована ШІ-модель (цільовий синтез та вивантаження артефактів).

Кожен вузол отримує власну автономну файлову чергу (`bridge/in/` та `bridge/out/`), а весь проєкт підпорядковується єдиному строгому реєстру ролей та маршрутів у корені — **`system_manifest.json`**.

---

## 🛠️ Step-by-Step Execution Plan for Cline

### Step 1: Create Central System Manifest (`system_manifest.json`)
Створити у корені проєкту файл `system_manifest.json` з таким вмістом:

```json
{
  "system_name": "DiscoveryEngine_Pipeline",
  "version": "2.0.0",
  "architecture": "Actor_Node_Pipeline",
  "governance": {
    "budget_limit": 0.0,
    "execution_mode": "Stateless_Autonomous_Sessions",
    "validation": "Strict_Contract_First"
  },
  "nodes": {
    "node_05_aggregator": {
      "name": "Knowledge Aggregator",
      "path": "05_Knowledge_Aggregator/",
      "bridge_in": "05_Knowledge_Aggregator/bridge/in/",
      "bridge_out": "05_Knowledge_Aggregator/bridge/out/",
      "roles": {
        "aggregator.architect": "Формування когнітивних моделей та метафор",
        "aggregator.orchestrator": "Агрегація OSINT-потоків та первинна нормалізація"
      }
    },
    "node_01_core": {
      "name": "Formal Core & Discovery Engine",
      "path": "01_Formal_Core/",
      "bridge_in": "01_Formal_Core/bridge/in/",
      "bridge_out": "01_Formal_Core/bridge/out/",
      "roles": {
        "core.formal_engineer": "Онтології RDF/OWL та графі знань",
        "core.bridge_engineer": "DSPy сигнатури та перевірка галюцинацій",
        "core.tda_engineer": "Топологічний аналіз та виявлення прогалин"
      }
    },
    "node_06_target_model": {
      "name": "Formalized AI Target Model",
      "path": "06_Formalized_Model/",
      "bridge_in": "06_Formalized_Model/bridge/in/",
      "bridge_out": "06_Formalized_Model/bridge/out/",
      "roles": {
        "model.builder": "Збірка математично заземленої когнітивної моделі",
        "model.validator": "Перевірка цілісності підсумкової моделі"
      }
    }
  }
}
```

---

### Step 2: Initialize Node 06 & Local Node Bridges

1. Створити нову директорію та її локальний шлюз:
   - `06_Formalized_Model/bridge/in/`
   - `06_Formalized_Model/bridge/out/`
   - `06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md`

2. Створити локальні шлюзи для вузла 05:
   - `05_Knowledge_Aggregator/bridge/in/`
   - `05_Knowledge_Aggregator/bridge/out/`

3. Створити локальні шлюзи для математичного ядра (вузол 01):
   - `01_Formal_Core/bridge/in/`
   - `01_Formal_Core/bridge/out/`

4. Зберегти зворотну сумісність для кореневої папки `Bridge/` (зберегти `Bridge/in/` та `Bridge/out/` як глобальний диспетчер).

---

### Step 3: Implement Automated Contract Schema Validator

Створити файл `05_Knowledge_Aggregator/schema_validator.py`, який примусово перевіряє будь-який JSON-файл із черги `bridge/in/` перед його передачею у макетний рушій `intake_processor.py`.

Скрипт повинен:
1. Зчитувати відповідну схему з `05_Knowledge_Aggregator/Intake_Queue/templates/`.
2. Перевіряти наявність обов'язкових полів (`meta`, `type`, `version`, `entities` / `source_domain` / `nodes`).
3. Виводити чистий лог та exit code 0 при валідності, або виводити зрозумілу помилку синтаксису без краху середовища.

---

### Step 4: Verification & Smoke Test

1. Виконати `py_compile` для:
   - `05_Knowledge_Aggregator/intake_processor.py`
   - `05_Knowledge_Aggregator/schema_validator.py`
2. Перевірити наявність та валідність `system_manifest.json` за допомогою `json.load()`.

---

### Step 5: State Update & Final Execution Report

1. Оновити `PROJECT_STATE.md`:
   - Додати роздел про `3-Node Actor Pipeline` та `system_manifest.json`.
   - Позначити статус вузла 06 як `🟢 Active (Initialized)`.
2. Зберегти підсумковий звіт у:
   `Bridge/out/execution_reports/report_pipeline_refactor_[TIMESTAMP].md`
