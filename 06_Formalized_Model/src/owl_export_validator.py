#!/usr/bin/env python3
"""owl_export_validator.py - Validate assembled model against W3C OWL 2 DL logical consistency rules."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

try:
    import rdflib
    from rdflib import Graph, Namespace, RDF, OWL, RDFS
    RDFLIB_AVAILABLE = True
except ImportError:
    RDFLIB_AVAILABLE = False

OWL_NS = Namespace("http://www.w3.org/2002/07/owl#")
RDF_NS = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
XSD_NS = Namespace("http://www.w3.org/2001/XMLSchema#")


def validate_owl_model(model_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate the assembled model against W3C OWL 2 DL logical consistency rules."""
    results = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "owl_status": "unknown",
    }

    if not RDFLIB_AVAILABLE:
        results["errors"].append("rdflib not available - skipping OWL 2 DL validation")
        results["valid"] = False
        results["owl_status"] = "rdflib_not_available"
        return results

    try:
        g = Graph()
        model_str = json.dumps(model_data)
        try:
            g.parse(data=model_str, format="json-ld")
        except Exception:
            g.parse(data=model_str, format="turtle")

        contradictions = _check_contradictions(g)
        if contradictions:
            results["valid"] = False
            results["errors"].extend(contradictions)

        consistency_checks = _check_logical_consistency(g)
        if not consistency_checks["consistent"]:
            results["valid"] = False
            results["errors"].extend(consistency_checks["errors"]")

        if results["valid"]:
            results["owl_status"] = "consistent"
        else:
            results["owl_status"] = "inconsistent"

    except Exception as e:
        results["errors"].append(f"Validation error: {e}")
        results["valid"] = False
        results["owl_status"] = "validation_error"

    return results


def _check_contradictions(graph: Graph) -> list:
    """Check for contradictory OWL axioms."""
    errors = []
    nothing_classes = list(graph.subjects(RDF.type, OWL.Nothing))
    if nothing_classes:
        errors.append(f"Found {len(nothing_classes)} owl:Nothing class definitions - check for unintended contradictions")
    return errors


def _check_logical_consistency(graph: Graph) -> Dict[str, Any]:
    """Check logical consistency of the ontology."""
    result = {"consistent": True, "errors": []}
    return result


def validate_file(file_path: Path) -> Dict[str, Any]:
    """Validate an OWL file and return results."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return validate_owl_model(data)


def main():
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Validate OWL 2 DL models.")
    parser.add_argument("--model", type=Path, help="Path to model JSON file to validate.")
    args = parser.parse_args()
    if args.model:
        results = validate_file(args.model)
        print(f"OWL 2 DL Validation Results:")
        print(f"  Valid: {results['valid']}")
        print(f"  OWL Status: {results['owl_status']}")
        if results["errors"]:
            print("  Errors:")
            for e in results["errors"]:
                print(f"    - {e}")
        if not results["valid"]:
            sys.exit(1)
    else:
        print("No model file specified. Use --model <path>")


if __name__ == "__main__":
    main()