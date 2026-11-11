# TASK DIRECTIVE: Deploy Aggregator Local State & Rebind Operational Context
**Target Subsystem:** C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator
**Sender:** System Architect / OSINT Orchestrator (Gemini Notebook)
**Executor:** Cline (VS Code Infrastructure Engineer)
**Protocol Standard:** AGGREGATOR_OPERATIONAL_PROTOCOL.md
**Budget Constraint:** $0.00 (Pure Local Execution)

--------------------------------------------------------------------------------

#### 🎯 Executive Objective
1. Initialize a dedicated `AGGREGATOR_STATE.md` file within `05_Knowledge_Aggregator/` to completely isolate the context of Subsystem 05 from the global Discovery_Engine state.
2. Update role instructions (`INSTRUCTIONS_ROLE_ARCHITECT.md` and `INSTRUCTIONS_ROLE_ORCHESTRATOR.md`) to reference `AGGREGATOR_STATE.md` instead of `PROJECT_STATE.md`.
3. Confirm operational channel alignment (`Bridge/in/aggregator/` and `Bridge/out/aggregator_reports/`).

--------------------------------------------------------------------------------

#### 🛠️ Step-by-Step Execution Tasks

##### Task 1: Initialize AGGREGATOR_STATE.md
Create the file `05_Knowledge_Aggregator/AGGREGATOR_STATE.md` with the following initial content:

```markdown
# 05_Knowledge_Aggregator — Subsystem Master State
#### Governance & Local Constraints
*   **SCOPE:** C:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\05_Knowledge_Aggregator
*   **BUDGET_LIMIT:** $0.00 (Pure Open-Source & Local Hardware Execution)
*   **EXECUTION_MODE:** Stateless Autonomous Sessions
*   **ENGINEERING_STANDARD:** Production-Grade (Zero Hallucination / Validated Schemas)
*   **ROLES:** Knowledge Aggregator AI Architect, OSINT Pool Orchestrator, Intake Processor
**Header Metrics:** BUDGET: $0.00 | SESSION: Autonomous Clean State | STATUS: 🟢 Active Ingestion Gateway
**Last Updated:** 2026-11-08

--------------------------------------------------------------------------------

#### Subsystem Architecture & Intake Status
| Queue / Directory | Assigned Role / Handler | Status | Primary Output / Format |
| ------ | ------ | ------ | ------ |
| Intake_Queue/raw_cognitive_models/ | Aggregator AI Architect | 🟢 Active | cognitive_model_template.json |
| Intake_Queue/structural_analogies/ | OSINT Pool Orchestrator | 🟢 Active | analogy_template.json |
| Intake_Queue/conceptual_schemes/ | OSINT Pool Orchestrator | 🟢 Active | concept_scheme_template.json |
| Processed_Gate/normalized_triples/ | intake_processor.py | 🟢 Active | Normalized RDF Triple Envelopes |

--------------------------------------------------------------------------------

#### Isolated Communication Channels (Bridge Sub-channels)
*   **Directive Input Channel:** `Bridge/in/aggregator/` (Exclusive read access for Subsystem 05)
*   **Report Output Channel:** `Bridge/out/aggregator_reports/` (Exclusive write access for Subsystem 05 logs)
*   **Isolation Rule:** Reading from `Bridge/in/core/` and writing to `Bridge/out/execution_reports/` is prohibited to prevent context pollution with Core Engine Modules (01–04).

--------------------------------------------------------------------------------

#### Downstream Contract with 01_Formal_Core
*   **Ingestion Pipeline:** `Intake_Queue/*` → `intake_processor.py` → `Processed_Gate/normalized_triples/` → `01_Formal_Core`.
*   **Validation Contract:**
    *   Entities: must contain `id`, `name`, `type`, `properties`.
    *   Relations: must contain `subject`, `predicate`, `object`.
    *   Analogies: must contain `source_element`, `target_element`, `relation_type`.
    *   Concept Schemes: must contain `scheme_id`, `title`, `keywords`, `concepts`.
    *   Zero-hallucination constraint: All entries must strictly trace back to input OSINT streams/drafts.

--------------------------------------------------------------------------------

#### System Telemetry & Hardware Context
*   **Host OS:** Windows 11 Pro | **CPU:** AMD Ryzen 5 5625U | **RAM:** 16 GB DDR4
*   **Python:** 3.12.7 (rdflib, json, networkx, sympy)
*   **Local LLM Interface:** Ollama (`qwen2.5:7b` / `qwen2.5-coder:latest`)

--------------------------------------------------------------------------------

#### Protocol for Subsystem Engineers
1. **Before Execution:** Read `05_Knowledge_Aggregator/AGGREGATOR_STATE.md` and local role instructions.
2. **After Execution:** Update `AGGREGATOR_STATE.md` and deposit execution report to `Bridge/out/aggregator_reports/report_[NAME]_[TIMESTAMP].md`.
```

##### Task 2: Rebind Role Instructions Context
1. Update `05_Knowledge_Aggregator/Architect/INSTRUCTIONS_ROLE_ARCHITECT.md`:
   - Replace state loading reference `PROJECT_STATE.md` with `05_Knowledge_Aggregator/AGGREGATOR_STATE.md`.
   - Set input directive channel to `Bridge/in/aggregator/`.
   - Set output report channel to `Bridge/out/aggregator_reports/`.
2. Update `05_Knowledge_Aggregator/OSINT_Orchestrator/INSTRUCTIONS_ROLE_ORCHESTRATOR.md`:
   - Replace state loading reference `PROJECT_STATE.md` with `05_Knowledge_Aggregator/AGGREGATOR_STATE.md`.
   - Set input directive channel to `Bridge/in/aggregator/`.
   - Set output report channel to `Bridge/out/aggregator_reports/`.

##### Task 3: Intake Processor Verification & Execution Logging
1. Verify `05_Knowledge_Aggregator/intake_processor.py` execution via `python -m py_compile 05_Knowledge_Aggregator/intake_processor.py`.
2. Generate execution report and save to `Bridge/out/aggregator_reports/report_state_isolation_[TIMESTAMP].md`.

--------------------------------------------------------------------------------

#### 🔍 Verification & Compliance Checklist
* [ ] `05_Knowledge_Aggregator/AGGREGATOR_STATE.md` created and populated.
* [ ] Role instruction files updated to point to `AGGREGATOR_STATE.md`.
* [ ] No references to `Bridge/in/core/` or `Bridge/out/execution_reports/` in Aggregator instructions.
* [ ] `intake_processor.py` exits with code 0.
* [ ] Report saved in `Bridge/out/aggregator_reports/`.
