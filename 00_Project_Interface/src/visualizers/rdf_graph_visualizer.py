#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rdf_graph_visualizer.py — Semantic Knowledge Network (v3.4.0)."""
from __future__ import annotations
import argparse
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT = PROJECT_ROOT / "00_Project_Interface" / "out" / "VISUAL_RDF_GRAPH.md"
def render_markdown() -> str:
    lines=["# RDF Knowledge Network (Bertin)","", "```mermaid","classDiagram","  class Node","  class Edge","  Node --> Edge","```",""]
    return "\n".join(lines)
def main(argv=None)->int:
    p=argparse.ArgumentParser(); p.add_argument("--export-md",action="store_true")
    args=p.parse_args(argv)
    md=render_markdown()
    if args.export_md: OUT.write_text(md,encoding="utf-8"); print(f"Exported {OUT}")
    else: print(md)
    return 0
if __name__=="__main__": raise SystemExit(main())