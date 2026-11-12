"""Integration tests for Genkit dotprompt templates and Pydantic schemas (Phase 39, v4.8.0)."""

import json
import sys
from pathlib import Path

from pydantic import ValidationError

# Add project src directories to path so we can import schemas
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "05_Knowledge_Aggregator" / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "06_Formalized_Model" / "src"))

from schemas import IntakeExtractionSchema, AxiomaticTransformSchema  # type: ignore


def test_intake_extraction_valid():
    """Valid intake extraction should pass schema validation."""
    data = {
        "prov_entities": [
            {
                "id": "ent1",
                "type": "Entity",
                "attributes": {"label": "Document A"},
            }
        ],
        "skos_concepts": [
            {
                "id": "c1",
                "prefLabel": "Concept One",
                "altLabel": ["Concept 1 alt"],
                "broader": ["c2"],
                "narrower": [],
                "exactMatch": [],
                "closeMatch": [],
            }
        ],
    }
    validated = IntakeExtractionSchema(**data)
    assert len(validated.prov_entities) == 1
    assert validated.prov_entities[0].type == "Entity"
    assert len(validated.skos_concepts) == 1
    assert validated.skos_concepts[0].prefLabel == "Concept One"


def test_intake_extraction_invalid_missing_field():
    """Missing required field should raise ValidationError."""
    data = {
        "prov_entities": [
            {"id": "ent1", "type": "Entity"}  # missing attributes is ok, but id and type required
        ],
        # skos_concepts missing entirely
    }
    try:
        IntakeExtractionSchema(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass  # expected


def test_intake_extraction_invalid_wrong_type():
    """Wrong type for prov_entities should raise ValidationError."""
    data = {
        "prov_entities": "not a list",
        "skos_concepts": [],
    }
    try:
        IntakeExtractionSchema(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass  # expected


def test_axiomatic_transform_valid():
    """Valid axiomatic transformation should pass schema validation."""
    data = {
        "log_basis_transformations": [
            {
                "original_base": 10,
                "target_base": 2,
                "conversion_factor": 3.321928094887362,
                "values": [1.0, 2.0, 3.0],
                "transformed_values": [3.321928094887362, 6.643856189774724, 9.965784284662086],
            }
        ],
        "dft_frequency_transformations": [
            {
                "original_freq": 440.0,
                "scaled_freq": 440.0 * 2.0,
                "alpha": 2.0,
                "phase_shift": 0.0,
            }
        ],
    }
    validated = AxiomaticTransformSchema(**data)
    assert len(validated.log_basis_transformations) == 1
    assert validated.log_basis_transformations[0].original_base == 10
    assert len(validated.dft_frequency_transformations) == 1
    assert validated.dft_frequency_transformations[0].original_freq == 440.0


def test_axiomatic_transform_invalid_missing_field():
    """Missing required field should raise ValidationError."""
    data = {
        "log_basis_transformations": [
            {
                "original_base": 10,
                # missing target_base, conversion_factor, values, transformed_values
            }
        ],
        "dft_frequency_transformations": [],
    }
    try:
        AxiomaticTransformSchema(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass  # expected


def test_axiomatic_transform_invalid_wrong_type():
    """Wrong type for log_basis_transformations should raise ValidationError."""
    data = {
        "log_basis_transformations": "not a list",
        "dft_frequency_transformations": [],
    }
    try:
        AxiomaticTransformSchema(**data)
        assert False, "Expected ValidationError"
    except ValidationError:
        pass  # expected


if __name__ == "__main__":
    # Run all tests
    test_intake_extraction_valid()
    print("PASS: test_intake_extraction_valid")

    test_intake_extraction_invalid_missing_field()
    print("PASS: test_intake_extraction_invalid_missing_field")

    test_intake_extraction_invalid_wrong_type()
    print("PASS: test_intake_extraction_invalid_wrong_type")

    test_axiomatic_transform_valid()
    print("PASS: test_axiomatic_transform_valid")

    test_axiomatic_transform_invalid_missing_field()
    print("PASS: test_axiomatic_transform_invalid_missing_field")

    test_axiomatic_transform_invalid_wrong_type()
    print("PASS: test_axiomatic_transform_invalid_wrong_type")

    print("\nAll integration tests passed!")