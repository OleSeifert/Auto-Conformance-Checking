"""Contains the routes for temporal conformance checking."""

import uuid
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request

from backend.api.celonis import get_celonis_connection
from backend.api.jobs import verify_correct_job_module
from backend.api.models.schemas.job_models import JobStatus
from backend.api.tasks.temporal_profile_tasks import (
    compute_and_store_temporal_conformance_result,
)
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(prefix="/api/temporal-profile", tags=["Temporal Profile CC"])
MODULE_NAME = "temporal"


@router.post("/compute-result", status_code=202)
async def compute_temporal_conformance_result(
    background_tasks: BackgroundTasks,
    request: Request,
    zeta: float = Query(
        0.5,
        description="Zeta value for temporal profile conformance checking",
        gt=0.0,
    ),
    celonis_connection: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Computes the temporal conformance result and stores it.

    Args:
        background_tasks: The background tasks manager.
        request: The FastAPI request object.
        zeta: The zeta value used for temporal profile conformance checking.
        celonis_connection: The Celonis connection manager instance.

    Returns:
        A dictionary containing the job ID of the scheduled task.
    """
    job_id = str(uuid.uuid4())
    request.app.state.jobs[job_id] = JobStatus(module=MODULE_NAME, status="pending")
    background_tasks.add_task(
        compute_and_store_temporal_conformance_result,
        request.app,
        job_id,
        celonis_connection,
        zeta,
    )
    return {"job_id": job_id}


@router.get("/get-result/{job_id}")
async def get_temporal_conformance_result(
    job_id: str,
    request: Request,
) -> dict:
    """Retrieves the temporal conformance result for a given job ID.

    This result is expected to be a list of lists of tuples, representing
    the raw output from TemporalProfile.get_temporal_conformance_result().

    Args:
        job_id: The ID of the job for which to retrieve the result.
        request: The FastAPI request object.

    Returns:
        The temporal conformance result as a list of lists of tuples.

    Raises:
        HTTPException: If the job is not found or if the result is not available.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    job: JobStatus = request.app.state.jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")

    if not job.result:
        raise HTTPException(
            status_code=500,
            detail=f"Job '{job_id}' is complete, but result data is missing internally.",
        )

    data = job.result.get("temporal_conformance_result")
    if data is None:
        raise HTTPException(
            status_code=404,
            detail=f"Temporal conformance result data not found for completed job '{job_id}'.",
        )

    if not data:
        return {"tables": [], "graphs": []}

    try:
        # Flatten while skipping empty sublists
        flattened = []
        for sublist in data:
            for tup in sublist:
                if isinstance(tup, tuple) and len(tup) == 4:
                    flattened.append(list(tup))

        return {
            "tables": [
                {
                    "headers": ["Activity A", "Activity B", "Time Passed", "Zeta"],
                    "rows": flattened,
                }
            ],
            "graphs": [],
        }

    except Exception as e:
        import traceback

        print("Error formatting temporal result:", e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Error formatting temporal result. Check tuple structure.",
        )
