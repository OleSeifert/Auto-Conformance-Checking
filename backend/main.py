"""Contains the main entry point for the FastAPI backend.

This module initializes the FastAPI application, sets up middleware, and
includes the API routers.
"""

from contextlib import asynccontextmanager
from typing import Dict

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.log import router as log_router
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
    app.state.current_log_columns = []

    yield
    # *** Shutdown ***
    # Potentially add something here, if we need to


# **************** Create Application ****************


app = FastAPI(lifespan=lifespan)

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


app.include_router(log_router)
app.include_router(setup_router)
