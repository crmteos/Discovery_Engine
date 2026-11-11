# Cline Directive: System Passports & Dual-Node Governance Synchronization (v2.6.0)

**Target:** Execution Engineer (Cline)  
**System Version:** v2.6.0  
**Phase:** Phase 16 — Node Passports & Standards Synchronization  
**Budget Constraint:** $0.00 (Pure Open-Source & Local Hardware Stack)  
**Execution Mode:** Stateless Autonomous Session  

---

## 🎯 Executive Goal
Synchronize **Node 05 (Knowledge Aggregator)** and **Node 06 (Formalized Model)** with the v2.6.0 architecture standard (Google A2A, Anthropic MCP, Logic Spec-Driven Contracts, and Universal Message Bus `Bridge/messages.jsonl`). Institutionalize W3C PROV-O/SKOS standards for knowledge ingestion, and W3C OWL 2 DL / ISO 42010 for target model formalization.

---

## 🛠️ Execution Steps

### Step 1: Update Node 05 Governance (`05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_AGGREGATOR.md`)
Update or create `05_Knowledge_Aggregator/INSTRUCTIONS_ROLE_AGGREGATOR.md` with the following standards:
1. **W3C PROV-O (Provenance Protocol):** All ingested items must declare `prov:wasAttributedTo` (Agent ID), `prov:generatedAtTime` (ISO UTC), `prov:hadPrimarySource` (Source URL/Metadata), and `confidence_score` (0.0–1.0).
2. **W3C SKOS (Simple Knowledge Organization System):** Concept schemes must map terms via `skos:broader`, `skos:narrower`, and `skos:related`.
3. **Schema-Driven Ingestion Protocol:** All entries must pass `05_Knowledge_Aggregator/schema_validator.py` before submission.
4. **Message Bus Protocol:** All outgoing requests to Core (`core.formal_engineer`, `core.tda_engineer`) must be written directly to `Bridge/messages.jsonl` using the `bus_manager.py` tool.

### Step 2: Update Node 06 Governance (`06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md`)
Update or create `06_Formalized_Model/INSTRUCTIONS_ROLE_MODEL.md` with the following standards:
1. **W3C OWL 2 DL (Description Logic):** Target models must adhere to decidable Description Logic subsets, ensuring 0 contradictions (`owl:disjointWith`, `owl:equivalentClass`).
2. **ISO/IEC/IEEE 42010 & MBSE:** Models must express 3 architectural views:
   - **Structural View:** Entity relationships & taxonomy.
   - **Behavioral View:** Event transitions & message flows.
   - **Parametric View:** Mathematical invariants & SymPy constraints.
3. **Export Standards:** Support OpenAPI 3.1 schema generation and JSON-LD 1.1 semantic export.
4. **Message Bus Protocol:** Communication with Core and Aggregator routes strictly through `Bridge/messages.jsonl`.

### Step 3: Deploy Standalone Passport Files on Disk
Create two standalone passport documents:
1. `05_Knowledge_Aggregator/NOTEBOOK_PASSPORT_AGGREGATOR.md` — Complete system context, operational rules, role definition (`aggregator.architect`), and JSONL message templates for Gemini Notebook #2.
2. `06_Formalized_Model/NOTEBOOK_PASSPORT_MODEL.md` — Complete system context, operational rules, role definition (`model.builder`), and JSON-LD/OWL export specs for Gemini Notebook #3.

### Step 4: Update Central Manifest & System State
1. Update `system_manifest.json` (v2.6.0) to register the new node passport paths and standards (`prov_o`, `skos`, `owl_2_dl`, `iso_42010`).
2. Update `PROJECT_STATE.md` to record **Phase 16 Complete: System Passports & Dual-Node Governance Deployed**.

### Step 5: Verification & Execution Report
1. Run `py_compile` on all updated/new python files.
2. Validate `system_manifest.json` with `json.load()`.
3. Test `bus_manager.py` with a sample PROV-O validated message.
4. Save final execution report to `Bridge/out/execution_reports/report_system_passports_v2.6.0_[TIMESTAMP].md`.

---

## 🛑 Verification Criteria
- `exit_code: 0` for all compilation and test scripts.
- Zero budget spent ($0.00).
- Both passport files successfully created on disk.
