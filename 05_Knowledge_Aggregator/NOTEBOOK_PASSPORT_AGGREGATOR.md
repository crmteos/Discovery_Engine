# 📘 NOTEBOOK PASSPORT — AGGREGATOR (Node 05) — v3.5.0

## 1. Systemic Context & Architecture

| Attribute | Value |
|-----------|-------|
| **Node** | `05_Knowledge_Aggregator` |
| **Roles** | `aggregator.architect`, `aggregator.osint_analyst` |
| **Notebook** | Gemini Notebook #2 |
| **System** | Discovery Engine Pipeline v3.5.0 |
| **Budget** | $0.00 (Local Execution, Zero-Hallucination) |
| **Message Bus** | `Bridge/messages.jsonl` (Universal Transactional JSONL Bus) |
| **Bus Manager** | `Bridge/bus_manager.py` |
| **Schema Engine** | `05_Knowledge_Aggregator/schema_validator.py` |
| **Isolation Standard** | Dynamic_N_Tier_Recursive_Isolation_v2.2.0 |
| **Notebook Context Standard** | 2 files: `NOTEBOOK_PASSPORT_AGGREGATOR.md` (Control Plane) + `CONTEXT_DOMAIN_AGGREGATOR.md` (Data Plane) |

### 1.1 Notebook Context Standard (v3.5.0)

This notebook is the **Architectural Interface (Control Plane)** of Node 05. It governs roles, capabilities, PROV-O/SKOS rules, and the JSONL bus contract. The companion file `CONTEXT_DOMAIN_AGGREGATOR.md` holds the **Data Plane**: raw intake templates, RDF triple normalization schemas, and ingestion rules. Together they form the strict 2-file notebook context for this node, per `system_manifest.json` rule `notebook_context_standard`.

### 1.2 Isolation Rule (v3.5.0)

- Node 05 roles (`aggregator.architect`, `aggregator.osint_analyst`) communicate exclusively via the universal transactional Message Bus (`Bridge/bus_manager.py` → `Bridge/messages.jsonl`); node-local `bridge/in` and `bridge/out` bindings are removed.
- Read `Bridge/in/core/` / write `Bridge/out/execution_reports/` is NOT permitted by this node's contract (isolation enforced by manifest rules, not filesystem permissions).
- Cross-node Python imports permitted only via manifest-registered paths under `01_Formal_Core/src/`.

## 2. Role Definition

### `aggregator.architect`

**Responsibilities:**
- Receives raw concept schemes & cognitive models from `Intake_Queue/` and from Node 01/06.
- Validates every entry against `schema_validator.py` (W3C PROV-O & SKOS compliant).
- Prevents hallucination: zero AI-generated free-text outside schema envelopes.
- Produces `concept_scheme_template.json` and `cognitive_model_template.json`.
- Publishes JSONL envelopes to `Bridge/messages.jsonl` via `Bridge/bus_manager.py`.

**Key Capabilities (from `system_manifest.json` v3.5.0):**
- `a2a_agent_card`: role_id `aggregator.architect`, subscriptions: `task_request`, `data_clarification`
- `mcp_spec.workspace_dir`: `05_Knowledge_Aggregator/`
- `mcp_spec.tools`: `intake_processor.py`, `schema_validator.py`
- `logic_spec_contracts.input_schema`: `05_Knowledge_Aggregator/schemas/cognitive_model_template.json`
- `logic_spec_contracts.output_schema`: `05_Knowledge_Aggregator/schemas/analogy_template.json`

### `aggregator.osint_analyst`

**Responsibilities:**
- Normalizes and aggregates open-source (OSINT) external data streams.
- Maps observed facts into SKOS concept schemes with `skos:broader` / `skos:narrower` / `skos:related`.
- Submits normalized envelopes via the Message Bus for Core ingestion.

