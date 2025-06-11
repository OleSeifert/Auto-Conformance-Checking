"""The file is an example of how to use the CelonisConnection Class.

It contains examples of how to create a Celonis connection, add a
dataframe to the data model, create a table, and get a dataframe from
Celonis.
"""

import time

from pandas import DataFrame as DF
from pm4py.objects.conversion.log.variants import (  # type : ignore
    to_data_frame as log_to_df,  # type: ignore
)
from pm4py.objects.log.importer.xes import importer as xes_importer  # type: ignore
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.pql_queries import resource_based_queries

EVENT_LOG_LOC = "/home/rene/MyProjects/Auto_CC/conformance_checking_spp/tests/input_data/receipt.xes"

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


# Example for a PQL query that counts the number of cases
# my_2_pql_query = {
#    "Case Count": """ COUNT (DISTINCT "ACTIVITIES"."case:concept:name" )"""
# }
# Example for a PQL query for a table representation of the DFG
# my_3_pql_query = {
#    "Source": """ SOURCE("ACTIVITIES"."concept:name")""",
#    "Target": """ TARGET("ACTIVITIES"."concept:name")""",
#    "Path": """ COUNT(SOURCE("ACTIVITIES"."concept:name"))""",
# }


# Example for getting a dataframe from Celonis with a generated PQL query
# dataframe = my_celonis.get_dataframe_from_celonis(my_pql_query)  # type: ignore

# Example for getting a dataframe from Celonis with a default PQL query
# Resulting in a "classic" event log with the columns "Case_ID", "Activity", and "Timestamp"
# dataframe = my_celonis.get_basic_dataframe_from_celonis()

# dataframe = my_celonis.get_basic_dataframe_from_celonis()
# if dataframe is not None:
#    ls = LogSkeleton(
#       dataframe,
#    )
#    ls.compute_skeleton()
#    print(ls.get_activity_frequencies())
print("Start query")
starttime = time.time()
result = resource_based_queries.get_group_member_interaction(my_celonis)
print(f"Execution time: {time.time() - starttime:.2f} seconds")
print(result)
