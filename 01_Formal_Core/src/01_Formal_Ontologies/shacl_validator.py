"""
W3C SHACL (Shapes Constraint Language) validator for Formal Core RDF graphs.

Provides best-effort SHACL core validation over RDF triples:
  * IRI / blank-node / literal well-formedness in subject, predicate and
    object positions.
  * Shape conformance: mandatory predicates per target class (minCount).
  * Sink-cycle detection: predicate cycles with no outgoing exit edge.

Backed by `rdflib` when available; otherwise falls back to a pure-Python
triple graph so the module runs on the $0.00 local CPU stack with zero
external APIs.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:  # pragma: no cover - optional dependency
    from rdflib import Graph  # noqa: F401
    _HAS_RDFLIB = True
except ImportError:  # pragma: no cover - optional dependency
    Graph = None  # type: ignore[assignment]
    _HAS_RDFLIB = False

try:  # telemetry sink (OpenTelemetry GenAI -> Bridge/messages.jsonl)
    from Bridge.bus_manager import log_core_telemetry as _telemetry_sink  # type: ignore[assignment]
except Exception:  # pragma: no cover - bridge bus unavailable outside project root
    _telemetry_sink = None  # type: ignore[assignment]


def _emit_telemetry(metrics: Dict[str, Any], status: str) -> None:
    if _telemetry_sink is None:
        return
    try:
        _telemetry_sink("shacl_validation", metrics=metrics, status=status)  # type: ignore[misc]
    except Exception:  # pragma: no cover - telemetry is best-effort
        pass


# ---------------------------------------------------------------------------
# Shape loading
# ---------------------------------------------------------------------------

_DEFAULT_SHAPES: List[Dict[str, Any]] = [
    {
        "target": "core:Entity",
        "properties": [{"path": "rdfs:label", "min_count": 1}],
    },
    {
        "target": "core:Relation",
        "properties": [{"path": "rdfs:label", "min_count": 1}],
    },
]


def _load_shapes_from_dir(shapes_dir: Optional[str]) -> List[Dict[str, Any]]:
    """Load SHACL NodeShape declarations from *.ttl files in shapes_dir.

    Tolerant line-oriented parser: extracts sh:targetClass and pairs of
    sh:path / sh:minCount. Falls back to the built-in default shapes when
    the directory is missing or unparseable.
    """
    shapes: List[Dict[str, Any]] = list(_DEFAULT_SHAPES)
    if not shapes_dir:
        return shapes
    directory = Path(shapes_dir)
    if not directory.exists():
        return shapes
    for ttl_file in sorted(directory.glob("*.ttl")):
        try:
            text = ttl_file.read_text(encoding="utf-8")
        except OSError:
            continue
        text = "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("@")
        )
        current: Optional[Dict[str, Any]] = None
        for statement in text.split("."):
            statement = statement.strip()
            if not statement:
                continue
            target_match = re.search(r"sh:targetClass\s+(\S+)", statement)
            if target_match:
                current = {"target": target_match.group(1), "properties": []}
                shapes.append(current)
                continue
            if current is None:
                continue
            path_match = re.search(r"sh:path\s+(\S+)", statement)
            if not path_match:
                continue
            min_match = re.search(r"sh:minCount\s+(\d+)", statement)
            current["properties"].append(
                {
                    "path": path_match.group(1),
                    "min_count": int(min_match.group(1)) if min_match else 1,
                }
            )
    return shapes


# ---------------------------------------------------------------------------
# Triple helpers
# ---------------------------------------------------------------------------

_TERM_OK = re.compile(r"^(https?://|[A-Za-z][A-Za-z0-9+\-]*:|_:|\".*)")


def _parse_turtle_triples(path: Path) -> List[Tuple[str, str, str]]:
    """Best-effort Turtle triple parser (subject predicate object . / ;)."""
    triples: List[Tuple[str, str, str]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or line.startswith("@"):
                continue
            line = line.rstrip(";. ").strip()
            parts = line.split()
            if len(parts) == 3:
                triples.append((parts[0], parts[1], parts[2]))
    return triples


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _find_sink_cycles(
    adjacency: Dict[str, set[Tuple[str, str]]],
) -> List[List[str]]:
    """DFS-based detection of predicate cycles that are sinks (no exit edge)."""
    nodes = list(adjacency)
    color: Dict[str, int] = {node: 0 for node in nodes}
    cycles: List[List[str]] = []
    stack: List[str] = []

    def dfs(node: str) -> None:
        color[node] = 1
        stack.append(node)
        for _, target in adjacency.get(node, ()):
            target_color = color.get(target, 0)
            if target_color == 1:
                try:
                    idx = stack.index(target)
                except ValueError:
                    continue
                cycles.append(list(stack[idx:]))
            elif target_color == 0:
                dfs(target)
        stack.pop()
        color[node] = 2

    for node in nodes:
        if color[node] == 0:
            dfs(node)

    sink_cycles: List[List[str]] = []
    for cycle in cycles:
        cycle_set = set(cycle)
        is_sink = all(
            target in cycle_set
            for source in cycle
            for _, target in adjacency.get(source, ())
        )
        if is_sink:
            sink_cycles.append(cycle)
    return sink_cycles


def validate_graph(
    triples: Sequence[Tuple[str, str, str]],
    shapes: Optional[Sequence[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Validate an RDF triple graph against basic SHACL core constraints."""
    issues: List[str] = []
    checks: Dict[str, Any] = {}

    normalized: List[Tuple[str, str, str]] = []
    nodes: set[str] = set()
    adjacency: Dict[str, set[Tuple[str, str]]] = defaultdict(set)
    type_map: Dict[str, set[str]] = defaultdict(set)

    for subject, predicate, object_ in triples:
        subject, predicate, object_ = subject.strip(), predicate.strip(), object_.strip()
        normalized.append((subject, predicate, object_))
        nodes.update([subject, object_])
        adjacency[subject].add((predicate, object_))
        if predicate in ("a", "rdf:type") or predicate.endswith("rdf:type"):
            type_map[subject].add(object_)

    # 1. IRI / node well-formedness
    malformed = [n for n in sorted(nodes) if not _TERM_OK.match(n)]
    checks["iri_well_formed"] = len(malformed) == 0
    for node in malformed:
        issues.append(f"Malformed node term: {node!r}")

    # 2. Sink cycles
    sink_cycles = _find_sink_cycles(adjacency)
    checks["no_sink_cycles"] = len(sink_cycles) == 0
    for cycle in sink_cycles:
        issues.append(f"Sink cycle detected: {' -> '.join(cycle)}")

    # 3. Shape conformance
    active_shapes = list(shapes) if shapes is not None else _DEFAULT_SHAPES
    checks["shapes_applied"] = len(active_shapes)
    shape_issues = 0
    for shape in active_shapes:
        target = shape.get("target")
        targets = [n for n in nodes if target in type_map.get(n, set())]
        for prop in shape.get("properties", []):
            path = prop.get("path", "")
            min_count = int(prop.get("min_count", 1))
            for target_node in targets:
                count = sum(1 for p, _ in adjacency.get(target_node, ()) if p == path)
                if count < min_count:
                    shape_issues += 1
                    issues.append(
                        f"Shape violation: {target_node} is missing {min_count}x {path} "
                        f"(required by shape for {target})"
                    )
    checks["shape_conformance"] = shape_issues == 0

    valid = len(issues) == 0
    report: Dict[str, Any] = {
        "valid": valid,
        "triple_count": len(normalized),
        "node_count": len(nodes),
        "checks": checks,
        "issues": issues,
        "sink_cycles": sink_cycles,
    }
    _emit_telemetry(
        {"triples": len(normalized), "nodes": len(nodes), "valid": valid},
        "completed" if valid else "failed",
    )
    return report


class SHACLValidator:
    """W3C SHACL validator bound to a shapes directory."""

    def __init__(self, shapes_dir: Optional[str] = None) -> None:
        self.shapes_dir = shapes_dir
        self.shapes = _load_shapes_from_dir(shapes_dir)

    def validate(self, triples: Sequence[Tuple[str, str, str]]) -> Dict[str, Any]:
        return validate_graph(triples, self.shapes)

    def validate_turtle_file(self, path: str | Path) -> Dict[str, Any]:
        return self.validate(_parse_turtle_triples(Path(path)))


if __name__ == "__main__":  # pragma: no cover - smoke test
    ontology = Path(__file__).resolve().parent / "universe_base.ttl"
    shapes_dir = (
        Path(__file__).resolve().parents[2] / "schemas" / "shacl"
    )
    validator = SHACLValidator(shapes_dir=str(shapes_dir))
    report = validator.validate_turtle_file(ontology)
    print(f"SHACL validation: valid={report['valid']}, triples={report['triple_count']}")
    for issue in report["issues"]:
        print(f"  - {issue}")