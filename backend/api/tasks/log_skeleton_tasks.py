"""Contains the tasks for handling log skeletons and related operations."""

import time

from fastapi import FastAPI

from backend.api.models.schemas.job_models import JobStatus
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.conformance_checking.log_skeleton import LogSkeleton


def compute_and_store_log_skeleton(
    app: FastAPI, job_id: str, celonis: CelonisConnectionManager
) -> None:
    """Computes the log skeleton and stores it in the app state.

    Args:
        app: The FastAPI app instance.
        job_id: The ID of the job to be computed.
        celonis: The CelonisConnectionManager instance.
    """
    # Get the job record from the app state
    rec: JobStatus = app.state.jobs[job_id]
    try:
        start_time = time.perf_counter_ns()
        rec.status = "running"

        # Get the log from Celonis
        df = celonis.get_basic_dataframe_from_celonis()

        if df is None:
            rec.status = "failed"
            return

        # Compute the log skeleton
        ls = LogSkeleton(df)
        ls.compute_skeleton()

        rec.result = ls.get_skeleton()
        rec.status = "complete"
        end_time = time.perf_counter_ns()

        print(f"*** TIME FOR COMPUTATION: {end_time - start_time} ns ***")
    except Exception as e:
        rec.status = "failed"
        rec.error = str(e)
