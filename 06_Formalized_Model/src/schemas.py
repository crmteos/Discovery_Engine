from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class LogBasisTransformation(BaseModel):
    """Log base conversion transformation model."""

    original_base: int = Field(..., description="Original logarithm base (e.g., 10)")
    target_base: int = Field(..., description="Target logarithm base (e.g., 2)")
    conversion_factor: float = Field(
        ..., description="Factor to convert from original base to target base (log2(10) ≈ 3.321928094887362)"
    )
    values: List[float] = Field(
        ..., description="Original log-values in the original base"
    )
    transformed_values: List[float] = Field(
        ..., description="Corresponding log-values in the target base"
    )


class DftFrequencyTransformation(BaseModel):
    """DFT frequency transformation model."""

    original_freq: float = Field(..., description="Original frequency value")
    scaled_freq: float = Field(
        ..., description="Frequency after applying alpha scaling and phase shift"
    )
    alpha: float = Field(
        ..., description="Scaling factor applied to the original frequency"
    )
    phase_shift: Optional[float] = Field(
        default=0.0, description="Optional phase shift in radians"
    )


class AxiomaticTransformSchema(BaseModel):
    """Root schema for axiomatic transformation output from LLM."""

    log_basis_transformations: List[LogBasisTransformation] = Field(
        ..., description="List of log base conversion transformations"
    )
    dft_frequency_transformations: List[DftFrequencyTransformation] = Field(
        ..., description="List of DFT frequency transformation records"
    )

    class Config:
        extra = "forbid"  # strict validation: reject any extra fields not defined


# End of schemas.py