"""Basis Transformer module for Discovery Engine Phase 47 v5.6.0.
Provides log10->log2 base conversion and Discrete Fourier Transform (DFT) of time-series.
"""

import math
import sys
from collections import defaultdict

import numpy as np


def log10_to_log2(data):
    """Convert arrays from base-10 logarithmic scale to natural logarithmic scale.

    Parameters
    ----------
    data : array-like
        Input data on log10 scale.

    Returns
    -------
    numpy.ndarray
        Data converted to log2 scale.
    """
    data = np.asarray(data)
    return data / math.log10(2)


def dft(time_series, dt=1.0):
    """Compute the Discrete Fourier Transform (DFT) of a time-series.

    Parameters
    ----------
    time_series : array-like
        Input time-domain signal.
    dt : float, optional
        Sampling interval in seconds (default: 1.0).

    Returns
    -------
    tuple
        (frequencies, complex_spectrum) - frequency axis and DFT coefficients.
    """
    n = len(time_series)
    freq = np.fft.fftfreq(n, d=dt)
    spectrum = np.fft.fft(time_series)
    return freq, spectrum


def dft_amplitude_spectrum(time_series, dt=None):
    """Compute the amplitude spectrum (magnitude) from a DFT.

    Parameters
    ----------
    time_series : array-like
        Input time-domain signal.
    dt : float, optional
        Sampling interval in seconds. If None, computed from time series length
        assuming 1-second total duration (default: None).

    Returns
    -------
    tuple
        (frequencies, amplitudes) - positive frequency axis and magnitudes.
    """
    n = len(time_series)
    if dt is None:
        dt = 1.0 / n
    freq = np.fft.fftfreq(n, d=dt)
    spectrum = np.fft.fft(time_series)
    amplitudes = np.abs(spectrum[:n // 2])
    frequencies = freq[:n // 2]
    return frequencies, amplitudes


def _test_log2_shift():
    """Test log10 -> log2 conversion."""
    data = np.array([1.0, 10.0, 100.0, 1000.0])
    log10_data = np.log10(data)
    log2_data = log10_to_log2(log10_data)
    expected = np.log2(data)
    assert np.allclose(log2_data, expected), f"log2 shift mismatch: {log2_data} vs {expected}"
    print(f"log2 shift test: data={data}, log2={log2_data}")
    return 0


def _test_dft():
    """Test DFT of a sinusoid."""
    t = np.linspace(0, 1, 1000, endpoint=False)
    dt = t[1] - t[0]  # sampling interval
    signal = np.sin(2 * math.pi * 50 * t)
    freq, spectrum = dft(signal, dt=dt)
    peak_idx = np.argmax(np.abs(spectrum[:len(spectrum) // 2]))
    peak_freq = abs(freq[peak_idx])
    assert abs(peak_freq - 50.0) < 1.0, f"Peak freq {peak_freq} far from 50"
    print(f"DFT test: peak frequency = {peak_freq:.1f} Hz")
    return 0


if __name__ == "__main__":
    sys.exit(_test_log2_shift() + _test_dft())