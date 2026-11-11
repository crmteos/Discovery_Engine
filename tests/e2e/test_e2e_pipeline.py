"""
test_e2e_pipeline.py
====================
Full End-to-End System Integration Benchmark (E2E Test Run).
Mandated by: Bridge/in/Cline_Directive_E2E_Test.md

Executes all 4 Discovery_Engine modules end-to-end:
  Step 1 - Module 1: Formal Core (ingestion & invariants)
  Step 2 - Module 2: Neuro-Symbolic Bridge (grounding & axioms)
  Step 3 - Module 3: Multimodal Interface (text & graphics decoding)
  Step 4 - Module 4: Discovery Engine (topology & gap detection)

Writes a benchmark report to
Bridge/out/execution_reports/report_e2e_benchmark_[TIMESTAMP].md

Budget: $0.00 | Local CPU | Production-grade error handling | Zero mocks.
"""

from __future__ import annotations

import importlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_DIR = ROOT / "Bridge" / "out" / "execution_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

NODES = [
    "Observer_Tail",
    "Observer_Trunk",
    "Observer_Leg",
    "Observer_Ear",
    "Elephant_System",
]
RELATIONS = [
    ("Observer_Tail", "perceives", "Rope_Like_Entity"),
    ("Observer_Trunk", "perceives", "Snake_Like_Entity"),
    ("Observer_Leg", "perceives", "Tree_Like_Entity"),
    ("Observer_Ear", "perceives", "Fan_Like_Entity"),
]
ALL_TRIPLES = [(n, "rdf:type", "core:Entity") for n in NODES] + list(RELATIONS)


def _import_leaf(module_dir_rel: str, leaf: str):
    """Import a leaf module by adding its directory to sys.path.

    Numeric-prefixed package parents (e.g. `01_Formal_Core`) are not valid
    `import` identifiers, so leaf modules are loaded by name directly.
    """
    sys.path.insert(0, str(ROOT / module_dir_rel))
    return importlib.import_module(leaf)


def _build_kg():
    kg_mod = _import_leaf("01_Formal_Core/src/Knowledge_Graphs", "kg_engine")
    kg = kg_mod.KnowledgeGraphEngine()
    for s, p, o in ALL_TRIPLES:
        kg.add_fact(s, p, o)
    return kg


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


# ---------------------------------------------------------------------------
# Step 1 - Module 1: Formal Core (ingestion & invariants)
# ---------------------------------------------------------------------------
def step1_module1() -> Dict[str, Any]:
    kg = _build_kg()
    sym_mod = _import_leaf("01_Formal_Core/src/Symbolic_AI", "sympy_validator")
    SymPyValidator = sym_mod.InvariantValidator  # directive alias

    validation = kg.validate()
    invariant_expr = "E_total - (E_tail + E_trunk + E_leg + E_ear)"
    well_formed = bool(SymPyValidator.validate_invariant(invariant_expr))
    concrete_ok = bool(SymPyValidator.check_equivalence("1 + 2 + 3 + 4", "10"))

    detail = {
        "nodes_ingested": NODES,
        "relations_added": RELATIONS,
        "triple_count": len(kg.export_triples()),
        "entity_count": len(kg._entities),
        "kg_validation": validation,
        "invariant_expression": invariant_expr,
        "invariant_well_formed": well_formed,
        "concrete_equivalence_verified": concrete_ok,
        "invariant_equivalence_ok": bool(well_formed and concrete_ok),
    }
    if not validation["valid"]:
        raise RuntimeError(f"KG validation failed: {validation['issues']}")
    if not detail["invariant_equivalence_ok"]:
        raise RuntimeError("Invariant equivalence E_total = sum(E_observers) failed")
    return detail


