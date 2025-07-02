backend.api.modules.general_router
==================================

.. py:module:: backend.api.modules.general_router

.. autoapi-nested-parse::

   Contains the router for general informtion API endpoints.



Attributes
----------

.. autoapisummary::

   backend.api.modules.general_router.router
   backend.api.modules.general_router.TableType
   backend.api.modules.general_router.GraphType
   backend.api.modules.general_router.EndpointReturnType


Functions
---------

.. autoapisummary::

   backend.api.modules.general_router.get_general_information
   backend.api.modules.general_router.transform_counts_df_to_endpoint_format
   backend.api.modules.general_router.transform_traces_df_to_endpoint_format
   backend.api.modules.general_router.transform_dfg_df_to_endpoint_format
   backend.api.modules.general_router.get_unique_activities


Module Contents
---------------

.. py:data:: router

.. py:type:: TableType
   :canonical: Dict[str, Union[List[str], List[List[str]]]]


.. py:type:: GraphType
   :canonical: Dict[str, List[Dict[str, str]]]


.. py:type:: EndpointReturnType
   :canonical: Dict[str, Union[List[TableType], List[GraphType]]]


.. py:function:: get_general_information(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> EndpointReturnType
   :async:


   Fetches general information about the process from Celonis.

   This endpoint retrieves the number of cases, activities, trace variants,
   and the Directly-Follows Graph (DFG) representation of the process.

   :param celonis: The CelonisConnectionManager. Defaults to
                   Depends(get_celonis_connection).
   :type celonis: optional

   :returns: A dictionary containing tables with general information and a graph
             representing the Directly-Follows Graph (DFG).


.. py:function:: transform_counts_df_to_endpoint_format(counts_df: pandas.DataFrame) -> TableType

   Transforms the counts DataFrame into a format suitable for the endpoint.

   :param counts_df: The DataFrame containing counts of cases, activities, and
                     trace variants.

   :returns: A dictionary encoding a table with general information.


.. py:function:: transform_traces_df_to_endpoint_format(traces_df: pandas.DataFrame) -> TableType

   Transforms the traces DataFrame into a format suitable for the endpoint.

   :param traces_df: The DataFrame containing traces and their counts.

   :returns: A dictionary encoding a table with trace variants and their counts.


.. py:function:: transform_dfg_df_to_endpoint_format(dfg_df: pandas.DataFrame, activities_df: pandas.DataFrame) -> GraphType

   Transforms the DFG DataFrame into a format suitable for the endpoint.

   This function encodes the DFG as a dictionary with nodes and edges,
   where nodes represent unique activities and edges represent the
   relationships between them with their respective counts.

   :param dfg_df: The DataFrame containing the DFG representation.
   :param activities_df: The DataFrame containing the activities.

   :returns: A dictionary containing the encoded DFG.


.. py:function:: get_unique_activities(activities_df: pandas.DataFrame) -> List[str]

   Extracts unique activities from the activities DataFrame.

   :param activities_df: The DataFrame containing activities.

   :returns: A list of the unique activities.


