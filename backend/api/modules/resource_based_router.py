"""Contains the routes for handling resource-based conformance checking."""

import uuid
from typing import Any, Dict, List, TypeAlias, Union

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request

from backend.api.celonis import get_celonis_connection
from backend.api.jobs import verify_correct_job_module
from backend.api.models.schemas.job_models import JobStatus
from backend.api.models.schemas.resource_based_models import OrganizationalRole, ResponseSchema
from backend.api.tasks.resource_based_tasks import (
    compute_and_store_resource_based_metrics,
)
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.conformance_checking.resource_based import ResourceBased
from backend.pql_queries import resource_based_queries

# **************** Type Aliases ****************

ReturnGraphType: TypeAlias = Dict[
    str, List[Dict[str, List[Union[str, Dict[str, str]]]]]
]

router = APIRouter(prefix="/api/resource-based", tags=["Resource-Based CC"])
MODULE_NAME = "resource_based"


@router.post("/compute", status_code=202)
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
    request.app.state.jobs[job_id] = JobStatus(module=MODULE_NAME, status="pending")
    background_tasks.add_task(
        compute_and_store_resource_based_metrics,
        request.app,
        job_id,
        celonis,
    )
    return {"job_id": job_id}


# **************** Social Network Analysis ****************


@router.get("/sna/handover-of-work/{job_id}")
async def get_handover_of_work_metric(
    job_id: str, request: Request
) -> Dict[str, List[Dict[str, List[Any]]]]:
    """Retrieves the computed Handover of Work SNA metric and returns it.

    In a frontend-compatible format.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    raw_values = (
        request.app.state.jobs[job_id]
        .result.get("handover_of_work", {})
        .get("values", [])
    )

    # Convert dicts to list of lists
    formatted_rows = [
        [entry.get("source"), entry.get("target"), entry.get("value")]
        for entry in raw_values
        if "source" in entry and "target" in entry and "value" in entry
    ]

    return {
        "tables": [{"headers": ["Source", "Target", "Value"], "rows": formatted_rows}],
        "graphs": [],
    }


@router.get("/sna/subcontracting/{job_id}")
async def get_subcontracting_metric(
    job_id: str, request: Request
) -> Dict[str, List[Dict[str, List[Any]]]]:
    """Returns subcontracting metric in table/graph format."""
    verify_correct_job_module(job_id, request, MODULE_NAME)
    raw = (
        request.app.state.jobs[job_id]
        .result.get("subcontracting", {})
        .get("values", [])
    )

    rows = [[item.get("source"), item.get("target"), item.get("value")] for item in raw]
    return {
        "tables": [{"headers": ["Source", "Target", "Value"], "rows": rows}],
        "graphs": [],
    }


@router.get("/sna/working-together/{job_id}")
async def get_working_together_metric(
    job_id: str, request: Request
) -> Dict[str, List[Dict[str, List[Any]]]]:
    """Returns working together metric in table/graph format."""
    verify_correct_job_module(job_id, request, MODULE_NAME)
    raw = (
        request.app.state.jobs[job_id]
        .result.get("working_together", {})
        .get("values", [])
    )

    rows = [[item.get("source"), item.get("target"), item.get("value")] for item in raw]
    return {
        "tables": [{"headers": ["Source", "Target", "Value"], "rows": rows}],
        "graphs": [],
    }


@router.get("/sna/similar-activities/{job_id}")
async def get_similar_activities_metric(
    job_id: str, request: Request
) -> Dict[str, List[Dict[str, List[Any]]]]:
    """Returns similar activities metric in table/graph format."""
    verify_correct_job_module(job_id, request, MODULE_NAME)
    raw = (
        request.app.state.jobs[job_id]
        .result.get("similar_activities", {})
        .get("values", [])
    )

    rows = [[item.get("source"), item.get("target"), item.get("value")] for item in raw]
    return {
        "tables": [{"headers": ["Source", "Target", "Value"], "rows": rows}],
        "graphs": [],
    }


# **************** Role Discovery ****************

@router.get(
    "/role-discovery/{job_id}",
    response_model=ResponseSchema,
)
async def get_organizational_roles_result(
    job_id: str, request: Request
) -> ResponseSchema:
    """
    Retrieves the computed organizational roles and returns them as a table.

    Args:
        job_id: The ID of the job to retrieve the organizational roles for.
        request: The FastAPI request object.

    Returns:
        A ResponseSchema object with a table:
        Headers: ["Activity", "Originator", "Importance"]
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    roles_data = request.app.state.jobs[job_id].result.get("organizational_roles", [])

    rows: List[List[str]] = []
    for role in roles_data:
        activities = role.get("activities", [])
        originators = role.get("originators_importance", {})
        for activity in activities:
            for originator, importance in originators.items():
                rows.append([activity, originator, str(importance)])

    return ResponseSchema(
        tables=[
            {
                "headers": ["Activity", "Originator", "Importance"],
                "rows": rows,
            }
        ],
        graphs=[],
    )



