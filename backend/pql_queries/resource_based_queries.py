"""Queries that can be used to get resource related data from celonis."""

from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from pandas import DataFrame
from pycelonis_core.utils.errors import PyCelonisNotFoundError
from scipy.stats import pearsonr  # type: ignore

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)


def get_number_of_resources(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the count of resources from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of resources
    """
    resource_query = {
        "Resource Count": """ COUNT (DISTINCT "ACTIVITIES"."org:resource" )"""
    }
    return celonis.get_dataframe_from_celonis(resource_query)  # type: ignore


def get_number_of_groups(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the count of groups from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of groups
    """
    activity_query = {"Groups Count": """ COUNT (DISTINCT "ACTIVITIES"."org:group" )"""}
    return celonis.get_dataframe_from_celonis(activity_query)  # type: ignore


def get_resource_for_activity(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that maps activities to their related resources.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the mapping between activities to their related resources
    """
    table_columns = celonis.get_table_columns()
    if table_columns is not None:
        try:
            query = {
                "Activity": table_columns.find("concept:name"),
                "Resource": table_columns.find("org:resource"),
            }
        except PyCelonisNotFoundError:
            print("Table columns not found in data model.")
    return celonis.get_dataframe_from_celonis(query)  # type: ignore


def get_handover_of_work_values(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the Handover of Work metric.

    The Handover of Work metric is a dictionary where the keys are
    tuples of two individuals and the values are the number of times
    the first individual is followed by the second individual
    in the execution of a business process.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        The Handover of Work metric.
    """
    handover_query = {
        "Resource 1": """ SOURCE("ACTIVITIES"."org:resource") """,
        "Resource 2": """ TARGET("ACTIVITIES"."org:resource") """,
        "Count": """ COUNT(SOURCE("ACTIVITIES"."org:resource")) """,
    }
    dataframe = celonis.get_dataframe_from_celonis(handover_query)  # type: ignore

    result_df = dataframe.copy()  # type: ignore
    result_df["Value"] = result_df["Count"] / result_df["Count"].sum()  # type: ignore
    result_df = result_df.drop(columns=["Count"])
    return result_df  # type: ignore


def get_subcontracting_values(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the Subcontracting metric.

    The Subcontracting metric is a dictionary where the keys are
    tuples of two individuals and the values are the number of times
    the first individual is interleaved by the second individual
    in the execution of a business process.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
         The Subcontracting metric.
    """
    subcontracting_query = {
        "Case": """ "ACTIVITIES"."case:concept:name" """,
        "Resource": """ "ACTIVITIES"."org:resource" """,
    }
    dataframe = celonis.get_dataframe_from_celonis(subcontracting_query)  # type: ignore

    df = dataframe.copy()  # type: ignore
    df = df.sort_values(by=["Case"])  # type: ignore

    # Set gap/distance between resources
    n = 2

    # Create resource sequences per case
    case_resource_seqs = df.groupby("Case")["Resource"].apply(list).tolist()  # type: ignore

    # Initialize counters
    sum_i_to_j = defaultdict(lambda: defaultdict(int))  # type: ignore
    total_sequences = len(case_resource_seqs)

    # Iterate through sequences
    for seq in case_resource_seqs:
        for i in range(len(seq) - n):
            res_i = seq[i]
            res_i_n = seq[i + n]

            # Only consider when the same resource reappears
            if res_i == res_i_n:
                for j in range(i + 1, i + n):
                    res_j = seq[j]
                    if res_j != res_i:
                        sum_i_to_j[res_i][res_j] += 1

    # Normalize by total number of sequences
    rows = []  # type: ignore
    for res_i in sum_i_to_j:  # type: ignore
        for res_j in sum_i_to_j[res_i]:  # type: ignore
            value = sum_i_to_j[res_i][res_j] / total_sequences
            rows.append((res_i, res_j, value))  # type: ignore

    result_df = pd.DataFrame(rows, columns=["Resource 1", "Resource 2", "Value"])
    return result_df


def get_working_together_values(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the Working Together metric.

    The Working Together metric is a dictionary where the keys are
    tuples of two individuals and the values are the number of times
    the two individuals worked together to resolve a process instance.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        The Working Together metric.
    """
    working_together_query = {
        "Case": """ "ACTIVITIES"."case:concept:name" """,
        "Resource": """ "ACTIVITIES"."org:resource" """,
    }
    dataframe = celonis.get_dataframe_from_celonis(working_together_query)  # type: ignore

    df = dataframe.copy()  # type: ignore

    cases = df["Case"].unique()  # type: ignore
    case_resource_lists = []

    # For each case, get the list of unique resources involved (order does not matter)
    for case in cases:
        res_list = df[df["Case"] == case]["Resource"].unique().tolist()  # type: ignore
        case_resource_lists.append(res_list)  # type: ignore

    # Flat list of all unique resources, sorted
    flat_list = sorted(  # type: ignore
        list(set(item for sublist in case_resource_lists for item in sublist))  # type: ignore
    )

    connections = Counter()  # type: ignore
    total_cases = len(cases)  # type: ignore

    for idx, rv in enumerate(case_resource_lists):  # type: ignore
        # Only consider unique resources per case (as in original logic)
        ord_res_list = sorted(list(set(rv)))  # type: ignore
        for i in range(len(ord_res_list) - 1):  # type: ignore
            res_i = flat_list.index(ord_res_list[i])  # type: ignore
            for j in range(i + 1, len(ord_res_list)):  # type: ignore
                res_j = flat_list.index(ord_res_list[j])  # type: ignore
                # Add to both (i, j) and (j, i) for undirected metric
                connections[(flat_list[res_i], flat_list[res_j])] += 1.0 / total_cases  # type: ignore
                connections[(flat_list[res_j], flat_list[res_i])] += 1.0 / total_cases  # type: ignore

    # Create the output DataFrame
    rows = [  # type: ignore
        (res1, res2, value / get_number_of_resources(celonis))
        for (res1, res2), value in connections.items()  # type: ignore
    ]
    result_df = pd.DataFrame(rows, columns=["Resource 1", "Resource 2", "Value"])
    return result_df


def get_similar_activities_values(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the Similar Activities metric.

    The Similar Activities metric is a dictionary where the keys are
    tuples of two individuals and the values are the similarity score
    between the two individuals.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        The Similar Activities metric.
    """
    similar_activities_query = {
        "Activity": """ "ACTIVITIES"."concept:name" """,
        "Resource": """ "ACTIVITIES"."org:resource" """,
    }
    dataframe = celonis.get_dataframe_from_celonis(similar_activities_query)  # type: ignore

    df = dataframe.copy()  # type: ignore

    # Count the frequency of each activity and resource
    activities = Counter(df["Activity"])  # type: ignore
    resources = Counter(df["Resource"])  # type: ignore

    # Count how many times each (resource, activity) pair occurs
    activity_resource_couples = Counter(zip(df["Resource"], df["Activity"]))  # type: ignore

    # Create sorted lists of unique activities and resources
    activities_keys = sorted(list(activities.keys()))  # type: ignore
    resources_keys = sorted(list(resources.keys()))  # type: ignore

    # Initialize a matrix where each row is a resource and each column is an activity
    rsc_act_matrix = np.zeros((len(resources_keys), len(activities_keys)))  # type: ignore

    # Fill the matrix with counts from the (resource, activity) pairs
    for (resource, activity), count in activity_resource_couples.items():  # type: ignore
        i = resources_keys.index(resource)  # type: ignore
        j = activities_keys.index(activity)  # type: ignore
        rsc_act_matrix[i, j] = count

    # Compute Pearson correlations between each pair of different resources
    records = []
    for i in range(rsc_act_matrix.shape[0]):  # type: ignore
        vect_i = rsc_act_matrix[i, :]  # type: ignore
        for j in range(
            i + 1,
            rsc_act_matrix.shape[0],  # type: ignore
        ):  # Only one direction, avoid repeats
            vect_j = rsc_act_matrix[j, :]  # type: ignore
            r, _ = pearsonr(vect_i, vect_j)  # type: ignore
            records.append(  # type: ignore
                {
                    "Source": resources_keys[i],
                    "Target": resources_keys[j],
                    "Pearson Correlation": r,
                }
            )

    result_df = pd.DataFrame(records)
    return result_df
