"""Contains the Pydantic models for resource-based conformance checking."""

from typing import Dict, List

from pydantic import BaseModel


class SNAMetric(BaseModel):
    """Represents a single connection (edge) in an SNA graph."""

    source: str
    target: str
    value: float


class OrganizationalRole(BaseModel):
    """Represents an organizational role used for role discovery."""

    activities: List[str]
    originators_importance: Dict[str, float]
