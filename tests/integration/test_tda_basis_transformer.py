"""Integration tests for TDA basis transformer.

Tests the TDA engine and basis transformer modules for Phase 47 v5.6.0.
"""

import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '01_Formal_Core', 'src'))

from pure_tda_engine import time_delay_embed, betti_from_embedded, betti_numbers
from basis_transformer import log10_to_log2, dft, dft_amplitude_spectrum, _test_log2_shift, _test_dft


def test_betti_numbers():
    """Test 1: Verify H0/H1 computation for test point cloud."""
    pts = [(0, 0), (1, 0), (0, 1), (5, 5)]
    res = betti_numbers(pts, 1.5)
    assert res["H0"] == 2, "Expected H0=2, got {}".format(res["H0"])
    assert res["H1"] == 1, "Expected H1=1, got {}".format(res["H1"])
    print("Test 1 passed: betti_numbers H0={}, H1={}".format(res["H0"], res["H1"]))


def test_log2_conversion():
    """Test 2: Verify log10 -> log2 conversion."""
    data = np.array([1.0, 10.0, 100.0, 1000.0])
    converted = log10_to_log2(np.log10(data))
    expected = np.log2(data)
    assert np.allclose(converted, expected), "log2 conversion mismatch"
    print("Test 2 passed: log10 -> log2 conversion")


def test_tde_and_betti():
    """Test 3: Verify TDE + Betti number computation."""
    t = np.linspace(0, 10, 500)
    series = np.sin(t).tolist()
    points = time_delay_embed(series, delay=5, dimension=3)
    assert len(points) > 0, "TDE should produce points"
    betti = betti_from_embedded(series, delay=5, dimension=3, eps=0.5)
    assert "H0" in betti and "H1" in betti, "Betti should have H0 and H1"
    print("Test 3 passed: TDE produced {} points, Betti={}".format(len(points), betti))


def test_dft_spectrum():
    """Test 4: Verify DFT spectral decomposition."""
    t = np.linspace(0, 1, 1000, endpoint=False)
    signal = np.sin(2 * np.pi * 50 * t)
    freqs, amplitudes = dft_amplitude_spectrum(signal)
    assert len(freqs) == len(amplitudes), "Frequency and amplitude arrays should have same length"
    peak_idx = np.argmax(amplitudes)
    peak_freq = freqs[peak_idx]
    assert abs(peak_freq - 50.0) < 1.0, "Peak frequency {} far from 50".format(peak_freq)
    print("Test 4 passed: DFT spectral decomposition")


if __name__ == "__main__":
    test_betti_numbers()
    test_log2_conversion()
    test_tde_and_betti()
    test_dft_spectrum()
    print("\nAll integration tests passed!")