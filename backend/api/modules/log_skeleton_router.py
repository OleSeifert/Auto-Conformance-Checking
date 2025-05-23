"""Contains the routes for handling log skeletons and related operations."""

import uuid
from typing import Dict

from api.celonis import get_celonis_connection
from api.models.schemas.job_models import JobStatus
from api.tasks.log_skeleton_tasks import compute_and_store_log_skeleton
from celonis_connection.celonis_connection_manager import CelonisConnectionManager
from fastapi import APIRouter, BackgroundTasks, Depends, Request

router = APIRouter(prefix="/api/log-skeleton", tags=["Log Skeleton CC"])


@router.post("/compute-skeleton", status_code=202)
async def compute_log_skeleton(
    background_tasks: BackgroundTasks,
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Computes the log skeleton and stores it.

    The log skeleton is computed in the background and stored in the app state.

    Args:
        background_tasks: The background tasks object. This is used to schedule
          the computation of the log skeleton.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.
        celonis (optional): The CelonisManager dependency injection.
          Defaults to Depends(get_celonis_connection).

    Returns:
        A dictionary containing the job ID of the scheduled task.
    """
    job_id = str(uuid.uuid4())

    # Intialize the record in the app state
    request.app.state.jobs[job_id] = JobStatus(module="log_skeleton", status="pending")

    # Schedule the worker
    background_tasks.add_task(
        compute_and_store_log_skeleton, request.app, job_id, celonis
    )

    return {"job_id": job_id}
