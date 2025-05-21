"""Contains a router for the setup of the application.

It contains several 'utility' endpoints that are used in the setup of
the application and the general configuration for event logs.
"""

from typing import Optional

from dotenv import dotenv_values, set_key
from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix="/api/setup", tags=["Setup"])


# **************** Pydantic classes for validation ****************


class CelonisCredentials(BaseModel):
    """Defines the Celonis credentials required for the connection."""

    celonis_base_url: str
    celonis_data_pool_name: str
    celonis_data_model_name: str
    api_token: str
    data_table_name: Optional[str] = None


class ColumnMapping(BaseModel):
    """Defines the column mapping for the event log."""

    case_id_column: str
    activity_column: str
    timestamp_column: str
    ressource_1_column: Optional[str] = None
    ressource_2_column: Optional[str] = None


# **************** Endpoints ****************


@router.post("/celonis-credentials")
async def celonis_credentials(credentials: CelonisCredentials):
    """Saves the Celonis credentials to the .env file.

    Args:
        credentials: The Celonis credentials to be saved. This should be a
          CelonisCredentials object.


    Returns:
        A dictionary containing a message indicating the success of the
        operation.
    """
    # Load environment variables
    env_vars = dotenv_values(".env")

    # Check whether they already exist and match
    if (
        env_vars.get("CELONIS_BASE_URL") == credentials.celonis_base_url
        and env_vars.get("CELONIS_DATA_POOL_NAME") == credentials.celonis_data_pool_name
        and env_vars.get("CELONIS_DATA_MODEL_NAME")
        == credentials.celonis_data_model_name
        and env_vars.get("API_TOKEN") == credentials.api_token
    ):
        return {"message": "Credentials already exist and match."}

    # If they don't exist or don't match, update the .env file
    set_key(".env", "CELONIS_BASE_URL", credentials.celonis_base_url)
    set_key(".env", "CELONIS_DATA_POOL_NAME", credentials.celonis_data_pool_name)
    set_key(".env", "CELONIS_DATA_MODEL_NAME", credentials.celonis_data_model_name)
    set_key(".env", "API_TOKEN", credentials.api_token)
    if credentials.data_table_name:
        set_key(".env", "DATA_TABLE_NAME", credentials.data_table_name)

    return {"message": "Credentials saved to .env"}


@router.post("/map-columns")
async def map_columns(column_mapping: ColumnMapping, request: Request):
    """Saves the column mapping to the app state.

    Args:
        column_mapping: The column mapping to be saved. This should be a
          ColumnMapping object.
        request: The FastAPI request object. This is used to access the app state
          and save the column mapping.

    Returns:
        A dictionary containing a message indicating the success of the
        operation.
    """
    # Save the column mapping as a dictionary in the request state
    request.app.state.column_mapping = column_mapping.model_dump()
    return {"message": "Column mapping saved."}
