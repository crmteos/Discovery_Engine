# 📘 NOTEBOOK PASSPORT — CORE (Node 01) — v3.5.0

## 1. Systemic Context & Architecture

| Attribute | Value |
|-----------|-------|
| **Node** | `01_Formal_Core` |
| **Roles** | `core.formal_engineer`, `core.bridge_engineer`, `core.tda_engineer` |
| **Notebook** | Gemini Notebook (Formal Core) |
| **System** | Discovery Engine Pipeline v3.5.0 |
| **Budget** | $0.00 (Local Execution, Real Math & Code) |
| **Message Bus** | `Bridge/messages.jsonl` (Universal Transactional JSONL Bus) |
| **Schema Dir** | `01_Formal_Core/schemas/shacl/` |
| **Companion** | `CONTEXT_DOMAIN_CORE.md` (Contextual Data Domain) |
| **Standard** | Notebook Context Standard — Control Plane (2-file notebook context) |

### 1.1 Notebook Context Standard (v3.5.0)

This notebook is the **Architectural Interface (Control Plane)** of Node 01. It governs SHACL shapes, the SymPy CAS Prover, and DSPy backtracking assertions. `CONTEXT_DOMAIN_CORE.md` holds the Data Plane: mathematical invariants, TDA Betti H0/H1 definitions, and ontology TTL base files.

### 1.2 Isolation Rule (v3.5.0)

- Node 01 exposes formal ontology contracts via `01_Formal_Core/src/01_Formal_Ontologies/`; all core sub-module code is encapsulated under `01_Formal_Core/src/`.
- Cross-node Python imports permitted only via manifest-registered paths under `01_Formal_Core/src/`.

## 2. Role Definition

### `core.formal_engineer`
- Ontologies RDF/OWL and knowledge graphs. SHACL shape validation (`schemas/shacl/core_universe_shapes.ttl`).
- Base ontologies: `universal_domain.ttl`, `universe_base.ttl`.

### `core.bridge_engineer`
- DSPy signatures and hallucination checking (`02_NeuroSymbolic_Bridge/dspy_signatures.py`, `Grounding_Validators/axiom_checker.py`).
- DSPy backtracking assertions enabled (`dspy_guardrails.backtracking: true`).

### `core.tda_engineer`
- Topological data analysis and gap detection (`04_Discovery_Engine/tda_gap_finder.py`).
- Vietoris-Rips TDA: homology dimensions H0, H1.

**Key Capabilities (from `system_manifest.json` v3.5.0):**
- `w3c_shacl`: enabled, `schema_dir`: `01_Formal_Core/schemas/shacl/`
- `dspy_guardrails`: enabled, backtracking: true
- `sympy_cas_prover`: enabled, canonical simplification: true
- `vietoris_rips_tda`: enabled, dimensions: H0, H1

## 3. Sub-Modules (encapsulated under `01_Formal_Core/src/`)

| Sub-module | Path | Role |
|------------|------|------|
| Formal Ontologies | `src/01_Formal_Ontologies/` | OWL/TTL/JSON-LD schemas & definitions |
| Knowledge Graphs | `src/Knowledge_Graphs/` | Graph DB schemas (NetworkX, RDF) |
| Symbolic AI | `src/Symbolic_AI/` | SymPy CAS Prover, invariant validation |
| Neuro-Symbolic Bridge | `src/02_NeuroSymbolic_Bridge/` | DSPy signatures, axiom checker, anythingllm bridge |
| Multimodal Interface | `src/03_Multimodal_Interface/` | Text/visual/media decoders |
| Discovery Engine | `src/04_Discovery_Engine/` | Topology, gap detection, novelty, symbolic regression |

## 4. Operational Standards

| Standard | Rule | Compliance Check |
|----------|------|------------------|
| **Budget** | $0.00 — pure local execution, zero mocks, real math | `py_compile` exit_code 0 |
| **SHACL** | W3C SHACL shapes validate RDF/OWL graphs | `shacl_validator.py` OK |
| **SymPy CAS** | Canonical simplification of invariants | `sympy_validator.validate_invariant` OK |
| **DSPy** | Backtracking assertions; hallucination checks | DSPy guardrails enabled |
| **TDA** | Vietoris-Rips homology H0/H1 | `tda_gap_finder.py` OK |

## 5. Compliance Checklist

- [ ] `py_compile` exit_code 0 on all core Python files
- [ ] `json.load()` on `system_manifest.json` PASSED
- [ ] SHACL shapes present under `schemas/shacl/`
- [ ] Ontology TTL base files present (`universal_domain.ttl`, `universe_base.ttl`)

### Phase 26: Pure Python Engine Core & Zero-Dependency Fallbacks (v3.5.0) — COMPLETE
**Status:** • Complete  **Date:** 2026-11-10  **Budget:** $0.00
- `01_Formal_Core/src/pure_tda_engine.py` — Vietoris-Rips H0/H1 Betti numbers
- `04_Discovery_Engine/src/pure_symbolic_engine.py` — AST/SymPy symbolic regression
- `05_Knowledge_Aggregator/src/pure_rdf_engine.py` — Native N-Triples/Turtle parser & serializer
- Verification: `py_compile` OK, all `--test` OK, E2E 4/4 OK
