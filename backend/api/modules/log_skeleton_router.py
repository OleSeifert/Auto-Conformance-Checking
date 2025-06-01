"""Contains the routes for handling log skeletons and related operations."""

import uuid
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from backend.api.celonis import get_celonis_connection
from backend.api.jobs import verify_correct_job_module
from backend.api.models.schemas.job_models import JobStatus
from backend.api.tasks.log_skeleton_tasks import compute_and_store_log_skeleton
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(prefix="/api/log-skeleton", tags=["Log Skeleton CC"])
MODULE_NAME = "log_skeleton"


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
    request.app.state.jobs[job_id] = JobStatus(module=MODULE_NAME, status="pending")

    # Schedule the worker
    background_tasks.add_task(
        compute_and_store_log_skeleton, request.app, job_id, celonis
    )

    return {"job_id": job_id}


# **************** Retrieving Log Skeleton Attributes ****************


# @router.get("/get_equivalence/{job_id}", response_model=List[List[str]])
# def get_equivalence(job_id: str, request: Request) -> List[List[str]]:
#     """Retrieves the equivalence relations from the log skeleton.

#     Args:
#         job_id: The ID of the job for which to retrieve the equivalence relations.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.



#     Returns:
#         A list of lists containing the equivalence relations for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("equivalence", [])


# @router.get("/get_always_after/{job_id}", response_model=List[List[str]])
# def get_always_after(job_id: str, request: Request) -> List[List[str]]:
#     """Retrieves the always-after relations from the log skeleton.

#     Args:
#         job_id: The ID of the job for which to retrieve the always-after relations.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.

#     Returns:
#         A list of lists containing the always-after relations for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("always_after", [])


# @router.get("/get_always_before/{job_id}", response_model=List[List[str]])
# def get_always_before(job_id: str, request: Request) -> List[List[str]]:
#     """Retrieves the always-before relations from the log skeleton.


#     Args:
#         job_id: The ID of the job for which to retrieve the always-before relations.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.

#     Returns:
#         A list of lists containing the always-before relations for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("always_before", [])



# @router.get("/get_never_together/{job_id}", response_model=List[List[str]])
# def get_never_together(job_id: str, request: Request) -> List[List[str]]:


#     Args:
#         job_id: The ID of the job for which to retrieve the never-together relations.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.

#     Returns:
#         A list of lists containing the never-together relations for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("never_together", [])



# @router.get("/get_directly_follows/{job_id}", response_model=List[List[str]])
# def get_directly_follows(job_id: str, request: Request) -> List[List[str]]:
#     """Retrieves the directly-follows relations from the log skeleton.

#     Args:
#         job_id: The ID of the job for which to retrieve the directly-follows relations.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.

#     Returns:
#         A list of lists containing the directly-follows relations for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("directly_follows", [])



# @router.get("/get_activity_frequencies/{job_id}", response_model=Dict[str, List[int]])
# def get_activity_frequencies(job_id: str, request: Request) -> Dict[str, List[int]]:
#     """Retrieves the activity frequencies from the log skeleton.

#     Args:
#         job_id: The ID of the job for which to retrieve the activity frequencies.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.

#     Returns:
#         A dictionary containing the activity frequencies for the specified job.
#     """
#     return request.app.state.jobs[job_id].result.get("activ_freq", {})





@router.get("/get_equivalence/{job_id}")
def get_equivalence(job_id: str, request: Request) -> dict:
    """
    Retrieves the equivalence relations from the log skeleton.

    Args:
        job_id: The ID of the job for which to retrieve the equivalence relations.
        request: The FastAPI request object.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result = request.app.state.jobs[job_id].result.get("equivalence", [])
    if not result:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Activity A", "Activity B"],
                "rows": result
            }
        ],
        "graphs": []
    }

@router.get("/get_always_after/{job_id}")
def get_always_after(job_id: str, request: Request) -> dict:
    """
    Retrieves the always-after relations from the log skeleton.

    Returns:
        A dictionary with a "tables" list and optional "graphs" list.
    """
    result = request.app.state.jobs[job_id].result.get("always_after", [])
    if not result:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Activity A", "Always After Activity B"],
                "rows": result
            }
        ],
        "graphs": []
    }

@router.get("/get_always_before/{job_id}")
def get_always_before(job_id: str, request: Request) -> dict:
    """Retrieves the always-before relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("always_before", [])
    if not result:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Activity A", "Always Before Activity B"],
                "rows": result
            }
        ],
        "graphs": []
    }

@router.get("/get_never_together/{job_id}")
def get_never_together(job_id: str, request: Request) -> dict:
    """Retrieves the never-together relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("never_together", [])
    if not result:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Activity A", "Activity B (Never Together)"],
                "rows": result
            }
        ],
        "graphs": []
    }

@router.get("/get_directly_follows/{job_id}")
def get_directly_follows(job_id: str, request: Request) -> dict:
    """Retrieves the directly-follows relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("directly_follows", [])
    if not result:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Preceding Activity", "Following Activity"],
                "rows": result
            }
        ],
        "graphs": []
    }

@router.get("/get_activity_frequencies/{job_id}")
def get_activity_frequencies(job_id: str, request: Request) -> dict:
    """Retrieves the activity frequencies from the log skeleton."""
    freq_dict = request.app.state.jobs[job_id].result.get("activ_freq", {})

    # Convert to table: [{"headers": [...], "rows": [...]}]
    rows = [[activity, count] for activity, count in freq_dict.items()]
    if not rows:
        return {
            "tables": [],
            "graphs": []
        }
    return {
        "tables": [
            {
                "headers": ["Activity", "Frequency"],
                "rows": rows
            }
        ],
        "graphs": []
    }
