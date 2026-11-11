# Directive: Deploy Advanced Multi-Agent Roles in 05_Knowledge_Aggregator

**Target Subsystem:** `05_Knowledge_Aggregator`  
**Execution Context:** Local execution only ($0.00 budget)  
**Architecture Patterns:** Hub-and-Spoke Orchestrator, A2A Protocol, MCP Tooling, Maker-Checker Quality Gate  

---

### 📋 Objective
Deploy specifications and operational handler scripts for 4 specialized AI Agent roles:
1. **Wide Discovery Agent (Zoom Out)** — Broad contextual query expander & ranked link indexer.
2. **Narrow Extractor Agent (Zoom In)** — Deep multi-format context harvester (web, PDF, media).
3. **Zero-Hallucination Auditor (Maker-Checker)** — Adversarial factual verifier measuring semantic drift.
4. **Knowledge Weaver (Graph Synthesizer)** — Cross-domain SKOS/PROV-O graph consolidator.

---

### 🛠️ Execution Steps

#### Step 1: Create Role Specification Files
Create the following role instruction markdown files under `05_Knowledge_Aggregator/roles/`:

1. `INSTRUCTIONS_ROLE_WIDE_DISCOVERY.md`:
   - Inputs: Queries/hypotheses from Formal Core.
   - Operations: Query expansion, candidate retrieval, coherence scoring using `similarity_analyzer.py` (Mode A/B).
   - Outputs: `link_index.json` (ranked by coherence score).

2. `INSTRUCTIONS_ROLE_NARROW_EXTRACTOR.md`:
   - Inputs: Specific target from `link_index.json`.
   - Operations: Deep parsing via `media_extractors/`, HTML/PDF extraction, RDF normalization.
   - Outputs: `Intake_Queue/` drafts and normalized RDF triples.

3. `INSTRUCTIONS_ROLE_ZERO_HALLUCINATION_AUDITOR.md`:
   - Inputs: Generated RDF triples vs. raw source text.
   - Operations: Semantic drift audit, vector alignment verification (`similarity_analyzer.py` threshold >= 0.85).
   - Outputs: Audit certificate in `Bridge/messages.jsonl` with `exit_code: 0`.

4. `INSTRUCTIONS_ROLE_KNOWLEDGE_WEAVER.md`:
   - Inputs: Processed RDF triples from `Processed_Gate/normalized_triples/`.
   - Operations: Cross-domain `skos:broader`, `skos:narrower`, and `skos:related` graph consolidation.
   - Outputs: Consolidated global graph schema.

#### Step 2: Implement Orchestration Handler
Create `05_Knowledge_Aggregator/agent_roles_orchestrator.py`:
- Implement class stubs and routing logic for each of the 4 roles.
- Ensure integration with `bus_manager.py` for A2A event logging.
- Verify syntax and run smoke test.

#### Step 3: Run Audit & Generate Report
- Execute `python 05_Knowledge_Aggregator/agent_roles_orchestrator.py`
- Run `python 05_Knowledge_Aggregator/bus_inspector.py`
- Save report to `Bridge/out/aggregator_reports/report_multi_agent_roles_[TIMESTAMP].md`

---

### 🔍 Acceptance Criteria
- [ ] All 4 role specification files created in `05_Knowledge_Aggregator/roles/`.
- [ ] `agent_roles_orchestrator.py` compiles with `exit_code: 0`.
- [ ] `bus_inspector.py` verifies 0 errors in transactional logs.
- [ ] Report saved to `Bridge/out/aggregator_reports/report_multi_agent_roles_[TIMESTAMP].md`.
- [ ] Cost strictly maintained at **$0.00**.
