# Intake Queue Templates Specification (Subsystem 05)

Цей документ містить офіційні JSON-шаблони для оцифрування та передачі когнітивних моделей, аналогій та концептуальних схем з Агрегатора Знань у Математичне Ядро.

---

## 1. Cognitive Model Template (cognitive_model_template.json)

```json
{
  "meta": {
    "type": "cognitive_model",
    "version": "1.0.0",
    "source_notebook": "Knowledge_Aggregator_01",
    "author_role": "Architect"
  },
  "model_name": "Cognitive_Model_Title",
  "description": "Опис когнітивної моделі чи ментального паттерну",
  "entities": [
    {"id": "entity_01", "label": "Елемент_1", "type": "Concept"},
    {"id": "entity_02", "label": "Елемент_2", "type": "Concept"}
  ],
  "relations": [
    {"source": "entity_01", "target": "entity_02", "relation_type": "influences"}
  ],
  "invariants": ["entity_01 + entity_02 == total_state"]
}
```

---

## 2. Analogy Structure Template (analogy_template.json)

```json
{
  "meta": {
    "type": "analogy_mapping",
    "version": "1.0.0",
    "source_notebook": "Knowledge_Aggregator_01",
    "author_role": "Architect"
  },
  "analogy_name": "Domain_A_to_Domain_B_Isomorphism",
  "source_domain": {"name": "Domain_A", "components": ["Source_Elem_1"]},
  "target_domain": {"name": "Domain_B", "components": ["Target_Elem_1"]},
  "isomorphic_mappings": [
    {"source_component": "Source_Elem_1", "target_component": "Target_Elem_1", "mapping_rationale": "Функціональний еквівалент"}
  ]
}
```

---

## 3. Concept Scheme Template (concept_scheme_template.json)

```json
{
  "meta": {
    "type": "concept_scheme",
    "version": "1.0.0",
    "source_notebook": "Knowledge_Aggregator_01",
    "author_role": "OSINT_Orchestrator"
  },
  "scheme_name": "OSINT_Network_Scheme",
  "nodes": [{"id": "node_01", "label": "Observed_Fact_A", "confidence": 0.95}],
  "edges": [{"from": "node_01", "to": "node_02", "type": "leads_to"}]
}
```