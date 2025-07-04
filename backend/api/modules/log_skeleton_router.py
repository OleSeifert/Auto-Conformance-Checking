"""Contains the routes for handling log skeletons and related operations."""

import uuid
from typing import Dict, List, Literal, TypedDict

from fastapi import APIRouter, BackgroundTasks, Depends, Request

from backend.api.celonis import get_celonis_connection
from backend.api.models.schemas.job_models import JobStatus
from backend.api.tasks.log_skeleton_tasks import compute_and_store_log_skeleton
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.pql_queries import general_queries, log_skeleton_queries

router = APIRouter(prefix="/api/log-skeleton", tags=["Log Skeleton CC"])
MODULE_NAME = "log_skeleton"

# **************** Type Definitions ****************


class Table(TypedDict):
    """Type definition for a table structure."""

    headers: List[str]
    rows: List[List[str]]


class Graph(TypedDict):
    """Type definition for a graph structure."""

    nodes: List[Dict[Literal["id"], str]]
    edges: List[Dict[Literal["from", "to", "label"], str]]


class EndpointReturnType(TypedDict):
    """Type definition for the return type of the endpoint."""

    tables: List[Table]
    graphs: List[Graph]


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


@router.get("/old/get_equivalence/{job_id}")
def get_equivalence(job_id: str, request: Request) -> EndpointReturnType:
    """Retrieves the equivalence relations from the log skeleton.

    Args:
        job_id: The ID of the job for which to retrieve the equivalence relations.
        request: The FastAPI request object.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result = request.app.state.jobs[job_id].result.get("equivalence", [])
    if not result:
        return {"tables": [], "graphs": []}
    return {
        "tables": [{"headers": ["Activity A", "Activity B"], "rows": result}],
        "graphs": [],
    }


@router.get("/get_equivalence/")
def get_equivalence_pql(
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Retrieves the equivalence relations from the log skeleton via PQL.

    Args:
        request: The FastAPI request object.
        celonis: The CelonisManager dependency injection.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result_df = log_skeleton_queries.get_equivalance_relation(celonis)
    if result_df.empty:
        return {"tables": [], "graphs": []}

    # Create tables sub-structure
    tables: Table = {"headers": [], "rows": []}
    tables["headers"] = result_df.columns.tolist()
    tables["rows"] = result_df[result_df["Rel"] == "true"].values.tolist()  # type: ignore

    # Create graphs sub-structure
    graphs: Graph = {"nodes": [], "edges": []}
    graphs["nodes"] = []
    graphs["edges"] = []

    activities = general_queries.get_activities(celonis)["Activity"].tolist()  # type: ignore
    for act in activities:  # type: ignore
        graphs["nodes"].append({"id": act})

    for _, row in result_df.iterrows():  # type: ignore
        if row["Rel"] == "true":
            graphs["edges"].append(
                {
                    "from": row["Activity A"],
                    "to": row["Activity B"],
                    "label": "equals_to",
                }
            )

    # Remove the "Rel" column from the headers and rows (as it is always "true")
    tables["headers"].remove("Rel")  # type: ignore
    tables["rows"] = [row[:-1] for row in tables["rows"]]  # type: ignore

    return {
        "tables": [tables],
        "graphs": [graphs],
    }


@router.get("/old/get_always_after/{job_id}")
def get_always_after(job_id: str, request: Request) -> EndpointReturnType:
    """Retrieves the always-after relations from the log skeleton.

    Returns:
        A dictionary with a "tables" list and optional "graphs" list.
    """
    result = request.app.state.jobs[job_id].result.get("always_after", [])
    if not result:
        return {"tables": [], "graphs": []}
    return {
        "tables": [
            {"headers": ["Activity A", "Always After Activity B"], "rows": result}
        ],
        "graphs": [],
    }


@router.get("/get_always_after/")
def get_always_after_pql(
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Retrieves the always-after relations from the log skeleton via PQL.

    Args:
        request: The FastAPI request object.
        celonis: The CelonisManager dependency injection.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result_df = log_skeleton_queries.get_always_after_relation(celonis)
    if result_df.empty:
        return {"tables": [], "graphs": []}  # type: ignore
    # Create tables sub-structure
    tables: Table = {"headers": [], "rows": []}
    tables["headers"] = result_df.columns.tolist()
    tables["rows"] = result_df[result_df["Rel"] == "true"].values.tolist()  # type: ignore

    # Create graphs sub-structure
    graphs: Graph = {"nodes": [], "edges": []}
    graphs["nodes"] = []
    graphs["edges"] = []

    activities = general_queries.get_activities(celonis)["Activity"].tolist()  # type: ignore
    for act in activities:  # type: ignore
        graphs["nodes"].append({"id": act})

    for _, row in result_df.iterrows():  # type: ignore
        if row["Rel"] == "true":
            graphs["edges"].append(
                {
                    "from": row["Activity A"],
                    "to": row["Activity B always after A"],
                    "label": "always_after",
                }
            )

    # Remove the "Rel" column from the headers and rows (as it is always "true")
    tables["headers"].remove("Rel")
    tables["rows"] = [row[:-1] for row in tables["rows"]]  # type: ignore

    return {
        "tables": [tables],
        "graphs": [graphs],
    }


@router.get("/old/get_always_before/{job_id}")
def get_always_before(job_id: str, request: Request) -> EndpointReturnType:
    """Retrieves the always-before relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("always_before", [])
    if not result:
        return {"tables": [], "graphs": []}
    return {
        "tables": [
            {"headers": ["Activity A", "Always Before Activity B"], "rows": result}
        ],
        "graphs": [],
    }


