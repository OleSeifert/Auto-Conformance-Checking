backend.api.modules.log_skeleton_router
=======================================

.. py:module:: backend.api.modules.log_skeleton_router

.. autoapi-nested-parse::

   Contains the routes for handling log skeletons and related operations.



Attributes
----------

.. autoapisummary::

   backend.api.modules.log_skeleton_router.router
   backend.api.modules.log_skeleton_router.MODULE_NAME


Functions
---------

.. autoapisummary::

   backend.api.modules.log_skeleton_router.compute_log_skeleton
   backend.api.modules.log_skeleton_router.get_equivalence
   backend.api.modules.log_skeleton_router.get_always_after
   backend.api.modules.log_skeleton_router.get_always_before
   backend.api.modules.log_skeleton_router.get_never_together
   backend.api.modules.log_skeleton_router.get_directly_follows
   backend.api.modules.log_skeleton_router.get_activity_frequencies


Module Contents
---------------

.. py:data:: router

.. py:data:: MODULE_NAME
   :value: 'log_skeleton'


.. py:function:: compute_log_skeleton(background_tasks: fastapi.BackgroundTasks, request: fastapi.Request, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> Dict[str, str]
   :async:


   Computes the log skeleton and stores it.

   The log skeleton is computed in the background and stored in the app state.

   :param background_tasks: The background tasks object. This is used to schedule
                            the computation of the log skeleton.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.
   :param celonis: The CelonisManager dependency injection.
                   Defaults to Depends(get_celonis_connection).
   :type celonis: optional

   :returns: A dictionary containing the job ID of the scheduled task.


.. py:function:: get_equivalence(job_id: str, request: fastapi.Request) -> dict

   Retrieves the equivalence relations from the log skeleton.

   :param job_id: The ID of the job for which to retrieve the equivalence relations.
   :param request: The FastAPI request object.

   :returns: A JSON object with "tables" and "graphs" keys.


.. py:function:: get_always_after(job_id: str, request: fastapi.Request) -> dict

   Retrieves the always-after relations from the log skeleton.

   :returns: A dictionary with a "tables" list and optional "graphs" list.


.. py:function:: get_always_before(job_id: str, request: fastapi.Request) -> dict

   Retrieves the always-before relations from the log skeleton.


.. py:function:: get_never_together(job_id: str, request: fastapi.Request) -> dict

   Retrieves the never-together relations from the log skeleton.


.. py:function:: get_directly_follows(job_id: str, request: fastapi.Request) -> dict

   Retrieves the directly-follows relations from the log skeleton.


.. py:function:: get_activity_frequencies(job_id: str, request: fastapi.Request) -> dict

   Retrieves the activity frequencies from the log skeleton.


