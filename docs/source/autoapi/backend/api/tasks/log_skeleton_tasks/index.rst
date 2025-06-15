backend.api.tasks.log_skeleton_tasks
====================================

.. py:module:: backend.api.tasks.log_skeleton_tasks

.. autoapi-nested-parse::

   Contains the tasks for handling log skeletons and related operations.



Functions
---------

.. autoapisummary::

   backend.api.tasks.log_skeleton_tasks.compute_and_store_log_skeleton


Module Contents
---------------

.. py:function:: compute_and_store_log_skeleton(app: fastapi.FastAPI, job_id: str, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> None

   Computes the log skeleton and stores it in the app state.

   :param app: The FastAPI app instance.
   :param job_id: The ID of the job to be computed.
   :param celonis: The CelonisConnectionManager instance.


