"""The module provides a class to manage the connection to Celonis and perform
operations on data models.

It includes methods to create tables, add data frames, and retrieve data
from Celonis via the help of PQL queries. It relies on the  PyCelonis
library.
"""

from collections.abc import MutableMapping

from pandas import DataFrame as DF
from pycelonis import get_celonis
from pycelonis.ems.data_integration.data_model_table_column import DataModelTableColumn
from pycelonis.pql.data_frame import DataFrame as pqlDataFrame
from pycelonis_core.utils.errors import PyCelonisNotFoundError
from saolapy.types import SeriesLike


class CelonisConnection:
    """Class to manage the connection to Celonis."""

    base_url: str
    api_token: str
    data_pool_name: str
    data_model_name: str
    data_frame: DF

    def __init__(
        self, base_url: str, api_token: str, data_pool_name: str, data_model_name: str
    ):
        """Initialize the CelonisConnection object.

        :param base_url: Base URL of the Celonis instance.
        :param api_token: API token for the Celonis instance.
        :param data_pool_name: Name of the data pool to use.
        :param data_model_name: Name of the data model to use.
        """
        self.base_url = base_url
        self.api_token = api_token
        self.data_pool_name = data_pool_name
        self.data_model_name = data_model_name
        self.celonis = get_celonis(base_url=base_url, api_token=api_token)
        self.data_pool = self._find_data_pool(data_pool_name)
        self.data_model = self._find_data_model(data_model_name)

    def _find_data_pool(self, data_pool_name: str):
        """Find a data pool by name.

        It will create a new one if it does not exist.
        :param data_pool_name: Name of the data pool to find.
        :return: Data pool object.
        """
        try:
            return self.celonis.data_integration.get_data_pools().find(data_pool_name)
        except PyCelonisNotFoundError:
            print(f"Data pool '{data_pool_name}' not found. Creating a new one.")
            return self.celonis.data_integration.create_data_pool(self.data_pool_name)

    def _find_data_model(self, data_model_name: str):
        """Find a data model by name.

        It will create a new one if it does not exist.
        :param data_model_name: Name of the data model to find.
        :return: Data model object.
        """
        if not self.data_pool:
            print("Data pool does not exist. Cannot find data model.")
            return None
        try:
            return self.data_pool.get_data_models().find(self.data_model_name)
        except PyCelonisNotFoundError:
            print(f"Data model '{data_model_name}' not found. Creating a new one.")
            return self.data_pool.create_data_model(self.data_model_name)

    def create_table(
        self,
        table_name: str = "ACTIVITIES",
        case_id_column: str = "case:concept:name",
        activity_column: str = "concept:name",
        timestamp_column: str = "time:timestamp",
        drop_if_exists: bool = True,
        force: bool = True,
    ):
        """Add a table to the data pool.

        :param table_name: Name of the table to add. Default is
            "ACTIVITIES".
        :param case_id_column: Name of the case ID column. Default is
            "case:concept:name".
        :param activity_column: Name of the activity column. Default is
            "concept:name".
        :param timestamp_column: Name of the timestamp column. Default
            is "time:timestamp".
        :param drop_if_exists: Whether to drop the table if it already
            exists.
        :param force: Whether to force the creation of the table.
        :return: Table object if creation was successfull.
        """
        if not self.data_pool or not self.data_model:
            print("Data pool or data model does not exist. Cannot create table.")
            return None

        if self.data_frame.empty:
            print("Data frame is empty. No reason to create a table.")
            return None

        # Create the table in the data pool
        table = self.data_pool.create_table(
            df=self.data_frame,
            table_name=table_name,
            drop_if_exists=drop_if_exists,
            force=force,
        )
        # Check if the table already exists in the data model
        # If it exists, delete it from the data model then add the new one
        # If it does not exist, add it to the data model
        try:
            table_in_celonis = self.data_model.get_tables().find(table.name)
            table_in_celonis.delete()
            print(f"Table '{table.name}' already exists in data model. Deleting it.")
            act_table = self.data_model.add_table(name=table.name, alias=table_name)
        except PyCelonisNotFoundError:
            print(f"Table '{table.name}' not found in data model. Adding it.")
            act_table = self.data_model.add_table(name=table.name, alias=table_name)

        self.data_model.create_process_configuration(
            activity_table_id=act_table.id,
            case_id_column=case_id_column,
            activity_column=activity_column,
            timestamp_column=timestamp_column,
        )

        # Reload the data model to reflect the changes
        self.data_model.reload()

    def add_dataframe(self, df: DF):
        """Add a DataFrame to the CelonisConnection object.

        Allows the data frame to be created outside of the class and
        then passed in. This is allows for more flexibility in how and
        when the data frame is created and used.
        :param df: DataFrame to add.
        """
        self.data_frame = df

    def get_basic_dataframe_from_celonis(self, table_name: str = "ACTIVITIES"):
        """Get the dataframe from the data model in Celonis.

        :param table_name: Name of the table to get. Default is
            "ACTIVITIES".
        :return: Table object.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get table.")
            return None
        try:
            table = self.data_model.get_tables().find(table_name)
        except PyCelonisNotFoundError:
            print(f"Table {table_name} not found in data model.")
            return None

        activities_columns = table.get_columns()

        df = pqlDataFrame(
            {
                "Case_ID": activities_columns.find("case:concept:name"),
                "Activity": activities_columns.find("concept:name"),
                "Timestamp": activities_columns.find("time:timestamp"),
            },
            data_model=self.data_model,
        )

        return df

    def get_dataframe_from_celonis(
        self,
        pql_query: MutableMapping[str, SeriesLike | DataModelTableColumn],
    ):
        """Get the dataframe from the data model in Celonis.

        :param pql_query: PQL query used to filter the results.
        :return: DataFrame object.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get table.")
            return None
        if not pql_query:
            print("PQL query is empty. Cannot get dataframe.")
            return None
        df = pqlDataFrame(
            pql_query,
            data_model=self.data_model,
        )
        return df

    def get_table(self, table_name: str = "ACTIVITIES"):
        """Get the table from the data model in Celonis.

        :param table_name: Name of the table to get. Default is
            "ACTIVITIES".
        :return: Table object.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get table.")
            return None
        try:
            return self.data_model.get_tables().find(table_name)
        except PyCelonisNotFoundError:
            print(f"Table {table_name} not found in data model.")
            return None

    def get_table_columns(self, table_name: str = "ACTIVITIES"):
        """Get the columns of the table from the data model in Celonis.

        :param table_name: Name of the table to get. Default is
            "ACTIVITIES".
        :return: Table object.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get table.")
            return None
        try:
            table = self.data_model.get_tables().find(table_name)
            return table.get_columns()
        except PyCelonisNotFoundError:
            print(f"Table {table_name} not found in data model.")
            return None

    def get_data_pool(self):
        """Get the data pool object.

        :return: Data pool object.
        """
        if not self.data_pool:
            print("Data pool does not exist. Cannot get data pool.")
            return None
        return self.data_pool

    def get_data_model(self):
        """Get the data model object.

        :return: Data model object.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get data model.")
            return None
        return self.data_model
