# 🗄️ CONTEXT DOMAIN — AGGREGATOR (Node 05) — v2.9.0

## 1. Systemic Context & Data Domain

| Attribute | Value |
|-----------|-------|
| **Node** | `05_Knowledge_Aggregator` |
| **Domain** | Raw intake templates, RDF triple normalization, ingestion rules |
| **Notebook** | Gemini Notebook #2 |
| **System** | Discovery Engine Pipeline v2.9.0 |
| **Budget** | $0.00 (Local Execution) |
| **Companion** | `NOTEBOOK_PASSPORT_AGGREGATOR.md` (Architectural / Control Plane) |
| **Standard** | Notebook Context Standard — Data Plane (2-file notebook context) |

## 2. Purpose

This notebook is the **Contextual Data Domain (Data Plane)** of Node 05. It defines the raw intake JSON templates consumed from external knowledge sources and OSINT feeds, the RDF-style triple normalization schemas applied by `intake_processor.py` / `schema_validator.py`, and the ingestion rules that prepare validated concept schemes, cognitive models, analogies, and media metadata for handoff to `01_Formal_Core`.

## 3. Intake Templates (`Intake_Queue/templates/`)

### 3.1 Cognitive Model Template (`cognitive_model_template.json`)

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

### 3.2 Analogy Structure Template (`analogy_template.json`)

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
    {
      "source_component": "Source_Elem_1",
      "target_component": "Target_Elem_1",
      "mapping_rationale": "Функціональний еквівалент"
    }
  ]
}
```

### 3.3 Concept Scheme Template (`concept_scheme_template.json`)

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

### 3.4 Media Metadata Templates

- `image_metadata_template.json` — visual keys, dimensions, timestamps → RDF triples.
- `video_index_template.json` — temporal chunks, frame indexes → RDF triples.
- `video_index/` — `video_001.json`, `video_index.json`, `vid_001.json` (sample media index records).

## 4. RDF Triple Normalization Rules

- Every intake item is validated against its schema contract by `schema_validator.py` **before** publication to `Bridge/messages.jsonl`.
- Valid items are normalized into RDF-style triples `(subject, predicate, object)` with W3C PROV-O provenance:
  - `prov:wasAttributedTo` — source agent / notebook
  - `prov:generatedAtTime` — ISO 8601 UTC `Z` timestamp
  - `prov:hadPrimarySource` — absolute path to source intake file
  - `confidence_score` — float ∈ [0.0, 1.0]
- SKOS organization: `skos:broader`, `skos:narrower`, `skos:related`, `skos:prefLabel`.
- On schema mismatch, the record is routed to `Bridge/messages_dlq.jsonl`.

## 5. Ingestion Rules

| Phase | Rule | Target |
|-------|------|--------|
| **Ingest** | Raw JSON drafts deposited in `Intake_Queue/{raw_cognitive_models,structural_analogies,conceptual_schemes}` | `Intake_Queue/` |
| **Validate** | Schema-driven validation per template category | `schema_validator.py` |
| **Normalize** | Convert to normalized RDF envelope `{"status": "NORMALIZED", ...}` | `Processed_Gate/normalized_triples/` |
| **Handoff** | Normalized triples formatted for `01_Formal_Core` ingestion | `01_Formal_Core` |
| **Media** | Image/video metadata mapped to visual keys & temporal chunks → RDF triples | `media_extractors/` |

## 6. Output Artifacts

- `Processed_Gate/normalized_triples/normalized_smoke_test_*.json` — validated normalized triples (smoke tests).
- `Bridge/messages.jsonl` — JSONL envelopes written exclusively via `Bridge/bus_manager.py`.
- `Bridge/messages_dlq.jsonl` — triaged invalid records.

## 7. Consolidation Source (Phase 20, v2.9.0)

## 8. CLI Completion Protocols (integrated from `CLI_COMPLETION.md` — Phase 20.1, v2.9.1)

The following CLI intake completion record was consolidated from `CLI_COMPLETION.md` (workspace root) into the Data Plane interface:

All tasks completed successfully. The Axiomatic Converter deployment directive has been executed with all acceptance criteria met:

1. ✅ Role spec `INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` created under `05_Knowledge_Aggregator/roles/`
2. ✅ `axiomatic_converter.py` deployed between Auditor and Knowledge Weaver
3. ✅ `agent_roles_orchestrator.py` updated with `AxiomaticTransformer` class
4. ✅ `bus_inspector.py` audit passed with 0 errors
5. ✅ Execution report saved to `Bridge/out/aggregator_reports/report_axiomatic_converter_[TIMESTAMP].md` under $0.00 budget

**Files Created/Modified:**
- `05_Knowledge_Aggregator/roles/INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` (new)
- `05_Knowledge_Aggregator/axiomatic_converter.py` (new)
- `05_Knowledge_Aggregator/agent_roles_orchestrator.py` (modified)
- `Bridge/out/aggregator_reports/report_axiomatic_converter_20261109_152914.md` (new)

Data-domain content consolidated from `Intake_Queue/templates/INTAKE_TEMPLATES.md` and the intake/normalization sections of `INSTRUCTIONS_ROLE_AGGREGATOR.md` and `AGGREGATOR_OPERATIONAL_PROTOCOL.md`.