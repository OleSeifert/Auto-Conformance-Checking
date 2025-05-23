"""Contains the router for handling jobs."""

from api.models.schemas.job_models import JobStatus
from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.get("/{job_id}", response_model=JobStatus)
async def get_jobs(job_id: str, request: Request) -> JobStatus:
    """Fetches the status of a job via its ID.

    Args:
        job_id: The ID of the job to be fetched.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.

    Raises:
        HTTPException: If the job with the given ID is not found in the
        application state.

    Returns:
        The status of the job as a JobStatus object.
    """
    job = request.app.state.jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found.")
    return job
