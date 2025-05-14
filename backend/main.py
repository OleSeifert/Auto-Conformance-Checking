"""Contains the main entry point for the FastAPI backend.

This module initializes the FastAPI application, sets up middleware, and
includes the API routers.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.log import router as log_router
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,  # type: ignore
)

# **************** Startup and Shutdown ****************


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes the CelonisConnectionManager and stores it in the app state.

    This function is used as a context manager to ensure that the
    CelonisConnectionManager is properly initialized.

    Args:
        app: The FastAPI application instance. This is used to store the
          CelonisConnectionManager instance in the application state.
    """
    # Load environment variables from .env file
    load_dotenv()
    # Get environment variables
    base_url_ = os.getenv("CELONIS_BASE_URL")
    data_pool_name_ = os.getenv("CELONIS_DATA_POOL_NAME")
    data_model_name_ = os.getenv("CELONIS_DATA_MODEL_NAME")
    api_token_ = str(os.getenv("API_TOKEN"))

    # Check if environment variables are set
    if not base_url_ or not data_pool_name_ or not data_model_name_ or api_token_:
        raise ValueError(
            """Please set the CELONIS_BASE_URL, CELONIS_DATA_POOL_NAME,
            CELONIS_DATA_MODEL_NAME, and API_TOKEN environment variables."""
        )

    # *** Startup ***
    app.state.celonis = CelonisConnectionManager(
        base_url=base_url_,
        data_pool_name=data_pool_name_,
        data_model_name=data_model_name_,
        api_token=api_token_,
    )
    yield
    # *** Shutdown ***
    # Potentially add something here, if we need to


# **************** Create Application ****************


app = FastAPI(lifespan=lifespan)

# CORS and middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# **************** Routers ****************


app.include_router(log_router, prefix="/api/logs", tags=["logs"])


# **************** API *****************
