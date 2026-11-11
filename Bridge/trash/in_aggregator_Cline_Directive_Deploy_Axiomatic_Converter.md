# Cline Directive: Deploy Axiomatic Converter & Axiomatic Invariants Transformer Role

## Objective
Deploy `axiomatic_converter.py` and the role specification `INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` under `05_Knowledge_Aggregator/`. This component sits strictly between `Zero-Hallucination Auditor` and `Knowledge Weaver`, responsible for translating human-centric anthropomorphic data (linear time, Euclidean 3D space, sensory metadata) into non-anthropomorphic formal invariant structures (Causal Sets, Posets, Categorical Morphisms, Topological Invariants) before graph weaving into `Processed_Gate/normalized_triples/`.

## Target Environment
- Workspace: `05_Knowledge_Aggregator/`
- Output Gate: `05_Knowledge_Aggregator/Processed_Gate/normalized_triples/`
- Role Specs: `05_Knowledge_Aggregator/roles/INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md`
- Code Script: `05_Knowledge_Aggregator/axiomatic_converter.py`
- Reports Directory: `Bridge/out/aggregator_reports/`

---

## Directives for Cline

### Step 1: Create Role Specification
Create `05_Knowledge_Aggregator/roles/INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` defining the responsibilities of the Axiomatic Invariants Transformer role:
- Identification of anthropomorphic cognitive artifacts (linear time $t$, Euclidean coordinates $x,y,z$, optical/sensory metaphors).
- Transformation of temporal-spatial continuum into Causal Order / Partial Order Graphs (Poset).
- Substitution of spatial coordinate bounds with Categorical Objects, Morphisms, and Topological Invariants.
- Guaranteeing zero data loss during axiom translation.

### Step 2: Implement `axiomatic_converter.py`
Create `05_Knowledge_Aggregator/axiomatic_converter.py`:
- Input: Verified raw drafts passed from `Zero-Hallucination Auditor`.
- Logic:
  1. Parse input JSON/RDF drafts for anthropomorphic markers (`timestamp`, `spatial_coordinates`, `human_perceptual_labels`).
  2. Map temporal sequences to `prov:wasInfluencedBy` and `prov:wasDerivedFrom` causal order chains.
  3. Map spatial metrics to `skos:related` topological vector relations.
  4. Generate de-anthropomorphized RDF triples output.
- Output: Pass clean invariant triples to `Knowledge Weaver` stage.

### Step 3: Update Main Pipeline Flow
Integrate `axiomatic_converter.py` into `agent_roles_orchestrator.py` between Stage 3 (Zero-Hallucination Auditor) and Stage 4 (Knowledge Weaver).

### Step 4: Verification and Bus Audit
- Execute `python 05_Knowledge_Aggregator/axiomatic_converter.py` smoke test.
- Run `python 05_Knowledge_Aggregator/bus_inspector.py` to ensure 0 errors.

### Step 5: Save Execution Report
Save execution report to `Bridge/out/aggregator_reports/report_axiomatic_converter_[TIMESTAMP].md`.

---

## Acceptance Criteria
1. Role spec `INSTRUCTIONS_ROLE_AXIOMATIC_TRANSFORMER.md` exists in `05_Knowledge_Aggregator/roles/`.
2. `axiomatic_converter.py` compiles with `exit_code: 0`.
3. Orchestration pipeline places the Axiomatic Converter strictly between Auditor and Knowledge Weaver.
4. `bus_inspector.py` passes with 0 errors.
5. Execution report generated under $0.00 budget limit.
