"""The file is an example of how to use the CelonisConnection Class.

It contains examples of how to create a Celonis connection, add a
dataframe to the data model, create a table, and get a dataframe from
Celonis.
"""

from celonis_connection.celonis_connection_manager import CelonisConnectionManager
from conformance_checking.log_skeleton import LogSkeleton
from pandas import DataFrame as DF
from pm4py.objects.conversion.log.variants import (  # type : ignore
    to_data_frame as log_to_df,  # type: ignore
)
from pm4py.objects.log.importer.xes import importer as xes_importer  # type: ignore
from pycelonis_core.utils.errors import PyCelonisNotFoundError
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

EVENT_LOG_LOC = "tests/input_data/running-example.xes"

# Import the event log as a dataframe
result = xes_importer.apply(EVENT_LOG_LOC)  # type: ignore
result = log_to_df.apply(result)  # type: ignore


class CelonisSettings(BaseSettings):
    """Settings for the Celonis connection.

    This class is used to load the Celonis connection settings from the
    environment variables. The settings are loaded from a .env file
    using the `pydantic_settings` library. The settings include the
    Celonis base URL, data pool name, data model name, and API token.
    """

    CELONIS_BASE_URL: str
    CELONIS_DATA_POOL_NAME: str
    CELONIS_DATA_MODEL_NAME: str
    API_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


# Create a Celonis connection
# and add the event log to the data model
try:
    cfg = CelonisSettings()  # type: ignore
except ValidationError:
    raise ValueError(
        "The .env file is not configured correctly. Please check the "
        "CELONIS_BASE_URL, CELONIS_DATA_POOL_NAME, CELONIS_DATA_MODEL_NAME, and API_TOKEN."
    )
my_celonis = CelonisConnectionManager(
    base_url=cfg.CELONIS_BASE_URL,
    data_pool_name=cfg.CELONIS_DATA_POOL_NAME,
    data_model_name=cfg.CELONIS_DATA_MODEL_NAME,
    api_token=cfg.API_TOKEN,
)
if isinstance(result, DF):
    my_celonis.add_dataframe(result)
    my_celonis.create_table()


# Example for a PQL query that maps Patients to their Blood Groups
table_columns = my_celonis.get_table_columns()
if table_columns is not None:
    try:
        my_pql_query = {
            "Patient": table_columns.find("case:concept:name"),
            "Blood Group": table_columns.find("org:resource"),
        }
    except PyCelonisNotFoundError:
        print("Table columns not found in data model.")

# Example for a PQL query that counts the number of cases
my_2_pql_query = {
    "Case Count": """ COUNT (DISTINCT "ACTIVITIES"."case:concept:name" )"""
}
# Example for a PQL query for a table representation of the DFG
my_3_pql_query = {
    "Source": """ SOURCE("ACTIVITIES"."concept:name")""",
    "Target": """ TARGET("ACTIVITIES"."concept:name")""",
    "Path": """ COUNT(SOURCE("ACTIVITIES"."concept:name"))""",
}


# Example for getting a dataframe from Celonis with a generated PQL query
dataframe = my_celonis.get_dataframe_from_celonis(my_pql_query)  # type: ignore

# Example for getting a dataframe from Celonis with a default PQL query
# Resulting in a "classic" event log with the columns "Case_ID", "Activity", and "Timestamp"
# dataframe = my_celonis.get_basic_dataframe_from_celonis()

dataframe = my_celonis.get_basic_dataframe_from_celonis()
if dataframe is not None:
    ls = LogSkeleton(
        dataframe,
    )
    ls.compute_skeleton()
    print(ls.get_activity_frequencies())
