"""Queries that can be used to get log-skeleton related data from celonis."""

from itertools import combinations
from typing import Dict, List, TypeAlias, Union, Any

from pandas import DataFrame
import pandas as pd

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.pql_queries.general_queries import get_activities

# **************** Type Aliases ****************

# TableType: TypeAlias = Dict[str, Union[List[str], List[List[str]]]]
# GraphType: TypeAlias = Dict[str, List[Dict[str, str]]]
TableType: TypeAlias = Dict[str, Any]
GraphType: TypeAlias = Dict[str, Any]
ReturnGraphType: TypeAlias = Dict[str, Union[List[TableType], List[GraphType]]]

# **************** Formatting Function ****************


def format_graph_and_table(curr_df: pd.DataFrame) -> ReturnGraphType:
    """Formats the DataFrame into a graph and table structure.

    Args:
        curr_df (pd.DataFrame): The DataFrame to format.

    Returns:
        ReturnGraphType: A dictionary containing the formatted graph and table.
    """
    output: ReturnGraphType = {"graphs": [], "tables": []}

    if not curr_df.empty:
        if curr_df.shape[1] == 3:
            nodes = []
            edges = []
            for i, row in curr_df.iterrows():  # type: ignore
                nodes.append(str(row[curr_df.columns[0]]))  # type: ignore
                nodes.append(str(row[curr_df.columns[1]]))  # type: ignore
                edges.append(
                    {  # type: ignore
                        "from": str(row[curr_df.columns[0]]),  # type: ignore
                        "to": str(row[curr_df.columns[1]]),  # type: ignore
                        "label": str(row[curr_df.columns[2]]),  # type: ignore
                    }
                )

            nodes = [{"id": str(ele)} for ele in list(set(list(nodes)))]  # type: ignore
            output["graphs"].append(
                {
                    "nodes": nodes,  # type: ignore
                    "edges": edges,
                }
            )

            headers = list(curr_df.columns)
            rows = curr_df.values.tolist()  # type: ignore
            output["tables"].append(
                {
                    "headers": headers,  # type: ignore
                    "rows": [[str(ele) for ele in row] for row in rows],  # type: ignore
                }
            )
        else:
            headers = list(curr_df.columns)
            rows = curr_df.values.tolist()  # type: ignore
            output["tables"].append(
                {
                    "headers": headers,  # type: ignore
                    "rows": [[str(ele) for ele in row] for row in rows],  # type: ignore
                }
            )
    return output


# **************** PQL Functions ****************


# Always before
def get_always_before_relation(celonis: CelonisConnectionManager) -> ReturnGraphType:
    """Compute Always-Before summary using PQL.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        ReturnGraphType: A dictionary containing the formatted graph and table.
    """
    target_df: pd.DataFrame = DataFrame(
        columns=["Activity A", "Activity B", "# Occurrences"]
    )
    act_table = get_activities(celonis)  # type: ignore
    activitiy_pairs = list(combinations(act_table["Activity"].to_list(), 2))  # type: ignore
    for i, pair in enumerate(activitiy_pairs):  # type: ignore
        query = {
            "A before B": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE ['{pair[0]}'] as src,
                            NODE ['{pair[1]}'] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
            "B before A": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE ['{pair[1]}'] as src,
                            NODE ['{pair[0]}'] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
        }
        pair_df = celonis.get_dataframe_from_celonis(query)  # type: ignore
        if (pair_df["B before A"] == 1).any() and not (
            pair_df["A before B"] == 1
        ).any():  # type: ignore
            target_df.loc[i] = [
                pair[1],
                pair[0],
                int((pair_df["B before A"] == 1).sum()),
            ]  # type: ignore
        elif (pair_df["A before B"] == 1).any() and not (
            pair_df["B before A"] == 1
        ).any():  # type: ignore
            target_df.loc[i] = [
                pair[0],
                pair[1],
                int((pair_df["A before B"] == 1).sum()),
            ]  # type: ignore
    output = format_graph_and_table(target_df)
    return output


# Always after
def get_always_after_relation(celonis: CelonisConnectionManager) -> ReturnGraphType:
    """Compute Always-After summary using PQL.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        ReturnGraphType: A dictionary containing the formatted graph and table.
    """
    target_df = DataFrame(columns=["Activity A", "Activity B", "# Occurrences"])
    act_table = get_activities(celonis)
    activitiy_pairs = list(combinations(act_table["Activity"].to_list(), 2))  # type: ignore
    for i, pair in enumerate(activitiy_pairs):  # type: ignore
        query = {
            "A after B": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE ['{pair[1]}'] as src,
                            NODE ['{pair[0]}'] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
            "B after A": f"""MATCH_PROCESS ("ACTIVITIES"."concept:name", NODE ['{pair[0]}'] as src,
                            NODE ['{pair[1]}'] as tgt CONNECTED BY EVENTUALLY [src , tgt])""",
        }
        pair_df = celonis.get_dataframe_from_celonis(query)  # type: ignore
        if (pair_df["B after A"] == 1).any() and not (pair_df["A after B"] == 1).any():  # type: ignore
            target_df.loc[i] = [
                pair[1],
                pair[0],
                int((pair_df["B after A"] == 1).sum()),
            ]  # type: ignore
        elif (pair_df["A after B"] == 1).any() and not (
            pair_df["B after A"] == 1
        ).any():  # type: ignore
            target_df.loc[i] = [
                pair[0],
                pair[1],
                int((pair_df["A after B"] == 1).sum()),
            ]  # type: ignore
    output = format_graph_and_table(target_df)
    return output
