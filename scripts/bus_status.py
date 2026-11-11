#!/usr/bin/env python3
"""CLI shortcut to inspect Bridge/messages.jsonl and Bridge/messages_dlq.jsonl."""
from __future__ import annotations
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIDGE = ROOT / "Bridge"

def _show(path, limit):
    if not path.exists():
        print(f"{path}: (missing)")
        return
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"=== {path.name} ({len(lines)} lines) ===")
    for line in lines[-limit:]:
        try:
            obj = json.loads(line)
            print(f"{obj.get('id')} | {obj.get('status')} | {obj.get('topic')}")
        except Exception:
            print(line)

def main():
    parser = argparse.ArgumentParser(description="Bus status inspector")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    _show(BRIDGE / "messages.jsonl", args.limit)
    _show(BRIDGE / "messages_dlq.jsonl", args.limit)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())