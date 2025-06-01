"""Contains the router for handling jobs."""

from fastapi import APIRouter, HTTPException, Request

from backend.api.models.schemas.job_models import JobStatus

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


def verify_correct_job_module(job_id: str, request: Request, module: str):
    """Verifies if a job belongs to the module.

    Helper funciton used for the request of job states.

    Args:
        job_id: The ID of the job to be fetched.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.
        module: The name of the module that the job is checked against

    Raises:
        HTTPException: If the job with the given ID does not belong to the module
    """
    if request.app.state.jobs[job_id].module != module:
        raise HTTPException(
            status_code=400, detail="Job ID belongs to a different module"
        )
