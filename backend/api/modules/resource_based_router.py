"""Contains the routes for handling resource-based conformance checking."""

import uuid
from typing import Dict, List

from api.models.schemas.resource_based_models import SNAMetricValue
from fastapi import APIRouter, BackgroundTasks, Depends, Request

from backend.api.celonis import get_celonis_connection
from backend.api.models.schemas.job_models import JobStatus
from backend.api.tasks.resource_based_tasks import (
    compute_and_store_sna_metrics,
)
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(prefix="/api/resource-based", tags=["Resource-Based CC"])


@router.post("/sna/compute", status_code=202)
async def compute_sna_metrics(
    background_tasks: BackgroundTasks,
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Computes the SNA metrics and stores it.

    Args:
        background_tasks: The background tasks manager.
        request: The FastAPI request object.
        celonis: The Celonis connection manager instance.

    Returns:
        A dictionary containing the job ID of the scheduled task.
    """
    job_id = str(uuid.uuid4())
    request.app.state.jobs[job_id] = JobStatus(
        module="resource_based", status="pending"
    )
    background_tasks.add_task(
        compute_and_store_sna_metrics,
        request.app,
        job_id,
        celonis,
    )
    return {"job_id": job_id}


@router.get("/sna/handover-of-work/{job_id}", response_model=List[SNAMetricValue])
def get_handover_of_work_metric(job_id: str, request: Request) -> List[SNAMetricValue]:
    """Retrieves the computed Handover of Work SNA metric.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        The Handover of Work metric.
    """
    return (
        request.app.state.jobs[job_id]
        .result.get("handover_of_work", {})
        .get("values", [])
    )


@router.get("/sna/subcontracting/{job_id}", response_model=List[SNAMetricValue])
def get_subcontracting_metric(job_id: str, request: Request) -> List[SNAMetricValue]:
    """Retrieves the computed Subcontracting metric.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        The Subcontracting metric.
    """
    return (
        request.app.state.jobs[job_id]
        .result.get("subcontracting", {})
        .get("values", [])
    )


@router.get("/sna/working-together/{job_id}", response_model=List[SNAMetricValue])
def get_working_together_metric(job_id: str, request: Request) -> List[SNAMetricValue]:
    """Retrieves the computed Working Together metric.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        The Working Together metric.
    """
    return (
        request.app.state.jobs[job_id]
        .result.get("working_together", {})
        .get("values", [])
    )


@router.get("/sna/similar-activities/{job_id}", response_model=List[SNAMetricValue])
def get_similar_activities_metric(
    job_id: str, request: Request
) -> List[SNAMetricValue]:
    """Retrieves the computed Similar Activities metric.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        The Similar Activities metric.
    """
    return (
        request.app.state.jobs[job_id]
        .result.get("similar_activities", {})
        .get("values", [])
    )
