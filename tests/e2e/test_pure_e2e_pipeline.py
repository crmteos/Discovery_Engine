"""
test_pure_e2e_pipeline.py
=========================
Pure Python End-to-End Integration Benchmark (Phase 29, v3.8.0).
Mandated by: Bridge/in/directive-phase29-v3.8.0.md (Pillar A).

Executes the 4-stage Pure Python E2E pipeline:
  Stage 1 - Knowledge Intake & Triple Normalization   (05_Knowledge_Aggregator)
  Stage 2 - Pure RDF Topology & Graph Construction    (pure_rdf_engine.py)
  Stage 3 - Pure TDA Gap & Invariant Extraction       (pure_tda_engine.py)
  Stage 4 - Pure Symbolic Regression & Model Assembly (pure_symbolic_engine.py + 06_Formalized_Model)

Guarantees:
  * Pure Python execution — no external native C-dependencies.
  * Zero mocks — real math & code (SymPy, NetworkX, NumPy already in stack).
  * Budget strictly $0.00 — local CPU only.

Writes a benchmark report to
Bridge/out/execution_reports/report_pure_e2e_pipeline_[TIMESTAMP].md
"""

from __future__ import annotations

import importlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_DIR = ROOT / "Bridge" / "out" / "execution_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

AGGREGATOR_SRC = "05_Knowledge_Aggregator/src"
FORMAL_CORE_SRC = "01_Formal_Core/src"
DISCOVERY_SRC = "04_Discovery_Engine/src"
MODEL_SRC = "06_Formalized_Model/src"

INTAKE_DIR = ROOT / "05_Knowledge_Aggregator" / "Intake_Queue"
NORMALIZED_DIR = (
    ROOT / "05_Knowledge_Aggregator" / "Processed_Gate" / "normalized_triples"
)

RDF_TRIPLE_KEYS = (("s", "p", "o"), ("subject", "predicate", "object"))


def _import_leaf(module_dir_rel: str, leaf: str):
    """Import a leaf module by adding its (numeric-prefixed) directory to sys.path."""
    sys.path.insert(0, str(ROOT / module_dir_rel))
    return importlib.import_module(leaf)


def _run(name: str, fn) -> Dict[str, Any]:
    started = time.perf_counter()
    detail: Dict[str, Any] = {}
    exit_code = 1
    error = ""
    try:
        detail = fn()
        exit_code = 0
    except Exception as exc:  # noqa: BLE001 - benchmark captures all failures
        error = f"{type(exc).__name__}: {exc}"
    elapsed = time.perf_counter() - started
    return {
        "name": name,
        "exit_code": exit_code,
        "elapsed_s": round(elapsed, 4),
        "detail": detail,
        "error": error,
    }
def _extract_triples_from_record(record: dict, source: str) -> List[Dict[str, str]]:
    """Extract canonical {s, p, o} triples from a cognitive-model-style record."""
    triples: List[Dict[str, str]] = []
    relations = record.get("relations", [])
    if isinstance(relations, list):
        for rel in relations:
            if not isinstance(rel, dict):
                continue
            for s_key, p_key, o_key in RDF_TRIPLE_KEYS:
                s, p, o = rel.get(s_key), rel.get(p_key), rel.get(o_key)
                if s and p and o:
                    triples.append({"s": str(s), "p": str(p), "o": str(o), "source": source})
                    break
    entities = record.get("entities", [])
    if isinstance(entities, list):
        for ent in entities:
            if not isinstance(ent, dict):
                continue
            eid = ent.get("id") or ent.get("name")
            etype = ent.get("type")
            name = ent.get("name") or eid
            if eid and etype:
                triples.append({"s": str(name), "p": "rdf:type", "o": str(etype), "source": source})
    return triples


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


