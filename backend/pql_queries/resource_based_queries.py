"""Queries that can be used to get resoruce related data from celonis."""

from pandas import DataFrame
from pycelonis_core.utils.errors import PyCelonisNotFoundError

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
        "Resource Count": """ COUNT (DISTINCT "ACTIVITIES"."org:resources" )"""
    }
    return celonis.get_dataframe_from_celonis(resource_query)  # type: ignore


def get_number_of_groups(celonis: CelonisConnectionManager) -> DataFrame:
    """A query that gets the count of groups from an event log.

    Args:
        celonis (CelonisConnectionManager): the celonis connection

    Returns:
        a pandas Dataframe that contains the count of groups
    """
    activity_query = {
        "Groups Count": """ COUNT (DISTINCT "ACTIVITIES"."org:groups" )"""
    }
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
