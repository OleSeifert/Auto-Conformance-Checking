"""Contains a router for the setup of the application.

It contains several 'utility' endpoints that are used in the setup of
the application and the general configuration for event logs.
"""

import os
from pathlib import Path
from typing import Dict, List

from dotenv import dotenv_values, set_key
from fastapi import APIRouter, HTTPException, Request
from filelock import FileLock

from backend.api.models.schemas.setup_models import CelonisCredentials

router = APIRouter(prefix="/api/setup", tags=["Setup"])

# **************** Global Variables ****************
ENV_PATH = Path(__file__).parents[2] / ".env"  # /app/.env inside container
LOCK_PATH = ENV_PATH.with_suffix(".env.lock")  # /app/.env.lock

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
    """Save (or update) Celonis credentials in the bind-mounted .env file."""
    env_vars = dotenv_values(ENV_PATH)

    # Short-circuit when they already match
    if all(
        (
            env_vars.get("CELONIS_BASE_URL") == credentials.celonis_base_url,
            env_vars.get("CELONIS_DATA_POOL_NAME")
            == credentials.celonis_data_pool_name,
            env_vars.get("CELONIS_DATA_MODEL_NAME")
            == credentials.celonis_data_model_name,
            env_vars.get("API_TOKEN") == credentials.api_token,
        )
    ):
        return {"message": "Credentials already exist and match."}

    # ---- atomic, thread-safe update ------------------------------------
    with FileLock(LOCK_PATH, timeout=5):
        set_key(
            ENV_PATH,
            "CELONIS_BASE_URL",
            credentials.celonis_base_url,
            quote_mode="never",
        )
        set_key(
            ENV_PATH,
            "CELONIS_DATA_POOL_NAME",
            credentials.celonis_data_pool_name,
            quote_mode="never",
        )
        set_key(
            ENV_PATH,
            "CELONIS_DATA_MODEL_NAME",
            credentials.celonis_data_model_name,
            quote_mode="never",
        )
        set_key(ENV_PATH, "API_TOKEN", credentials.api_token, quote_mode="never")

    # ---- refresh live process env vars so the change is effective now --
    os.environ.update(
        {
            "CELONIS_BASE_URL": credentials.celonis_base_url,
            "CELONIS_DATA_POOL_NAME": credentials.celonis_data_pool_name,
            "CELONIS_DATA_MODEL_NAME": credentials.celonis_data_model_name,
            "API_TOKEN": credentials.api_token,
        }
    )

    return {"message": "Credentials saved to .env"}


@router.get("/get-column-names")
async def get_column_names(request: Request) -> Dict[str, List[str]]:
    """Provides the column names of the current log.

    Args:
        request: The FastAPI request object. This is used to access the app state
          and retrieve the current log columns.

    Returns:
        A dictionary containing the column names of the current log.

    Raises:
        HTTPException: If no log columns are found in the app state, a 400 error is raised
        with a message indicating that no log columns were found. The user should
        upload a log first.
    """
    if not request.app.state.current_log_columns:
        raise HTTPException(
            status_code=400,
            detail="No log columns found. Please upload a log first.",
        )
    return {
        "columns": request.app.state.current_log_columns,
    }