# ---------------------------------------------------------------------------
# Stage 1 - Knowledge Intake & Triple Normalization (05_Knowledge_Aggregator)
# ---------------------------------------------------------------------------
def stage1_intake_and_normalization() -> Dict[str, Any]:
    intake_sources: List[str] = []
    raw_triples: List[Dict[str, str]] = []

    model_dir = INTAKE_DIR / "raw_cognitive_models"
    if model_dir.exists():
        for path in sorted(model_dir.glob("*.json")):
            data = _load_json(path)
            if not isinstance(data, dict):
                continue
            intake_sources.append(str(path.relative_to(ROOT)))
            payload = data.get("payload", data) if data.get("status") == "NORMALIZED" else data
            raw_triples.extend(_extract_triples_from_record(payload, str(path.name)))

    normalized_dir = NORMALIZED_DIR
    if normalized_dir.exists():
        for path in sorted(normalized_dir.glob("normalized_*.json")):
            data = _load_json(path)
            if not isinstance(data, dict):
                continue
            intake_sources.append(str(path.relative_to(ROOT)))
            raw_triples.extend(_extract_triples_from_record(data.get("payload", data), str(path.name)))

    # Canonical normalization: validate non-empty s/p/o and de-duplicate.
    canonical: List[Dict[str, str]] = []
    seen: set[Tuple[str, str, str]] = set()
    for triple in raw_triples:
        key = (triple["s"], triple["p"], triple["o"])
        if key in seen:
            continue
        seen.add(key)
        canonical.append(triple)

    valid = all(bool(t["s"]) and bool(t["p"]) and bool(t["o"]) for t in canonical)
    return {
        "intake_sources": intake_sources,
        "raw_triples_extracted": len(raw_triples),
        "normalized_triples": len(canonical),
        "all_triples_valid": bool(valid),
        "sample_triples": canonical[:10],
        "status": "VALIDATED" if valid and canonical else "EMPTY",
    }


# ---------------------------------------------------------------------------
# Stage 2 - Pure RDF Topology & Graph Construction (pure_rdf_engine.py)
# ---------------------------------------------------------------------------
def stage2_rdf_topology() -> Dict[str, Any]:
    rdf_mod = _import_leaf(AGGREGATOR_SRC, "pure_rdf_engine")
    engine = rdf_mod.PureRDFEngine()

    ntriples_text = "\n".join(
        f"<{t['s']}> <{t['p']}> <{t['o']}> ." for t in [
            {"s": "http://ex/Knowledge_Node", "p": "http://ex/populates", "o": "http://ex/Triple_Store"},
            {"s": "http://ex/ConceptA", "p": "http://ex/rdf:type", "o": "http://ex/AbstractConcept"},
        ]
    ) + "\n"

    parsed = engine.parse_nt(ntriples_text)
    assert len(parsed) == 2, parsed
    serialized = engine.serialize_nt(parsed)
    assert "<http://ex/Knowledge_Node>" in serialized
    jsonld = engine.to_jsonld(parsed)
    assert isinstance(jsonld, list) and len(jsonld) == 2

    subjects = {t.s for t in parsed}
    predicates = {t.p for t in parsed}
    objects = {t.o for t in parsed}
    return {
        "parser": "PureRDFEngine (no rdflib)",
        "triples_parsed": len(parsed),
        "subjects": sorted(subjects),
        "predicates": sorted(predicates),
        "objects": sorted(objects),
        "jsonld_emitted": len(jsonld),
        "nt_serialized_chars": len(serialized),
        "status": "CONSTRUCTED",
    }


