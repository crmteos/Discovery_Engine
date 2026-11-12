"""Pure Python TDA Engine - Vietoris-Rips filtration & Betti numbers (no giotto/gudhi).
"""
import math, sys
from collections import defaultdict, deque

def build_vr(points, eps):
    n = len(points)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            d = math.dist(points[i], points[j])
            if d <= eps:
                edges.append((i, j))
    return edges

def betti_numbers(points, eps):
    n = len(points)
    edges = build_vr(points, eps)
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
    b1 = max(0, len(edges) - n + comp)
    return {"H0": comp, "H1": b1, "edges": len(edges), "vertices": n}

def time_delay_embed(series, delay, dimension):
    """Time-Delay Embedding (Takens' Theorem).

    Reconstructs a phase space from a scalar time series.

    Parameters
    ----------
    series : list[float]
        Scalar time-series data.
    delay : int
        Time delay tau (in number of steps).
    dimension : int
        Embedding dimension m (number of delayed coordinates).

    Returns
    -------
    list[tuple]
        List of embedded points in R^m, each point is a tuple of m coordinates.
    """
    n = len(series)
    if n < dimension * delay:
        raise ValueError(
            f"Series length {n} is too small for delay={delay}, dimension={dimension}. "
            f"Need at least {dimension * delay} points."
        )
    points = []
    for i in range(n - (dimension - 1) * delay):
        point = tuple(series[i + k * delay] for k in range(dimension))
        points.append(point)
    return points

def betti_from_embedded(series, delay, dimension, eps):
    """Compute Betti numbers from a time-delay embedded point cloud."""
    points = time_delay_embed(series, delay, dimension)
    return betti_numbers(points, eps)

def _test_log2_shift():
    """Test log10 -> log2 base conversion."""
    data = [1.0, 10.0, 100.0, 1000.0]
    log10 = [math.log10(x) for x in data]
    log2 = [math.log2(x) for x in data]
    expected = [l / math.log10(2) for l in log10]
    assert all(abs(a - b) < 1e-10 for a, b in zip(log2, expected)), "log2 shift mismatch"
    print(f"log2 shift test: data={data}, log10={log10}, log2={log2}")
    return 0

def _test_fft():
    """Test Discrete Fourier Transform (DFT) via scipy.fft."""
    try:
        from scipy.fft import fft
        import numpy as np
        t = np.linspace(0, 1, 1000, endpoint=False)
        signal = np.sin(2 * math.pi * 50 * t)
        spectrum = fft(signal)
        freqs = np.fft.fftfreq(t.size, d=t[1] - t[0])
        peak_idx = np.argmax(np.abs(spectrum[:len(spectrum)//2]))
        peak_freq = abs(freqs[peak_idx])
        assert abs(peak_freq - 50.0) < 1.0, f"Peak freq {peak_freq} far from 50"
        print(f"FFT test: peak frequency = {peak_freq:.1f} Hz")
        return 0
    except ImportError:
        print("scipy not available, skipping FFT test")
        return 1

def _test():
    pts = [(0, 0), (1, 0), (0, 1), (5, 5)]
    res = betti_numbers(pts, 1.5)
    assert res["H0"] == 2, res
    print("pure_tda_engine --test: OK", res)
    return 0

if __name__ == "__main__":
    sys.exit(_test() if "--test" in sys.argv else 0)