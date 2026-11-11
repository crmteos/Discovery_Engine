# 📘 NOTEBOOK PASSPORT — DISCOVERY ENGINE (Node 04) — v3.5.0

## 1. Systemic Context

| Attribute | Value |
|-----------|-------|
| **Node** | `04_Discovery_Engine` |
| **Roles** | `discovery.tda_engineer`, `discovery.symbolic_engineer` |
| **Notebook** | Gemini Notebook (Formal Core) |
| **System** | Discovery Engine Pipeline v3.5.0 |
| **Budget** | $0.00 (Local Execution, Real Math & Code) |
| **Message Bus** | `Bridge/messages.jsonl` (Universal Transactional JSONL Bus) |
| **Engine** | Pure Python — no giotto-tda/gudhi/pysr/C++ compilers |

## 2. Role Definition

### `discovery.tda_engineer`
- Vietoris-Rips filtration and Betti numbers H0/H1.
- Protocol: `01_Formal_Core/src/pure_tda_engine.py --test` exit_code 0.

### `discovery.symbolic_engineer`
- AST/SymPy formula discovery and invariant fitting.
- Protocol: `04_Discovery_Engine/src/pure_symbolic_engine.py --test` exit_code 0.

## 3. Sub-Modules

| Sub-module | Path | Role |
|------------|------|------|
| Pure TDA Engine | `01_Formal_Core/src/pure_tda_engine.py` | H0/H1 computation |
| Pure Symbolic Engine | `04_Discovery_Engine/src/pure_symbolic_engine.py` | Formula discovery |
| Topological Gap Finder | `01_Formal_Core/src/04_Discovery_Engine/Topological_Data_Analysis/tda_gap_finder.py` | Structural gaps |

## 4. Operational Standards

| Standard | Rule | Compliance Check |
|----------|------|------------------|
| Budget | $0.00 — pure local execution | `py_compile` exit_code 0 |
| TDA | Pure Python Vietoris-Rips H0/H1 | `--test` exit_code 0 |
| Symbolic | Pure Python AST/SymPy regression | `--test` exit_code 0 |
| E2E | 4/4 stages pass | `test_e2e_pipeline.py` exit_code 0 |

## 5. Compliance Checklist

- [x] `py_compile` exit_code 0 on all core Python files
- [x] `json.load()` on `system_manifest.json` PASSED
- [x] E2E pipeline 4/4 exit_code 0
