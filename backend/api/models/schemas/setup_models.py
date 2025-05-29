"""Contains the Pydantic models for the setup API.

This module defines the Pydantic models used for validating the input
data for the setup API endpoints. It includes models for Celonis
credentials, and column mapping.
"""

from typing import Optional

from pydantic import BaseModel

# **************** Celonis Credentials ****************


class CelonisCredentials(BaseModel):
    """Defines the Celonis credentials required for the connection."""

    celonis_base_url: str
    celonis_data_pool_name: str
    celonis_data_model_name: str
    api_token: str


# **************** Column Mapping ****************


class ColumnMapping(BaseModel):
    """Defines the column mapping for the event log."""

    case_id_column: str
    activity_column: str
    timestamp_column: str
    resource_1_column: Optional[str] = None
