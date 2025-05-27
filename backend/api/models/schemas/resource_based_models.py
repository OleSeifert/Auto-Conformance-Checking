"""Contains the Pydantic model for resource-based conformance checking."""

from pydantic import BaseModel


class SNAMetricValue(BaseModel):
    """Represents a single connection (edge) in an SNA graph."""

    source: str
    target: str
    value: float
