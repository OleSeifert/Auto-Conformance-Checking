"""Contains the router for general informtion API endpoints."""

import asyncio
from typing import Dict, List, TypeAlias, Union

import pandas as pd
from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from backend.api.celonis import get_celonis_connection
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.pql_queries import general_queries

router = APIRouter(
    prefix="/api/general",
    tags=["General Information"],
)

# **************** Type Aliases ****************

TableType: TypeAlias = Dict[str, Union[List[str], List[List[str]]]]
GraphType: TypeAlias = Dict[str, List[Dict[str, str]]]
EndpointReturnType: TypeAlias = Dict[str, Union[List[TableType], List[GraphType]]]

# **************** Endpoint ****************


@router.get("/get-general-information", response_model=EndpointReturnType)
async def get_general_information(
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> EndpointReturnType:
    """Fetches general information about the process from Celonis.

    This endpoint retrieves the number of cases, activities, trace variants,
    and the Directly-Follows Graph (DFG) representation of the process.

    Args:
        celonis (optional): The CelonisConnectionManager. Defaults to
          Depends(get_celonis_connection).

    Returns:
        A dictionary containing tables with general information and a graph
        representing the Directly-Follows Graph (DFG).
    """
    # Retrieve all information in an asynchronous manner and await it
    counts_df, traces_df, activities_df, dfg_df = await asyncio.gather(  # type: ignore
        run_in_threadpool(general_queries.get_general_information, celonis),
        run_in_threadpool(general_queries.get_traces_with_count, celonis),
        run_in_threadpool(general_queries.get_activities, celonis),
        run_in_threadpool(general_queries.get_dfg_representation, celonis),
    )

    # Perform transformations to the wanted output format
    counts_table = transform_counts_df_to_endpoint_format(counts_df)
    trace_variants_table = transform_traces_df_to_endpoint_format(traces_df)
    dfg_graph = transform_dfg_df_to_endpoint_format(dfg_df, activities_df)

    res: EndpointReturnType = {
        "tables": [counts_table, trace_variants_table],
        "graphs": [dfg_graph],
    }
    return res


# **************** Helper Functions ****************


def transform_counts_df_to_endpoint_format(
    counts_df: pd.DataFrame,
) -> TableType:
    """Transforms the counts DataFrame into a format suitable for the endpoint.

    Args:
        counts_df: The DataFrame containing counts of cases, activities, and
          trace variants.

    Returns:
        A dictionary encoding a table with general information.
    """
    case_count: int = counts_df["CaseCount"].iloc[0] if not counts_df.empty else 0  # type: ignore
    activity_count: int = (  # type: ignore
        counts_df["ActivityCount"].iloc[0] if not counts_df.empty else 0  # type: ignore
    )
    trace_variants: int = (  # type: ignore
        counts_df["TraceVariants"].iloc[0] if not counts_df.empty else 0  # type: ignore
    )

    res: Dict[str, Union[List[str], List[List[str]]]] = {
        "headers": ["Information", "Count"],
        "rows": [
            ["Number of Cases", str(case_count)],  # type: ignore
            ["Number of Activities", str(activity_count)],  # type: ignore
            ["Number of Trace Variants", str(trace_variants)],  # type: ignore
        ],
    }

    return res


def transform_traces_df_to_endpoint_format(
    traces_df: pd.DataFrame,
) -> TableType:
    """Transforms the traces DataFrame into a format suitable for the endpoint.

    Args:
        traces_df: The DataFrame containing traces and their counts.

    Returns:
        A dictionary encoding a table with trace variants and their counts.
    """
    if traces_df.empty:
        res: Dict[str, Union[List[str], List[List[str]]]] = {"headers": [], "rows": []}
        return res

    res_: Dict[str, Union[List[str], List[List[str]]]] = {
        "headers": ["Trace Variant", "Count"],
        "rows": [
            # Convert each count to a string
            [trace, str(count)]  # type: ignore
            for trace, count in traces_df.values.tolist()  # type: ignore
        ],
    }

    return res_


def transform_dfg_df_to_endpoint_format(
    dfg_df: pd.DataFrame, activities_df: pd.DataFrame
) -> GraphType:
    """Transforms the DFG DataFrame into a format suitable for the endpoint.

    This function encodes the DFG as a dictionary with nodes and edges,
    where nodes represent unique activities and edges represent the
    relationships between them with their respective counts.

    Args:
        dfg_df: The DataFrame containing the DFG representation.
        activities_df: The DataFrame containing the activities.

    Returns:
        A dictionary containing the encoded DFG.
    """
    # Gather unique activities
    unique_activities = get_unique_activities(activities_df)

    if dfg_df.empty:
        res: Dict[str, List[Dict[str, str]]] = {"nodes": [], "edges": []}
        return res

    res_: Dict[str, List[Dict[str, str]]] = {
        "nodes": [{"id": str(activity)} for activity in unique_activities],
        "edges": [
            {"from": from_act, "to": to_act, "label": str(count)}  # type: ignore
            for from_act, to_act, count in dfg_df.values.tolist()  # type: ignore
        ],
    }

    return res_


def get_unique_activities(activities_df: pd.DataFrame) -> List[str]:
    """Extracts unique activities from the activities DataFrame.

    Args:
        activities_df: The DataFrame containing activities.

    Returns:
        A list of the unique activities.
    """
    if activities_df.empty:
        return []
    return activities_df["Activity"].tolist()  # type: ignore
