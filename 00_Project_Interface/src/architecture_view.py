#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_Project_Interface/src/architecture_view.py — Dashboard Node (v2.7.0).

Inspects system_manifest.json, Bridge/messages.jsonl, Bridge/messages_dlq.jsonl
and PROJECT_STATE.md, then outputs a CLI diagnostic summary of system health,
active nodes, bus transactions, and DLQ status.

Supports --test flag returning exit_code: 0 on clean state.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST_PATH = PROJECT_ROOT / "system_manifest.json"
STATE_PATH = PROJECT_ROOT / "PROJECT_STATE.md"
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
BUS_FILE = BRIDGE_DIR / "messages.jsonl"
DLQ_FILE = BRIDGE_DIR / "messages_dlq.jsonl"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


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


def _load_text(path: Path) -> str:
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def diagnose() -> dict[str, Any]:
    manifest = _load_json(MANIFEST_PATH) or {}
    bus_messages = _load_jsonl(BUS_FILE)
    dlq_messages = _load_jsonl(DLQ_FILE)
    state_text = _load_text(STATE_PATH)

    pending = [m for m in bus_messages if m.get("status") == "pending"]
    completed = [m for m in bus_messages if m.get("status") == "completed"]
    failed = [m for m in bus_messages if m.get("status") == "failed"]

    nodes = manifest.get("nodes", {})
    active_nodes = [
        node_id for node_id, node in nodes.items() if node
    ]

    # Detect active anomalies: failed bus messages and circuit-broken DLQ entries.
    failed = [m for m in bus_messages if m.get("status") == "failed"]
    dlq_alerts = [m for m in dlq_messages if m.get("status") == "circuit_broken"]

    clean = (
        dlq_alerts == []
        and failed == []
        and BUS_FILE.exists()
        and MANIFEST_PATH.exists()
    )

    return {
        "timestamp": _utc_now(),
        "manifest_version": manifest.get("version"),
        "architecture": manifest.get("architecture"),
        "message_bus": str(BUS_FILE),
        "bus_messages_total": len(bus_messages),
        "pending": len(pending),
        "completed": len(completed),
        "failed": len(failed),
        "dlq_total": len(dlq_messages),
        "dlq_alerts": len(dlq_alerts),
        "active_nodes": active_nodes,
        "node_count": len(active_nodes),
        "state_phase": "Phase 18" if "Phase 18" in state_text else "unknown",
        "clean": clean,
    }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 68)
    print(" 00_Project_Interface — Architecture Diagnostic Summary (v2.7.0)")
    print("=" * 68)
    print(f" Timestamp        : {report['timestamp']}")
    print(f" Manifest version : {report['manifest_version']}")
    print(f" Architecture     : {report['architecture']}")
    print(f" State phase      : {report['state_phase']}")
    print("-" * 68)
    print(" Message Bus")
    print(f"  Bus file        : {report['message_bus']}")
    print(f"  Total messages  : {report['bus_messages_total']}")
    print(f"  Pending         : {report['pending']}")
    print(f"  Completed       : {report['completed']}")
    print(f"  Failed          : {report['failed']}")
    print("-" * 68)
    print(" Dead-Letter Queue")
    print(f"  DLQ total       : {report['dlq_total']}")
    print(f"  DLQ alerts      : {report['dlq_alerts']}")
    print("-" * 68)
    print(" Nodes")
    print(f"  Active nodes    : {report['node_count']}")
    for node in report["active_nodes"]:
        print(f"   - {node}")
    print("-" * 68)
    print(f" System clean     : {report['clean']}")
    print("=" * 68)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="architecture_view.py",
        description="00_Project_Interface architecture diagnostic (v2.7.0)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode; exit_code 0 on clean state.",
    )
    args = parser.parse_args(argv)

    report = diagnose()
    print_report(report)

    if args.test:
        return 0 if report["clean"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
