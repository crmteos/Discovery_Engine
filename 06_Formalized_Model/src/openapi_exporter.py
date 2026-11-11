#!/usr/bin/env python3
"""openapi_exporter.py - Translate the assembled model into OpenAPI 3.1 & JSON-LD 1.1."""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

OPENAPI_3_1_NS = "https://spec.openapis.org/oas/3.1.0"
JSON_LD_CONTEXT = "https://json-ld.org/contexts/schema.org"


def export_openapi_31(model_data: Dict[str, Any], title: str = "Model API") -> Dict[str, Any]:
    """Translate the assembled model into OpenAPI 3.1 specification."""
    paths = {}
    components = {
        "schemas": {},
        "securitySchemes": {},
        "parameters": {},
        "responses": {},
    }

    # Extract structural view for API endpoints
    structural = model_data.get("structural_view", {}) or model_data.get("structural", {})
    nodes = structural.get("nodes", [])
    edges = structural.get("edges", [])

    # Generate API paths from edges (relationships)
    for i, edge in enumerate(edges):
        src = edge.get("source", f"resource{i}")
        tgt = edge.get("target", f"resource{i+1}")
        method = edge.get("method", "GET").upper()
        label = edge.get("label", "").lower().replace(" ", "-")

        if not paths.get(src):
            paths[src] = {}

        path_item = {
            method: {
                "operationId": f"{method.lower()}_{label}",
                "summary": f"{method} {label}",
                "description": f"{method} operation for {label}",
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/" + tgt}
                            }
                        },
                    },
                    "400": {"description": "Bad request"},
                    "404": {"description": "Not found"},
                },
            }
        }

        paths[src][method] = path_item.get(method, {})

    openapi = {
        "openapi": "3.1.0",
        "info": {"title": title, "version": "v2.6.0"},
        "paths": paths if paths else {"/": {"get": {"description": "Default endpoint", "responses": {"200": {"description": "OK"}}}}},
        "components": components,
        "servers": [{"url": "", "description": "Default server"}],
    }

    return openapi


def export_json_ld(model_data: Dict[str, Any]) -> Dict[str, Any]:
    """Translate the assembled model into JSON-LD 1.1 context."""
    context = {
        "@context": JSON_LD_CONTEXT,
        "@type": "obo:Entity",
    }

    # Map model fields to JSON-LD
    structural = model_data.get("structural_view", {}) or model_data.get("structural", {})
    parametric = model_data.get("parametric_view", {}) or model_data.get("parametric", {})

    # Build subject node
    subject = {
        "@id": structural.get("nodes", [{}])[0].get("id", "model") if structural.get("nodes") else "model",
        "@type": "Model:" + structural.get("view_type", ""),
    }

    # Add invariants as properties
    invariants = parametric.get("mathematical_invariants", [])
    if invariants:
        subject["obo:invariant"] = invariants

    # Add provenance
    metadata = model_data.get("metadata", {})
    if metadata:
        prov = metadata.get("prov", {})
        if prov:
            subject["prov:wasGeneratedBy"] = {"@type": "prov:Generation", "generateAt": list(prov.keys())}

    json_ld = {"@graph": [subject]}
    return json_ld


def export_model(model_data: Dict[str, Any], output_dir: Path) -> Dict[str, Any]:
    """Export the model in both OpenAPI 3.1 and JSON-LD 1.1 formats."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export OpenAPI 3.1
    openapi_spec = export_openapi_31(model_data, title="Discovery Engine Model API")
    openapi_path = output_dir / "openapi_31.json"
    with open(openapi_path, "w", encoding="utf-8") as f:
        json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
    print(f"Exported OpenAPI 3.1 to: {openapi_path}")

    # Export JSON-LD 1.1
    json_ld_spec = export_json_ld(model_data)
    json_ld_path = output_dir / "json_ld_11.json"
    with open(json_ld_path, "w", encoding="utf-8") as f:
        json.dump(json_ld_spec, f, indent=2, ensure_ascii=False)
    print(f"Exported JSON-LD 1.1 to: {json_ld_path}")

    return {"openapi_31": openapi_path, "json_ld_11": json_ld_path}


def main():
    """CLI entry point."""
    import argparse
    parser = argparse.ArgumentParser(description="Export model in OpenAPI 3.1 & JSON-LD 1.1.")
    parser.add_argument("--model", type=Path, required=True, help="Path to assembled model JSON.")
    parser.add_argument("--output", type=Path, default=None, help="Output directory.")
    args = parser.parse_args()
    if args.model and args.model.exists():
        with open(args.model, "r", encoding="utf-8") as f:
            model_data = json.load(f)
        output_dir = args.output or Path(".")
        result = export_model(model_data, output_dir)
        print(f"Exported: {result}")
    else:
        print(f"Model file not found: {args.model}")
        sys.exit(1)


if __name__ == "__main__":
    main()