#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
00_Project_Interface/src/context_view.py — Dashboard Node (v2.7.0).

Inspects knowledge graph state, normalized triple counts in
05_Knowledge_Aggregator/Processed_Gate/normalized_triples/, OWL shapes in
01_Formal_Core, and assembled target models in 06_Formalized_Model.

Supports --test flag returning exit_code: 0 on clean state.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TRIPLES_DIR = PROJECT_ROOT / "05_Knowledge_Aggregator" / "Processed_Gate" / "normalized_triples"
OWL_DIR = PROJECT_ROOT / "01_Formal_Core" / "src" / "01_Formal_Ontologies"
TARGET_MODELS_DIR = PROJECT_ROOT / "06_Formalized_Model"


def _count_files(path: Path, pattern: str = "*") -> int:
    if not path.exists():
        return 0
    return len([p for p in path.glob(pattern) if p.is_file()])


def _list_files(path: Path, pattern: str = "*") -> list[str]:
    if not path.exists():
        return []
    return sorted(p.name for p in path.glob(pattern) if p.is_file())


def inspect_context() -> dict[str, Any]:
    normalized_triples_count = _count_files(TRIPLES_DIR)
    triple_files = _list_files(TRIPLES_DIR)

    owl_files = _list_files(OWL_DIR, "*.ttl") + _list_files(OWL_DIR, "*.owl")
    owl_shapes = _list_files(OWL_DIR)

    target_models = _list_files(TARGET_MODELS_DIR, "*")

    clean = True
    issues: list[str] = []
    if not TRIPLES_DIR.exists():
        clean = False
        issues.append(f"Missing normalized triples dir: {TRIPLES_DIR}")
    if not OWL_DIR.exists():
        clean = False
        issues.append(f"Missing OWL shapes dir: {OWL_DIR}")
    if not TARGET_MODELS_DIR.exists():
        clean = False
        issues.append(f"Missing target models dir: {TARGET_MODELS_DIR}")

    return {
        "timestamp": __import__("datetime").datetime.now().astimezone().isoformat(),
        "normalized_triples_dir": str(TRIPLES_DIR),
        "normalized_triples_count": normalized_triples_count,
        "triple_files": triple_files,
        "owl_shapes_dir": str(OWL_DIR),
        "owl_shapes": owl_shapes,
        "target_models_dir": str(TARGET_MODELS_DIR),
        "target_models": target_models,
        "clean": clean,
        "issues": issues,
    }


def print_report(report: dict[str, Any]) -> None:
    print("=" * 68)
    print(" 00_Project_Interface — Context Diagnostic Summary (v2.7.0)")
    print("=" * 68)
    print(f" Timestamp         : {report['timestamp']}")
    print("-" * 68)
    print(" Normalized Triples (05_Knowledge_Aggregator)")
    print(f"  Dir              : {report['normalized_triples_dir']}")
    print(f"  Triple files     : {report['normalized_triples_count']}")
    for name in report["triple_files"]:
        print(f"   - {name}")
    print("-" * 68)
    print(" OWL Shapes (01_Formal_Core)")
    print(f"  Dir              : {report['owl_shapes_dir']}")
    print(f"  Shape files      : {len(report['owl_shapes'])}")
    for name in report["owl_shapes"]:
        print(f"   - {name}")
    print("-" * 68)
    print(" Target Models (06_Formalized_Model)")
    print(f"  Dir              : {report['target_models_dir']}")
    print(f"  Model entries    : {len(report['target_models'])}")
    for name in report["target_models"]:
        print(f"   - {name}")
    print("-" * 68)
    print(f" Context clean     : {report['clean']}")
    if report["issues"]:
        print(" Issues:")
        for issue in report["issues"]:
            print(f"   - {issue}")
    print("=" * 68)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="context_view.py",
        description="00_Project_Interface context diagnostic (v2.7.0)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run in test mode; exit_code 0 on clean state.",
    )
    args = parser.parse_args(argv)

    report = inspect_context()
    print_report(report)

    if args.test:
        return 0 if report["clean"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