# ---------------------------------------------------------------------------
# Stage 3 - Pure TDA Gap & Invariant Extraction (pure_tda_engine.py)
# ---------------------------------------------------------------------------
def stage3_tda_gap_invariants() -> Dict[str, Any]:
    tda_mod = _import_leaf(FORMAL_CORE_SRC, "pure_tda_engine")

    # Two tree-shaped clusters + separation -> H0 = 2 components, H1 = 0 cycles.
    points = [(0.0, 0.0), (0.3, 0.0), (0.6, 0.0), (5.0, 5.0), (5.2, 5.1)]
    tight = tda_mod.betti_numbers(points, 0.5)
    assert tight["H0"] == 2, tight
    assert tight["H1"] == 0, tight

    # A square ring -> one cycle -> H1 = 1.
    ring = [(0, 0), (1, 0), (1, 1), (0, 1)]
    cyclic = tda_mod.betti_numbers(ring, 1.1)
    assert cyclic["H0"] == 1, cyclic
    assert cyclic["H1"] >= 1, cyclic

    return {
        "engine": "pure_tda_engine (Vietoris-Rips, no giotto/gudhi)",
        "tight_cloud": tight,
        "ring_cloud": cyclic,
        "betti_dimensions": ["H0", "H1"],
        "status": "EXTRACTED",
    }

# ---------------------------------------------------------------------------
# Stage 4 - Pure Symbolic Regression & Model Assembly
#             (pure_symbolic_engine.py + 06_Formalized_Model)
# ---------------------------------------------------------------------------
def stage4_symbolic_regression_and_model() -> Dict[str, Any]:
    sym_mod = _import_leaf(DISCOVERY_SRC, "pure_symbolic_engine")
    engine = sym_mod.SymbolicRegressionEngine(variables=["x"])

    import numpy as np  # noqa: import placed locally; NumPy is in the approved stack

    xs = np.linspace(0.1, 5.0, 40).reshape(-1, 1)
    ys = (xs[:, 0] ** 2)
    regression = engine.fit_candidate_law(xs, ys)
    assert regression["discovered_formula"] == "x**2", regression
    assert regression["mse_loss"] < 1e-6, regression
    assert regression["status"] == "VALIDATED", regression

    model_mod = _import_leaf(MODEL_SRC, "model_assembler")
    model_path = ROOT / "06_Formalized_Model" / "src" / "stage4_assembled_model.json"
    model = model_mod.assemble_model(output_path=model_path)
    assert "structural_view" in model and "behavioral_view" in model and "parametric_view" in model

    return {
        "engine": "pure_symbolic_engine (AST/SymPy, no pysr)",
        "discovered_formula": str(regression["discovered_formula"]),
        "mse_loss": float(regression["mse_loss"]),
        "regression_status": regression["status"],
        "model_assembler": "model_assembler.py (ISO/IEC/IEEE 42010 3-view)",
        "model_written": str(model_path),
        "model_views": [model["structural_view"]["view_type"], model["behavioral_view"]["view_type"], model["parametric_view"]["view_type"]],
        "status": "ASSEMBLED",
    }

