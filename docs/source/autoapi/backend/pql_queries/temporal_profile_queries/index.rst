backend.pql_queries.temporal_profile_queries
============================================

.. py:module:: backend.pql_queries.temporal_profile_queries

.. autoapi-nested-parse::

   Queries tused to get temporal profile related data from Celonis.



Functions
---------

.. autoapisummary::

   backend.pql_queries.temporal_profile_queries.get_temporal_conformance_result


Module Contents
---------------

.. py:function:: get_temporal_conformance_result(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, zeta: float) -> pandas.DataFrame

   Returns the temporal conformance result from Celonis.

   Parameters:
   celonis: CelonisConnectionManager
       The Celonis connection manager instance.
   zeta: float
       The zeta value used for temporal conformance checking.

   Returns:
   DataFrame
       A DataFrame containing the deviations for each trace. Each row contains:
       - Case ID of the recorded deviation.
       - Source activity of the recorded deviation.
       - Target activity of the recorded deviation.
       - Time passed between the occurrence of the source activity and the target activity.
       - Value of (time passed - mean)/std for this occurrence (zeta).


