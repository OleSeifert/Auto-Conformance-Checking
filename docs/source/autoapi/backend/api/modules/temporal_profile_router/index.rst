backend.api.modules.temporal_profile_router
===========================================

.. py:module:: backend.api.modules.temporal_profile_router

.. autoapi-nested-parse::

   Contains the routes for temporal conformance checking.



Attributes
----------

.. autoapisummary::

   backend.api.modules.temporal_profile_router.router
   backend.api.modules.temporal_profile_router.MODULE_NAME


Functions
---------

.. autoapisummary::

   backend.api.modules.temporal_profile_router.compute_temporal_conformance_result
   backend.api.modules.temporal_profile_router.get_temporal_conformance_result


Module Contents
---------------

.. py:data:: router

.. py:data:: MODULE_NAME
   :value: 'temporal'


.. py:function:: compute_temporal_conformance_result(background_tasks: fastapi.BackgroundTasks, request: fastapi.Request, zeta: float = Query(0.5, description='Zeta value for temporal profile conformance checking', gt=0.0), celonis_connection: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> Dict[str, str]
   :async:


   Computes the temporal conformance result and stores it.

   :param background_tasks: The background tasks manager.
   :param request: The FastAPI request object.
   :param zeta: The zeta value used for temporal profile conformance checking.
   :param celonis_connection: The Celonis connection manager instance.

   :returns: A dictionary containing the job ID of the scheduled task.


.. py:function:: get_temporal_conformance_result(job_id: str, request: fastapi.Request) -> dict
   :async:


   Retrieves the temporal conformance result for a given job ID.

   This result is expected to be a list of lists of tuples, representing
   the raw output from TemporalProfile.get_temporal_conformance_result().

   :param job_id: The ID of the job for which to retrieve the result.
   :param request: The FastAPI request object.

   :returns: The temporal conformance result as a list of lists of tuples.

   :raises HTTPException: If the job is not found or if the result is not available.


