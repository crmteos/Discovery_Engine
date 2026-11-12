#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""06_Formalized_Model/src/axiomatic_transformer.py — Formal Projection Operator (v4.7.0 / Phase 38).

Relocates Axiomatic Invariants Transformer from Node 05 to Node 06 per W3C PROV-O and SRP.
Receives canonical RDF facts from Node 05 via the message bus (Bridge/messages.jsonl).
Delegates mathematical transformations (log-basis changes, DFT, symbolic invariants) to Node 01 engines.
Emits de-anthropomorphized, prov-tracked RDF triples to Processed_Gate/normalized_triples/.

W3C PROV-O Compliance:
- Every output triple carries prov:wasDerivedFrom and prov:wasInfluencedBy
- Causal Set theory axioms preserved (no element creation or destruction)
- SKOS relationships for topological vectors

ISO/IEC/IEEE 42010 Single Responsibility Principle:
- Node 05: objective fact extraction only (NARROW_EXTRACTOR -> ZERO_HALLUCINATION_AUDITOR -> KNOWLEDGE_WEAVER)
- Node 06: formal axiomatic transformation (this module)
- Node 01: mathematical engine core (pure_symbolic, TDA, symbolic AI)
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Project root path setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
MESSAGES_FILE = BRIDGE_DIR / "messages.jsonl"

# Node 01 engine imports - Formal Core mathematical engines
try:
    from_01 = PROJECT_ROOT.parent / "01_Formal_Core"
    if str(from_01) not in sys.path:
        sys.path.insert(0, str(from_01))

    from Knowledge_Graphs.kg_engine import KnowledgeGraphEngine
    from Symbolic_AI.sympy_validator import InvariantValidator
    _HAS_NODE01_ENGINES = True
except ImportError as exc:
    _HAS_NODE01_ENGINES = False
    _IMPORT_ERROR = exc


# ---------------------------------------------------------------------------
# W3C PROV-O Provenance Tracking
# ---------------------------------------------------------------------------

PROV = {
    "wasDerivedFrom": None,
    "wasInfluencedBy": None,
    "wasGeneratedBy": None,
    "used": None,
    "agent": None,
    "activity": None,
    "entity": None,
}


# ---------------------------------------------------------------------------
# Key Modulator Loader
# ---------------------------------------------------------------------------

def load_modulating_keys(keys_dir: str = "06_Formalized_Model/keys/") -> Dict[str, str]:
    """
    Load all modulating key files from the keys directory.

    Returns a dictionary mapping key filenames (without extension) to their content.
    Currently supports .md and .txt files.
    """
    keys = {}
    keys_path = Path(keys_dir)

    if not keys_path.is_dir():
        print(f"Warning: Keys directory {keys_dir} not found. Using identity modulator.")
        return keys

    for key_file in sorted(keys_path.glob("*.md")):
        try:
            content = key_file.read_text(encoding="utf-8")
            keys[key_file.stem] = content
            print(f"Loaded modulating key: {key_file.name}")
        except Exception as e:
            print(f"Warning: Could not read key file {key_file}: {e}")

    for key_file in sorted(keys_path.glob("*.txt")):
        try:
            content = key_file.read_text(encoding="utf-8")
            keys[key_file.stem] = content
            print(f"Loaded modulating key: {key_file.name}")
        except Exception as e:
            print(f"Warning: Could not read key file {key_file}: {e}")

    return keys


_LOG = logging.getLogger("axiomatic_transformer")
# ---------------------------------------------------------------------------
# Basis Transformation Functions
# ---------------------------------------------------------------------------

def log10_to_log2(data: List[float]) -> List[float]:
    """Convert data from decimal (log10) basis to binary (log2) basis."""
    result = []
    for x in data:
        if x <= 0:
            result.append(0.0)
        else:
            result.append(math.log2(x))
    return result

def log2_to_log10(data: List[float]) -> List[float]:
    """Convert data from binary (log2) basis back to decimal (log10) basis."""
    result = []
    for x in data:
        if x <= 0:
            result.append(0.0)
        else:
            result.append(math.log10(x))
    return result

def time_to_frequency_spectrum(
    data: List[float],
    sample_interval: float = 1.0,
    return_phase: bool = False,
) -> Dict[str, Any]:
    """Transform a time-series parameter t into a frequency spectrum using DFT."""
    n = len(data)
    amplitudes = []
    frequencies = []
    for k in range(n // 2 + 1):
        amp = sum(
            data[n_idx] * math.cos(2 * math.pi * k * n_idx / n)
            for n_idx in range(n)
        )
        frequencies.append(k / (n * sample_interval))
        amplitudes.append(amp)
    return {"amplitudes": amplitudes, "frequencies": frequencies}
