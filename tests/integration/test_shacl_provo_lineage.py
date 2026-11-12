"""Integration tests for SHACL validator and PROV-O lineage auditor."""

import sys
from pathlib import Path

# Ensure project root and node 06 src are on path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "06_Formalized_Model" / "src"))

from shacl_validator import SHACLValidator  # type: ignore
from provo_lineage import PROVOLineageAuditor  # type: ignore


def test_shacl_validator_valid_triples():
    """SHACLValidator should accept triples with all required fields."""
    validator = SHACLValidator()
    triples = [
        {
            "subject": "ex:entity1",
            "predicate": "ex:pred1",
            "object": "ex:obj1",
            "prov:wasDerivedFrom": "ex:source1",
        },
        {
            "subject": "ex:entity2",
            "predicate": "ex:pred2",
            "object": "ex:obj2",
            # missing prov:wasDerivedFrom -> should be invalid
        },
    ]
    result = validator.validate(triples)
    assert len(result["valid"]) == 1, f"Expected 1 valid, got {len(result['valid'])}"
    assert len(result["invalid"]) == 1, f"Expected 1 invalid, got {len(result['invalid'])}"
    print("test_shacl_validator_valid_triples PASSED")


def test_shacl_validator_shape_validation():
    """SHACLValidator.shape validation should filter by allowed predicates."""
    validator = SHACLValidator()
    triples = [
        {"subject": "ex:s1", "predicate": "ex:allowed", "object": "ex:o1", "prov:wasDerivedFrom": "ex:src1"},
        {"subject": "ex:s2", "predicate": "ex:forbidden", "object": "ex:o2", "prov:wasDerivedFrom": "ex:src2"},
    ]
    shapes = {"predicates": ["ex:allowed"]}
    result = validator.validate_shape(triples, shapes)
    assert len(result["valid"]) == 1
    assert len(result["invalid"]) == 1
    print("test_shacl_validator_shape_validation PASSED")


def test_provo_lineage_generate():
    """PROVOLineageAuditor should generate provenance dict with required keys."""
    auditor = PROVOLineageAuditor()
    prov = auditor.generate_provenance(
        entity_id="ex:result1",
        activity_id="ex:act1",
        agent_id="ex:agent1",
        was_generated_by="ex:act1",
        was_derived_from="ex:src1",
    )
    validation = auditor.validate_provenance(prov)
    assert "prov:Entity" in validation["present"]
    assert "prov:wasGeneratedBy" in validation["present"]
    assert "prov:wasDerivedFrom" in validation["present"]
    assert validation["missing"] == []
    print("test_provo_lineage_generate PASSED")


def test_provo_lineage_missing():
    """PROVOLineageAuditor.validate_provenance should detect missing required keys."""
    auditor = PROVOLineageAuditor()
    prov = {"prov:Entity": "ex:result1"}  # missing wasGeneratedBy, wasDerivedFrom
    validation = auditor.validate_provenance(prov)
    assert "prov:Entity" in validation["present"]
    assert "prov:wasGeneratedBy" in validation["missing"]
    assert "prov:wasDerivedFrom" in validation["missing"]
    print("test_provo_lineage_missing PASSED")


def main():
    test_shacl_validator_valid_triples()
    test_shacl_validator_shape_validation()
    test_provo_lineage_generate()
    test_provo_lineage_missing()
    print("\nAll integration tests PASSED")


if __name__ == "__main__":
    main()