from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ProvEntity(BaseModel):
    """Base PROV-O entity model."""

    id: str = Field(..., description="Unique identifier for the PROV-O entity")
    type: str = Field(..., description="PROV-O class name (Entity, Activity, Agent, Generation, Usage, Invalidation, Communication, Start, End)")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional attributes specific to the entity type")


class SkosConcept(BaseModel):
    """SKOS concept model."""

    id: str = Field(..., description="Unique identifier for the SKOS concept")
    prefLabel: str = Field(..., description="Preferred label in the user's language")
    altLabel: Optional[List[str]] = Field(default_factory=list, description="Alternative labels")
    broader: Optional[List[str]] = Field(default_factory=list, description="More general concepts (URI references)")
    narrower: Optional[List[str]] = Field(default_factory=list, description="More specific concepts (URI references)")
    exactMatch: Optional[List[str]] = Field(default_factory=list, description="Equivalent concept in another schema (URI references)")
    closeMatch: Optional[List[str]] = Field(default_factory=list, description="Related concept in another schema (URI references)")


class IntakeExtractionSchema(BaseModel):
    """Root schema for W3C PROV-O / SKOS extraction from LLM output."""

    prov_entities: List[ProvEntity] = Field(
        ..., description="Array of PROV-O entities extracted from the source text"
    )
    skos_concepts: List[SkosConcept] = Field(
        ..., description="Array of SKOS concepts extracted from the source text"
    )

    class Config:
        json_encoders = {}
        extra = "forbid"  # strict validation: reject any extra fields not defined


# End of schemas.py