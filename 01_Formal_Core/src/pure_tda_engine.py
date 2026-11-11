"""Pure Python TDA Engine - Vietoris-Rips filtration & Betti numbers (no giotto/gudhi)."""
import math, sys
from collections import defaultdict, deque

def build_vr(points, eps):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            d = math.dist(points[i], points[j])
            if d <= eps:
                edges.append((i, j))
    return edges

def betti_numbers(points, eps):
    n = len(points)
    edges = build_vr(points, eps)
    # H0: connected components
    adj = defaultdict(list)
    for i, j in edges:
        adj[i].append(j); adj[j].append(i)
    seen = set()
    comp = 0
    for i in range(n):
        if i in seen: continue
        comp += 1
        dq = deque([i]); seen.add(i)
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); dq.append(v)
    # H1: cycle rank = E - V + C
    b1 = max(0, len(edges) - n + comp)
    return {"H0": comp, "H1": b1, "edges": len(edges), "vertices": n}

def _test():
    pts = [(0,0),(1,0),(0,1),(5,5)]
    res = betti_numbers(pts, 1.5)
    assert res["H0"] == 2, res
    print("pure_tda_engine --test: OK", res)
    return 0

if __name__ == "__main__":
    sys.exit(_test() if "--test" in sys.argv else 0)
