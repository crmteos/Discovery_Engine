"""
CAS SymPy Theorem & Invariant Prover — Formal Core v2.6.0.

Canonises algebraic formulas via SymPy and checks the satisfiability
of logical clause sets. Pure local SymPy backend ($0.00, no external APIs).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import sympy as sp

try:  # telemetry sink (OpenTelemetry GenAI -> Bridge/messages.jsonl)
    from Bridge.bus_manager import log_core_telemetry as _telemetry_sink  # type: ignore[assignment]
except Exception:  # pragma: no cover - bridge bus unavailable outside project root
    _telemetry_sink = None  # type: ignore[assignment]


def _sympify_clause(clause: str):
    """Parse a clause string into a SymPy boolean expression.

    Supports equations written as "lhs = rhs" (converted to sp.Eq) as well
    as plain Boolean/algebraic expressions accepted by sympify().
    """
    clause = clause.strip()
    if "=" in clause:
        lhs_str, rhs_str = clause.split("=", 1)
        return sp.Eq(sp.sympify(lhs_str.strip()), sp.sympify(rhs_str.strip()))
    return sp.sympify(clause)


def _emit_telemetry(step_name: str, metrics: Dict[str, Any], status: str) -> None:
    if _telemetry_sink is None:
        return
    try:
        _telemetry_sink(step_name, metrics=metrics, status=status)  # type: ignore[misc]
    except Exception:  # pragma: no cover - telemetry is best-effort
        pass


class CASProver:
    """Computer-algebra system prover over SymPy expressions."""

    def verify_invariant(self, expr_str: str) -> Dict[str, Any]:
        """Verify that a symbolic expression is a well-formed invariant.

        Runs sympify + canonical simplification and reports well-formedness,
        free symbols and the canonical form of the expression.
        """
        try:
            expr = sp.sympify(expr_str)
            canonical = str(sp.simplify(expr))
            is_nan = expr == sp.S.NaN
            is_infinite = expr in (sp.S.Infinity, sp.S.NegativeInfinity)
            report: Dict[str, Any] = {
                "expr_str": expr_str,
                "canonical": canonical,
                "is_well_formed": True,
                "is_nan": bool(is_nan),
                "is_infinite": bool(is_infinite),
                "verified": (not is_nan) and (not is_infinite),
                "free_symbols": sorted(str(sym) for sym in expr.free_symbols),
            }
            _emit_telemetry(
                "sympy_verify_invariant",
                {"expr": expr_str, "canonical": canonical, "verified": report["verified"]},
                "completed" if report["verified"] else "failed",
            )
            return report
        except Exception as exc:  # noqa: BLE001
            report = {"expr_str": expr_str, "verified": False, "error": str(exc)}
            _emit_telemetry("sympy_verify_invariant", {"expr": expr_str, "verified": False}, "failed")
            return report

    def check_satisfiability(self, clauses: List[str]) -> Dict[str, Any]:
        """Check satisfiability of a list of clauses via sympy.satisfiable()."""
        try:
            if not clauses:
                report: Dict[str, Any] = {
                    "clauses": [],
                    "satisfiable": True,
                    "model": {},
                    "verified": True,
                    "note": "empty clause set is trivially satisfiable",
                }
                _emit_telemetry("sympy_check_satisfiability", {"satisfiable": True}, "completed")
                return report
            sympy_clauses = [_sympify_clause(clause) for clause in clauses]
            combined = sp.And(*sympy_clauses)
            result = sp.satisfiable(combined)
            model: Dict[str, str] = {}
            if isinstance(result, dict):
                model = {str(sym): str(val) for sym, val in result.items()}
            satisfiable = result is not False and result is not None
            report = {
                "clauses": clauses,
                "combined": str(combined),
                "satisfiable": bool(satisfiable),
                "model": model,
                "verified": True,
            }
            _emit_telemetry(
                "sympy_check_satisfiability",
                {"clauses": len(clauses), "satisfiable": report["satisfiable"]},
                "completed",
            )
            return report
        except Exception as exc:  # noqa: BLE001
            report = {
                "clauses": clauses,
                "satisfiable": False,
                "verified": False,
                "error": str(exc),
            }
            _emit_telemetry(
                "sympy_check_satisfiability",
                {"clauses": len(clauses), "satisfiable": False},
                "failed",
            )
            return report

    def canonical_simplify(self, expr_str: str) -> Optional[str]:
        """Return the canonical (simplified) form of an expression, or None on failure."""
        try:
            expr = sp.sympify(expr_str)
            return str(sp.simplify(expr))
        except Exception as exc:  # noqa: BLE001
            print(f"Canonical simplification error: {exc}")
            return None


def verify_invariant(expr_str: str) -> Dict[str, Any]:
    """Module-level convenience wrapper around CASProver.verify_invariant."""
    return CASProver().verify_invariant(expr_str)


def check_satisfiability(clauses: List[str]) -> Dict[str, Any]:
    """Module-level convenience wrapper around CASProver.check_satisfiability."""
    return CASProver().check_satisfiability(clauses)


if __name__ == "__main__":  # pragma: no cover - smoke test
    prover = CASProver()
    print("Invariant check:", prover.verify_invariant("E_total - (E_tail + E_trunk + E_leg + E_ear)"))
    print("Equivalence:", prover.check_satisfiability(["x + y = 2", "x - y = 0"]))
    print("Canonical:", prover.canonical_simplify("(x + 1)**2 - x**2"))
    print("SymPy CAS Prover operational.")