"""Contains the main entry point for the FastAPI backend.

This module initializes the FastAPI application, sets up middleware, and
includes the API routers.
"""

from contextlib import asynccontextmanager
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.jobs import router as jobs_router
from backend.api.log import router as log_router
from backend.api.modules.declarative_router import router as declarative_router
from backend.api.modules.log_skeleton_router import router as log_skeleton_router
from backend.api.modules.resource_based_router import router as resource_based_router
from backend.api.modules.temporal_profile_router import (
    router as temporal_profile_router,
)
from backend.api.setup import router as setup_router

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

    # Initialize the CelonisConnectionManager
    # It is handled by the get_celonis_connection DI
    app.state.celonis = None

    # Store the log's columns in the app state
    app.state.current_log = None  # will get path to tmp file
    app.state.current_log_columns = []

    # *** Log Skeleton ***
    app.state.jobs = {}

    yield
    # *** Shutdown ***
    # Potentially add something here, if we need to


# **************** Create Application ****************


app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"displayRequestDuration": True})

# CORS and middleware
app.add_middleware(
    CORSMiddleware,
    # TODO: Allow later only the frontend URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 'Empty' route
@app.get("/")
def home() -> Dict[str, str]:
    """Returns a simple message indicating that the API is running."""
    return {"message": "API is running."}


# **************** Routers ****************

app.include_router(jobs_router)
app.include_router(setup_router)
app.include_router(log_router)

app.include_router(declarative_router)
app.include_router(log_skeleton_router)
app.include_router(resource_based_router)
app.include_router(temporal_profile_router)
