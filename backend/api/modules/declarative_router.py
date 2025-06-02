"""Contains the routes for handling declarative constraints and related
operations."""

import uuid
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from backend.api.celonis import get_celonis_connection
from backend.api.jobs import verify_correct_job_module
from backend.api.models.schemas.job_models import JobStatus
from backend.api.tasks.declarative_constraints_tasks import (
    compute_and_store_declarative_constraints,
)
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(
    prefix="/api/declarative-constraints", tags=["Declarative Constraints CC"]
)
MODULE_NAME = "declarative_constraints"


@router.post("/compute-constraints", status_code=202)
async def compute_declarative_constraints(
    background_tasks: BackgroundTasks,
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Computes the declarative constraints and stores it.

    The declarative model is computed in the background and stored in the app state.

    Args:
        background_tasks: The background tasks object. This is used to schedule
          the computation of the declarative model.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.
        celonis (optional): The CelonisManager dependency injection.
          Defaults to Depends(get_celonis_connection).

    Returns:
        A dictionary containing the job ID of the scheduled task.
    """
    job_id = str(uuid.uuid4())

    # Intialize the record in the app state
    request.app.state.jobs[job_id] = JobStatus(module=MODULE_NAME, status="pending")

    # Schedule the worker
    background_tasks.add_task(
        compute_and_store_declarative_constraints, request.app, job_id, celonis
    )

    return {"job_id": job_id}


# **************** Retrieving Declarative Model Attributes ****************


@router.get("/get_existance_violations/{job_id}")
def get_existance_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the existance violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the existance violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.


    Returns:
        A list of lists containing the existance violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("existance", [])


@router.get("/get_absence_violations/{job_id}")
def get_absence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the absence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the absence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("absence", [])


@router.get("/get_exactly_one_violations/{job_id}")
def get_exactly_one_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the exactly_one violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the exactly_one violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("exactly_one", [])


@router.get("/get_init_violations/{job_id}")
def get_init_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the init violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the init violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("init", [])


@router.get("/get_responded_existence_violations/{job_id}")
def get_responded_existence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the responded_existence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the responded_existence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("responded_existence", [])


@router.get("/get_coexistence_violations/{job_id}")
def get_coexistence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the coexistence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the coexistence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("coexistence", [])


@router.get("/get_response_violations/{job_id}")
def get_response_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the response violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the response violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("response", [])


@router.get("/get_precedence_violations/{job_id}")
def get_precedence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the precedence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the precedence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("precedence", [])


@router.get("/get_succession_violations/{job_id}")
def get_succession_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the succession violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the succession violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("succession", [])


@router.get("/get_altprecedence_violations/{job_id}")
def get_altprecedence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the altprecedence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the altprecedence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("altprecedence", [])


@router.get("/get_altsuccession_violations/{job_id}")
def get_altsuccession_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the altsuccession violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the altsuccession violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("altsuccession", [])


@router.get("/get_chainresponse_violations/{job_id}")
def get_chainresponse_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the chainresponse violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the chainresponse violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("chainresponse", [])


@router.get("/get_chainprecedence_violations/{job_id}")
def get_chainprecedence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the chainprecedence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the chainprecedence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("chainprecedence", [])


@router.get("/get_chainsuccession_violations/{job_id}")
def get_chainsuccession_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the chainsuccession violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the chainsuccession violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("chainsuccession", [])


@router.get("/get_noncoexistence_violations/{job_id}")
def get_noncoexistence_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the noncoexistence violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the noncoexistence violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("noncoexistence", [])


@router.get("/get_nonsuccession_violations/{job_id}")
def get_nonsuccession_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the nonsuccession violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the nonsuccession violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("nonsuccession", [])


@router.get("/get_nonchainsuccession_violations/{job_id}")
def get_nonchainsuccession_violations(job_id: str, request: Request) -> Dict:
    """Retrieves the nonchainsuccession violations from the declarative model.

    Args:
        job_id: The ID of the job for which to retrieve the  violations.
        request: The FastAPI request object. This is used to access the
            application state via `request.app.state`.

    Returns:
        A list of lists containing the nonchainsuccession violations for the specified job.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    return request.app.state.jobs[job_id].result.get("nonchainsuccession", [])
