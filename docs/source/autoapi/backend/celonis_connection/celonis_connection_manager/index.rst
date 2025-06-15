backend.celonis_connection.celonis_connection_manager
=====================================================

.. py:module:: backend.celonis_connection.celonis_connection_manager

.. autoapi-nested-parse::

   The module provides a class to manage the connection to Celonis.

   It includes methods to create tables, add data frames, and retrieve data
   from Celonis via the help of PQL queries. It relies on the  PyCelonis
   library.



Classes
-------

.. autoapisummary::

   backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager


Module Contents
---------------

.. py:class:: CelonisConnectionManager(base_url: str, data_pool_name: str, data_model_name: str, api_token: str)

   Class to manage the connection to Celonis.


   .. py:attribute:: base_url
      :type:  str


   .. py:attribute:: api_token
      :type:  str


   .. py:attribute:: data_pool_name
      :type:  str


   .. py:attribute:: data_model_name
      :type:  str


   .. py:attribute:: data_frame
      :type:  pandas.DataFrame


   .. py:attribute:: celonis


   .. py:attribute:: data_pool
      :value: None



   .. py:attribute:: data_model
      :value: None



   .. py:method:: find_data_pool(data_pool_name: str) -> pycelonis.ems.data_integration.data_pool.DataPool

      Find a data pool by name.

      It will return the datapool if it is found or create a new one if it does not exist.

      :param data_pool_name: Name of the data pool to find.

      :returns: Data pool object.



   .. py:method:: find_data_model(data_model_name: str) -> Union[pycelonis.ems.data_integration.data_model.DataModel, None]

      Find a data model by name.

      It will return the data model if it is found or create a new one if it does not exist.
      If the data pool does not exist, it will return None.

      :param data_model_name: Name of the data model to find.

      :returns: Data model object or None.



   .. py:method:: create_table(table_name: str = 'ACTIVITIES', case_id_column: str = 'case:concept:name', activity_column: str = 'concept:name', timestamp_column: str = 'time:timestamp', drop_if_exists: bool = True, force: bool = True) -> None

      Add a table to the data pool.

      It will create a new table in the data pool and add it to the
      data model. If the table already exists, it will delete it and
      create a new one. The function then uses the specified columns
      to create a process configuration in the data model and reload it.

      :param table_name: Name of the table to create.
      :param case_id_column: Name of the case ID column.
      :param activity_column: Name of the activity column.
      :param timestamp_column: Name of the timestamp column.
      :param drop_if_exists: If True, drop the table if it already exists.
      :param force: If True, force the creation of the table.

      :returns: None



   .. py:method:: add_dataframe(df: pandas.DataFrame) -> None

      Add a DataFrame to the CelonisConnection object.

      Allows the data frame to be created outside of the class and
      then passed in. This is allows for more flexibility in how and
      when the data frame is created and used.

      :param df: DataFrame to add to the CelonisConnection object.

      :returns: None



   .. py:method:: get_basic_dataframe_from_celonis(table_name: str = 'ACTIVITIES') -> Union[pandas.DataFrame, None]

      Get the dataframe from the data model in Celonis.

      It will create a new dataframe with the columns "case:concept:name",
      "concept:name" and "time:timestamp" from the table in the data model.
      Returns None if the data model does not exist or the table is not
      found.

      :param table_name: Name of the table to get. Default is "ACTIVITIES".

      :returns: DataFrame object or None.



   .. py:method:: get_dataframe_with_resource_group_from_celonis(table_name: str = 'ACTIVITIES') -> Union[pandas.DataFrame, None]

      Get the dataframe from the data model in Celonis.

      It will create a new dataframe with the columns "case:concept:name",
      "concept:name", "time:timestamp", "org:resource", and "org:group"
      from the table in the data model. Returns None if the data model
      does not exist or the table is not found.

      :param table_name: Name of the table to get. Default is "ACTIVITIES".

      :returns: DataFrame object or None.



   .. py:method:: get_dataframe_from_celonis(pql_query: collections.abc.MutableMapping[str, saolapy.types.SeriesLike | pycelonis.ems.data_integration.data_model_table_column.DataModelTableColumn]) -> Union[pandas.DataFrame, None]

      Get the dataframe from the data model in Celonis.

      It will create a new dataframe with the columns from the PQL
      query. The PQL query must be a dictionary with the column names
      as keys and the column values as values. The column values can
      be either a string or a DataModelTableColumn object. The
      function will return None if the data model does not exist or
      the PQL query is empty.

      :param pql_query: PQL query used to define the dataframe.

      :returns: DataFrame object or None.



   .. py:method:: get_table(table_name: str = 'ACTIVITIES') -> Union[pycelonis.ems.data_integration.data_model_table.DataModelTable, None]

      Get the table from the data model in Celonis.

      It will return the table object if it is found or None if it
      does not exist. The table name must be the same as the one used
      in the data model.

      :param table_name: Name of the table to get. Default is "ACTIVITIES".

      :returns: DataModelTable object or None.



   .. py:method:: get_table_columns(table_name: str = 'ACTIVITIES') -> Union[pycelonis_core.base.collection.CelonisCollection[pycelonis.ems.data_integration.data_model_table_column.DataModelTableColumn], None]

      Get the columns of the table from the data model in Celonis.

      It will return the columns of the table object if it is found or
      None if it does not exist. The table name must be the same as the
      one used in the data model.

      :param table_name: Name of the table to get. Default is "ACTIVITIES".

      :returns: List of DataModelTableColumn objects or None.



   .. py:method:: get_data_pool() -> Union[pycelonis.ems.data_integration.data_pool.DataPool, None]

      Get the data pool object.

      :returns: Data pool object or None.



   .. py:method:: get_data_model() -> Union[pycelonis.ems.data_integration.data_model.DataModel, None]

      Get the data model object.

      :returns: Data model object or None.



