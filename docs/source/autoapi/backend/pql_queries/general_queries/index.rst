backend.pql_queries.general_queries
===================================

.. py:module:: backend.pql_queries.general_queries

.. autoapi-nested-parse::

   Queries that can be used to get general data from celonis.



Functions
---------

.. autoapisummary::

   backend.pql_queries.general_queries.get_dfg_representation
   backend.pql_queries.general_queries.get_cases
   backend.pql_queries.general_queries.get_number_of_cases
   backend.pql_queries.general_queries.get_activities
   backend.pql_queries.general_queries.get_number_of_activities
   backend.pql_queries.general_queries.get_traces_with_count
   backend.pql_queries.general_queries.get_general_information


Module Contents
---------------

.. py:function:: get_dfg_representation(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the DFG representation of a process.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that represents a graph


.. py:function:: get_cases(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the cases from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the cases


.. py:function:: get_number_of_cases(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the count of cases from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the count of cases


.. py:function:: get_activities(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the activities from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the count of cases


.. py:function:: get_number_of_activities(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the count of activities from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the count of activites


.. py:function:: get_traces_with_count(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the traces and their count.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the traces and their count


.. py:function:: get_general_information(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Fetches number of cases, activities, and trace variants from Celonis.

   :param celonis: The CelonisConnectionManager instance to interact with Celonis.

   :returns: A pandas DataFrame containing the counts of cases, activities, and trace
             variants.