**Key Capabilities:**
- `a2a_agent_card`: role_id `aggregator.osint_analyst`, subscriptions: `task_request`, `data_clarification`, `hypothesis_submission`
- `mcp_spec.workspace_dir`: `05_Knowledge_Aggregator/`
- `mcp_spec.tools`: `intake_processor.py`, `schema_validator.py`
- `logic_spec_contracts.input_schema`: `05_Knowledge_Aggregator/schemas/cognitive_model_template.json`

## 3. Operational Standards

| Standard | Rule | Compliance Check |
|----------|------|------------------|
| **Budget** | $0.00 — pure local execution, no external API calls beyond local model | `py_compile` exit_code 0 |
| **Zero-Hallucination** | All content derived deterministically from inputs or validated by schema/validator | `schema_validator.py` return code 0 |
| **W3C PROV-O** | `prov:wasAttributedTo`, `prov:generatedAtTime`, `prov:hadPrimarySource`, `confidence_score` on every record | fields present & non-null |
| **W3C SKOS** | `skos:broader`, `skos:narrower`, `skos:related` for hierarchical/related concepts | present where applicable |
| **Message Bus** | `Bridge/bus_manager.py` is the only writer to `Bridge/messages.jsonl` | SHA256 idempotency key on each record |

## 4. JSONL Message Templates for `Bridge/messages.jsonl`

All messages MUST be written using `Bridge/bus_manager.py`. The file `messages.jsonl` is an append-only event log — never truncate or replace.

### 4.1 Concept Scheme Registration (`submit_task`)

```jsonl
{
  "timestamp": "2026-11-10T10:04:56Z",
  "task_id": "TSK-AGG-CS-001",
  "action": "submit_task",
  "payload": {
    "role": "aggregator.architect",
    "agent_id": "aggregator.architect@discovery_engine",
    "data_type": "concept_scheme",
    "schema": "05_Knowledge_Aggregator/schemas/concept_scheme_template.json",
    "content": {
      "scheme_id": "CS::Cognitive::v1",
      "title": "Cognitive Architecture Concept Scheme",
      "keywords": ["cognition", "architecture", "formal"],
      "concepts": [
        {
          "name": "perception_loop",
          "definition": "Closed-loop model of sensory processing and action selection",
          "skos_prefLabel": "Perception Loop",
          "skos_broader": "CS::Cognitive::v1::process",
          "skos_narrower": [],
          "skos_related": ["CS::Cognitive::v1::feedback"],
          "prov_wasAttributedTo": "aggregator.architect",
          "prov_generatedAtTime": "2026-11-10T10:04:56Z",
          "prov_hadPrimarySource": "05_Knowledge_Aggregator/Intake_Queue/CS::Cognitive::v1.json",
          "confidence_score": 0.92
        }
      ]
    },
    "hop_count": 0
  }
}
```

### 4.2 Cognitive Model Submission (`submit_task`)

```jsonl
{
  "timestamp": "2026-11-10T10:04:56Z",
  "task_id": "TSK-AGG-CM-001",
  "action": "submit_task",
  "payload": {
    "role": "aggregator.architect",
    "agent_id": "aggregator.architect@discovery_engine",
    "data_type": "cognitive_model",
    "schema": "05_Knowledge_Aggregator/schemas/cognitive_model_template.json",
    "content": {
      "metadata": {
        "model_name": "Perception-Action-Cognition Loop",
        "author": "aggregator.architect",
        "timestamp": "2026-11-10T10:04:56Z",
        "source_notebook": "Gemini Notebook #2"
      },
      "entities": [
        {"id": "e1", "name": "sensor", "type": "input"},
        {"id": "e2", "name": "actuator", "type": "output"},
        {"id": "e3", "name": "belief_state", "type": "state"}
      ],
      "relations": [
        {"subject": "e1", "predicate": "feeds", "object": "e3"},
        {"subject": "e3", "predicate": "drives", "object": "e2"}
      ],
      "invariants": [
        "belief_state consistency > 0.7",
        "actuator response < 100ms"
      ]
    },
    "hop_count": 0
  }
}
```

