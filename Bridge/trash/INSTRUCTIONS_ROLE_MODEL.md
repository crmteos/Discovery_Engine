# ROLE INSTRUCTION: Formalized AI Model Builder

**Scope:** `Discovery_Engine/06_Formalized_Model/`
**Budget:** $0.00 (Local Execution)
**Header Metrics:** BUDGET: $0.00 | SESSION: Autonomous Clean State

## Mission
Збірка та валідація математично заземленої когнітивної моделі, яка є цільовим синтезом усіх попередніх вузлів конвеєра (Node 05 → Node 01 → Node 06).

## Responsibilities
- Отримує нормалізовані тройки з `05_Knowledge_Aggregator/bridge/out/` через `bridge/in/`.
- Збирає фінальну формалізовану ШІ-модель на основі заземлених онтологій `01_Formal_Core`.
- Wydawnняє артефакти моделі у `bridge/out/` для downstream використання.
- Підтримує цілісність моделі через `model.validator`.

## Interface Contract
- **Input:** `bridge/in/` — нормалізовані JSON-енvelope з Node 05 та Node 01.
- **Output:** `bridge/out/` — фінальні артекти формалізованої моделі (JSON, RDF/OWL, DOT).
- **Channel rule:** Виключний доступ через локальний шлюз `bridge/in/` та `bridge/out/`. Недоступно для 직접ного читання з інших вузлів без intermédiaire через системний маніфест.

## State Reference
`06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md` — lokalnyj stan subsystému (замість глобального `PROJECT_STATE.md` для контексту вузла).

## Protocol for Subsystem Engineers
1. **Before Execution:** Read `system_manifest.json` (root) та `06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md`.
2. **After Execution:** Update `PROJECT_STATE.md` та зберегти звіт у `06_Formalized_Model/bridge/out/`.

## Standards Compliance

### W3C OWL 2 DL (Description Logic)

- Target modelsзи повинні бути дотримані до decidable Description Logic subtypes (ALCHI, SROIQ).
- Володіння 0 протирічень:
  - `owl:disjointWith` — докладність класів
  - `owl:equivalentClass` — еквівалентність
  - `owl:Ontology` — reification MetaModel `& owl:versionInfo`
- Перевірка онтології: `rdflib`/`owlready2` або `rove` (OWL 2 DL reasoner).

### ISO/IEC/IEEE 42010 ↔ MBSE: Three Architectural Views

| View | Contents | Artifact |
|------|----------|----------|
| **Structural View** | Entity relationships, taxonomy, concept scheme | `06_Formalized_Model/bridge/out/structure.dot` |
| **Behavioral View** | Event transitions, message flows, state machines | `06_Formalized_Model/bridge/out/behavior_statechart.pdf` |
| **Parametric View** | Mathematical invariants, SymPy constraints, verification recipes | `06_Formalized_Model/bridge/out/parametric_invariants.py` |

### Export Standards

- **OpenAPI 3.1**: REST API contract for the formalized model (`-openapi.yaml`).
- **JSON-LD 1.1**: Semantic export with `@context`, `@id`, `@type` for W3C Linked Data interoperability.

### Message Bus Protocol

- Communication with Core and Aggregator routes through `Bridge/messages.jsonl`.
- Headers: `action`, `task_id`, `hop_count`, `payload`.
- Strict JSON schema validation before write.
