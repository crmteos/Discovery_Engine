#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""executive_dashboard.py — At-a-Glance Executive Bus Dashboard (v3.4.0)."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BRIDGE_DIR = PROJECT_ROOT / "Bridge"
BUS_FILE = BRIDGE_DIR / "messages.jsonl"
OUT = PROJECT_ROOT / "00_Project_Interface" / "out" / "VISUAL_EXECUTIVE_DASHBOARD.md"

def _load_jsonl(p):
    r=[]
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip(): r.append(json.loads(line))
    return r

def render_markdown() -> str:
    msgs=_load_jsonl(BUS_FILE)
    states={}
    for m in msgs: states[m.get("status","unknown")]=states.get(m.get("status","unknown"),0)+1
    lines=["# Executive Dashboard (Few 5-second rule)","",f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}","","```mermaid","graph LR","  M[Messages] --> S[Status]","```",""]
    lines.append("## KPIs")
    lines.append("| State | Count |"); lines.append("|-------|-------|")
    for k,v in sorted(states.items()): lines.append(f"| {k} | {v} |")
    return "\n".join(lines)

def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--export-md",action="store_true")
    args=p.parse_args(argv)
    md=render_markdown()
    if args.export_md:
        OUT.write_text(md,encoding="utf-8"); print(f"Exported {OUT}")
    else:
        print(md)
    return 0

if __name__=="__main__": raise SystemExit(main())