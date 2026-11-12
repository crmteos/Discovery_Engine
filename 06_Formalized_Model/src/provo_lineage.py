#!/usr/bin/env python3
"""W3C PROV-O Lineage Auditor.

Generates and validates PROV-O provenance graphs for axiomatic transformations.

Entities, Activities, Agents, wasDerivedFrom, wasGeneratedBy.
Pure Python, no external paid APIs.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional


class PROVOLineageAuditor:
    """Audit PROV-O lineage for fact transformations.

    Provides methods to create PROV-O graph records and validate that
    required PROV-O relationships are present.
    """

    # PROV-O core constants
    NS = "http://www.w3.org/ns/prov#"

    def generate_provenance(
        self,
        *,
        entity_id: str,
        activity_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        was_generated_by: Optional[str] = None,
        was_derived_from: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate a PROV-O provenance dict.

        Args:
            entity_id: Identifier of the resulting entity.
            activity_id: Identifier of the activity that produced the entity.
            agent_id: Identifier of the agent that performed the activity.
            was_generated_by: Identifier of the activity that generated this entity.
            was_derived_from: Identifier of the entity from which this was derived.

        Returns:
            Dict representing PROV-O statements.
        """
        provenance: Dict[str, Any] = {
            "prov:Entity": {"id": entity_id},
        }
        if activity_id:
            provenance["prov:Activity"] = {"id": activity_id}
        if agent_id:
            provenance["prov:Agent"] = {"id": agent_id}
        if was_generated_by:
            provenance["prov:wasGeneratedBy"] = {"id": was_generated_by}
        if was_derived_from:
            provenance["prov:wasDerivedFrom"] = {"id": was_derived_from}

        return provenance

    def validate_provenance(self, provenance: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate that a PROV-O provenance dict contains required relationships.

        Returns:
            Dict with 'present' and 'missing' lists of relationship keys.
        """
        required = {"prov:Entity", "prov:wasGeneratedBy", "prov:wasDerivedFrom"}
        present = [k for k in provenance.keys() if k in required]
        missing = [k for k in required if k not in provenance]
        return {"present": present, "missing": missing}