@router.get("/get_always_before/")
def get_always_before_pql(
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Retrieves the always-before relations from the log skeleton via PQL.

    Args:
        request: The FastAPI request object.
        celonis: The CelonisManager dependency injection.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result_df = log_skeleton_queries.get_always_before_relation(celonis)
    if result_df.empty:
        return {"tables": [], "graphs": []}  # type: ignore
    # Create tables sub-structure
    tables: Table = {"headers": [], "rows": []}
    tables["headers"] = result_df.columns.tolist()
    tables["rows"] = result_df[result_df["Rel"] == "true"].values.tolist()  # type: ignore

    # Create graphs sub-structure
    graphs: Graph = {"nodes": [], "edges": []}
    graphs["nodes"] = []
    graphs["edges"] = []

    activities = general_queries.get_activities(celonis)["Activity"].tolist()  # type: ignore
    for act in activities:  # type: ignore
        graphs["nodes"].append({"id": act})

    for _, row in result_df.iterrows():  # type: ignore
        if row["Rel"] == "true":
            graphs["edges"].append(
                {
                    "from": row["Activity A always before"],
                    "to": row["Activity B"],
                    "label": "always_before",
                }
            )

    # Remove the "Rel" column from the headers and rows (as it is always "true")
    tables["headers"].remove("Rel")
    tables["rows"] = [row[:-1] for row in tables["rows"]]  # type: ignore

    return {
        "tables": [tables],
        "graphs": [graphs],
    }


@router.get("/old/get_never_together/{job_id}")
def get_never_together(job_id: str, request: Request) -> EndpointReturnType:  # type: ignore
    """Retrieves the never-together relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("never_together", [])
    if not result:
        return {"tables": [], "graphs": []}
    return {
        "tables": [
            {"headers": ["Activity A", "Activity B (Never Together)"], "rows": result}
        ],
        "graphs": [],
    }


@router.get("/get_never_together/")
def get_never_together_pql(
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Retrieves the never-together relations from the log skeleton via PQL.

    Args:
        request: The FastAPI request object.
        celonis: The CelonisManager dependency injection.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result_df = log_skeleton_queries.get_never_together_relation(celonis)
    if result_df.empty:
        return {"tables": [], "graphs": []}  # type: ignore
    # Create tables sub-structure
    tables: Table = {"headers": [], "rows": []}
    tables["headers"] = result_df.columns.tolist()
    tables["rows"] = result_df[result_df["Rel"] == "true"].values.tolist()  # type: ignore

    # Create graphs sub-structure
    graphs: Graph = {"nodes": [], "edges": []}
    graphs["nodes"] = []
    graphs["edges"] = []

    activities = general_queries.get_activities(celonis)["Activity"].tolist()  # type: ignore
    for act in activities:  # type: ignore
        graphs["nodes"].append({"id": act})

    for _, row in result_df.iterrows():  # type: ignore
        if row["Rel"] == "true":
            graphs["edges"].append(
                {
                    "from": row["Activity A"],
                    "to": row["Activity B"],
                    "label": "never_together",
                }
            )

    # Remove the "Rel" column from the headers and rows (as it is always "true")
    tables["headers"].remove("Rel")
    tables["rows"] = [row[:-1] for row in tables["rows"]]  # type: ignore

    return {
        "tables": [tables],
        "graphs": [graphs],
    }


@router.get("/old/get_directly_follows/{job_id}")
def get_directly_follows(job_id: str, request: Request) -> EndpointReturnType:
    """Retrieves the directly-follows relations from the log skeleton."""
    result = request.app.state.jobs[job_id].result.get("directly_follows", [])
    if not result:
        return {"tables": [], "graphs": []}
    return {
        "tables": [
            {"headers": ["Preceding Activity", "Following Activity"], "rows": result}
        ],
        "graphs": [],
    }


@router.get("/get_directly_follows_and_count/")
def get_directly_follows_pql(
    request: Request,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Retrieves the directly-follows relations from the log skeleton via PQL.

    Args:
        request: The FastAPI request object.
        celonis: The CelonisManager dependency injection.

    Returns:
        A JSON object with "tables" and "graphs" keys.
    """
    result_df = log_skeleton_queries.get_directly_follows_relation_and_count(celonis)
    if result_df.empty:
        return {"tables": [], "graphs": []}  # type: ignore

    # Create tables sub-structure
    tables: Table = {"headers": [], "rows": []}
    tables["headers"] = result_df.columns.tolist()
    tables["rows"] = result_df[result_df["Rel"] == "true"].astype(str).values.tolist()  # type: ignore

    # Create graphs sub-structure
    graphs: Graph = {"nodes": [], "edges": []}
    graphs["nodes"] = []
    graphs["edges"] = []

    activities = general_queries.get_activities(celonis)["Activity"].tolist()  # type: ignore
    for act in activities:  # type: ignore
        graphs["nodes"].append({"id": act})

    for _, row in result_df.iterrows():  # type: ignore
        if row["Rel"] == "true":
            graphs["edges"].append(
                {
                    "from": row["Activity A"],
                    "to": row["Activity B Directly-follows A"],
                    "label": str(row["Count"]),  # type: ignore
                }
            )

    # Remove the "Rel" column from the headers and rows (as it is always "true")
    tables["headers"].remove("Rel")
    tables["rows"] = [row[:-2] + row[-1:] for row in tables["rows"]]  # type: ignore

    return {
        "tables": [tables],
        "graphs": [graphs],
    }


@router.get("/old/get_activity_frequencies/{job_id}")
def get_activity_frequencies(job_id: str, request: Request) -> EndpointReturnType:
    """Retrieves the activity frequencies from the log skeleton."""
    freq_dict = request.app.state.jobs[job_id].result.get("activ_freq", {})

    # Format the frequencies into a list of lists for the table
    rows = [  # type: ignore
        [activity, ", ".join(map(str, count))] for activity, count in freq_dict.items()
    ]
    if not rows:
        return {"tables": [], "graphs": []}
    return {
        "tables": [{"headers": ["Activity", "Frequency"], "rows": rows}],  # type: ignore
        "graphs": [],
    }
