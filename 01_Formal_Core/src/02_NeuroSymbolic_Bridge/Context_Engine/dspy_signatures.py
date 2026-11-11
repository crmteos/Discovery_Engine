"""
DSPy Signatures for Formal Core Translation.

Defines declarative DSPy signatures for translating raw natural language
inputs into formal ontology predicates without anthropomorphic noise.
DSPy is optional; the module degrades gracefully when it is not installed.
"""

from __future__ import annotations

try:
    import dspy
except ImportError:  # pragma: no cover - optional dependency
    dspy = None  # type: ignore[assignment]


class NaturalLanguageToFormalTriple:
    """
    Translates natural language statements into strict (Subject, Predicate, Object)
    ontology triples adhering to universal_domain.ttl.
    """

    input_text: str = "Raw user observation or hypothesis"
    formal_triples: str = "Extracted RDF triples adhering strictly to universal_domain.ttl"
    confidence_score: str = "Mathematical confidence measure (0.0 to 1.0)"


class QueryToFormalInvariant:
    """
    Translates domain queries into symbolic math equations for SymPy verification.
    """

    user_query: str = "Domain query"
    symbolic_expression: str = "SymPy algebraic expression"


class DSPyAssertGuardrail:
    """
    Guardrail applying dspy.Assert() semantics to logical conditions.

    Falls back to a plain Python assertion when DSPy is not installed,
    keeping the Neuro-Symbolic Bridge fully operational on the $0.00
    local stack.
    """

    @staticmethod
    def assert_condition(condition: bool, message: str) -> bool:
        """Assert a logical condition. Returns True when the guardrail passes."""
        if dspy is not None and hasattr(dspy, "Assert"):
            try:
                dspy.Assert(bool(condition), message)  # type: ignore[attr-defined]
                return True
            except Exception as exc:  # noqa: BLE001
                print(f"DSPy Assert guardrail failed: {exc}")
                return False
        return bool(condition)

    @staticmethod
    def assert_triple_well_formed(triple: tuple[str, str, str]) -> bool:
        subject, predicate, object_ = triple
        return bool(subject and predicate and object_)


__all__ = [
    "NaturalLanguageToFormalTriple",
    "QueryToFormalInvariant",
    "DSPyAssertGuardrail",
    "dspy",
]


if __name__ == "__main__":
    print("DSPy Signatures initialized.")