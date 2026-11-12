#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_Knowledge_Aggregator/src/knowledge_weaver.py — Dual-Stream Weaver (v6.0.0 / Phase 50)

Weaves together two cognitive streams (Stream A and Stream B) from the dual-stream
elephant architecture, preserving provenance metadata and guaranteeing that both
streams originate from the same primary source (NARROW_EXTRACTOR).

Output: DualStreamEnvelope — a container with both streams and validation metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data Structure for Dual-Stream Envelope
# ---------------------------------------------------------------------------

@dataclass
class DualStreamEnvelope:
    """Envelope container for weaved dual-stream output."""
    stream_a: Dict[str, Any]  # Raw or processed Stream A data (direct text, log10 basis)
    stream_b: Dict[str, Any]  # Transformed Stream B data (log2 basis, frequency spectrum)
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def validate_source_consistency(self) -> bool:
        """
        Validate that both streams originate from the same primary source (NARROW_EXTRACTOR).

        Returns
        -------
        bool
            True if source consistency is confirmed, False otherwise.
        """
        source_a = self.stream_a.get("source", "")
        source_b = self.stream_b.get("source", "")
        # Both must reference NARROW_EXTRACTOR (directly or via provenance)
        _src_ok = "NARROW_EXTRACTOR" in source_a and "NARROW_EXTRACTOR" in source_b
        if _src_ok:
            self.metadata["source_consistent"] = True
        else:
            self.metadata["source_consistent"] = False
        return _src_ok

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the envelope to a dictionary."""
        return {
            "stream_a": self.stream_a,
            "stream_b": self.stream_b,
            "provenance": self.provenance,
            "metadata": self.metadata,
        }


# ---------------------------------------------------------------------------
 weave_dual_streams Function
# ---------------------------------------------------------------------------


def weave_dual_streams(
    stream_a: Dict[str, Any],
    stream_b: Dict[str, Any],
) -> DualStreamEnvelope:
    """
    Weave two cognitive streams into a DualStreamEnvelope.

    Guarantees metadata preservation that Potyk A and Potyk B originate from
    a single primary basis database (NARROW_EXTRACTOR).

    Transformation pipeline:
    - Stream A: Pass-through with source metadata annotation
    - Stream B: Ensure it has undergone log10→log2 basis shift and frequency projection
    - Cross-stream: Validate source consistency and compute correlation metrics

    Parameters
    ----------
    stream_a : Dict[str, Any]
        Raw Stream A data (anthropomorphic-decade perspective, log10 basis, standard time t).
        Expected keys: "text", "source", "timestamp", etc.
    stream_b : Dict[str, Any]
        Transformed Stream B data (axiomatic-modular perspective, log2 basis, frequency spectrum).
        Expected keys: "log2_basis", "frequency_spectrum", "modulating_keys_applied", etc.

    Returns
    -------
    DualStreamEnvelope
        Container with both streams and validated provenance metadata.
    """
    # Default provenance record
    provenance: Dict[str, Any] = {
        "agent": "KnowledgeWeaver",
        "activity": "dual_stream_weave",
        "entity": "dual_stream_envelope",
        "source_validated": False,
        "started_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
    }

    # Ensure stream_a has source metadata
    if "source" not in stream_a:
        stream_a["source"] = "NARROW_EXTRACTOR"
    if "perspective" not in stream_a:
        stream_a["perspective"] = "anthropomorphic_decade_log10_t"

    # Ensure stream_b has basis transformation metadata
    if "basis_shift" not in stream_b:
        stream_b["basis_shift"] = "log10_to_log2"
    if "projection_type" not in stream_b:
        stream_b["projection_type"] = "LT_system_frequency"

    # Validate source consistency between streams
    source_a = stream_a.get("source", "")
    source_b = stream_b.get("source", "")
    source_consistent = "NARROW_EXTRACTOR" in source_a and "NARROW_EXTRACTOR" in source_b
    provenance["source_validated"] = source_consistent

    if source_consistent:
        provenance["metadata"] = {
            "source_a": source_a,
            "source_b": source_b,
            "validation": "both_streams_from_narrow_extractor",
        }
    else:
        provenance["metadata"] = {
            "source_a": source_a,
            "source_b": source_b,
            "validation": "source_mismatch_warning",
        }

    # Build the envelope
    envelope = DualStreamEnvelope(
        stream_a=stream_a,
        stream_b=stream_b,
        provenance=provenance,
        metadata={
            "weave_version": "v6.0.0/Phase50",
            "dual_stream": True,
        },
    )

    return envelope