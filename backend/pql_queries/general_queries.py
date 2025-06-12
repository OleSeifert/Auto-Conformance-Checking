"""Queries that can be used to get general data from celonis."""

from pandas import DataFrame

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)


def get_dfg_representation(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the DFG representation of a process.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that represents a graph
    """
    dfg_query = {
        "Source": """ SOURCE("ACTIVITIES"."concept:name")""",
        "Target": """ TARGET("ACTIVITIES"."concept:name")""",
        "Path": """ COUNT(SOURCE("ACTIVITIES"."concept:name"))""",
    }
    return celonis.get_dataframe_from_celonis(dfg_query)  # type: ignore


def get_cases(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the cases from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the cases
    """
    case_query = {
        "Cases": """ "ACTIVITIES"."case:concept:name" """,
        "Case Count": """ COUNT (DISTINCT "ACTIVITIES"."case:concept:name" )""",
    }
    return celonis.get_dataframe_from_celonis(case_query)  # type: ignore


def get_number_of_cases(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the count of cases from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of cases
    """
    case_query = {
        "Case Count": """ COUNT (DISTINCT "ACTIVITIES"."case:concept:name" )"""
    }
    return celonis.get_dataframe_from_celonis(case_query)  # type: ignore


def get_activities(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the activities from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of cases
    """
    activity_query = {
        "Activity": """ "ACTIVITIES"."concept:name" """,
        "Activity Count": """ COUNT (DISTINCT "ACTIVITIES"."concept:name" )""",
    }
    return celonis.get_dataframe_from_celonis(activity_query)  # type: ignore


def get_number_of_activities(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the count of activities from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of activites
    """
    activity_query = {
        "Activity Count": """ COUNT (DISTINCT "ACTIVITIES"."concept:name" )"""
    }
    return celonis.get_dataframe_from_celonis(activity_query)  # type: ignore


def get_traces_with_count(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the traces and their count.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the traces and their count
    """
    trace_query = {
        "Trace": """ VARIANT ("ACTIVITIES"."concept:name")""",
        "Count": """COUNT (VARIANT ("ACTIVITIES"."concept:name"))""",
    }
    return celonis.get_dataframe_from_celonis(trace_query)  # type: ignore


def get_general_information(celonis: CelonisConnectionManager) -> DataFrame:
    """Fetches number of cases, activities, and trace variants from Celonis.

    Args:
        celonis: The CelonisConnectionManager instance to interact with Celonis.

    Returns:
        A pandas DataFrame containing the counts of cases, activities, and trace
        variants.
    """
    query = {
        "CaseCount": """COUNT(DISTINCT "ACTIVITIES"."case:concept:name")""",
        "ActivityCount": """COUNT(DISTINCT "ACTIVITIES"."concept:name")""",
        "TraceVariants": """COUNT(DISTINCT VARIANT("ACTIVITIES"."concept:name"))""",
    }
    return celonis.get_dataframe_from_celonis(query)  # type: ignore