### 4.3 Status Update to `core.formal_engineer` (`status_update`)

```jsonl
{
  "timestamp": "2026-11-10T10:04:56Z",
  "task_id": "TSK-AGG-SU-001",
  "action": "status_update",
  "payload": {
    "role": "aggregator.architect",
    "status": "ready",
    "ready_artifacts": ["schema_validated_concept_scheme_v1.jsonl"],
    "pending_reqs": [],
    "confidence_score": 0.95
  },
  "hop_count": 1
}
```

## 5. Workflow

```
1. Read intake queue →
2. Validate schema (schema_validator.py) →
3. Add PROV-O/SKOS metadata →
4. Write JSONL via Bridge/bus_manager.py →
5. Log status →
6. Await response from core (01_Formal_Core)
```

## 6. Compliance Checklist (Pre-Submission)

- [ ] `schema_validator.py` returned `exit_code: 0`
- [ ] `prov:wasAttributedTo` = `aggregator.architect`
- [ ] `prov:generatedAtTime` = ISO 8601 UTC with `Z` suffix
- [ ] `prov:hadPrimarySource` = absolute path to source file
- [ ] `confidence_score` ∈ [0.0, 1.0]
- [ ] `skos:broader` / `skos:narrower` / `skos:related` set where applicable
- [ ] Record written through `Bridge/bus_manager.py` (not direct file IO)

## 7. Consolidation Record (Phase 20, v3.5.0 → v2.9.1)

The following Node 05 governance files were consolidated into this passport and `CONTEXT_DOMAIN_AGGREGATOR.md`:

- `INSTRUCTIONS_ROLE_AGGREGATOR.md` → role definition, PROV-O/SKOS compliance, message bus protocol → Section 8 (this file) [Phase 20.1, v2.9.1]
- `AGGREGATOR_OPERATIONAL_PROTOCOL.md` → notebook ↔ operator ↔ Cline interaction protocol → Section 9 (this file) [Phase 20.1, v2.9.1]
- `AGGREGATOR_CHECKLIST.md` → ingestion phases & operational readiness checklist → Section 10 (this file) [Phase 20.1, v2.9.1]
- `AGGREGATOR_STATE.md` → local subsystem state telemetry & metrics history → Section 11 (this file) [Phase 20.1, v2.9.1]
- `CLI_COMPLETION.md` (workspace root) → CLI intake completion protocol → `CONTEXT_DOMAIN_AGGREGATOR.md` Section 8 (Data Plane) [Phase 20.1, v2.9.1]
- `roles/INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` → role responsibilities (this file)
- `roles/INSTRUCTIONS_ROLE_KNOWLEDGE_WEAVER.md` → role responsibilities (this file)
- `roles/INSTRUCTIONS_ROLE_NARROW_EXTRACTOR.md` → role responsibilities (this file)
- `roles/INSTRUCTIONS_ROLE_WIDE_DISCOVERY.md` → role responsibilities (this file)
- `roles/INSTRUCTIONS_ROLE_ZERO_HALLUCINATION_AUDITOR.md` → zero-hallucination rule (this file)
- `Intake_Queue/templates/INTAKE_TEMPLATES.md` → intake templates → `CONTEXT_DOMAIN_AGGREGATOR.md`

### 7.1 Phase 20.1 Cleanup Record (v2.9.1)

On 2026-11-10, the remaining 4 legacy governance files (`INSTRUCTIONS_ROLE_AGGREGATOR.md`, `AGGREGATOR_OPERATIONAL_PROTOCOL.md`, `AGGREGATOR_CHECKLIST.md`, `AGGREGATOR_STATE.md`) plus `CLI_COMPLETION.md` (workspace root) were fully integrated into the strict 2-File Notebook Context Standard and permanently removed from disk. Node 05 now maintains exactly 2 canonical interfaces:

