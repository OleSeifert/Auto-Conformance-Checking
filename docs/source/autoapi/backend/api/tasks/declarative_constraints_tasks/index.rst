backend.api.tasks.declarative_constraints_tasks
===============================================

.. py:module:: backend.api.tasks.declarative_constraints_tasks

.. autoapi-nested-parse::

   Contains the tasks for handling log skeletons and related operations.



Functions
---------

.. autoapisummary::

   backend.api.tasks.declarative_constraints_tasks.compute_and_store_declarative_constraints


Module Contents
---------------

.. py:function:: compute_and_store_declarative_constraints(app: fastapi.FastAPI, job_id: str, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, min_support_ratio: float = 0.3, min_confidence_ratio: float = 0.75) -> None

   Computes the declarative constraints and stores it in the app state.

   :param app: The FastAPI app instance.
   :param job_id: The ID of the job to be computed.
   :param celonis: The CelonisConnectionManager instance.
   :param min_support_ratio: The minimum support ratio for the constraints.
   :param min_confidence_ratio: The minimum confidence ratio for the constraints.