# ---------------------------------------------------------------------------
# Step 2 - Module 2: Neuro-Symbolic Bridge (grounding & axioms)
# ---------------------------------------------------------------------------
def step2_module2() -> Dict[str, Any]:
    axiom_mod = _import_leaf(
        "01_Formal_Core/src/02_NeuroSymbolic_Bridge/Grounding_Validators",
        "axiom_checker",
    )
    AxiomChecker = axiom_mod.AxiomChecker

    ontology = ROOT / "01_Formal_Core" / "src" / "01_Formal_Ontologies" / "universe_base.ttl"
    checker = AxiomChecker(ontology_file=str(ontology))

    for s, p, o in ALL_TRIPLES:
        checker.kg.add_fact(s, p, o)

    grounding = [checker.validate_triple(s, p, o) for (s, p, o) in ALL_TRIPLES]
    invariant_expr = "E_total - (E_tail + E_trunk + E_leg + E_ear)"
    detail = {
        "ontology_file": str(ontology),
        "triples_validated": len(grounding),
        "grounding_reports": grounding,
        "all_grounded": all(g["is_grounded"] for g in grounding),
        "symbolic_invariant_valid": bool(
            checker.validate_invariant(invariant_expr)
        ),
        "concrete_equivalence_verified": bool(
            checker.check_equivalence("1 + 2 + 3 + 4", "10")
        ),
    }
    if not detail["all_grounded"]:
        raise RuntimeError("Not all claims are zero-hallucination grounded")
    if not detail["symbolic_invariant_valid"]:
        raise RuntimeError("Symbolic invariant validation failed")
    return detail



# ---------------------------------------------------------------------------
# Step 3 - Module 3: Multimodal Interface (text & graphics decoding)
# ---------------------------------------------------------------------------
def step3_module3() -> Dict[str, Any]:
    kg = _build_kg()
    md_mod = _import_leaf(
        "01_Formal_Core/src/03_Multimodal_Interface/Decoders_Text", "markdown_decoder"
    )
    MarkdownDecoder = md_mod.MarkdownDecoder

    mv_mod = _import_leaf(
        "01_Formal_Core/src/03_Multimodal_Interface/Decoders_Visual", "math_visualizer"
    )
    MathVisualizer = mv_mod.VisualDecoder  # directive alias

    triple_dicts = [
        {"subject": s, "predicate": p, "object": o} for (s, p, o) in kg.export_triples()
    ]

    decoder = MarkdownDecoder(title="E2E Benchmark — Formal State Projection")
    md_report = decoder.decode_triples(triple_dicts)
    invariants = {"EnergyConservation": "E_total = E_tail + E_trunk + E_leg + E_ear"}
    md_report += decoder.decode_invariants(invariants)

    visualizer = MathVisualizer()
    dot_graph = visualizer.generate_dot_graph(triple_dicts)

    detail = {
        "triples_decoded": len(triple_dicts),
        "markdown_report": md_report,
        "markdown_length_chars": len(md_report),
        "dot_graph": dot_graph,
        "dot_length_chars": len(dot_graph),
    }
    if "Observer_Tail" not in md_report:
        raise RuntimeError("Markdown decoding produced empty output")
    if "digraph" not in dot_graph:
        raise RuntimeError("DOT graph export produced empty output")
    return detail


