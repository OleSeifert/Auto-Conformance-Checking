"""Queries that can be used to get resource related data from celonis."""

from collections import Counter, defaultdict
from itertools import product

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


# **************** Social Network Analysis ****************


def get_handover_of_work_values(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the Handover of Work metric.

    The Handover of Work metric is a dictionary where the keys are
    tuples of two individuals and the values are the number of times
    the first individual is followed by the second individual
    in the execution of a business process.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A DataFrame containing the Handover of Work metric.
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
        A DataFrame containing the Subcontracting metric.
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
        A DataFrame containing the Working Together metric.
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
        A DataFrame containing the Similar Activities metric.
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


# **************** Role Discovery ****************


def get_organizational_roles(celonis: CelonisConnectionManager) -> DataFrame:
    """Returns the organizational roles.

    The organizational roles are stored as a semi-structured list of
    activity groups, where each group associates a list of activities
    with a dictionary of originators and their corresponding
    importance scores.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        A DataFrame containing the organizational roles.
    """
    organizational_roles_query = {
        "Activity": """ "ACTIVITIES"."concept:name" """,
        "Resource": """ "ACTIVITIES"."org:resource" """,
    }
    dataframe = celonis.get_dataframe_from_celonis(organizational_roles_query)  # type: ignore

    df = dataframe.copy()  # type: ignore

    grouped = df.groupby(["Activity", "Resource"]).size().reset_index(name="count")  # type: ignore

    # Pivot to nested dict per activity
    result_df = (
        grouped.groupby("Activity")  # type: ignore
        .apply(lambda g: dict(zip(g["Resource"], g["count"])))  # type: ignore
        .reset_index(name="originators_importance")  # type: ignore
    )

    return result_df


# **************** Resource Profiles ****************


def get_number_of_distinct_activities(
    celonis: CelonisConnectionManager, start_time: str, end_time: str, resource: str
) -> int:
    """Calculates the number of distinct activities.

    Number of distinct activities done by a resource in a given time
    interval [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the number of
            distinct activities.

    Returns:
        An integer denoting the number of distinct activities.
    """
    distinct_activities_query = {
        "Distinct Activities Count": f"""
        COUNT(DISTINCT
            CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                 AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                 AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
            THEN "ACTIVITIES"."concept:name"
            END
        )
    """
    }
    dataframe = celonis.get_dataframe_from_celonis(distinct_activities_query)  # type: ignore
    return int(dataframe["Distinct Activities Count"].iloc[0])  # type: ignore


def get_activity_frequency(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
    activity: str,
) -> float:
    """Calculates the activity frequency.

    Fraction of completions of a given activity a by a given
    resource r during a given time slot [t1, t2), with respect to
    the total number of activity completions by resource r during
    [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the activity
            frequency.
        activity (str): The activity for which to calculate the frequency.

    Returns:
        A float indicating the activity frequency of the given activity
        by the resource in the given time interval.
    """
    activity_frequency_query = {
        "Activity Frequency": f"""
            CASE
                WHEN COUNT(
                    CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                         AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                         AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                    THEN "ACTIVITIES"."concept:name"
                    END
                ) = 0
                THEN 0.0
                ELSE
                    COUNT(
                        CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                             AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                             AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                             AND "ACTIVITIES"."concept:name" = '{activity}'
                        THEN "ACTIVITIES"."concept:name"
                        END
                    ) * 1.0 /
                    COUNT(
                        CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                             AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                             AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                        THEN "ACTIVITIES"."concept:name"
                        END
                    )
            END
        """
    }
    dataframe = celonis.get_dataframe_from_celonis(activity_frequency_query)  # type: ignore
    return float(dataframe["Activity Frequency"].iloc[0])  # type: ignore


def get_activity_completions(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> int:
    """Calculates the number of activity completions.

    Number of completions of a given activity by a given resource
    during a given time slot [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the number of
            activity completions.

    Returns:
        An integer denoting the number of activity completions by the
        resource in the given time interval.
    """
    activity_completions_query = {
        "Activity Completions": f"""
        COUNT(
            CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                 AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                 AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
            THEN "ACTIVITIES"."concept:name"
            END
        )
    """
    }
    dataframe = celonis.get_dataframe_from_celonis(activity_completions_query)  # type: ignore
    return int(dataframe["Activity Completions"].iloc[0])  # type: ignore


def get_case_completions(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> int:
    """Calculates the number of case completions.

    Number of completions of a given case by a given resource
    during a given time slot [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the number of
            case completions.

    Returns:
        An integer denoting the number of case completions by the
        resource in the given time interval.
    """
    case_completions_query = {
        "Case Completions": f"""
        COUNT(DISTINCT
            CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                 AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                 AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
            THEN "ACTIVITIES"."case:concept:name"
            END
        )
    """
    }

    dataframe = celonis.get_dataframe_from_celonis(case_completions_query)  # type: ignore
    return int(dataframe["Case Completions"].iloc[0])  # type: ignore


def get_fraction_case_completions(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> float:
    """Calculates the fraction of case completions.

    Fraction of completions of a case by a given resource r during
    a given time slot [t1, t2), with respect to the total number of
    case completions during [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the fraction
            of case completions.

    Returns:
        A float indicating the fraction of case completions by the
        resource in the given time interval.
    """
    fraction_case_completions_query = {
        "Fraction Case Completions": f"""
        CASE
            WHEN COUNT(DISTINCT
                CASE WHEN "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                     AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                THEN "ACTIVITIES"."case:concept:name"
                END
            ) = 0 THEN 0.0
            ELSE
                COUNT(DISTINCT
                    CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                         AND "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                         AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                    THEN "ACTIVITIES"."case:concept:name"
                    END
                ) * 1.0 /
                COUNT(DISTINCT
                    CASE WHEN "ACTIVITIES"."time:timestamp" >= {{d'{start_time}'}}
                         AND "ACTIVITIES"."time:timestamp" < {{d'{end_time}'}}
                    THEN "ACTIVITIES"."case:concept:name"
                    END
                )
        END
    """
    }
    dataframe = celonis.get_dataframe_from_celonis(fraction_case_completions_query)  # type: ignore
    return float(dataframe["Fraction Case Completions"].iloc[0])  # type: ignore


def get_average_workload(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> float:
    """Calculates the average workload.

    Average workload of a given resource r during a given time slot
    [t1, t2).

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the average
            workload.

    Returns:
        A float indicating the average workload of the resource in the
        given time interval.
    """
    average_workload_query = {
        "Average Workload": f"""
        COUNT(
            CASE WHEN "ACTIVITIES"."org:resource" = '{resource}'
                AND PU_FIRST(DOMAIN_TABLE("ACTIVITIES"."case:concept:name"), "ACTIVITIES"."time:timestamp") < {{d'{end_time}'}}
                AND PU_LAST(DOMAIN_TABLE("ACTIVITIES"."case:concept:name"), "ACTIVITIES"."time:timestamp") >= {{d'{end_time}'}}
            THEN 1
        END
        ) * 1.0
    """
    }

    dataframe = celonis.get_dataframe_from_celonis(average_workload_query)  # type: ignore
    return float(dataframe["Average Workload"].iloc[0])  # type: ignore


def get_average_activity_duration(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
    activity: str,
) -> float:
    """Calculates the average activity duration.

    The average duration of instances of a given activity completed
    during a given time slot by a given resource.

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the average
            activity duration.
        activity (str): The activity for which to calculate the average
            duration.

    Returns:
        A float indicating the average duration of the given activity
        by the resource in the given time interval.
    """
    activity_duration_query = {
        "Resource": 'SOURCE("ACTIVITIES"."org:resource")',
        "Activity": 'SOURCE("ACTIVITIES"."concept:name")',
        "Start Time": 'SOURCE("ACTIVITIES"."time:timestamp")',
        "End Time": 'TARGET("ACTIVITIES"."time:timestamp")',
        "Duration": 'SECONDS_BETWEEN(SOURCE("ACTIVITIES"."time:timestamp"), TARGET("ACTIVITIES"."time:timestamp"))',
    }

    dataframe = celonis.get_dataframe_from_celonis(activity_duration_query)  # type: ignore

    mask = (  # type: ignore
        (dataframe["Resource"] == resource)  # type: ignore
        & (dataframe["Activity"] == activity)  # type: ignore
        & (dataframe["Start Time"] >= start_time)  # type: ignore
        & (dataframe["End Time"] <= end_time)  # type: ignore
    )

    average_case_duration = dataframe.loc[mask, "Duration"].mean()  # type: ignore
    return average_case_duration


def get_average_case_duration(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> float:
    """Calculates the average case duration.

    The average duration of cases completed during a given time slot
    in which a given resource was involved.

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the average
            case duration.

    Returns:
        A float indicating the average duration of cases completed
        by the resource in the given time interval.
    """
    case_duration_query = {
        "Case": '"ACTIVITIES"."case:concept:name"',
        "Case Start": 'MIN("ACTIVITIES"."time:timestamp")',
        "Case End": 'MAX("ACTIVITIES"."time:timestamp")',
    }
    case_df = celonis.get_dataframe_from_celonis(case_duration_query)  # type: ignore

    resource_case_query = {
        "Case": '"ACTIVITIES"."case:concept:name"',
        "Resource": '"ACTIVITIES"."org:resource"',
    }
    resource_df = celonis.get_dataframe_from_celonis(resource_case_query)  # type: ignore

    resource_cases = set(
        resource_df[resource_df["Resource"] == resource]["Case"].unique()  # type: ignore
    )

    case_df["Case Start"] = pd.to_datetime(case_df["Case Start"])  # type: ignore
    case_df["Case End"] = pd.to_datetime(case_df["Case End"])  # type: ignore

    mask = (  # type: ignore
        case_df["Case"].isin(resource_cases)  # type: ignore
        & (case_df["Case End"] >= pd.to_datetime(start_time))  # type: ignore
        & (case_df["Case End"] <= pd.to_datetime(end_time))  # type: ignore
    )

    durations = (
        case_df.loc[mask, "Case End"] - case_df.loc[mask, "Case Start"]  # type: ignore
    ).dt.total_seconds()

    average_case_duration = durations.mean()  # type: ignore
    return average_case_duration


def get_interaction_two_resources(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource1: str,
    resource2: str,
) -> float:
    """Calculates the interaction between two resources.

    The number of cases completed during a given time slot in which
    two given resources were involved.

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource1 (str): The first resource for which to calculate the
            interaction.
        resource2 (str): The second resource for which to calculate the
            interaction.

    Returns:
        A float indicating the interaction between the two resources
        in the given time interval.
    """
    case_query = {
        "Case": '"ACTIVITIES"."case:concept:name"',
        "Case End": 'MAX("ACTIVITIES"."time:timestamp")',
    }
    case_df = celonis.get_dataframe_from_celonis(case_query)  # type: ignore

    resource_query = {
        "Case": '"ACTIVITIES"."case:concept:name"',
        "Resource": '"ACTIVITIES"."org:resource"',
    }
    resource_df = celonis.get_dataframe_from_celonis(resource_query)  # type: ignore

    resource_set = resource_df.groupby("Case")["Resource"].apply(set).reset_index()  # type: ignore

    merged_df = pd.merge(case_df, resource_set, on="Case", how="inner")  # type: ignore

    merged_df["Case End"] = pd.to_datetime(merged_df["Case End"])  # type: ignore
    mask = (
        (merged_df["Case End"] >= pd.to_datetime(start_time))  # type: ignore
        & (merged_df["Case End"] <= pd.to_datetime(end_time))  # type: ignore
        & (merged_df["Resource"].apply(lambda x: resource1 in x and resource2 in x))  # type: ignore
    )

    interaction_count = merged_df.loc[mask, "Case"].nunique()
    return float(interaction_count)


def get_social_position(
    celonis: CelonisConnectionManager,
    start_time: str,
    end_time: str,
    resource: str,
) -> float:
    """Calculates the social position of a resource.

    The social position is the fraction of resources that interacted
    with a given resource during a given time slot with respect to
    the total number of resources that were active during that time
    slot.

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
        start_time (str): The start time of the interval.
        end_time (str): The end time of the interval.
        resource (str): The resource for which to calculate the social
            position.

    Returns:
        A float indicating the social position of the resource in the
        given time interval.
    """
    event_query = {
        "Case": '"ACTIVITIES"."case:concept:name"',
        "Resource": '"ACTIVITIES"."org:resource"',
        "Timestamp": '"ACTIVITIES"."time:timestamp"',
    }
    dataframe = celonis.get_dataframe_from_celonis(event_query)  # type: ignore
    dataframe["Timestamp"] = pd.to_datetime(dataframe["Timestamp"])  # type: ignore

    dataframe = dataframe[  # type: ignore
        (dataframe["Timestamp"] >= pd.to_datetime(start_time))  # type: ignore
        & (dataframe["Timestamp"] <= pd.to_datetime(end_time))  # type: ignore
    ]

    all_active_resources = set(dataframe["Resource"].unique())  # type: ignore

    target_cases = set(dataframe[dataframe["Resource"] == resource]["Case"].unique())  # type: ignore

    resources_in_same_cases = set(  # type: ignore
        dataframe[dataframe["Case"].isin(target_cases)]["Resource"].unique()  # type: ignore
    )
    resources_in_same_cases.discard(resource)  # type: ignore

    if not all_active_resources:
        return 0.0
    social_position = round(len(resources_in_same_cases) / len(all_active_resources))  # type: ignore
    return float(social_position)


# ***************** Organizational Mining ****************


def get_group_relative_focus(
    celonis: CelonisConnectionManager,
) -> DataFrame:
    """Returns the Group Relative Focus.

    The Group Relative Focus metric specifies for a given work how
    much a resource group performed this type of work compared to
    the overall workload of the group. It can be used to measure how
    the workload of a resource group is distributed over different
    types of work, i.e., work diversification of the group.


    Args:
        celonis (CelonisConnectionManager): The Celonis connection

    Returns:
        A DataFrame containing the Group Relative Focus for each group
        and activity.
    """
    activity_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Activity": '"ACTIVITIES"."concept:name"',
        "Activity Count": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    activity_df = celonis.get_dataframe_from_celonis(activity_query)  # type: ignore

    total_per_activity_query = {
        "Activity": '"ACTIVITIES"."concept:name"',
        "Total Activity Count": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    total_per_activity_df = celonis.get_dataframe_from_celonis(total_per_activity_query)  # type: ignore

    merged_df = activity_df.merge(total_per_activity_df, on="Activity")  # type: ignore
    merged_df["Group Relative Focus"] = (
        merged_df["Activity Count"] / merged_df["Total Activity Count"]
    )

    all_groups = merged_df["Group"].unique()  # type: ignore
    all_activities = merged_df["Activity"].unique()  # type: ignore

    all_combinations = pd.DataFrame(
        list(product(all_groups, all_activities)),  # type: ignore
        columns=["Group", "Activity"],  # type: ignore
    )

    result_df = all_combinations.merge(
        merged_df[["Group", "Activity", "Group Relative Focus"]],
        on=["Group", "Activity"],
        how="left",
    )

    result_df["Group Relative Focus"] = result_df["Group Relative Focus"].fillna(0)  # type: ignore

    return result_df.pivot(
        index="Group", columns="Activity", values="Group Relative Focus"
    )


def get_group_relative_stake(
    celonis: CelonisConnectionManager,
) -> DataFrame:
    """Returns" the Group Relative Stake.

    The Group Relative Stake metric specifies for a given work how much
    this type of work was performed by a certain resource group among
    all groups. It can be used to measure how the workload devoted to
    a certain type of work is distributed over resource groups in an
    organizational model, i.e., work participation by different groups.


    Args:
        celonis (CelonisConnectionManager): The Celonis connection

    Returns:
        A DataFrame containing the Group Relative Stake for each group
        and activity.
    """
    activity_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Activity": '"ACTIVITIES"."concept:name"',
        "Activity Count": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    activity_df = celonis.get_dataframe_from_celonis(activity_query)  # type: ignore

    total_per_group_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Total Group Activities": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    total_per_group_df = celonis.get_dataframe_from_celonis(total_per_group_query)  # type: ignore

    merged_df = activity_df.merge(total_per_group_df, on="Group")  # type: ignore
    merged_df["Group Relative Stake"] = (
        merged_df["Activity Count"] / merged_df["Total Group Activities"]
    )

    all_groups = merged_df["Group"].unique()  # type: ignore
    all_activities = merged_df["Activity"].unique()  # type: ignore

    all_combinations = pd.DataFrame(
        list(product(all_groups, all_activities)),  # type: ignore
        columns=["Group", "Activity"],  # type: ignore
    )

    result_df = all_combinations.merge(
        merged_df[["Group", "Activity", "Group Relative Stake"]],
        on=["Group", "Activity"],
        how="left",
    )

    result_df["Group Relative Stake"] = result_df["Group Relative Stake"].fillna(0)  # type: ignore

    return result_df.pivot(
        index="Group", columns="Activity", values="Group Relative Stake"
    )


def get_group_coverage(
    celonis: CelonisConnectionManager,
) -> DataFrame:
    """Returns the Group Coverage metric.

    The Group Coverage metric with respect to a given type of work,
    specifies the proportion of members of a resource group that
    performed this type of work.

    Returns:
        A dictionary where the keys are the names of the resources
        and the values are dictionaries containing resources and the
        Group Coverage metric.
    """
    resource_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Resource": '"ACTIVITIES"."org:resource"',
        "Resource Activity Count": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    resource_df = celonis.get_dataframe_from_celonis(resource_query)  # type: ignore

    total_per_group_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Total Group Activities": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    total_per_group_df = celonis.get_dataframe_from_celonis(total_per_group_query)  # type: ignore

    merged_df = resource_df.merge(total_per_group_df, on="Group")  # type: ignore
    merged_df["Group Coverage"] = (
        merged_df["Resource Activity Count"] / merged_df["Total Group Activities"]
    )

    result_df = merged_df.pivot(
        index="Resource", columns="Group", values="Group Coverage"
    )

    result_df = result_df.fillna(0)  # type: ignore

    return result_df


def get_group_member_interaction(
    celonis: CelonisConnectionManager,
) -> pd.DataFrame:
    """Returns the Group Member Contribution metric.

    The Group Member Contribution metric of a member of a resource group
    with respect to a given type of work specifies how much of this type
    of work by the group was performed by the member. It can be used to
    measure how the workload of the entire group devoted to a certain
    type of work is distributed over the group members.

    Args:
        celonis (CelonisConnectionManager): The Celonis connection
    """
    member_activity_query = {
        "Group": '"ACTIVITIES"."org:group"',
        "Resource": '"ACTIVITIES"."org:resource"',
        "Activity": '"ACTIVITIES"."concept:name"',
        "Activity Count": 'COUNT("ACTIVITIES"."case:concept:name")',
    }
    member_activity_df = celonis.get_dataframe_from_celonis(member_activity_query)  # type: ignore

    all_resources = member_activity_df["Resource"].unique()  # type: ignore
    all_activities = member_activity_df["Activity"].unique()  # type: ignore

    all_combinations = pd.DataFrame(
        list(product(all_resources, all_activities)),  # type: ignore
        columns=["Resource", "Activity"],
    )

    aggregated_df = (
        member_activity_df.groupby(["Resource", "Activity"])["Activity Count"]  # type: ignore
        .sum()
        .reset_index()
    )

    result_df = all_combinations.merge(
        aggregated_df,
        on=["Resource", "Activity"],
        how="left",
    )

    result_df["Activity Count"] = result_df["Activity Count"].fillna(0)  # type: ignore

    final_df = result_df.pivot(
        index="Resource",
        columns="Activity",
        values="Activity Count",
    )

    final_df = final_df.fillna(0)  # type: ignore

    return final_df
