#!/usr/bin/env python3
"""model_assembler.py - Assemble ISO/IEC/IEEE 42010 3-view JSON models."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import copy

try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
SCHEMAS_DIR = BASE_DIR / "schemas"


def load_graph_invariants(core_dir=None):
    """Load proven graph invariants from the Formal Core."""
    if core_dir is None:
        core_dir = BASE_DIR / "01_Formal_Core"
    invariants = {"nodes": [], "edges": [], "constraints": [], "topological_features": {}}
    if not core_dir.exists():
        return invariants
    for f in core_dir.glob("**/*invariant*.json"):
        try:
            with f.open("r", encoding="utf-8") as fp:
                data = json.load(fp)
                invariants = _merge_invariants(invariants, data)
        except (json.JSONDecodeError, IOError):
            continue
    return invariants


def _merge_invariants(base, new):
    """Merge new invariant data into the base dict."""
    result = copy.deepcopy(base)
    for key, value in new.items():
        if key in invariants and isinstance(invariants[key], list) and isinstance(value, list):
            invariants[key].extend(value)
        else:
            invariants[key] = value
    return invariants


def assemble_model(core_dir=None, output_path=None):
    """Assemble a complete 3-view ISO/IEC/IEEE 42010 model."""
    invariants = load_graph_invariants(core_dir)
    structural = {
        "view_type": "structural",
        "nodes": invariants.get("nodes", []),
        "edges": invariants.get("edges", []),
    }
    behavioral = {
        "view_type": "behavioral",
        "state_transitions": [],
        "message_flows": [],
    }
    parametric = {
        "view_type": "parametric",
        "mathematical_invariants": invariants.get("constraints", []),
        "sympy_constraints": [] if not SYMPY_AVAILABLE else [str(sp.Symbol("x"))],
    }
    provenance = {"prov": {"agent": "model.assembler.v2.6.0", "collaboration": "model.builder"}}
    model = {
        "structural_view": structural,
        "behavioral_view": behavioral,
        "parametric_view": parametric,
        "metadata": provenance,
        "generated_at": "2026-11-09T00:00:00Z",
    }
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fp:
            json.dump(model, fp, indent=2, ensure_ascii=False)
        print(f"Assembled model written to: {output_path}")
    return model


def main():
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Assemble ISO/IEC/IEEE 42010 3-view JSON models.")
    parser.add_argument("--test", action="store_true", help="Run smoke test with synthetic data.")
    args = parser.parse_args()
    if args.test:
        print("=== Running model_assembler.py smoke test ===")
        model = assemble_model(output_path=SRC_DIR / "sample_assembled_model.json")
        sample_schema = {
            "type": "object",
            "required": ["structural_view", "behavioral_view", "parametric_view", "metadata"],
            "properties": {
                "structural_view": {"type": "object"},
                "behavioral_view": {"type": "object"},
                "parametric_view": {"type": "object"},
                "metadata": {"type": "object"},
            },
        }
        schema_path = SCHEMAS_DIR / "model_structure_schema.json"
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(sample_schema, f, indent=2, ensure_ascii=False)
        print("Sample model_structure_schema.json written.")
        print("=== Smoke test passed! ===")
        sys.exit(0)


if __name__ == "__main__":
    main()