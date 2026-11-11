# Master Directive: Transition to Universal Transactional Message Bus (v2.3.0)

**Target:** Execution Engineer (Cline)  
**Specification:** Universal File-Based JSONL Message Bus & N-Tier Communication Architecture  
**Budget Constraint:** $0.00 (Pure Open-Source & Local Hardware Stack)  
**Execution Mode:** Dynamic N-Tier Recursive Isolation with Centralized Message Sourcing  

---

## 🏛️ Executive Architectural Decision

Following the multi-agent research standards (FIPA-ACL, Event Sourcing, AutoGen v0.4, Agentic OS), the project transitions to a **single transactional message bus file: `Bridge/messages.jsonl`**.

### Key Rules:
1. **Clean Directory Trees:** Remove all nested `bridge/in` and `bridge/out` folders from sub-modules (`01_Formal_Core`, `05_Knowledge_Aggregator`, `06_Formalized_Model`). Sub-module folders must contain ONLY executable code (`src/`), ontologies/schemas (`schemas/`), and role instructions (`INSTRUCTIONS_ROLE.md`).
2. **Centralized Message Bus:** All inter-agent and cross-module communications (Vertical, Horizontal, Diagonal) must pass through append-only records in `Bridge/messages.jsonl`.
3. **Zero-Overhead Scaling:** Roles across any module can directly query or post requests to any other role using standardized role namespaces (`sender` -> `receiver`).

---

## 📋 Comprehensive Message Schema Specification (`Bridge/messages.jsonl`)

Every record in `Bridge/messages.jsonl` MUST be a single-line valid JSON object conforming to this schema:

```json
{
  "id": "msg_20261108_001",
  "timestamp": "2026-11-08T07:15:00Z",
  "communication_vector": "diagonal", 
  "sender": "core.tda_engineer",
  "receiver": "aggregator.osint_analyst",
  "performative": "data_clarification",
  "topic": "Refinement of topological gap boundary facts",
  "context_scope": "01_Formal_Core/src/04_Discovery_Engine",
  "in_reply_to": null,
  "payload": {
    "description": "TDA algorithm detected a 5-component topological gap in HYPOTHESIS_UNIFIED_CORE_001. Requesting targeted OSINT verification on node_04.",
    "schema_ref": "05_Knowledge_Aggregator/schemas/concept_scheme_template.json",
    "data_refs": [
      "05_Knowledge_Aggregator/Intake_Queue/normalized_smoke_test_concept_scheme.json"
    ],
    "constraints": {
      "budget": 0.0,
      "zero_hallucination": true
    }
  },
  "status": "pending",
  "result": {
    "exit_code": null,
    "report_ref": null,
    "response_payload": null
  }
}
```

### Protocol Fields Breakdown:
- **`communication_vector`**: 
  - `vertical`: Parent-Child / Hierarchy (e.g. `system.master_architect` <-> `aggregator.architect`)
  - `horizontal`: Peer-to-peer within same tier (e.g. `core.formal_engineer` <-> `core.tda_engineer`)
  - `diagonal`: Cross-module role request (e.g. `core.tda_engineer` <-> `aggregator.osint_analyst`)
  - `system`: Execution system event (e.g. `cline.executor` <-> `system.master_architect`)
- **`performative`** (FIPA-ACL communicative intent):
  - `task_request`: Assign work or ask for file execution
  - `query_refinement`: Request additional data or parameters
  - `data_clarification`: Resolve ambiguities in facts/triples
  - `hypothesis_submission`: Send newly discovered topological hypotheses
  - `validation_response`: Return verification status or RDF consistency check
  - `status_update`: Progress reporting
  - `error_report`: Runtime or validation failure alert
- **Role Namespace Registry**:
  - `system.master_architect`: Gemini Notebook 1 (Formal Core Architect)
  - `aggregator.architect`: Gemini Notebook 2 (Knowledge Aggregator Architect)
  - `aggregator.osint_analyst`: OSINT Analyst Pool
  - `core.formal_engineer`: Ontology & RDF Knowledge Graph Engineer
  - `core.bridge_engineer`: DSPy & Axiom Validator Engineer
  - `core.multimodal_engineer`: Multimodal Decoder Engineer
  - `core.tda_engineer`: TDA & Symbolic Discovery Engineer
  - `model.builder`: Gemini Notebook 3 (Target Model Engineer)
  - `cline.executor`: Local Execution Engineer (Cline CLI / Environment)
  - `user.operator`: Gateway Operator (User)

---

## 🛠️ Step-by-Step Execution Plan for Cline

### Step 1: Cleanup Nested Bridge Folders
- Safely remove empty nested bridge directories:
  - `01_Formal_Core/bridge/`
  - `05_Knowledge_Aggregator/bridge/`
  - `06_Formalized_Model/bridge/`
- Ensure root `Bridge/` folder remains active as the sole system gateway containing:
  - `Bridge/in/` (for manual operator directive drops)
  - `Bridge/out/` (for execution reports)
  - `Bridge/messages.jsonl` (universal transactional message bus)

### Step 2: Initialize Universal Message Bus (`Bridge/messages.jsonl`)
- Create `Bridge/messages.jsonl` if it does not exist.
- Append initial system setup record (`msg_system_init_v2.3.0`).

### Step 3: Implement Lightweight Python Helper (`Bridge/bus_manager.py`)
Create `Bridge/bus_manager.py` with helper functions:
- `post_message(sender, receiver, vector, performative, topic, payload, in_reply_to=None)` -> appends valid JSON line.
- `get_pending_messages(receiver_role=None)` -> returns list of pending messages.
- `update_message_status(msg_id, status, exit_code=0, report_ref=None, response_payload=None)`.
- Include CLI entry point for rapid command-line dispatch by Cline:
  `python Bridge/bus_manager.py --list-pending`

### Step 4: System Manifest & State Update
- Update `system_manifest.json` to **version 2.3.0**:
  - `isolation_standard`: `"Dynamic N-Tier Recursive Isolation with Universal Message Bus (v2.3.0)"`
  - `message_bus`: `"Bridge/messages.jsonl"`
  - Add `bus_manager`: `"Bridge/bus_manager.py"`
- Update `PROJECT_STATE.md` with milestone **Phase 12 — Universal JSONL Message Bus Standard Deployed**.

### Step 5: Verification & Smoke Test
1. Run `py_compile Bridge/bus_manager.py`.
2. Execute a smoke test using `bus_manager.py`:
   - Post a test diagonal message from `core.tda_engineer` to `aggregator.osint_analyst`.
   - Retrieve pending message via `--list-pending`.
   - Update message status to `completed`.
3. Verify `messages.jsonl` line formatting and syntax.
4. Save final execution report to `Bridge/out/execution_reports/report_message_bus_v2.3.0_[TIMESTAMP].md`.

---

**Execution Authorization:** Granted by System Master Architect. Proceed with refactoring immediately.