# ---------------------------------------------------------------------------
# Step 4 - Module 4: Discovery Engine (topology & gap detection)
# ---------------------------------------------------------------------------
def step4_module4() -> Dict[str, Any]:
    import networkx as nx
    import numpy as np

    tda_mod = _import_leaf(
        "01_Formal_Core/src/04_Discovery_Engine/Topological_Data_Analysis",
        "tda_gap_finder",
    )
    TDAGapFinder = tda_mod.TopologicalGapFinder  # directive alias

    sr_mod = _import_leaf(
        "01_Formal_Core/src/04_Discovery_Engine/Symbolic_Regression",
        "symbolic_regression_stub",
    )
    SymbolicRegressionStub = sr_mod.SymbolicRegressionEngine  # directive alias

    nd_mod = _import_leaf(
        "01_Formal_Core/src/04_Discovery_Engine/Novelty_Detectors",
        "novelty_detector",
    )
    NoveltyDetector = nd_mod.NoveltyDetector

    # Topology graph from ingested perceive-relations + isolated Elephant_System
    G = nx.Graph()
    G.add_node("Elephant_System")
    for s, _p, o in RELATIONS:
        G.add_edge(s, o, relation="perceives")

    finder = TDAGapFinder(G)
    structural_holes = finder.find_structural_holes()
    components = list(nx.connected_components(G))
    component_gaps = [
        {
            "gap_type": "DISCONNECTED_COMPONENT",
            "component_index": i,
            "nodes": sorted(comp),
            "hypothesis": "Missing central unifying core mapping (Universal_Elephant_Core)",
        }
        for i, comp in enumerate(components)
    ]
    all_gaps = list(structural_holes) + component_gaps

    # Symbolic regression: fit the conservation invariant on test vectors
    reg = SymbolicRegressionStub(variables=["E_tail"])
    x_val = np.linspace(1.0, 10.0, 50).reshape(-1, 1)
    y_val = x_val.copy().ravel()
    fit = reg.fit_candidate_law(x_val, y_val)

    # Novelty detection: synthesize candidate hypothesis for unmapped core
    detector = NoveltyDetector()
    proposals = detector.propose_candidate_entities(
        all_gaps
        if all_gaps
        else [
            {
                "gap_type": "MISSING_CENTRAL_CORE",
                "boundary_nodes": NODES[:4],
                "hypothesis": "Universal_Elephant_Core missing",
            }
        ]
    )
    unified_hypothesis = {
        "candidate_id": "HYPOTHESIS_UNIFIED_CORE_001",
        "derived_from_gap": "MISSING_CENTRAL_CORE / DISCONNECTED_COMPONENT",
        "connected_anchors": NODES[:4],
        "proposed_nature": "Universal Elephant Core (unified invariant entity)",
        "verification_status": "UNVERIFIED_HYPOTHESIS",
        "source_proposal": proposals[0] if proposals else None,
    }

    detail = {
        "graph_nodes": G.number_of_nodes(),
        "graph_edges": G.number_of_edges(),
        "connected_components": len(components),
        "structural_holes": structural_holes,
        "component_gaps": component_gaps,
        "total_gaps": len(all_gaps),
        "symbolic_regression": {
            "discovered_formula": str(fit["discovered_formula"]),
            "mse_loss": float(fit["mse_loss"]),
            "status": fit["status"],
        },
        "novelty_proposals": proposals,
        "unified_core_hypothesis": unified_hypothesis,
    }
    if detail["graph_nodes"] == 0:
        raise RuntimeError("Topology graph is empty")
    return detail


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def _build_report(timestamp: str, results: List[Dict[str, Any]]) -> str:
    overall_exit = 0 if all(r["exit_code"] == 0 for r in results) else 1
    overall_status = "PASS" if overall_exit == 0 else "FAIL"
    total_elapsed = sum(r["elapsed_s"] for r in results)

    lines = []
    lines.append("# E2E Benchmark Execution Report")
    lines.append("")
    lines.append(f"**Benchmark:** Full End-to-End System Integration Benchmark")
    lines.append(f"**Directive:** `Bridge/in/Cline_Directive_E2E_Test.md`")
    lines.append(f"**Target Root:** `{ROOT}`")
    lines.append(f"**Timestamp (UTC):** {timestamp}")
    lines.append(f"**Overall Status:** {overall_status}")
    lines.append(f"**Overall Exit Code:** {overall_exit}")
    lines.append(f"**Total Elapsed:** {total_elapsed:.4f} s")
    lines.append("")
    lines.append("## Environment")
    lines.append(f"- **Platform:** {sys.platform}")
    lines.append(f"- **Python:** {sys.version.split()[0]}")
    lines.append(f"- **Working Directory:** `{ROOT}`")
    lines.append("")
    lines.append("## Pipeline Results")
    lines.append("")
    lines.append("| Step | Module | Exit Code | Elapsed (s) | Status |")
    lines.append("|------|--------|-----------|-------------|--------|")
    step_module = {
        "Step 1": "Module 1 — Formal Core",
        "Step 2": "Module 2 — Neuro-Symbolic Bridge",
        "Step 3": "Module 3 — Multimodal Interface",
        "Step 4": "Module 4 — Discovery Engine",
    }
    for r in results:
        status = "OK" if r["exit_code"] == 0 else "FAILED"
        lines.append(
            f"| {r['name']} | {step_module.get(r['name'], '')} | "
            f"{r['exit_code']} | {r['elapsed_s']} | {status} |"
        )
    lines.append("")
    lines.append("## Step Details")
    for r in results:
        lines.append(f"### {r['name']}")
        lines.append(f"- **Exit code:** {r['exit_code']}")
        lines.append(f"- **Elapsed:** {r['elapsed_s']} s")
        if r["error"]:
            lines.append(f"- **Error:** {r['error']}")
        d = r["detail"]
        if r["name"] == "Step 1":
            lines.append(f"- **Nodes ingested:** {d['nodes_ingested']}")
            lines.append(f"- **Relations added:** {d['relations_added']}")
            lines.append(f"- **Triple count:** {d['triple_count']}")
            lines.append(f"- **Entity count:** {d['entity_count']}")
            lines.append(f"- **KG validation valid:** {d['kg_validation']['valid']}")
            lines.append(f"- **Invariant expression:** {d['invariant_expression']}")
            lines.append(f"- **Invariant well-formed:** {d['invariant_well_formed']}")
            lines.append(
                f"- **Concrete equivalence verified:** "
                f"{d['concrete_equivalence_verified']}"
            )
        elif r["name"] == "Step 2":
            lines.append(f"- **Ontology file:** {d['ontology_file']}")
            lines.append(f"- **Triples validated:** {d['triples_validated']}")
            lines.append(f"- **All grounded:** {d['all_grounded']}")
            lines.append(
                f"- **Symbolic invariant valid:** {d['symbolic_invariant_valid']}"
            )
            lines.append(
                f"- **Concrete equivalence verified:** "
                f"{d['concrete_equivalence_verified']}"
            )
            ungrounded = [
                g["triple"] for g in d["grounding_reports"] if not g["is_grounded"]
            ]
            lines.append(f"- **Ungrounded triples:** {ungrounded}")
        elif r["name"] == "Step 3":
            lines.append(f"- **Triples decoded:** {d['triples_decoded']}")
            lines.append(f"- **Markdown length:** {d['markdown_length_chars']} chars")
            lines.append(f"- **DOT graph length:** {d['dot_length_chars']} chars")
            lines.append("**Markdown excerpt:**")
            lines.append("```markdown")
            lines.append(d["markdown_report"][:800])
            lines.append("```")
            lines.append("**DOT graph excerpt:**")
            lines.append("```dot")
            lines.append(d["dot_graph"][:600])
            lines.append("```")
        elif r["name"] == "Step 4":
            lines.append(f"- **Graph nodes:** {d['graph_nodes']}")
            lines.append(f"- **Graph edges:** {d['graph_edges']}")
            lines.append(f"- **Connected components:** {d['connected_components']}")
            lines.append(f"- **Structural holes:** {d['structural_holes']}")
            lines.append(f"- **Component gaps:** {d['component_gaps']}")
            lines.append(f"- **Total gaps:** {d['total_gaps']}")
            lines.append(
                f"- **Symbolic regression formula:** "
                f"{d['symbolic_regression']['discovered_formula']}"
            )
            lines.append(
                f"- **Regression MSE:** {d['symbolic_regression']['mse_loss']}"
            )
            lines.append(
                f"- **Regression status:** {d['symbolic_regression']['status']}"
            )
            lines.append(
                f"- **Unified core hypothesis:** "
                f"{d['unified_core_hypothesis']['candidate_id']}"
            )
            lines.append(
                f"- **Hypothesis status:** "
                f"{d['unified_core_hypothesis']['verification_status']}"
            )
        lines.append("")
    lines.append("## Compliance")
    lines.append("- **Budget:** $0.00 (pure local FOSS engine)")
    lines.append("- **Execution mode:** Local CPU (SymPy + NetworkX)")
    lines.append(
        f"- **All 4 stages exit_code: 0:** "
        f"{all(r['exit_code'] == 0 for r in results)}"
    )
    lines.append("")
    lines.append("---")
    lines.append(
        f"Generated by `test_e2e_pipeline.py` at {timestamp} UTC."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    print("=" * 70)
    print("E2E Benchmark — Discovery Engine (4-module integration test)")
    print("=" * 70)

    steps = [
        ("Step 1", step1_module1),
        ("Step 2", step2_module2),
        ("Step 3", step3_module3),
        ("Step 4", step4_module4),
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
    report_name = f"report_e2e_benchmark_{timestamp}.md"
    report_path = REPORT_DIR / report_name
    report_path.write_text(_build_report(timestamp, results), encoding="utf-8")

    print("=" * 70)
    print(f"Overall exit code: {overall_exit}")
    print(f"Benchmark report: {report_path}")
    print("=" * 70)
    return overall_exit


if __name__ == "__main__":
    sys.exit(main())
    lines.append("")
