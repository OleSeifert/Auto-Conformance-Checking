"""Contains the tasks for handling log skeletons and related operations."""

from fastapi import FastAPI

from backend.api.models.schemas.job_models import JobStatus
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.conformance_checking.declarative_constraints import DeclarativeConstraints


def compute_and_store_declarative_constraints(
    app: FastAPI,
    job_id: str,
    celonis: CelonisConnectionManager,
    min_support_ratio: float = 0.3,
    min_confidence_ratio: float = 0.75,
) -> None:
    """Computes the declarative constraints and stores it in the app state.

    Args:
        app: The FastAPI app instance.
        job_id: The ID of the job to be computed.
        celonis: The CelonisConnectionManager instance.
        min_support_ratio: The minimum support ratio for the constraints.
        min_confidence_ratio: The minimum confidence ratio for the constraints.
    """
    # Get the job record from the app state
    rec: JobStatus = app.state.jobs[job_id]
    try:
        rec.status = "running"

        # Get the log from Celonis
        df = celonis.get_basic_dataframe_from_celonis()

        if df is None:
            rec.status = "failed"
            return

        # Compute the declarative constraints
        dc = DeclarativeConstraints(df)
        dc.run_model(
            min_support_ratio=min_support_ratio,
            min_confidence_ratio=min_confidence_ratio,
        )
        rec.result = dc.run_all_rules()
        rec.status = "complete"

    except Exception as e:
        rec.status = "failed"
        rec.error = str(e)