- `NOTEBOOK_PASSPORT_AGGREGATOR.md` — Architectural Interface / Control Plane (roles, PROV-O/SKOS rules, bus contract, state).
- `CONTEXT_DOMAIN_AGGREGATOR.md` — Contextual Data Domain / Data Plane (intake templates, RDF triple normalization, ingestion rules, CLI completion protocols).

**Verified:** `json.load()` on `system_manifest.json` → exit_code 0; `python test_e2e_pipeline.py` → all 4 stages exit_code 0.

## 8. Role Passport & Identity (integrated from `INSTRUCTIONS_ROLE_AGGREGATOR.md`)

### Mission
Збірка, нормалізація та агрегація знань із різноманітних джерел з підтримкою стандартів W3C PROV-O (provenance) та W3C SKOS (organizational schemes). Всі входження підлягають валідації схемою `schema_validator.py` та передачі в `Bridge/messages.jsonl` через `bus_manager.py`.

### Responsibilities
- Нормалізує внутрішні (Node 01, Node 06) та зовнішні (OSINT) потоки даних.
- Створює пре-агреговані `concept_scheme` та `cognitive_model` творі.
- Гарантує відстеження provenance через W3C PROV-O.
- Підтримує SKOS-організацію через `skos:broader`, `skos:narrower`, `skos:related`.
- Відправляє JSONL-енvelop'и через `Bridge/bus_manager.py`.

### Interface Contract
- **Input:** `05_Knowledge_Aggregator/Intake_Queue/` — raw JSON-концепти, `bridge/in/core/` — нормалізовані тройки.
- **Output:** `05_Knowledge_Aggregator/bridge/out/` — валідовані моделі, `Bridge/messages.jsonl` — JSONL-повідомлення.
- **Channel rule:** Виключний доступ через локальний шлюз `bridge/in/` та `bridge/out/`.

## 9. Operational Protocol & Rules of Engagement (integrated from `AGGREGATOR_OPERATIONAL_PROTOCOL.md`)

### 1. Фундаментальний статус ШІ-Агрегатора
Ви є ШІ-Архітектором / ШІ-Оркестратором у середовищі Gemini Notebook.
- Ви НЕ маєте прямого доступу до файлової системи ПК.
- Ви не можете безпосередньо створювати, редагувати чи видаляти файли на диску.
- Усі фізичні дії на ПК виконує Клін (Cline) — автономний інженер у VS Code.

### 2. Протокол взаємодії "Блокнот ➔ Оператор ➔ Клін"
Будь-яка ваша дія з розгортання моделей, оновлення файлів чи створення JSON-драфтів відбуваються за суворим 3-етапним протоколом:
1. Генерація Директиви (Ваша дія): Ви формуєте для Користувача готовий текст Директиви для Кліна (у форматі Markdown) та готову Command для чату Кліна.
2. Передача (Дія Оператора): Користувач копіює вашу директиву у файл на диску `Bridge/in/aggregator/Cline_Directive_[НАЗВА].md` та відправляє команду Кліну у VS Code.
3. Виконання та Звіт (Дія Кліна): Клін виконує директиву на ПК, створює потрібні JSON/MD файли та викладає звіт у `Bridge/out/aggregator_reports/report_[НАЗВА]_[TIMESTAMP].md`.

### 3. Точні шляхи та правила каналу Aggregator
- Куди Клін має класти нові JSON-драфти знань: `05_Knowledge_Aggregator/Intake_Queue/`
- Куди ви відправляєте директиви для Кліна: `Bridge/in/aggregator/Cline_Directive_[НАЗВА].md`
- Звідки ви зчитуєте звіти Кліна (через додані джерела): `Bridge/out/aggregator_reports/`
- Заборонені дії: Ніколи не стверджуйте, що ви "зберегли файл на диск" чи "оновили стан системи". Ви лише створюєте ТЕКСТ ДИРЕКТИВИ для Кліна!

