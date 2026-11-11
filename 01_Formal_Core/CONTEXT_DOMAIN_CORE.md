# 🗄️ CONTEXT DOMAIN — CORE (Node 01) — v2.9.0

## 1. Systemic Context & Data Domain

| Attribute | Value |
|-----------|-------|
| **Node** | `01_Formal_Core` |
| **Domain** | Mathematical invariants, TDA Betti H0/H1 definitions, ontology TTL base files |
| **Notebook** | Gemini Notebook (Formal Core) |
| **System** | Discovery Engine Pipeline v2.9.0 |
| **Budget** | $0.00 (Local Execution) |
| **Companion** | `NOTEBOOK_PASSPORT_CORE.md` (Architectural / Control Plane) |
| **Standard** | Notebook Context Standard — Data Plane (2-file notebook context) |

## 2. Purpose

This notebook is the **Contextual Data Domain (Data Plane)** of Node 01. It defines the mathematical invariants, topological data analysis (TDA) Betti number definitions, and the base ontology TTL files that constitute the formal mathematical core of the Discovery Engine.

## 3. Ontology Base Files (`src/01_Formal_Ontologies/`)

### `universal_domain.ttl`
Base OWL/TTL domain declarations for the universal concept universe. Declares core entity classes, concept schemes, and the PROV-O/SKOS alignment used across Node 01 → Node 05 → Node 06.

### `universe_base.ttl`
Foundational universe axioms: entity taxonomy, relation vocabulary, and disjointness/equivalence constraints (`owl:disjointWith`, `owl:equivalentClass`).

### SHACL Shapes (`schemas/shacl/core_universe_shapes.ttl`)
W3C SHACL shapes constraining the shape of RDF graphs ingested into the core: node shapes, property constraints, cardinality, and datatype restrictions.

## 4. Mathematical Invariants (SymPy CAS Prover)

| Invariant | Domain | Verification |
|-----------|--------|--------------|
| `E_total - (E_tail + E_trunk + E_leg + E_ear)` | Knowledge graph conservation | `sympy_validator.validate_invariant` |
| `1 + 2 + 3 + 4 == 10` | Equivalence check | `sympy_validator.check_equivalence` |

Invariants are validated by `sympy_cas_prover.py` with canonical simplification enabled.

## 5. TDA — Vietoris-Rips Homology

| Dimension | Meaning | Use |
|-----------|---------|-----|
| **H0** | Connected components | Graph connectivity / gap detection |
| **H1** | 1-dimensional holes (cycles) | Structural hole / loop detection |

Implemented in `04_Discovery_Engine/tda_gap_finder.py` and `novelty_detector.py`. Outputs: graph nodes/edges, connected components, structural holes, component gaps.

## 6. Data Flow into Core

```
Normalized triples (Node 05)
    → bridge/in → schema validation (SHACL)
    → Knowledge Graph Engine (kg_engine.add_fact)
    → Invariant validation (SymPy CAS Prover)
    → TDA gap detection (H0/H1)
    → DSPy backtracking assertions / hallucination check
    → Formal ontology contracts exposed to Node 06
```

## 7. Compliance Checklist

- [ ] Ontology TTL base files present (`universal_domain.ttl`, `universe_base.ttl`)
- [ ] SHACL shapes present under `schemas/shacl/core_universe_shapes.ttl`
- [ ] SymPy CAS Prover invariants validate (exit_code 0)
- [ ] TDA homology dimensions H0, H1 configured