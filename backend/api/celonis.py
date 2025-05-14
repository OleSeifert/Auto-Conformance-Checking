"""Contains the dependency injection for the CelonisConnectionManager.

This module contains one function, which is used to return a
CelonisConnectionManager instance. The function is used as a dependency
in the FastAPI application.
"""

from fastapi import Request

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)


def get_celonis_connection(request: Request) -> CelonisConnectionManager:
    """Returns a CelonisConnectionManager instance.

    This function is used as a dependency in the FastAPI application.
    It retrieves the CelonisConnectionManager instance from the
    application state.
    The CelonisConnectionManager instance is created in the main.py file
    and stored in the application state.

    Args:
        request: The FastAPI request object. This is used to access the


    Returns:
        The CelonisConnectionManager instance. This is used to connect to the
        Celonis API and perform operations on the data pool.
    """
    return request.app.state.celonis