### 4. Шаблон форматування відповіді для Користувача
Коли ви хочете створити нову когнітивну модель чи оновити стан, ваша відповідь ЗАВЖДИ повинна мати такий формат:
1. Текст JSON-драфту (за шаблоном `INTAKE_TEMPLATES.md`)
2. Директива для Кліна (для збереження в `Bridge/in/aggregator/`)
3. Пряма команда для Кліна (для копіювання в чат VS Code)

## 10. System Readiness Checklist (integrated from `AGGREGATOR_CHECKLIST.md`)

#### Subsystem Scope & Target Directory
`C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`

#### 📋 Phase 1: Ingestion Infrastructure & Schema Audit
- [x] **Subsystem Isolation:** Dedicated `AGGREGATOR_STATE.md` initialized.
- [x] **Channel Architecture:** Sub-channels `Bridge/in/aggregator/` and `Bridge/out/aggregator_reports/` configured.
- [x] **Schema Contract Validation:** Upgraded `schema_validator.py` for W3C PROV-O and SKOS compliance across all 5 categories (cognitive_model, analogy, concept_scheme, image_metadata, video_index).
- [x] **Intake Handler Health Check:** Test run `intake_processor.py` on sample drafts to verify schema validation and RDF envelope conversion.

#### 📋 Phase 2: OSINT Data Stream Ingestion & Bus Inspection
- [x] **Message Bus Integration:** `bus_manager.py` implementing SHA256-keyed append-only logging to `Bridge/messages.jsonl`.
- [x] **Bus Integrity Inspection:** Deploy `bus_inspector.py` to audit SHA256 idempotency keys, timestamp ISO 8601 UTC compliance, and message payload schemas.
- [ ] **Raw Cognitive Models Intake:** Deposit and validate cognitive model drafts in `Intake_Queue/raw_cognitive_models/`.
- [ ] **Structural Analogies Intake:** Process cross-domain mapping schemes in `Intake_Queue/structural_analogies/`.
- [ ] **Conceptual Schemes Intake:** Maintain domain concepts in `Intake_Queue/conceptual_schemes/`.

#### 📋 Phase 3: Triple Normalization & Gate Output
- [ ] **RDF Envelope Verification:** Ensure output files in `Processed_Gate/normalized_triples/` carry `"status": "NORMALIZED"`.
- [ ] **Zero-Hallucination Audit:** Verify that 100% of generated triples trace back to valid intake sources.
- [ ] **Core Handoff Readiness:** Confirm normalized triples are formatted for seamless ingestion into `01_Formal_Core`.

#### 📋 Phase 4: Media & Multimodal Intake Infrastructure
- [x] **Media Schema Standards:** Created `image_metadata_template.json` and `video_index_template.json` under `Intake_Queue/templates/`.
- [ ] **Media Auto-Extractors:** Build local image metadata parser and video timestamp indexer under `05_Knowledge_Aggregator/media_extractors/`.
- [ ] **Cross-Media RDF Linking:** Enrich `intake_processor.py` to map visual keys and temporal chunks to formal RDF triples.

#### 📋 Phase 5: End-to-End Live Knowledge Ingestion
- [ ] **Sample Model Processing:** Ingest comprehensive multi-domain cognitive model with linked image and video metadata.
- [ ] **Zero-Hallucination Audit:** Verify 100% deterministic traceability from intake files to `Processed_Gate/normalized_triples/`.
- [ ] **Core Handoff Verification:** Validate RDF triples and message bus logs for ingestion by `01_Formal_Core`.

#### 📋 Phase 6: Execution & Logging
- [x] **Log Storage:** Record intake summary reports to `Bridge/out/aggregator_reports/`.
- [x] **Local Metrics Sync:** Maintain `AGGREGATOR_STATE.md` with local hardware and queue telemetry.

## 11. Local Node State & Metrics History (integrated from `AGGREGATOR_STATE.md`)

