#!/usr/bin/env python3
"""Axiomatic Converter: Translates human-centric data into formal invariants."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGGREGATOR_ROOT = PROJECT_ROOT / "05_Knowledge_Aggregator"
BRIDGE_DIR = AGGREGATOR_ROOT.parent / "Bridge"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(BRIDGE_DIR))


def parse_anthropomorphic_markers(data):
    """Detect and extract anthropomorphic markers from input data."""
    markers = {
        "has_timestamp": False,
        "has_spatial_coordinates": False,
        "has_human_perceptual_labels": False,
        "timestamp_value": None,
        "spatial_coords": None,
        "perceptual_labels": [],
    }

    if not isinstance(data, dict):
        return markers

    if "timestamp" in data:
        markers["has_timestamp"] = True
        markers["timestamp_value"] = data["timestamp"]

    if "spatial_coordinates" in data:
        markers["has_spatial_coordinates"] = True
        markers["spatial_coords"] = data["spatial_coordinates"]

    for key, value in data.items():
        key_lower = key.lower()
        if any(prefix in key_lower for prefix in ["human", "optical", "visual", "sensory", "perceptual"]):
            if isinstance(value, str):
                markers["perceptual_labels"].append(value)
            elif isinstance(value, list):
                markers["perceptual_labels"].extend(value)

    return markers


def map_temporal_to_causal(input_data):
    """Map temporal sequences to prov:wasInfluencedBy and prov:wasDerivedFrom causal order chains."""
    markers = parse_anthropomorphic_markers(input_data)

    if not markers["has_timestamp"]:
        return {"causal_chains": [], "prov_annotations": {}}

    timestamp = markers["timestamp_value"]

    if isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            iso_timestamp = dt.isoformat()
        except ValueError:
            iso_timestamp = timestamp
    elif isinstance(timestamp, datetime):
        iso_timestamp = timestamp.isoformat()
    else:
        iso_timestamp = str(timestamp)

    chain_id = f"causal_chain_{uuid4().hex[:8]}"

    causal_chains = [
        {
            "chain_id": chain_id,
            "timestamp": iso_timestamp,
            "prov_terms": [
                f"prov:wasInfluencedBy_{uuid4().hex[:8]}",
                f"prov:wasDerivedFrom_{uuid4().hex[:8]}"
            ]
        }
    ]

    prov_annotations = {
        "was_influenced_by": chain_id,
        "was_derived_from": chain_id,
        "generated_at": iso_timestamp
    }

    return {
        "causal_chains": causal_chains,
        "prov_annotations": prov_annotations
    }


def map_spatial_to_topological(input_data):
    """Map spatial metrics to skos:related topological vector relations."""
    markers = parse_anthropomorphic_markers(input_data)

    if not markers["has_spatial_coordinates"]:
        return {"spatial_invariants": [], "topological_relations": {}}

    coords = markers["spatial_coords"] if markers["spatial_coords"] else None

    if coords is None or not isinstance(coords, dict):
        return {"spatial_invariants": [], "topological_relations": {}}

    x = coords.get("x", 0)
    y = coords.get("y", 0)
    z = coords.get("z", 0)

    vector_id = f"spatial_vector_{uuid4().hex[:8]}"

    spatial_invariants = [
        {
            "vector_id": vector_id,
            "coordinate_bounds": {"x": x, "y": y, "z": z},
            "topological_relation": "skos:related",
            "spatial_qualities": {
                "connectedness": "connected" if all(c is not None for c in [x, y, z]) else "disconnected",
                "proximity": "relative_proximity",
                "orientation": "cartesian_orientation"
            }
        }
    ]

    topological_relations = {
        "vector_reference": vector_id,
        "x_coordinate": x,
        "y_coordinate": y,
        "z_coordinate": z,
        "relation_type": "skos:related"
    }

    return {
        "spatial_invariants": spatial_invariants,
        "topological_relations": topological_relations
    }


def generate_de_anthropomorphized_triples(input_data):
    """Generate de-anthropomorphized RDF triples from input data."""
    causal_result = map_temporal_to_causal(input_data)
    spatial_result = map_spatial_to_topological(input_data)
    provenance = input_data.get("prov_annotations", {})

    triples = []

    triple_set_id = f"triple_{uuid4().hex[:8]}"

    for chain in causal_result["causal_chains"]:
        triples.append({
            "subject": triple_set_id,
            "predicate": "prov:wasDerivedFrom",
            "object": chain["chain_id"],
            "prov_type": "causal_chain"
        })
        triples.append({
            "subject": triple_set_id,
            "predicate": "prov:wasInfluencedBy",
            "object": chain["chain_id"],
            "prov_type": "causal_chain"
        })

    if causal_result["prov_annotations"]:
        for key, value in causal_result["prov_annotations"].items():
            triples.append({
                "subject": triple_set_id,
                "predicate": f"prov:{key}",
                "object": value,
                "prov_type": "temporal_annotation"
            })

    for inv in spatial_result["spatial_invariants"]:
        triples.append({
            "subject": triple_set_id,
            "predicate": "skos:related",
            "object": inv["vector_id"],
            "prov_type": "spatial_invariant"
        })
        triples.append({
            "subject": inv["vector_id"],
            "predicate": "a",
            "object": "skos:Concept",
            "prov_type": "spatial_concept"
        })
        triples.append({
            "subject": inv["vector_id"],
            "predicate": "skos:topologicalVector",
            "object": str(inv["coordinate_bounds"]),
            "prov_type": "spatial_vector"
        })

    if spatial_result["topological_relations"]:
        for key, value in spatial_result["topological_relations"].items():
            triples.append({
                "subject": triple_set_id,
                "predicate": f":{key}",
                "object": value,
                "prov_type": "spatial_attribute"
            })

    if provenance:
        for key, value in provenance.items():
            triples.append({
                "subject": triple_set_id,
                "predicate": f"prov:{key}",
                "object": str(value),
                "prov_type": "original_provenance"
            })

    if "content" in input_data:
        triples.append({
            "subject": triple_set_id,
            "predicate": "rdf:value",
            "object": input_data["content"],
            "prov_type": "propositional_content"
        })

    return triples


def convert(input_path, output_path=None):
    """Main conversion function: read input, convert, and write output."""
    input_str = str(input_path)
    with open(input_str, 'r', encoding='utf-8') as f:
        if input_str.endswith('.json'):
            data = json.load(f)
        elif input_str.endswith('.rdf') or input_str.endswith('.ttl'):
            data = {"content": f.read(), "format": "rdf"}
        else:
            data = {"content": f.read()}

    triples = generate_de_anthropomorphized_triples(data)

    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "triple_set_id": triples[0]["subject"] if triples else "unknown",
                "triple_count": len(triples),
                "triples": triples,
                "conversion_timestamp": datetime.now(timezone.utc).isoformat(),
                "source_format": "anthropomorphic_to_invariant"
            }, f, indent=2, ensure_ascii=False)

        print(f"Output written to: {output_file}")

    return triples


def smoke_test():
    """Run a smoke test to verify the converter compiles and executes correctly."""
    print("Running Axiomatic Converter smoke test...")

    test_input = {
        "timestamp": "2024-01-15T10:30:00Z",
        "spatial_coordinates": {"x": 1.0, "y": 2.0, "z": 3.0},
        "human_perceptual_label": "observed at position",
        "content": "knowledge graph integration pattern",
        "prov_annotations": {"source": "audit_validated"}
    }

    test_input_path = PROJECT_ROOT / "test_input_axiomatic.json"
    with open(test_input_path, 'w', encoding='utf-8') as f:
        json.dump(test_input, f, indent=2)

    output_path = PROJECT_ROOT / "test_output_axiomatic_triples.json"
    triples = convert(test_input_path, output_path)

    if triples and len(triples) > 0:
        print(f"Smoke test passed: {len(triples)} triples generated")
        print(f"  - Triple set ID: {triples[0].get('subject', 'N/A')}")
        return True
    else:
        print("Smoke test failed: No triples generated")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke-test":
        success = smoke_test()
        sys.exit(0 if success else 1)

    if len(sys.argv) < 2:
        print("Usage: python axiomatic_converter.py <input_path> [output_path]")
        print("      python axiomatic_converter.py --smoke-test")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    triples = convert(input_path, output_path)
    print(f"Conversion complete: {len(triples)} triples generated")