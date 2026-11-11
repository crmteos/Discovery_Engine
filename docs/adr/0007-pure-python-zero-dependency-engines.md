---
title: ADR-0007 — Pure Python Zero-Dependency Engines
status: accepted
date: 2026-11-10
deciders: system.master_architect, cline.executor
consulted: 01_Formal_Core, 04_Discovery_Engine, 05_Knowledge_Aggregator
considered: rdflib, giotto-tda, gudhi, pysr, ollama
---

# ADR-0007 — Pure Python Zero-Dependency Engines

## Context

The system runs in an isolated zero-dollar budget environment without an external C/C++ compiler or guaranteed preinstalled Python packages. Required semantic and topological capabilities were previously bound to `rdflib`, `giotto-tda`, `gudhi`, and `pysr`/C++ backends, which are not guaranteed on client hardware.

## Decision

Introduce three native Pure Python engines and remove heavy external dependencies:

1. `05_Knowledge_Aggregator/src/pure_rdf_engine.py` — N-Triples/Turtle parsing, validation, and serialization without `rdflib`.
2. `01_Formal_Core/src/pure_tda_engine.py` — Vietoris-Rips filtration and exact Betti numbers H0/H1 without `giotto-tda` or `gudhi`.
3. `04_Discovery_Engine/src/pure_symbolic_engine.py` — AST and SymPy formula discovery without `pysr` or compiled backends.

The codebase continues to use only Python standard library plus SymPy/NetworkX for symbolic and graph math. Existing integration points (`--test` CLI, JSON-LD/N-Triples formats, and the E2E pipeline `tests/e2e/test_e2e_pipeline.py`) were preserved by keeping backward-compatible aliases and copied modules under `01_Formal_Core/src/04_Discovery_Engine/...`.

## Consequences

- The pipeline is fully offline/zero-dependency for graph and symbolic math.
- All three engines expose a `--test` mode for deterministic assertions.
- `py_compile` and `tests/e2e/test_e2e_pipeline.py` must pass on every supported platform.
- Core manifests (`system_manifest.json`, `PROJECT_STATE.md`) and node passports are updated to `v3.5.0`.
