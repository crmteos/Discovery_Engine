"""
Zero-Hallucination Axiom Checker.

Validates LLM-generated triples against Formal Core Ontologies
(01_Formal_Core) and SymPy invariants, ensuring every derived statement
is grounded before it leaves the Neuro-Symbolic Bridge.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:  # pragma: no cover - optional dependency
    import dspy
    _HAS_DSPY = True
except ImportError:  # pragma: no cover - optional dependency
    dspy = None  # type: ignore[assignment]
    _HAS_DSPY = False

_DSPY_HAS_ASSERT = _HAS_DSPY and hasattr(dspy, "Assert")

try:  # telemetry sink (OpenTelemetry GenAI -> Bridge/messages.jsonl)
    from Bridge.bus_manager import log_core_telemetry as _telemetry_sink  # type: ignore[assignment]
except Exception:  # pragma: no cover - bridge bus unavailable outside project root
    _telemetry_sink = None  # type: ignore[assignment]


def _emit_telemetry(step_name: str, metrics: Dict[str, Any], status: str) -> None:
    if _telemetry_sink is None:
        return
    try:
        _telemetry_sink(step_name, metrics=metrics, status=status)  # type: ignore[misc]
    except Exception:  # pragma: no cover - telemetry is best-effort
        pass


# Add Formal_Core to import path
# __file__: .../01_Formal_Core/src/02_NeuroSymbolic_Bridge/Grounding_Validators/axiom_checker.py
# parents[2] -> 01_Formal_Core/src (Knowledge_Graphs & Symbolic_AI now live under src/)
formal_core_path = Path(__file__).resolve().parents[2]
sys.path.append(str(formal_core_path))

from Knowledge_Graphs.kg_engine import KnowledgeGraphEngine  # noqa: E402
from Symbolic_AI.sympy_validator import InvariantValidator  # noqa: E402

CORE_NAMESPACE = "http://discovery.engine/core#"
CORE_PREFIX = "core:"


class AxiomChecker:
    """Automated zero-hallucination validator for LLM-generated statements."""

    def __init__(self, ontology_file: Optional[str] = None) -> None:
        self.kg = KnowledgeGraphEngine()
        self.validator = InvariantValidator()
        if ontology_file and Path(ontology_file).exists():
            self.load_ontology(ontology_file)

    # ------------------------------------------------------------------
    # Ontology loading
    # ------------------------------------------------------------------
    def load_ontology(self, ontology_file: str) -> None:
        """Load core triples from a Turtle ontology file (best-effort parser)."""
        path = Path(ontology_file)
        if not path.exists():
            raise FileNotFoundError(f"Ontology file not found: {ontology_file}")
        with path.open("r", encoding="utf-8") as fh:
            for raw_line in fh:
                line = raw_line.strip()
                if not line or line.startswith("#") or line.startswith("@"):
                    continue
                if line.endswith(";"):
                    line = line[:-1].strip()
                if line.endswith("."):
                    line = line[:-1].strip()
                parts = line.split()
                if len(parts) == 3 and all(not p.startswith("@") for p in parts):
                    self.kg.add_fact(parts[0], parts[1], parts[2])

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def normalize_iri(self, term: str) -> str:
        """Expand a short core: prefixed term to its full IRI."""
        term = term.strip()
        if term.startswith(CORE_PREFIX):
            return f"{CORE_NAMESPACE}{term[len(CORE_PREFIX):]}"
        if term.startswith("http://") or term.startswith("https://"):
            return term
        return f"{CORE_NAMESPACE}{term}"

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_triple(self, s: str, p: str, o: str) -> Dict[str, Any]:
        """
        Checks if a triple exists or is logically consistent with the Formal Core.

        Returns a report dict with the triple, grounding flag, and status.
        """
        s_raw, p_raw, o_raw = s.strip(), p.strip(), o.strip()
        s_n = self.normalize_iri(s_raw)
        p_n = self.normalize_iri(p_raw)
        o_n = self.normalize_iri(o_raw)

        # Direct presence in the Formal Core knowledge graph.
        # Compare canonical normalized IRIs so both short prefixed form
        # (core:Energy) and full IRI form match stored triples.
        direct = any(
            (
                self.normalize_iri(ss),
                self.normalize_iri(pp),
                self.normalize_iri(oo),
            )
            == (s_n, p_n, o_n)
            for ss, pp, oo in self.kg.triples
        )

        # Symmetric-property consistency (e.g. core:isEquivalentTo)
        symmetric = False
        if p_n.endswith("isEquivalentTo") or p_raw.endswith("isEquivalentTo"):
            symmetric = (
                (o_n, p_n, s_n) in self.kg.triples
                or (o_raw, p_raw, s_raw) in self.kg.triples
            )

        is_grounded = bool(direct or symmetric)
        return {
            "triple": (s_raw, p_raw, o_raw),
            "normalized_triple": (s_n, p_n, o_n),
            "direct_match": bool(direct),
            "symmetric_consistent": bool(symmetric),
            "is_grounded": is_grounded,
            "status": "VALIDATED" if is_grounded else "UNGROUNDED_HYPOTHESIS",
        }

    def validate_invariant(self, expression_str: str) -> bool:
        """Delegates symbolic invariant validation to SymPy InvariantValidator."""
        return bool(self.validator.validate_invariant(expression_str))

    def check_equivalence(self, expr1_str: str, expr2_str: str) -> bool:
        """Checks symbolic equivalence of two expressions via SymPy."""
        return bool(self.validator.check_equivalence(expr1_str, expr2_str))

    # ------------------------------------------------------------------
    # DSPy Assert guardrails with backtracking hints
    # ------------------------------------------------------------------
    def assert_axiom(
        self,
        condition: bool,
        message: str,
        axiom_ref: Optional[str] = None,
    ) -> Dict[str, Any]:
        """dspy.Assert()-compatible guardrail for logical conditions.

        Delegates to dspy.Assert() when DSPy is installed, otherwise falls
        back to a plain Python boolean check. On failure, emits
        backtracking hints derived from the loaded universe_base.ttl axioms.
        """
        passed = bool(condition)
        report: Dict[str, Any] = {
            "condition": passed,
            "message": message,
            "axiom_ref": axiom_ref,
            "passed": passed,
            "dspy_used": _HAS_DSPY,
        }
        if _DSPY_HAS_ASSERT:
            try:
                dspy.Assert(bool(condition), message)  # type: ignore[attr-defined]
                report["passed"] = True
            except Exception as exc:  # noqa: BLE001 - guardrail reports failures
                passed = False
                report["passed"] = False
                report["dspy_error"] = str(exc)
        if not passed:
            report["backtracking_hints"] = self.backtracking_hints(message)
        _emit_telemetry(
            "axiom_assertion",
            {"passed": passed, "axiom_ref": axiom_ref},
            "completed" if passed else "failed",
        )
        return report

    def backtracking_hints(self, proposition: str) -> List[str]:
        """Automatic hinting: suggest alternative axioms from the core ontology."""
        hints: List[str] = []
        proposition = proposition.strip()
        lowered = proposition.lower()
        seen: set[str] = set()
        for subject, predicate, object_ in self.kg.triples:
            for term in (subject, object_):
                if lowered in term.lower() or term.lower() in lowered:
                    for s2, p2, o2 in self.kg.triples:
                        if s2 == term and p2 != predicate:
                            hint = f"Alternative axiom: {s2} {p2} {o2}"
                            if hint not in seen:
                                seen.add(hint)
                                hints.append(hint)
                        if o2 == term and p2 != predicate:
                            hint = f"Alternative axiom (inverse): {s2} {p2} {o2}"
                            if hint not in seen:
                                seen.add(hint)
                                hints.append(hint)
        if not hints:
            hints.append(
                "No alternative axioms found in universe_base.ttl; "
                "manual revision of the proposition is required."
            )
        return hints[:5]

    def verify_statement(
        self,
        s: str,
        p: str,
        o: str,
        expression: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Combined triple + symbolic invariant verification."""
        report = self.validate_triple(s, p, o)
        if expression is not None:
            report["symbolic_valid"] = self.validate_invariant(expression)
            report["expression"] = expression
        return report


if __name__ == "__main__":
    checker = AxiomChecker()
    # Smoke test: register a Formal Core fact, then validate it
    checker.kg.add_fact("core:Energy", "core:hasInvariant", "core:EnergyConservation")
    result = checker.validate_triple("Energy", "hasInvariant", "EnergyConservation")
    print("Axiom Checker initialized successfully.")
    print(f"Smoke test: {result['status']} -> {result['triple']}")