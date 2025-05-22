"""The module provides a class to manage the connection to Celonis.

It includes methods to create tables, add data frames, and retrieve data
from Celonis via the help of PQL queries. It relies on the  PyCelonis
library.
"""

from collections.abc import MutableMapping
from os import curdir, environ, path
from typing import Union

import pandas as pd
from dotenv import load_dotenv, set_key
from pycelonis import get_celonis
from pycelonis.ems.data_integration.data_model import DataModel
from pycelonis.ems.data_integration.data_model_table import DataModelTable
from pycelonis.ems.data_integration.data_model_table_column import DataModelTableColumn
from pycelonis.ems.data_integration.data_pool import DataPool
from pycelonis.pql.data_frame import DataFrame as pqlDataFrame
from pycelonis_core.base.collection import CelonisCollection
from pycelonis_core.utils.errors import PyCelonisNotFoundError
from saolapy.types import SeriesLike


class CelonisConnectionManager:
    """Class to manage the connection to Celonis."""

    base_url: str
    api_token: str
    data_pool_name: str
    data_model_name: str
    data_frame: pd.DataFrame

    def __init__(
        self,
        base_url: str,
        data_pool_name: str,
        data_model_name: str,
        api_token: str = "",
    ) -> None:
        """Initialize the CelonisConnection object.

        Args:
            base_url: Base URL of the Celonis instance.
            api_token: API token for the Celonis instance.
            data_pool_name: Name of the data pool to use.
            data_model_name: Name of the data model to use.
        """
        self.base_url = base_url
        self.data_pool_name = data_pool_name
        self.data_model_name = data_model_name
        self.data_frame = pd.DataFrame()
        if api_token == "":
            self.api_token = self.acquire_api_token()
        else:
            self.api_token = self.acquire_api_token(api_token)
        self.celonis = get_celonis(base_url=base_url, api_token=self.api_token)
        self.data_pool = self.find_data_pool(data_pool_name)
        self.data_model = self.find_data_model(data_model_name)

    def find_data_pool(self, data_pool_name: str) -> DataPool:
        """Find a data pool by name.

        It will return the datapool if it is found or create a new one if it does not exist.

        Args:
            data_pool_name: Name of the data pool to find.

        Returns:
            Data pool object.
        """
        try:
            return self.celonis.data_integration.get_data_pools().find(data_pool_name)
        except PyCelonisNotFoundError:
            print(f"Data pool '{data_pool_name}' not found. Creating a new one.")
            return self.celonis.data_integration.create_data_pool(self.data_pool_name)

    def find_data_model(self, data_model_name: str) -> Union[DataModel, None]:
        """Find a data model by name.

        It will return the data model if it is found or create a new one if it does not exist.
        If the data pool does not exist, it will return None.

        Args:
            data_model_name: Name of the data model to find.

        Returns:
            Data model object or None.
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
    ) -> None:
        """Add a table to the data pool.

        It will create a new table in the data pool and add it to the
        data model. If the table already exists, it will delete it and
        create a new one. The function then uses the specified columns
        to create a process configuration in the data model and reload it.

        Args:
            table_name: Name of the table to create.
            case_id_column: Name of the case ID column.
            activity_column: Name of the activity column.
            timestamp_column: Name of the timestamp column.
            drop_if_exists: If True, drop the table if it already exists.
            force: If True, force the creation of the table.

        Returns:
            None
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

    def add_dataframe(self, df: pd.DataFrame) -> None:
        """Add a DataFrame to the CelonisConnection object.

        Allows the data frame to be created outside of the class and
        then passed in. This is allows for more flexibility in how and
        when the data frame is created and used.

        Args:
            df: DataFrame to add to the CelonisConnection object.

        Returns:
            None
        """
        self.data_frame = df

    def get_basic_dataframe_from_celonis(
        self, table_name: str = "ACTIVITIES"
    ) -> Union[pd.DataFrame, None]:
        """Get the dataframe from the data model in Celonis.

        It will create a new dataframe with the columns "case:concept:name",
        "concept:name" and "time:timestamp" from the table in the data model.
        Returns None if the data model does not exist or the table is not
        found.

        Args:
            table_name: Name of the table to get. Default is "ACTIVITIES".

        Returns:
            DataFrame object or None.
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
                "case:concept:name": activities_columns.find("case:concept:name"),
                "concept:name": activities_columns.find("concept:name"),
                "time:timestamp": activities_columns.find("time:timestamp"),
            },
            data_model=self.data_model,
        )

        return df.to_pandas()

    def get_dataframe_from_celonis(
        self,
        pql_query: MutableMapping[str, SeriesLike | DataModelTableColumn],
    ) -> Union[pd.DataFrame, None]:
        """Get the dataframe from the data model in Celonis.

        It will create a new dataframe with the columns from the PQL
        query. The PQL query must be a dictionary with the column names
        as keys and the column values as values. The column values can
        be either a string or a DataModelTableColumn object. The
        function will return None if the data model does not exist or
        the PQL query is empty.

        Args:
            pql_query: PQL query used to define the dataframe.

        Returns:
            DataFrame object or None.
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
        return df.to_pandas()

    def get_table(self, table_name: str = "ACTIVITIES") -> Union[DataModelTable, None]:
        """Get the table from the data model in Celonis.

        It will return the table object if it is found or None if it
        does not exist. The table name must be the same as the one used
        in the data model.

        Args:
            table_name: Name of the table to get. Default is "ACTIVITIES".

        Returns:
            DataModelTable object or None.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get table.")
            return None
        try:
            return self.data_model.get_tables().find(table_name)
        except PyCelonisNotFoundError:
            print(f"Table {table_name} not found in data model.")
            return None

    def get_table_columns(
        self, table_name: str = "ACTIVITIES"
    ) -> Union[CelonisCollection[DataModelTableColumn], None]:
        """Get the columns of the table from the data model in Celonis.

        It will return the columns of the table object if it is found or
        None if it does not exist. The table name must be the same as the
        one used in the data model.

        Args:
            table_name: Name of the table to get. Default is "ACTIVITIES".

        Returns:
            List of DataModelTableColumn objects or None.
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

    def get_data_pool(self) -> Union[DataPool, None]:
        """Get the data pool object.

        Returns:
             Data pool object or None.
        """
        if not self.data_pool:
            print("Data pool does not exist. Cannot get data pool.")
            return None
        return self.data_pool

    def get_data_model(self) -> Union[DataModel, None]:
        """Get the data model object.

        Returns:
             Data model object or None.
        """
        if not self.data_model:
            print("Data model does not exist. Cannot get data model.")
            return None
        return self.data_model

    def acquire_api_token(self, api_token: str = "") -> str:
        """Get the API token.

        At first, it will check if the .env file exists and create it
        if it does not. Then, it will load the environment variables
        from the .env file. If the API token is provided, it will set
        it in the environment variables. If the API token is not
        provided, it will get it from the environment variables. If the
        API token is not found in the environment variables, it will
        raise a ValueError.

        Args:
            api_token: API token to set in the environment variables.

        Returns:
            API token as str.

        Raises:
            ValueError: If the API token is not found in the environment
            variables.
        """
        # Check if the .env file exists and create it if it does not
        root_path = path.abspath(curdir)
        if not path.isfile(path.join(root_path, ".env")):
            open(path.join(root_path, ".env"), "w").close()

        # Load the environment variables from the .env file
        load_dotenv()

        # Check if the API token is provided
        # If it is, set it in the environment variables
        # If it is not, get it from the environment variables

        if api_token == "":
            token = environ.get("API_TOKEN")
            if not token:
                raise ValueError(
                    "API token not found. Please provide the API Token when creating a Celonis connection for the first time."
                )
            return token
        else:
            set_key(
                dotenv_path=path.join(root_path, ".env"),
                key_to_set="API_TOKEN",
                value_to_set=api_token,
            )
            return api_token
