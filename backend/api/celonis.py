"""Contains the dependency injection for the CelonisConnectionManager.

This module contains one function, which is used to return a
CelonisConnectionManager instance. The function is used as a dependency
in the FastAPI application.
"""

from typing import Union

from fastapi import HTTPException, Request
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

# **************** Celonis Settings ****************


class CelonisSettings(BaseSettings):
    """Settings for the Celonis connection.

    This class is used to load the Celonis connection settings from the
    environment variables. The settings are loaded from a .env file
    using the `pydantic_settings` library. The settings include the
    Celonis base URL, data pool name, data model name, and API token.
    """

    CELONIS_BASE_URL: str
    CELONIS_DATA_POOL_NAME: str
    CELONIS_DATA_MODEL_NAME: str
    API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


def get_celonis_connection(request: Request) -> CelonisConnectionManager:
    """Returns a CelonisConnectionManager instance.

    It tryies to get the CelonisConnectionManager instance from the
    application state. If it is not present, it creates a new instance
    using the settings from the environment variables. The instance is
    then stored in the application state for later use.
    This function is used as a dependency in the FastAPI application.

    Args:
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`. The application state
          contains the `CelonisConnectionManager` instance, which is created
          during application startup and stored for later use.

    Returns:
        The CelonisConnectionManager instance. This is used to connect to the
        Celonis API and perform operations on the data pool.
    """
    # If it is already in the app state, return it
    mgr: Union[CelonisConnectionManager, None] = getattr(
        request.app.state, "celonis", None
    )
    if mgr is not None:
        return mgr

    # If it is not in the app state, create a new one
    try:
        cfg = CelonisSettings()  # type: ignore
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail="""Celonis not configured. POST to
            /api/setup/celonis-credentials first.""",
        )

    # Build the connection manager and cache it
    mgr = CelonisConnectionManager(
        base_url=cfg.CELONIS_BASE_URL,
        data_pool_name=cfg.CELONIS_DATA_POOL_NAME,
        data_model_name=cfg.CELONIS_DATA_MODEL_NAME,
        api_token=cfg.API_TOKEN,
    )
    request.app.state.celonis = mgr
    return mgr
