"""Contains the tasks for handling resource-based conformance checking."""

from typing import Any, Dict, List

from fastapi import FastAPI

from backend.api.models.schemas.job_models import JobStatus
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.conformance_checking.resource_based import (
    ResourceBased,
    SocialNetworkAnalysisType,
)


def _serialize_sna_connections(
    connections: SocialNetworkAnalysisType,
) -> List[Dict[str, Any]]:
    """Helper function to serialize the connections for SNA."""
    return [
        {"source": k[0], "target": k[1], "value": v} for k, v in connections.items()
    ]


def compute_and_store_resource_based_metrics(
    app: FastAPI,
    job_id: str,
    celonis_connection: CelonisConnectionManager,
    resource_column_name: str,
) -> None:
    """Computes the resource-based metrics and stores it in the app state.

    Args:
        app: The FastAPI application instance.
        job_id: The job ID for tracking the task.
        celonis_connection: The CelonisConnectionManager instance.
        resource_column_name: The name of the resource column in the DataFrame.

    Raises:
        RuntimeError: If the DataFrame is empty.
    """
    rec: JobStatus = app.state.jobs[job_id]

    try:
        rec.status = "running"
        app.state.jobs[job_id] = rec
        df = celonis_connection.get_basic_dataframe_from_celonis()

        if df is None or df.empty:
            rec.status = "failed"
            raise RuntimeError(
                "The DataFrame is empty. Please check the Celonis connection and the data."
            )

        rb = ResourceBased(df, resource_col=resource_column_name)
        rb.compute_handover_of_work()
        rb.compute_subcontracting()
        rb.compute_working_together()
        rb.compute_similar_activities()

        rb.compute_organizational_roles()

        rb.compute_organizational_diagnostics()

        rec.result = {
            "handover_of_work": {
                "values": _serialize_sna_connections(rb.get_handover_of_work_values()),
                "is_directed": rb.is_handover_of_work_directed(),
            },
            "subcontracting": {
                "values": _serialize_sna_connections(rb.get_subcontracting_values()),
                "is_directed": rb.is_subcontracting_directed(),
            },
            "working_together": {
                "values": _serialize_sna_connections(rb.get_working_together_values()),
                "is_directed": rb.is_working_together_directed(),
            },
            "similar_activities": {
                "values": _serialize_sna_connections(
                    rb.get_similar_activities_values()
                ),
                "is_directed": rb.is_similar_activities_directed(),
            },
            "organizational_roles": rb.get_organizational_roles(),
            "organizational_diagnostics": {
                "group_relative_focus": rb.get_group_relative_focus(),
                "group_relative_stake": rb.get_group_relative_stake(),
                "group_coverage": rb.get_group_coverage(),
                "group_member_contribution": rb.get_group_member_contribution(),
            },
        }
        rec.status = "complete"
        rec.error = None

    except Exception as e:
        rec.status = "failed"
        rec.error = str(e)

    finally:
        app.state.jobs[job_id] = rec
