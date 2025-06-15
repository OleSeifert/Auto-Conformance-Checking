backend.api.modules.declarative_router
======================================

.. py:module:: backend.api.modules.declarative_router

.. autoapi-nested-parse::

   Contains the routes for handling declarative constraints.



Attributes
----------

.. autoapisummary::

   backend.api.modules.declarative_router.ReturnGraphType
   backend.api.modules.declarative_router.router
   backend.api.modules.declarative_router.MODULE_NAME


Functions
---------

.. autoapisummary::

   backend.api.modules.declarative_router.compute_declarative_constraints
   backend.api.modules.declarative_router.get_existance_violations
   backend.api.modules.declarative_router.get_absence_violations
   backend.api.modules.declarative_router.get_exactly_one_violations
   backend.api.modules.declarative_router.get_init_violations
   backend.api.modules.declarative_router.get_responded_existence_violations
   backend.api.modules.declarative_router.get_coexistence_violations
   backend.api.modules.declarative_router.get_response_violations
   backend.api.modules.declarative_router.get_precedence_violations
   backend.api.modules.declarative_router.get_succession_violations
   backend.api.modules.declarative_router.get_altprecedence_violations
   backend.api.modules.declarative_router.get_altsuccession_violations
   backend.api.modules.declarative_router.get_chainresponse_violations
   backend.api.modules.declarative_router.get_chainprecedence_violations
   backend.api.modules.declarative_router.get_chainsuccession_violations
   backend.api.modules.declarative_router.get_noncoexistence_violations
   backend.api.modules.declarative_router.get_nonsuccession_violations
   backend.api.modules.declarative_router.get_nonchainsuccession_violations


Module Contents
---------------

.. py:type:: ReturnGraphType
   :canonical: Dict[str, List[Dict[str, List[Union[str, Dict[str, str]]]]]]


.. py:data:: router

.. py:data:: MODULE_NAME
   :value: 'declarative_constraints'


.. py:function:: compute_declarative_constraints(background_tasks: fastapi.BackgroundTasks, request: fastapi.Request, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> Dict[str, str]
   :async:


   Computes the declarative constraints and stores it.

   The declarative model is computed in the background and stored in the app state.

   :param background_tasks: The background tasks object. This is used to schedule
                            the computation of the declarative model.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.
   :param celonis: The CelonisManager dependency injection.
                   Defaults to Depends(get_celonis_connection).
   :type celonis: optional

   :returns: A dictionary containing the job ID of the scheduled task.


.. py:function:: get_existance_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the existance violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the existance violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the existance violations for the specified job.


.. py:function:: get_absence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the absence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the absence violations for the specified job.


.. py:function:: get_exactly_one_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the exactly_one violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the exactly_one violations for the specified job.


.. py:function:: get_init_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the init violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the init violations for the specified job.


.. py:function:: get_responded_existence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the responded_existence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the responded_existence violations for the specified job.


.. py:function:: get_coexistence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the coexistence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the coexistence violations for the specified job.


.. py:function:: get_response_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the response violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the response violations for the specified job.


.. py:function:: get_precedence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the precedence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the precedence violations for the specified job.


.. py:function:: get_succession_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the succession violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the succession violations for the specified job.


.. py:function:: get_altprecedence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the altprecedence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the altprecedence violations for the specified job.


.. py:function:: get_altsuccession_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the altsuccession violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the altsuccession violations for the specified job.


.. py:function:: get_chainresponse_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the chainresponse violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the chainresponse violations for the specified job.


.. py:function:: get_chainprecedence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the chainprecedence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the chainprecedence violations for the specified job.


.. py:function:: get_chainsuccession_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the chainsuccession violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the chainsuccession violations for the specified job.


.. py:function:: get_noncoexistence_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the noncoexistence violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the noncoexistence violations for the specified job.


.. py:function:: get_nonsuccession_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the nonsuccession violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the nonsuccession violations for the specified job.


.. py:function:: get_nonchainsuccession_violations(job_id: str, request: fastapi.Request) -> ReturnGraphType

   Retrieves the nonchainsuccession violations from the declarative model.

   :param job_id: The ID of the job for which to retrieve the  violations.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: A list of lists containing the nonchainsuccession violations for the specified job.


