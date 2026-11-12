#!/usr/bin/env python3
"""
genkit_tracer.py - Genkit Tracing & Telemetry Module

Implements local telemetry logging and trace collection for Genkit flows
running across Node 05 (Knowledge Aggregator) and Node 06 (Formalized Model).
"""

import json
import os
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TRACE_LOG_PATH = PROJECT_ROOT / "logs" / "genkit_traces.jsonl"


def ensure_trace_dir():
    """Ensure the logs directory exists."""
    TRACE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def trace_flow(
    flow_name: str,
    node: str,
    prompt: str = None,
    input_data: dict = None,
    output_data: dict = None,
    latency_ms: float = None,
    error: str = None,
    metadata: dict = None,
) -> None:
    """
    Record a Genkit flow execution trace.

    Args:
        flow_name: Name of the Genkit flow
        node: Node identifier (e.g., "Node05", "Node06")
        prompt: The prompt string (optional)
        input_data: Input parameters dict (optional)
        output_data: Output results dict (optional)
        latency_ms: Execution latency in milliseconds (optional)
        error: Error message if flow failed (optional)
        metadata: Additional metadata dict (optional)
    """
    ensure_trace_dir()

    timestamp = time.time()
    entry = {
        "timestamp": timestamp,
        "flow_name": flow_name,
        "node": node,
        "prompt": prompt,
        "input_data": input_data or {},
        "output_data": output_data or {},
        "latency_ms": latency_ms,
        "error": error,
        "metadata": metadata or {},
    }

    with open(TRACE_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def get_traces(
    since: float = None,
    flow_name: str = None,
    node: str = None,
) -> list:
    """
    Retrieve trace entries from the log file.

    Args:
        since: Return only entries after this timestamp (float)
        flow_name: Filter by flow name
        node: Filter by node identifier

    Returns:
        List of trace entry dicts
    """
    if not TRACE_LOG_PATH.is_file():
        return []

    entries = []
    with open(TRACE_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            if since is not None and entry.get("timestamp", 0) <= since:
                continue
            if flow_name is not None and entry.get("flow_name") != flow_name:
                continue
            if node is not None and entry.get("node") != node:
                continue

            entries.append(entry)

    return entries


def get_trace_stats() -> dict:
    """Get statistics about recorded traces."""
    if not TRACE_LOG_PATH.is_file():
        return {
            "total_traces": 0,
            "flows": {},
            "nodes": {},
            "total_latency_ms": 0,
            "average_latency_ms": 0,
        }

    total = 0
    flow_counts = {}
    node_counts = {}
    total_latency = 0.0

    with open(TRACE_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            total += 1
            flow_name = entry.get("flow_name", "unknown")
            node = entry.get("node", "unknown")
            latency = entry.get("latency_ms", 0) or 0

            flow_counts[flow_name] = flow_counts.get(flow_name, 0) + 1
            node_counts[node] = node_counts.get(node, 0) + 1
            total_latency += (latency or 0)

    return {
        "total_traces": total,
        "flows": flow_counts,
        "nodes": node_counts,
        "total_latency_ms": round(total_latency, 2),
        "average_latency_ms": round(total_latency / total, 2) if total > 0 else 0,
    }


def clear_traces() -> None:
    """Clear all trace entries from the log file."""
    ensure_trace_dir()
    with open(TRACE_LOG_PATH, "w", encoding="utf-8") as f:
        f.write("")


if __name__ == "__main__":
    # Simple CLI test: print trace stats
    print(f"genkit_tracer.py - Project root: {PROJECT_ROOT}")
    print(f"Trace log: {TRACE_LOG_PATH}")
    stats = get_trace_stats()
    print(f"Trace statistics: {json.dumps(stats, indent=2)}")