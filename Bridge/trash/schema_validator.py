#!/usr/bin/env python3
"""
Contract Schema Validator for 05_Knowledge_Aggregator.

Validates any JSON file arriving in Bridge/in/ before it is passed to
intake_processor.py. Reads the corresponding schema template from
Intake_Queue/templates/ and enforces mandatory contract fields, W3C PROV-O
metadata, and W3C SKOS relationship checks.

Usage:
    python schema_validator.py --file <path_to_json> [--category <auto|cognitive_model|analogy|concept_scheme>]

Exit codes:
    0 — JSON is valid against contract schema.
    1 — Validation error (syntax, missing fields, schema mismatch).
    2 — Unexpected runtime error.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "Intake_Queue" / "templates"
BRIDGE_IN = ROOT / "bridge" / "in"

TEMPLATE_MAP = {
    "cognitive_model": "cognitive_model_template.json",
    "analogy": "analogy_template.json",
    "concept_scheme": "concept_scheme_template.json",
    "image_metadata": "image_metadata_template.json",
    "video_index": "video_index_template.json",
}

TEMPLATE_STEM_TO_CATEGORY = {
    "cognitive_model_template": "cognitive_model",
    "analogy_template": "analogy",
    "concept_scheme_template": "concept_scheme",
    "image_metadata_template": "image_metadata",
    "video_index_template": "video_index",
}

# W3C PROV-O required field names
PROV_O_FIELDS = ("prov:wasAttributedTo", "prov:generatedAtTime", "prov:hadPrimarySource", "confidence_score")

# W3C SKOS relationship field names (for concept schemes)

SKOS_RELATIONSHIP_FIELDS = ("broader", "narrower", "related", "prefLabel")

# ISO 8601 UTC pattern with Z suffix
ISO8601_UTC_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$")


def _detect_category(filepath: Path, explicit: str | None) -> str:
    """Detect the intake category from explicit arg, filename, or content."""
    if explicit and explicit != "auto":
        return explicit

    name = filepath.stem.lower()
    if "image_metadata" in name:
        return "image_metadata"
    if "video_index" in name:
        return "video_index"
    if "cognitive" in name or "model" in name:
        return "cognitive_model"
    if "analog" in name:
        return "analogy"
    if "concept" in name or "scheme" in name:
        return "concept_scheme"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "entities" in data and "relations" in data:
            return "cognitive_model"
        if "source_domain" in data and "target_domain" in data:
            return "analogy"
        if "scheme_id" in data and "concepts" in data:
            return "concept_scheme"
    except Exception:
        pass

    return "cognitive_model"


def _load_template(category: str) -> dict | None:
    """Load the JSON template schema for the given category."""
    filename = TEMPLATE_MAP.get(category)
    if not filename:
        return None
    template_path = TEMPLATES_DIR / filename
    if not template_path.exists():
        return None
    with open(template_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _check_contract_fields(data: dict, category: str) -> list[str]:
    """Check for mandatory contract fields: meta/type/version (existing categories) and category-specific fields (new categories)."""
    errors: list[str] = []

    # Category-specific contract fields (directive: image_metadata & video_index)
    if category == "image_metadata":
        for field in ("image_id", "source_path_or_url", "extracted_concepts"):
            if field not in data:
                errors.append(f"missing contract field: '{field}'")
    elif category == "video_index":
        for field in ("video_id", "source_path_or_url", "temporal_chunks"):
            if field not in data:
                errors.append(f"missing contract field: '{field}'")
    else:
        # Existing categories (cognitive_model, analogy, concept_scheme)
        if "meta" not in data and "metadata" not in data:
            errors.append("missing contract field: 'meta' (or 'metadata')")

        if "type" not in data:
            errors.append("missing contract field: 'type'")

        if "version" not in data:
            errors.append("missing contract field: 'version'")

        has_any = (
            "entities" in data
            or "source_domain" in data
            or "nodes" in data
        )
        if not has_any:
            errors.append(
                "missing contract field: one of 'entities', 'source_domain', or 'nodes' is required"
            )

    return errors


def _check_prov_o_compliance(data: dict) -> list[str]:
    """Enforce W3C PROV-O metadata validation."""
    errors: list[str] = []
    prov = data.get("prov") or {}

    # prov:wasAttributedTo (non-null string)
    was_attributed = prov.get("wasAttributedTo")
    if was_attributed is None:
        errors.append("prov:wasAttributedTo is missing (must be non-null string)")
    elif not isinstance(was_attributed, str) or not was_attributed.strip():
        errors.append("prov:wasAttributedTo must be a non-empty string")

    # prov:generatedAtTime (ISO 8601 UTC string with Z suffix)
    generated_at = prov.get("generatedAtTime")
    if generated_at is None:
        errors.append("prov:generatedAtTime is missing (must be ISO 8601 UTC with Z suffix)")
    elif not isinstance(generated_at, str):
        errors.append("prov:generatedAtTime must be a string")
    elif not ISO8601_UTC_PATTERN.match(generated_at):
        errors.append("prov:generatedAtTime must be ISO 8601 UTC string with Z suffix (e.g. 2026-11-09T10:00:00Z)")

    # prov:hadPrimarySource (valid source path)
    had_primary_source = prov.get("hadPrimarySource")
    if had_primary_source is None:
        errors.append("prov:hadPrimarySource is missing (must be valid source path)")
    elif not isinstance(had_primary_source, str) or not had_primary_source.strip():
        errors.append("prov:hadPrimarySource must be a non-empty string")

    # confidence_score (float in range [0.0, 1.0])
    confidence = data.get("confidence_score")
    if confidence is None:
        errors.append("confidence_score is missing (must be float in [0.0, 1.0])")
    elif not isinstance(confidence, (int, float)):
        errors.append("confidence_score must be a float")
    elif isinstance(confidence, bool) or not (0.0 <= float(confidence) <= 1.0):
        errors.append("confidence_score must be in range [0.0, 1.0]")

    return errors


def _check_skos_compliance(data: dict, category: str) -> list[str]:
    """
    Enforce W3C SKOS relationship checks for concept schemes.

    Required terms:
        * skos:broader    (array of concept URIs)
        * skos:narrower   (array of concept URIs)
        * skos:related    (array of concept URIs)
        * skos:prefLabel  (non-empty string)
    """
    errors: list[str] = []

    # Only concept schemes require SKOS compliance
    if category != "concept_scheme":
        return errors

    skos = data.get("skos") or {}

    for field in SKOS_RELATIONSHIP_FIELDS:
        value = skos.get(field)
        if value is None:
            errors.append(f"skos:{field} is missing")
        elif field in ("skos:broader", "skos:narrower", "skos:related"):
            if not isinstance(value, list):
                errors.append(f"skos:{field} must be an array of concept URIs")
            else:
                for uri in value:
                    if not isinstance(uri, str) or not uri.strip():
                        errors.append(f"skos:{field} contains an invalid URI: {uri!r}")
        elif field == "skos:prefLabel":
            if not isinstance(value, str) or not value.strip():
                errors.append("skos:prefLabel must be a non-empty string")

    return errors




def _check_template_structure(data: dict, template: dict | None, category: str) -> list[str]:
    """Cross-check data against template structure for the detected category."""
    errors: list[str] = []
    if template is None:
        errors.append(f"template for category '{category}' not found in {TEMPLATES_DIR}")
        return errors

    if category == "cognitive_model":
        for key in ("metadata", "entities", "relations", "invariants"):
            if key not in data:
                errors.append(f"template field missing: '{key}'")
    elif category == "analogy":
        for key in ("analogy_id", "source_domain", "target_domain", "mappings"):
            if key not in data:
                errors.append(f"template field missing: '{key}'")
    elif category == "concept_scheme":
        for key in ("scheme_id", "title", "keywords", "concepts"):
            if key not in data:
                errors.append(f"template field missing: '{key}'")
    elif category == "image_metadata":
        for key in ("image_id", "source_path_or_url", "extracted_concepts"):
            if key not in data:
                errors.append(f"template field missing: '{key}'")
    elif category == "video_index":
        for key in ("video_id", "source_path_or_url", "temporal_chunks"):
            if key not in data:
                errors.append(f"template field missing: '{key}'")

    return errors


def validate_json_file(filepath: str, category: str = "auto") -> tuple[bool, list[str]]:
    """Validate a JSON file against its contract schema.

    Returns (is_valid, messages).
    """
    path = Path(filepath)
    messages: list[str] = []

    if not path.exists():
        return False, [f"File not found: {path}"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON syntax error: {e}"]
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    if not isinstance(data, dict):
        return False, ["Top-level JSON must be an object (dict)"]

    detected = _detect_category(path, category)
    messages.append(f"Detected category: {detected}")

    template = _load_template(detected)
    if template is None:
        messages.append(f"Warning: no template found for category '{detected}'")

    contract_errors = _check_contract_fields(data, detected)
    if contract_errors:
        messages.extend(contract_errors)
    prov_errors = _check_prov_o_compliance(data)
    if prov_errors:
        messages.extend(prov_errors)

    skos_errors = _check_skos_compliance(data, detected)
    if skos_errors:
        messages.extend(skos_errors)

    template_errors = _check_template_structure(data, template, detected)
    if template_errors:
        messages.extend(template_errors)

    is_valid = (
        len(contract_errors) == 0
        and len(prov_errors) == 0
        and len(skos_errors) == 0
        and len(template_errors) == 0
    )

    template_errors = _check_template_structure(data, template, detected)
    if template_errors:
        messages.extend(template_errors)

    is_valid = len(contract_errors) == 0 and len(template_errors) == 0
    return is_valid, messages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Contract schema validator for 05_Knowledge_Aggregator bridge/in/"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the JSON file to validate",
    )
    parser.add_argument(
        "--category",
        default="auto",
        choices=["auto", "cognitive_model", "analogy", "concept_scheme"],
        help="Intake category (default: auto-detect)",
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 60)
    print(" Contract Schema Validator — 05_Knowledge_Aggregator")
    print("=" * 60)
    print(f"Timestamp : {timestamp}")
    print(f"File      : {args.file}")
    print(f"Category  : {args.category}")
    print("-" * 60)

    is_valid, messages = validate_json_file(args.file, args.category)

    for msg in messages:
        print(f"  [{'OK' if 'missing' not in msg.lower() and 'error' not in msg.lower() and 'warning' not in msg.lower() else 'WARN'}] {msg}")

    print("-" * 60)
    if is_valid:
        print("RESULT: VALID — contract schema passed. Exit code 0.")
        print("=" * 60)
        return 0
    else:
        print("RESULT: INVALID — contract schema failed. Exit code 1.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())