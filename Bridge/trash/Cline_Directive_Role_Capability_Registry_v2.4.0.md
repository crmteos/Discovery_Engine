# Cline Directive: Implementation of Role & Capability Registry Bus (v2.4.0)

**Target System:** Discovery Engine Infrastructure  
**Version:** 2.4.0 (A2A + MCP + Logic Spec-Driven Standard)  
**Execution Governance:** Stateless Autonomous Session | Budget: $0.00  
**Artifact ID:** `Cline_Directive_Role_Capability_Registry_v2.4.0.md`

---

## 🎯 Meta-Goal

Оновити центральний конфігураційний файл `system_manifest.json` до версії **v2.4.0**, інтегрувавши світові інженерні стандарти побудови багатоагентних систем:

1. **Google A2A (Agent2Agent) Protocol (Agent Cards / Рольові паспорти):** Декларативний опис кожної ролі, її зв'язків та дозволених векторів комунікації (`vertical`, `horizontal`, `diagonal`).
2. **Anthropic MCP (Model Context Protocol):** Точне визначення матеріальних ресурсів ролі — дозволені робочі папки (`workspace_dir`), інструменти виконання (`tools`) та контекстні інструкції (`context_resources`).
3. **Logic Spec-Driven Contracts:** Жорстко типізовані JSON-схеми вхідних та вихідних payload'ів для усунення синтаксичних помилок та недетермінованості.

---

## 🛠️ Step-by-Step Execution Plan

### Step 1 — Upgrade `system_manifest.json` to v2.4.0

Оновити `system_manifest.json` у корені проєкту, додавши новий розділ `"role_capability_registry"`. Кожна роль повинна мати таку структуру паспорта:

