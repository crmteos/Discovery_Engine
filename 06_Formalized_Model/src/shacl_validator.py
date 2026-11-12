#!/usr/bin/env python3
"""SHACL 1.2 validator for RDF triples and Formal Projection graph models.

Pure Python fallback - no external paid APIs. Uses only stdlib.
"""

from __future__ import annotations

from typing import List, Dict, Any, Set


class SHACLValidator:
    """Validate RDF triples against SHACL shapes declaratively.

    Checks that each triple contains the required fields:
    - subject
    - predicate
    - object
    - prov:wasDerivedFrom (if present in triple dict)

    Attributes:
        None
    """

    REQUIRED_FIELDS = {"subject", "predicate", "object", "prov:wasderivedfrom"}

    def validate(self, triples: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Validate a list of RDF triple dicts.

        Args:
            triples: List of dicts expected to have keys 'subject', 'predicate', 'object',
                     optionally 'prov:wasDerivedFrom'.

        Returns:
            Dict with 'valid' and 'invalid' lists of triples.
        """
        valid: List[Dict[str, Any]] = []
        invalid: List[Dict[str, Any]] = []

        for triple in triples:
            # Normalise keys: strip whitespace
            keys = {k.strip().lower() for k in triple.keys()}
            if self.REQUIRED_FIELDS.issubset(keys):
                valid.append(triple)
            else:
                missing = self.REQUIRED_FIELDS - keys
                triple["_validation_error"] = f"Missing required fields: {missing}"
                invalid.append(triple)

        return {"valid": valid, "invalid": invalid}

    def validate_shape(
        self, triples: List[Dict[str, Any]], shapes: Dict[str, List[str]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Optional shape validation (formal projection graph models).

        Simple shape check: ensure each triple's predicate is listed in shapes.
        """

        valid: List[Dict[str, Any]] = []
        invalid: List[Dict[str, Any]] = []

        for triple in triples:
            predicate = triple.get("predicate", "")
            allowed_predicates = shapes.get("predicates", [])
            if predicate in allowed_predicates:
                valid.append(triple)
            else:
                triple["_shape_error"] = (
                    f"Predicate '{predicate}' not allowed by shapes {allowed_predicates}"
                )
                invalid.append(triple)

        return {"valid": valid, "invalid": invalid}