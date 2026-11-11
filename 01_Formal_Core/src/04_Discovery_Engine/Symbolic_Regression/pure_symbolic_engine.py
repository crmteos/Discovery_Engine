"""Pure Python Symbolic Engine - AST/SymPy formula discovery (no pysr)."""
import sys
import numpy as np
import sympy as sp

class SymbolicRegressionEngine:
    def __init__(self, variables=None):
        variables = variables or ["x"]
        self.variables = variables
        self.symbols = [sp.Symbol(v) for v in variables]
    def fit_candidate_law(self, data_points, target):
        x = self.symbols[0] if self.symbols else sp.Symbol("x")
        data_points = np.asarray(data_points)
        target = np.asarray(target).ravel()
        xs = data_points[:, 0] if data_points.ndim > 1 else data_points.ravel()
        candidates = [x, x**2, sp.sin(x), sp.exp(x), x**3]
        best_expr = None
        best_error = float("inf")
        for cand in candidates:
            try:
                fn = sp.lambdify(x, cand, modules=["numpy"])
                preds = np.asarray(fn(xs)).ravel()
                mse = float(np.mean((preds - target) ** 2))
                if mse < best_error:
                    best_error = mse
                    best_expr = cand
            except Exception:
                continue
        return {
            "discovered_formula": str(best_expr),
            "symbolic_expression": best_expr,
            "mse_loss": best_error,
            "status": "VALIDATED" if best_error < 1e-3 else "APPROXIMATE",
        }

def _test():
    eng = SymbolicRegressionEngine(variables=["x"])
    x_val = np.linspace(0.1, 5.0, 50).reshape(-1, 1)
    y_val = (x_val[:, 0] ** 2)
    res = eng.fit_candidate_law(x_val, y_val)
    print("pure_symbolic_engine --test: OK", res["discovered_formula"], res["mse_loss"])
    return 0

if __name__ == "__main__":
    sys.exit(_test() if "--test" in sys.argv else 0)