```json
{
  "system_name": "DiscoveryEngine_Pipeline",
  "version": "2.4.0",
  "architecture": "Dynamic_N_Tier_Actor_Pipeline_with_Universal_Message_Bus",
  "isolation_standard": "Dynamic_N_Tier_Recursive_Isolation_v2.2.0",
  "communication_protocol": "Universal_Transactional_JSONL_Message_Bus_v2.3.0",
  "capability_standards": ["Google_A2A_Protocol", "Anthropic_MCP", "Logic_Spec_Driven_Contracts"],
  "role_capability_registry": {
    "system.master_architect": {
      "a2a_agent_card": {
        "role_id": "system.master_architect",
        "name": "Master System Architect",
        "description": "Головний системний архітектор (Перший Блокнот / Ядро)",
        "allowed_vectors": ["vertical", "horizontal", "diagonal"],
        "subscriptions": ["hypothesis_submission", "status_update", "error_report"]
      },
      "mcp_spec": {
        "workspace_dir": ".",
        "tools": ["system_manifest.json", "PROJECT_STATE.md"],
        "context_resources": ["PROJECT_STATE.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/concept_scheme_template.json",
        "output_schema": null
      }
    },
    "aggregator.architect": {
      "a2a_agent_card": {
        "role_id": "aggregator.architect",
        "name": "Knowledge Aggregator Architect",
        "description": "ШІ-Архітектор Агрегатора Знань (Другий Блокнот)",
        "allowed_vectors": ["vertical", "horizontal", "diagonal"],
        "subscriptions": ["task_request", "data_clarification"]
      },
      "mcp_spec": {
        "workspace_dir": "05_Knowledge_Aggregator/",
        "tools": ["05_Knowledge_Aggregator/src/intake_processor.py", "05_Knowledge_Aggregator/schema_validator.py"],
        "context_resources": ["05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_ARCHITECT.md", "05_Knowledge_Aggregator/AGGREGATOR_OPERATIONAL_PROTOCOL.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/cognitive_model_template.json",
        "output_schema": "05_Knowledge_Aggregator/schemas/analogy_template.json"
      }
    },
    "aggregator.osint_analyst": {
      "a2a_agent_card": {
        "role_id": "aggregator.osint_analyst",
        "name": "OSINT Analyst",
        "description": "Пули OSINT-аналітиків Агрегатора Знань",
        "allowed_vectors": ["horizontal", "diagonal"],
        "subscriptions": ["data_clarification", "query_refinement"]
      },
      "mcp_spec": {
        "workspace_dir": "05_Knowledge_Aggregator/src/",
        "tools": ["05_Knowledge_Aggregator/src/intake_processor.py"],
        "context_resources": ["05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_ORCHESTRATOR.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/concept_scheme_template.json",
        "output_schema": "05_Knowledge_Aggregator/schemas/concept_scheme_template.json"
      }
    },
    "core.formal_engineer": {
      "a2a_agent_card": {
        "role_id": "core.formal_engineer",
        "name": "Formal Core Engineer",
        "description": "Інженер онтологій RDF/OWL та графових структур",
        "allowed_vectors": ["vertical", "horizontal", "diagonal"],
        "subscriptions": ["task_request", "hypothesis_submission"]
      },
      "mcp_spec": {
        "workspace_dir": "01_Formal_Core/src/01_Formal_Ontologies/",
        "tools": ["01_Formal_Core/src/Knowledge_Graphs/kg_engine.py"],
        "context_resources": ["01_Formal_Core/INSTRUCTIONS_ROLE.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/cognitive_model_template.json",
        "output_schema": null
      }
    },
    "core.tda_engineer": {
      "a2a_agent_card": {
        "role_id": "core.tda_engineer",
        "name": "Topological Data Analysis Engineer",
        "description": "Інженер топологічного аналізу даних та виявлення прогалин",
        "allowed_vectors": ["horizontal", "diagonal"],
        "subscriptions": ["task_request", "data_clarification"]
      },
      "mcp_spec": {
        "workspace_dir": "01_Formal_Core/src/04_Discovery_Engine/",
        "tools": ["01_Formal_Core/src/04_Discovery_Engine/Topological_Data_Analysis/tda_gap_finder.py", "01_Formal_Core/src/04_Discovery_Engine/Novelty_Detectors/novelty_detector.py"],
        "context_resources": ["01_Formal_Core/INSTRUCTIONS_ROLE.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/cognitive_model_template.json",
        "output_schema": null
      }
    },
    "model.builder": {
      "a2a_agent_card": {
        "role_id": "model.builder",
        "name": "Target Model Builder",
        "description": "Інженер побудови підсумкової заземленої ШІ-моделі (Третій Блокнот)",
        "allowed_vectors": ["vertical", "horizontal", "diagonal"],
        "subscriptions": ["task_request", "validation_response"]
      },
      "mcp_spec": {
        "workspace_dir": "06_Formalized_Model/",
        "tools": ["06_Formalized_Model/src/"],
        "context_resources": ["06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md"]
      },
      "logic_spec_contracts": {
        "input_schema": "05_Knowledge_Aggregator/schemas/cognitive_model_template.json",
        "output_schema": null
      }
    },
    "cline.executor": {
      "a2a_agent_card": {
        "role_id": "cline.executor",
        "name": "Cline Execution Engineer",
        "description": "Локальний виконавець команд на ПК",
        "allowed_vectors": ["vertical", "horizontal", "diagonal"],
        "subscriptions": ["*"]
      },
      "mcp_spec": {
        "workspace_dir": ".",
        "tools": ["Bridge/bus_manager.py", "05_Knowledge_Aggregator/schema_validator.py", "test_e2e_pipeline.py"],
        "context_resources": ["PROJECT_STATE.md"]
      },
      "logic_spec_contracts": {
        "input_schema": null,
        "output_schema": null
      }
    }
  }
}
```

---

### Step 2 — Integrate Registry Validation into `Bridge/bus_manager.py`

Оновити скрипт `Bridge/bus_manager.py`, додавши перевірку повідомлень проти реєстру ролей з `system_manifest.json`:

1. При відправці (`post_message`):
   - Перевірити, що `sender` та `receiver` зареєстровані у `role_capability_registry`.
   - Перевірити, що `communication_vector` входить до `allowed_vectors` відправника.
   - Валідувати `payload` за допомогою `Logic Spec Contract` (якщо заданий `input_schema` для адресата).
2. Якщо перевірка успішна — записувати повідомлення у `Bridge/messages.jsonl`.
3. Якщо перевірка відхилена — повертати `exit_code != 0` із чітким описом порушення стандарту A2A/MCP/Logic-Spec.

---

### Step 3 — Verification & Execution History

1. Запустити `py_compile Bridge/bus_manager.py`.
2. Виконати дим-тест розширеного `bus_manager.py`: відправити тестове діагональне повідомлення з підтримкою A2A/MCP між `core.tda_engineer` та `aggregator.osint_analyst`.
3. Оновити `PROJECT_STATE.md` (зафіксувати Phase 13: Role & Capability Registry Bus v2.4.0 Deployed).
4. Зберегти звіт у `Bridge/out/execution_reports/report_role_registry_v2.4.0_[TIMESTAMP].md`.

---

**System Integrity Check:**
- Budget: **$0.00**
- Mode: **Stateless Autonomous Sessions**
- Standard: **A2A + MCP + Logic Spec-Driven v2.4.0**
