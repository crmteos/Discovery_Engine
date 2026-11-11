# 🗄️ CONTEXT DOMAIN — MODEL (Node 06) — v2.9.0

## 1. Systemic Context & Data Domain

| Attribute | Value |
|-----------|-------|
| **Node** | `06_Formalized_Model` |
| **Domain** | OpenAPI 3.1 & JSON-LD 1.1 exporter specifications |
| **Notebook** | Gemini Notebook #3 |
| **System** | Discovery Engine Pipeline v2.9.0 |
| **Budget** | $0.00 (Local Execution) |
| **Companion** | `NOTEBOOK_PASSPORT_MODEL.md` (Architectural / Control Plane) |
| **Standard** | Notebook Context Standard — Data Plane (2-file notebook context) |

## 2. Purpose

This notebook is the **Contextual Data Domain (Data Plane)** of Node 06. It defines the OpenAPI 3.1 REST contract and JSON-LD 1.1 semantic export specifications used to publish the final mathematically grounded cognitive model assembled from validated triples (Node 05 → Node 01 → Node 06).

## 3. Export Specifications

### 3.1 OpenAPI 3.1 REST Contract (`openapi_template.json`, `model-assembler` output)

- REST API contract for the formalized model's exposed endpoints.
- Template: `06_Formalized_Model/schemas/openapi_template.json`.
- Exporter: `06_Formalized_Model/src/openapi_exporter.py`.
- Artifact: `*-openapi.yaml` (validated per OpenAPI 3.1).

### 3.2 JSON-LD 1.1 Semantic Export

- Semantic export with `@context`, `@id`, `@type` for W3C Linked Data interoperability.
- Round-trips through a JSON-LD 1.1 processor.
- Artifact: `*-*.jsonld`.

## 4. Model Assembly Artifacts (`src/`, `schemas/`)

| Artifact | Description | Source |
|----------|-------------|--------|
| `model_structure_schema.json` | JSON schema for assembled model structure | `schemas/model_structure_schema.json` |
| `openapi_template.json` | OpenAPI 3.1 export template | `schemas/openapi_template.json` |
| `sample_assembled_model.json` | Sample assembled cognitive model | `src/sample_assembled_model.json` |
| `model_assembler.py` | Assembles ISO 42010 3-view JSON model | `src/model_assembler.py` |
| `openapi_exporter.py` | Exports to OpenAPI 3.1 + JSON-LD 1.1 | `src/openapi_exporter.py` |
| `owl_export_validator.py` | Validates OWL 2 DL logical consistency | `src/owl_export_validator.py` |
| `model_bus_listener.py` | Reads `messages.jsonl` for `model.builder` | `src/model_bus_listener.py` |

## 5. Data Flow

```
Validated triples (Node 05) + ontologies (Node 01)
    → bridge/in → model_bus_listener.py reads Bridge/messages.jsonl
    → model_assembler.py builds ISO 42010 3-view model
    → owl_export_validator.py (OWL 2 DL consistency, 0 contradictions)
    → openapi_exporter.py (OpenAPI 3.1 + JSON-LD 1.1)
    → bridge/out artifacts
```

## 6. Compliance Checklist

- [ ] OpenAPI 3.1 template present (`schemas/openapi_template.json`)
- [ ] Model structure schema present (`schemas/model_structure_schema.json`)
- [ ] `py_compile` exit_code 0 on all Node 06 Python scripts
- [ ] OWL 2 DL validation passes (`owl_export_validator.py`)
- [ ] JSON-LD 1.1 round-trip verified