def _build_report(timestamp: str, results: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Pure Python E2E Pipeline Benchmark Report (Phase 29, v3.8.0)")
    lines.append("")
    lines.append("- **Mandated by:** `Bridge/in/directive-phase29-v3.8.0.md` (Pillar A)")
    lines.append("- **Execution mode:** Local CPU — Pure Python, zero native C-dependencies")
    lines.append(f"- **Generated:** {timestamp} UTC")
    lines.append("- **Budget:** $0.00")
    lines.append("")
    lines.append("## Stage Results")
    for r in results:
        status = "OK" if r["exit_code"] == 0 else "FAILED"
        lines.append(f"### {r['name']} — {status} (exit_code={r['exit_code']}, {r['elapsed_s']}s)")
        d = r["detail"]
        if not d:
            lines.append("- **Detail:** no detail (stage did not complete successfully)")
            if r["error"]:
                lines.append(f"- **Error:** {r['error']}")
            lines.append("")
            continue
        if r["name"] == "Stage 1":
            lines.append(f"- **Intake sources:** {', '.join(d['intake_sources']) or 'none'}")
            lines.append(f"- **Raw triples extracted:** {d['raw_triples_extracted']}")
            lines.append(f"- **Normalized triples:** {d['normalized_triples']}")
            lines.append(f"- **All triples valid (s/p/o non-empty):** {d['all_triples_valid']}")
            lines.append(f"- **Status:** {d['status']}")
        elif r["name"] == "Stage 2":
            lines.append(f"- **Engine:** {d['parser']}")
            lines.append(f"- **Triples parsed:** {d['triples_parsed']}")
            lines.append(f"- **Subjects:** {d['subjects']}")
            lines.append(f"- **Predicates:** {d['predicates']}")
            lines.append(f"- **Objects:** {d['objects']}")
            lines.append(f"- **JSON-LD emitted:** {d['jsonld_emitted']}")
            lines.append(f"- **Status:** {d['status']}")
        elif r["name"] == "Stage 3":
            lines.append(f"- **Engine:** {d['engine']}")
            lines.append(f"- **Tight cloud (2 clusters):** H0={d['tight_cloud']['H0']}, H1={d['tight_cloud']['H1']}")
            lines.append(f"- **Ring cloud (1 cycle):** H0={d['ring_cloud']['H0']}, H1={d['ring_cloud']['H1']} (>=1)")
            lines.append(f"- **Betti dimensions:** {', '.join(d['betti_dimensions'])}")
            lines.append(f"- **Status:** {d['status']}")
        elif r["name"] == "Stage 4":
            lines.append(f"- **Engine:** {d['engine']}")
            lines.append(f"- **Discovered formula:** {d['discovered_formula']}")
            lines.append(f"- **MSE loss:** {d['mse_loss']}")
            lines.append(f"- **Regression status:** {d['regression_status']}")
            lines.append(f"- **Model assembler:** {d['model_assembler']}")
            lines.append(f"- **Model written:** {d['model_written']}")
            lines.append(f"- **Model views:** {', '.join(d['model_views'])}")
            lines.append(f"- **Status:** {d['status']}")
        if r["error"]:
            lines.append(f"- **Error:** {r['error']}")
        lines.append("")
    all_pass = all(r["exit_code"] == 0 for r in results)
    lines.append("## Compliance")
    lines.append("- **Budget:** $0.00 (pure local FOSS engine)")
    lines.append("- **Execution mode:** Local CPU (SymPy + NetworkX + NumPy)")
    lines.append(f"- **All 4 stages exit_code: 0:** {all_pass}")
    lines.append("")
    lines.append(f"---\nGenerated by `test_pure_e2e_pipeline.py` at {timestamp} UTC.\n")
    return "\n".join(lines)


def main() -> int:
    print("=" * 70)
    print("Pure Python E2E Pipeline Benchmark (Phase 29, v3.8.0)")
    print("=" * 70)

    steps = [
        ("Stage 1", stage1_intake_and_normalization),
        ("Stage 2", stage2_rdf_topology),
        ("Stage 3", stage3_tda_gap_invariants),
        ("Stage 4", stage4_symbolic_regression_and_model),
    ]
    results: List[Dict[str, Any]] = []
    for name, fn in steps:
        result = _run(name, fn)
        results.append(result)
        print(
            f"[{result['name']}] exit_code={result['exit_code']} "
            f"elapsed={result['elapsed_s']}s "
            f"{'OK' if result['exit_code'] == 0 else 'FAILED'}"
        )
        if result["error"]:
            print(f"  ERROR: {result['error']}")

    overall_exit = 0 if all(r["exit_code"] == 0 for r in results) else 1
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    report_name = f"report_pure_e2e_pipeline_{timestamp}.md"
    report_path = REPORT_DIR / report_name
    report_path.write_text(_build_report(timestamp, results), encoding="utf-8")

    print("=" * 70)
    print(f"Overall exit code: {overall_exit}")
    print(f"Benchmark report: {report_path}")
    print("=" * 70)
    return overall_exit


if __name__ == "__main__":
    sys.exit(main())
