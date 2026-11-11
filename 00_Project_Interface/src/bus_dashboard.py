#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bus_dashboard.py — Live Observability Bus Dashboard (v3.3.0)."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
BUS_FILE = BRIDGE_DIR / "messages.jsonl"
DLQ_FILE = BRIDGE_DIR / "messages_dlq.jsonl"
DASHBOARD_MD = PROJECT_ROOT / "BUS_OBSERVABILITY_DASHBOARD.md"
TOPOLOGY_SVG = PROJECT_ROOT / "system_topology.svg"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                records.append(json.loads(stripped))
    return records


def _latency_seconds(msg: dict[str, Any]) -> float | None:
    created = msg.get("timestamp") or msg.get("created_at")
    completed = msg.get("completed_at") or msg.get("updated_at")
    if not created or not completed:
        return None
    try:
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        t0 = datetime.strptime(created, fmt)
        t1 = datetime.strptime(completed, fmt)
        return (t1 - t0).total_seconds()
    except (ValueError, TypeError):
        return None


def build_metrics() -> dict[str, Any]:
    messages = _load_jsonl(BUS_FILE)
    dlq = _load_jsonl(DLQ_FILE)
    states = Counter(m.get("status", "unknown") for m in messages)
    for s in ("pending", "in_progress", "completed", "failed", "dlq"):
        states.setdefault(s, 0)
    vector_matrix: dict[str, int] = defaultdict(int)
    for m in messages:
        vector_matrix[m.get("vector", "unknown")] += 1
    actor_latency: dict[str, list[float]] = defaultdict(list)
    for m in messages:
        lat = _latency_seconds(m)
        if lat is not None:
            actor_latency[m.get("sender", "unknown")].append(lat)
    actor_stats = {}
    for actor, lats in actor_latency.items():
        actor_stats[actor] = {
            "count": len(lats),
            "avg_latency_s": round(sum(lats) / len(lats), 3) if lats else 0.0,
            "max_latency_s": round(max(lats), 3) if lats else 0.0,
        }
    dlq_count = len(dlq)
    states["dlq"] = states.get("dlq", 0) + dlq_count
    return {
        "timestamp": _utc_now(),
        "total_messages": len(messages),
        "states": dict(states),
        "vector_matrix": dict(vector_matrix),
        "actor_latency": actor_stats,
        "dlq_total": dlq_count,
    }




def render_cli(metrics: dict[str, Any]) -> None:
    print("=" * 72)
    print(" Live Observability Bus Dashboard (v3.3.0)")
    print("=" * 72)
    print(f" Timestamp      : {metrics['timestamp']}")
    print(f" Total messages : {metrics['total_messages']}")
    print("-" * 72)
    print(" Message States")
    for k in ("pending", "in_progress", "completed", "failed", "dlq"):
        print(f"  {k:14s}: {metrics['states'].get(k, 0)}")
    print("-" * 72)
    print(" Vector Traffic Matrix")
    for vec, cnt in sorted(metrics["vector_matrix"].items()):
        print(f"  {vec:32s}: {cnt}")
    print("-" * 72)
    print(" Actor Latency")
    for actor, st in sorted(metrics["actor_latency"].items()):
        print(f"  {actor:28s}: n={st['count']} avg={st['avg_latency_s']}s max={st['max_latency_s']}s")
    print("-" * 72)
    print(f" DLQ total      : {metrics['dlq_total']}")
    print("=" * 72)


def render_markdown(metrics: dict[str, Any]) -> str:
    lines = []
    lines.append("# Live Observability Bus Dashboard")
    lines.append("")
    lines.append(f"**Generated:** {metrics['timestamp']}")
    lines.append("")
    lines.append("## Message States")
    lines.append("")
    lines.append("| State | Count |")
    lines.append("|-------|-------|")
    for k in ("pending", "in_progress", "completed", "failed", "dlq"):
        lines.append(f"| {k} | {metrics['states'].get(k, 0)} |")
    lines.append("")
    lines.append("## Vector Traffic Matrix")
    lines.append("")
    lines.append("| Vector | Count |")
    lines.append("|--------|-------|")
    for vec, cnt in sorted(metrics["vector_matrix"].items()):
        lines.append(f"| {vec} | {cnt} |")
    lines.append("")
    lines.append("## Actor Latency")
    lines.append("")
    lines.append("| Actor | Count | Avg (s) | Max (s) |")
    lines.append("|-------|-------|---------|---------|")
    for actor, st in sorted(metrics["actor_latency"].items()):
        lines.append(f"| {actor} | {st['count']} | {st['avg_latency_s']} | {st['max_latency_s']} |")
    lines.append("")
    lines.append("## System Topology (Mermaid)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("graph LR")
    lines.append("  M[system.master_architect] -->|vertical| C[cline.executor]")
    lines.append("  A[aggregator.architect] -->|interface_to_bus| M")
    lines.append("  K[core.tda_engineer] -->|interface_to_bus| M")
    lines.append("  B[model.builder] -->|interface_to_bus| M")
    lines.append("  I[interface.operator] -->|interface_to_anythingllm| L[AnythingLLM]")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def export_svg(metrics: dict[str, Any]) -> None:
    svg = "<svg xmlns='http://www.w3.org/2000/svg' width='600' height='200'><text x='10' y='20' font-size='14'>Discovery Engine Topology v3.3.0</text></svg>"
    TOPOLOGY_SVG.write_text(svg, encoding="utf-8")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="bus_dashboard.py", description="Live Observability Bus Dashboard")
    parser.add_argument("--cli", action="store_true", help="Render CLI dashboard.")
    parser.add_argument("--export-md", action="store_true", help="Export Markdown dashboard.")
    parser.add_argument("--export-svg", action="store_true", help="Export SVG topology.")
    args = parser.parse_args(argv)

    metrics = build_metrics()

    if args.cli or (not args.export_md and not args.export_svg):
        render_cli(metrics)

    if args.export_md:
        md = render_markdown(metrics)
        DASHBOARD_MD.write_text(md, encoding="utf-8")
        print(f"Exported Markdown dashboard to {DASHBOARD_MD}")

    if args.export_svg:
        export_svg(metrics)
        print(f"Exported SVG topology to {TOPOLOGY_SVG}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
