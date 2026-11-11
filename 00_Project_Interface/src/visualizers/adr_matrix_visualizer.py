#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""adr_matrix_visualizer.py — ADR & Interaction Map (v3.4.0)."""
from __future__ import annotations
import argparse
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT = PROJECT_ROOT / "00_Project_Interface" / "out" / "VISUAL_ADR_MATRIX.md"
def render_markdown() -> str:
    lines=["# ADR & Interaction Map (Sibbet)","", "```mermaid","graph TD","  ADR0001 --> ADR0006","```",""]
    return "\n".join(lines)
def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--export-md",action="store_true")
    args=p.parse_args(argv)
    md=render_markdown()
    if args.export_md: OUT.write_text(md,encoding="utf-8"); print(f"Exported {OUT}")
    else: print(md)
    return 0
if __name__=="__main__": raise SystemExit(main())