# **************** Resource Profiles ****************


@router.get("/resource-profile/distinct-activities", response_model=int)
async def get_distinct_activities(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time."),
    end_time: str = Query(..., description="End time."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of distinct activities.

    Args:
        start_time: The start time of the range.
        end_time: The end time of the range.
        resource: The resource for which to calculate the number of
                distinct activities.
        celonis: The Celonis connection manager instance.

    Returns:
        The number of distinct activities for the specified resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()

    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_number_of_distinct_activities(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Internal server error calculating metric."
        )


@router.get("/pql/resource-profile/distinct-activities", response_model=int)
async def get_distinct_activities_pql(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time."),
    end_time: str = Query(..., description="End time."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of distinct activities via a pql query.

    Args:
        start_time: The start time of the range.
        end_time: The end time of the range.
        resource: The resource for which to calculate the number of
                distinct activities.
        celonis: The Celonis connection manager instance.

    Returns:
        The number of distinct activities for the specified resource.
    """
    try:
        result = resource_based_queries.get_number_of_distinct_activities(
            celonis, start_time, end_time, resource
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/activity-frequency", response_model=float)
async def get_resource_activity_frequency(
    resource: str = Query(..., description="The resource identifier."),
    activity: str = Query(..., description="The specific activity name."),
    start_time: str = Query(
        ...,
        description="Start time of the interval.",
    ),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the activity frequency for a given resource and activity.

    Args:
        resource: The resource for which to calculate the activity frequency.
        activity: The activity for which to calculate the frequency.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the activity frequency.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_activity_frequency(start_time, end_time, resource, activity)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating activity frequency.",
        )


@router.get("/pql/resource-profile/activity-frequency", response_model=float)
async def get_resource_activity_frequency_pql(
    resource: str = Query(..., description="The resource identifier."),
    activity: str = Query(..., description="The specific activity name."),
    start_time: str = Query(
        ...,
        description="Start time of the interval.",
    ),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the activity frequency for an activity via a PQL query.

    Args:
        resource: The resource for which to calculate the activity frequency.
        activity: The activity for which to calculate the frequency.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the activity frequency.
    """
    try:
        result = resource_based_queries.get_activity_frequency(
            celonis, start_time, end_time, resource, activity
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/activity-completions", response_model=int)
async def get_resource_activity_completions(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of activity instances completed by a resource.

    Args:
        resource: The resource for which to calculate activity completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        An integer indicating the number of activity completions.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_activity_completions(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating activity completions.",
        )


@router.get("/pql/resource-profile/activity-completions", response_model=int)
async def get_resource_activity_completions_pql(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of activity instances completed via a PQL query.

    Args:
        resource: The resource for which to calculate activity completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        An integer indicating the number of activity completions.
    """
    try:
        result = resource_based_queries.get_activity_completions(
            celonis, start_time, end_time, resource
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/case-completions", response_model=int)
async def get_resource_case_completions(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of cases completed by a resource.

    Args:
        resource: The resource for which to calculate case completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        An integer indicating the number of case completions involving the resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_case_completions(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating case completions.",
        )


@router.get("/pql/resource-profile/case-completions", response_model=int)
async def get_resource_case_completions_pql(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> int:
    """Retrieves the number of cases completed by a resource via a PQL query.

    Args:
        resource: The resource for which to calculate case completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        An integer indicating the number of case completions involving the resource.
    """
    try:
        result = resource_based_queries.get_case_completions(
            celonis, start_time, end_time, resource
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return result


@router.get("/resource-profile/fraction-case-completions", response_model=float)
async def get_resource_fraction_case_completions(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the fraction of cases completed by a resource.

    Args:
        resource: The resource for which to calculate the fraction of case completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the fraction of case completions involving the resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_fraction_case_completions(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating fraction of case completions.",
        )


@router.get("/pql/resource-profile/fraction-case-completions", response_model=float)
async def get_resource_fraction_case_completions_pql(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the fraction of cases completed by a resource via a PQL query.

    Args:
        resource: The resource for which to calculate the fraction of case completions.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the fraction of case completions involving the resource.
    """
    try:
        result = resource_based_queries.get_fraction_case_completions(
            celonis, start_time, end_time, resource
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/average-workload", response_model=float)
async def get_resource_average_workload(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the average workload for a given resource in a time interval.

    Args:
        resource: The resource for which to calculate the average workload.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the average workload.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_average_workload(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating average workload.",
        )


@router.get("/pql/resource-profile/average-workload", response_model=float)
async def get_resource_average_workload_pql(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the average workload for a resource via a PQL query.

    Args:
        resource: The resource for which to calculate the average workload.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the average workload.
    """
    try:
        result = resource_based_queries.get_average_workload(
            celonis, start_time, end_time, resource
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/multitasking", response_model=float)
async def get_resource_multitasking(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the multitasking metric for a given resource.

    Args:
        resource: The resource for which to calculate multitasking.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the multitasking metric.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_multitasking(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Internal server error calculating multitasking."
        )


@router.get("/resource-profile/average-activity-duration", response_model=float)
async def get_resource_average_activity_duration(
    resource: str = Query(..., description="The resource identifier."),
    activity: str = Query(..., description="The specific activity name."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the average duration for an activity completed by a resource.

    Args:
        resource: The resource involved.
        activity: The activity name.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the average duration of the activity for the resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_average_activity_duration(
            start_time, end_time, resource, activity
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating average activity duration.",
        )


@router.get("/resource-profile/average-case-duration", response_model=float)
async def get_resource_average_case_duration(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the average duration of cases completed by a resource.

    Args:
        resource: The resource involved.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the average duration of cases involving the resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_average_case_duration(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating average case duration.",
        )


@router.get("/resource-profile/interaction-two-resources", response_model=float)
async def get_interaction_of_two_resources(
    resource1: str = Query(..., description="The first resource identifier."),
    resource2: str = Query(..., description="The second resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the interaction between two resources.

    Args:
        resource1: The first resource.
        resource2: The second resource.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the interaction (number of common cases) between the two resources.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_interaction_two_resources(
            start_time, end_time, resource1, resource2
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error calculating interaction between resources.",
        )


@router.get("/pql/resource-profile/interaction-two-resources", response_model=float)
async def get_interaction_of_two_resources_pql(
    resource1: str = Query(..., description="The first resource identifier."),
    resource2: str = Query(..., description="The second resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the interaction between two resources via a PQL query.

    Args:
        resource1: The first resource.
        resource2: The second resource.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the interaction (number of common cases) between the two resources.
    """
    try:
        result = resource_based_queries.get_interaction_two_resources(
            celonis, start_time, end_time, resource1, resource2
        )
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    return result


@router.get("/resource-profile/social-position", response_model=float)
async def get_resource_social_position(
    resource: str = Query(..., description="The resource identifier."),
    start_time: str = Query(..., description="Start time of the interval."),
    end_time: str = Query(..., description="End time of the interval."),
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> float:
    """Retrieves the social position of a given resource in a time interval.

    Args:
        resource: The resource for which to calculate the social position.
        start_time: The start time of the interval.
        end_time: The end time of the interval.
        celonis: The Celonis connection manager instance.

    Returns:
        A float indicating the social position of the resource.
    """
    df = celonis.get_dataframe_with_resource_group_from_celonis()
    if df is None or df.empty:
        raise HTTPException(status_code=404, detail="No data retrieved from Celonis.")
    try:
        rb = ResourceBased(log=df)
        return rb.get_social_position(start_time, end_time, resource)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Internal server error calculating social position."
        )

# **************** Organizational Mining ****************


@router.get(
    "/organizational-mining/group-relative-focus/{job_id}",
    response_model=ResponseSchema,
)
async def get_group_relative_focus_metric(
    job_id: str, request: Request
) -> ResponseSchema:
    """
    Retrieves the Group Relative Focus metric formatted as a table with headers and rows.

    Returns:
        ResponseSchema with a single table, no graph.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    focus_data = (
        request.app.state.jobs[job_id]
        .result.get("organizational_diagnostics", {})
        .get("group_relative_focus", {})
    )

    rows: List[List[Any]] = [
        [group, activity, f"{score:.4f}"]
        for group, activity_scores in focus_data.items()
        for activity, score in activity_scores.items()
    ]

    return ResponseSchema(
        tables=[
            {
                "headers": ["Group", "Activity", "Relative Focus"],
                "rows": rows,
            }
        ],
        graphs=[],
    )


@router.get(
    "/organizational-mining/group-relative-stake/{job_id}",
    response_model=ResponseSchema,
)
async def get_group_relative_stake_metric(
    job_id: str, request: Request
) -> ResponseSchema:
    """
    Retrieves the Group Relative Stake metric formatted as a table with headers and rows.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        A ResponseSchema containing the Group Relative Stake table.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    stake_data = (
        request.app.state.jobs[job_id]
        .result.get("organizational_diagnostics", {})
        .get("group_relative_stake", {})
    )

    rows: List[List[str]] = [
        [group, activity, f"{score:.4f}"]
        for group, activity_scores in stake_data.items()
        for activity, score in activity_scores.items()
    ]

    return ResponseSchema(
        tables=[
            {
                "headers": ["Group", "Activity", "Relative Stake"],
                "rows": rows,
            }
        ],
        graphs=[],
    )

@router.get(
    "/organizational-mining/group-coverage/{job_id}",
    response_model=ResponseSchema,
)
async def get_group_coverage_metric(
    job_id: str, request: Request
) -> ResponseSchema:
    """
    Retrieves the Group Coverage metric formatted as a table with headers and rows.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        A ResponseSchema containing the Group Coverage table.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    coverage_data = (
        request.app.state.jobs[job_id]
        .result.get("organizational_diagnostics", {})
        .get("group_coverage", {})
    )

    rows: List[List[str]] = [
        [group, resource, f"{score:.4f}"]
        for group, resource_scores in coverage_data.items()
        for resource, score in resource_scores.items()
    ]

    return ResponseSchema(
        tables=[
            {
                "headers": ["Group", "Resource", "Coverage"],
                "rows": rows,
            }
        ],
        graphs=[],
    )

@router.get(
    "/organizational-mining/group-member-contribution/{job_id}",
    response_model=ResponseSchema,
)
async def get_group_member_contribution_metric(
    job_id: str, request: Request
) -> ResponseSchema:
    """
    Retrieves the Group Member Contribution metric formatted as a table.

    Args:
        job_id: The ID of the job to retrieve the metric for.
        request: The FastAPI request object.

    Returns:
        A ResponseSchema containing the Group Member Contribution table.
    """
    verify_correct_job_module(job_id, request, MODULE_NAME)

    contribution_data = (
        request.app.state.jobs[job_id]
        .result.get("organizational_diagnostics", {})
        .get("group_member_contribution", {})
    )

    rows: List[List[str]] = []
    for group, member_dict in contribution_data.items():
        for member, activity_dict in member_dict.items():
            for activity, count in activity_dict.items():
                rows.append([group, member, activity, str(count)])

    return ResponseSchema(
        tables=[
            {
                "headers": ["Group", "Member", "Activity", "Count"],
                "rows": rows,
            }
        ],
        graphs=[],
    )