#### Governance & Local Constraints
*   **SCOPE:** `C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator`
*   **BUDGET_LIMIT:** $0.00 (Pure Open-Source & Local Hardware Execution)
*   **EXECUTION_MODE:** Stateless Autonomous Sessions
*   **ENGINEERING_STANDARD:** Production-Grade (Zero Hallucination / Validated Schemas)
*   **ROLES:** Knowledge Aggregator AI Architect, OSINT Pool Orchestrator, Intake Processor
**Header Metrics:** BUDGET: $0.00 | SESSION: Autonomous Clean State | STATUS: 🟢 Active Ingestion Gateway
**Last Updated:** 2026-11-08

#### Subsystem Architecture & Intake Status
| Queue / Directory | Assigned Role / Handler | Status | Primary Output / Format |
| ------ | ------ | ------ | ------ |
| Intake_Queue/raw_cognitive_models/ | Aggregator AI Architect | 🟢 Active | cognitive_model_template.json |
| Intake_Queue/structural_analogies/ | OSINT Pool Orchestrator | 🟢 Active | analogy_template.json |
| Intake_Queue/conceptual_schemes/ | OSINT Pool Orchestrator | 🟢 Active | concept_scheme_template.json |
| Processed_Gate/normalized_triples/ | intake_processor.py | 🟢 Active | Normalized RDF Triple Envelopes |

#### Isolated Communication Channels (Bridge Sub-channels)
*   **Directive Input Channel:** `Bridge/in/aggregator/` (Exclusive read access for Subsystem 05)
*   **Report Output Channel:** `Bridge/out/aggregator_reports/` (Exclusive write access for Subsystem 05 logs)
*   **Isolation Rule:** Reading from `Bridge/in/core/` and writing to `Bridge/out/execution_reports/` is prohibited to prevent context pollution with Core Engine Modules (01–04).

#### Downstream Contract with 01_Formal_Core
*   **Ingestion Pipeline:** `Intake_Queue/*` → `intake_processor.py` → `Processed_Gate/normalized_triples/` → `01_Formal_Core`.
*   **Validation Contract:**
    *   Entities: must contain `id`, `name`, `type`, `properties`.
    *   Relations: must contain `subject`, `predicate`, `object`.
    *   Analogies: must contain `source_element`, `target_element`, `relation_type`.
    *   Concept Schemes: must contain `scheme_id`, `title`, `keywords`, `concepts`.
    *   Zero-hallucination constraint: All entries must strictly trace back to input OSINT streams/drafts.

#### System Telemetry & Hardware Context
*   **Host OS:** Windows 11 Pro | **CPU:** AMD Ryzen 5 5625U | **RAM:** 16 GB DDR4
*   **Python:** 3.12.7 (rdflib, json, networkx, sympy)
*   **Local LLM Interface:** Ollama (`qwen2.5:7b` / `qwen2.5-coder:latest`)

#### Protocol for Subsystem Engineers
1. **Before Execution:** Read `05_Knowledge_Aggregator/AGGREGATOR_STATE.md` and local role instructions.
2. **After Execution:** Update `AGGREGATOR_STATE.md` and deposit execution report to `Bridge/out/aggregator_reports/report_[NAME]_[TIMESTAMP].md`.

### Phase 26: Pure Python Engine Core & Zero-Dependency Fallbacks (v3.5.0) — COMPLETE
**Status:** • Complete  **Date:** 2026-11-10  **Budget:** $0.00
- `01_Formal_Core/src/pure_tda_engine.py` — Vietoris-Rips H0/H1 Betti numbers
- `04_Discovery_Engine/src/pure_symbolic_engine.py` — AST/SymPy symbolic regression
- `05_Knowledge_Aggregator/src/pure_rdf_engine.py` — Native N-Triples/Turtle parser & serializer
- Verification: `py_compile` OK, all `--test` OK, E2E 4/4 OK
