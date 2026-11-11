"""
SymPy Symbolic Invariant Validator.

Validates mathematical equations, checks symbolic equivalence, and identifies
structural invariants under coordinate transforms.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import sympy as sp


class InvariantValidator:
    """Symbolic verification engine for mathematical invariants."""

    @staticmethod
    def check_equivalence(expr1_str: str, expr2_str: str) -> bool:
        """Checks if two mathematical expressions are symbolically identical.

        Returns True if expr1 - expr2 simplifies to 0.
        """
        try:
            e1 = sp.sympify(expr1_str)
            e2 = sp.sympify(expr2_str)
            return sp.simplify(e1 - e2) == 0
        except Exception as err:  # noqa: BLE001
            print(f"Validation Error: {err}")
            return False

    @staticmethod
    def validate_invariant(expression_str: str) -> bool:
        """Verifies if an algebraic expression simplifies to a valid invariant identity.

        Returns True if the expression is a well-formed non-NaN symbolic object.
        """
        try:
            expr = sp.sympify(expression_str)
            return expr != sp.S.NaN
        except Exception as err:  # noqa: BLE001
            print(f"Validation error: {err}")
            return False

    @staticmethod
    def check_invariance_under_transform(
        expr_str: str,
        transform_map: Dict[str, str],
    ) -> bool:
        """Checks whether an expression remains invariant under a variable transform.

        Applies the given substitution map to the expression and compares
        the result with the original symbolically.
        """
        try:
            expr = sp.sympify(expr_str)
            subs = {sp.symbols(k): sp.sympify(v) for k, v in transform_map.items()}
            transformed = expr.subs(subs)
            return sp.simplify(expr - transformed) == 0
        except Exception as err:  # noqa: BLE001
            print(f"Invariance check error: {err}")
            return False

    @staticmethod
    def find_equivalent_invariants(
        expressions: List[str],
    ) -> List[Tuple[str, str]]:
        """Finds pairs of symbolically equivalent expressions from a list."""
        equivalents: List[Tuple[str, str]] = []
        for i in range(len(expressions)):
            for j in range(i + 1, len(expressions)):
                if InvariantValidator.check_equivalence(
                    expressions[i], expressions[j]
                ):
                    equivalents.append((expressions[i], expressions[j]))
        return equivalents

    @staticmethod
    def simplify_expression(expression_str: str) -> Optional[str]:
        """Returns the simplified form of a mathematical expression, or None on failure."""
        try:
            expr = sp.sympify(expression_str)
            return str(sp.simplify(expr))
        except Exception as err:  # noqa: BLE001
            print(f"Simplification error: {err}")
            return None

    @staticmethod
    def compute_derivative(expression_str: str, variable: str) -> Optional[str]:
        """Computes the symbolic derivative of an expression with respect to a variable."""
        try:
            expr = sp.sympify(expression_str)
            var = sp.symbols(variable)
            return str(sp.diff(expr, var))
        except Exception as err:  # noqa: BLE001
            print(f"Derivative error: {err}")
            return None

    @staticmethod
    def check_dimension_consistency(
        equation_str: str,
        symbol_dims: Dict[str, str],
    ) -> bool:
        """Basic structural consistency check: verifies both sides parse and share symbols.

        This is a lightweight syntactic check, not a full dimensional analysis.
        """
        try:
            lhs_str, rhs_str = equation_str.split("=", 1)
            lhs = sp.sympify(lhs_str.strip())
            rhs = sp.sympify(rhs_str.strip())
            lhs_symbols = {str(s) for s in lhs.free_symbols}
            rhs_symbols = {str(s) for s in rhs.free_symbols}
            declared = set(symbol_dims.keys())
            return lhs_symbols.issubset(declared) and rhs_symbols.issubset(declared)
        except Exception as err:  # noqa: BLE001
            print(f"Dimension consistency error: {err}")
            return False


if __name__ == "__main__":
    validator = InvariantValidator()

    # Test identity E = mc^2 -> E - m*c^2 = 0
    is_valid = validator.check_equivalence("E", "m * c**2")
    print(f"E == m*c**2: {is_valid}")

    # Test invariant under transform x -> -x for x**2
    is_invariant = validator.check_invariance_under_transform("x**2", {"x": "-x"})
    print(f"x**2 invariant under x -> -x: {is_invariant}")

    # Find equivalents
    exprs = ["x + y", "y + x", "x**2", "x * x"]
    eq_pairs = validator.find_equivalent_invariants(exprs)
    print(f"Equivalent pairs: {eq_pairs}")

    print("SymPy Validator operational.")
