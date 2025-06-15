backend.api.tasks.resource_based_tasks
======================================

.. py:module:: backend.api.tasks.resource_based_tasks

.. autoapi-nested-parse::

   Contains the tasks for handling resource-based conformance checking.



Functions
---------

.. autoapisummary::

   backend.api.tasks.resource_based_tasks.compute_and_store_resource_based_metrics


Module Contents
---------------

.. py:function:: compute_and_store_resource_based_metrics(app: fastapi.FastAPI, job_id: str, celonis_connection: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> None

   Computes the resource-based metrics and stores it in the app state.

   :param app: The FastAPI application instance.
   :param job_id: The job ID for tracking the task.
   :param celonis_connection: The CelonisConnectionManager instance.
   :param resource_column_name: The name of the resource column in the DataFrame.

   :raises RuntimeError: If the DataFrame is empty.


