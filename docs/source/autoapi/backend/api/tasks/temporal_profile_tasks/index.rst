backend.api.tasks.temporal_profile_tasks
========================================

.. py:module:: backend.api.tasks.temporal_profile_tasks

.. autoapi-nested-parse::

   Contains the tasks for temporal profile based conformance checking.



Functions
---------

.. autoapisummary::

   backend.api.tasks.temporal_profile_tasks.compute_and_store_temporal_conformance_result


Module Contents
---------------

.. py:function:: compute_and_store_temporal_conformance_result(app: fastapi.FastAPI, job_id: str, celonis_connection: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, zeta: float) -> None

   Computes the temporal conformance result and stores it in the app state.

   :param app: The FastAPI application instance.
   :type app: FastAPI
   :param job_id: The ID of the job.
   :param celonis_connection: The Celonis connection manager instance.
   :param zeta: The zeta value used for temporal profile conformance checking.

   :raises RuntimeError: If the DataFrame is empty.


