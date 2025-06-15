backend.api.modules.resource_based_router
=========================================

.. py:module:: backend.api.modules.resource_based_router

.. autoapi-nested-parse::

   Contains the routes for handling resource-based conformance checking.



Attributes
----------

.. autoapisummary::

   backend.api.modules.resource_based_router.ReturnGraphType
   backend.api.modules.resource_based_router.router
   backend.api.modules.resource_based_router.MODULE_NAME


Functions
---------

.. autoapisummary::

   backend.api.modules.resource_based_router.compute_sna_metrics
   backend.api.modules.resource_based_router.get_handover_of_work_metric
   backend.api.modules.resource_based_router.get_subcontracting_metric
   backend.api.modules.resource_based_router.get_working_together_metric
   backend.api.modules.resource_based_router.get_similar_activities_metric
   backend.api.modules.resource_based_router.get_organizational_roles_result
   backend.api.modules.resource_based_router.get_distinct_activities
   backend.api.modules.resource_based_router.get_distinct_activities_pql
   backend.api.modules.resource_based_router.get_resource_activity_frequency
   backend.api.modules.resource_based_router.get_resource_activity_frequency_pql
   backend.api.modules.resource_based_router.get_resource_activity_completions
   backend.api.modules.resource_based_router.get_resource_activity_completions_pql
   backend.api.modules.resource_based_router.get_resource_case_completions
   backend.api.modules.resource_based_router.get_resource_case_completions_pql
   backend.api.modules.resource_based_router.get_resource_fraction_case_completions
   backend.api.modules.resource_based_router.get_resource_fraction_case_completions_pql
   backend.api.modules.resource_based_router.get_resource_average_workload
   backend.api.modules.resource_based_router.get_resource_average_workload_pql
   backend.api.modules.resource_based_router.get_resource_multitasking
   backend.api.modules.resource_based_router.get_resource_average_activity_duration
   backend.api.modules.resource_based_router.get_resource_average_case_duration
   backend.api.modules.resource_based_router.get_interaction_of_two_resources
   backend.api.modules.resource_based_router.get_interaction_of_two_resources_pql
   backend.api.modules.resource_based_router.get_resource_social_position
   backend.api.modules.resource_based_router.get_group_relative_focus_metric
   backend.api.modules.resource_based_router.get_group_relative_stake_metric
   backend.api.modules.resource_based_router.get_group_coverage_metric
   backend.api.modules.resource_based_router.get_group_member_contribution_metric


Module Contents
---------------

.. py:type:: ReturnGraphType
   :canonical: Dict[str, List[Dict[str, List[Union[str, Dict[str, str]]]]]]


.. py:data:: router

.. py:data:: MODULE_NAME
   :value: 'resource_based'


.. py:function:: compute_sna_metrics(background_tasks: fastapi.BackgroundTasks, request: fastapi.Request, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> Dict[str, str]
   :async:


   Computes the SNA metrics and stores it.

   :param background_tasks: The background tasks manager.
   :param request: The FastAPI request object.
   :param celonis: The Celonis connection manager instance.

   :returns: A dictionary containing the job ID of the scheduled task.


.. py:function:: get_handover_of_work_metric(job_id: str, request: fastapi.Request) -> Dict[str, List[Dict[str, List[Any]]]]
   :async:


   Retrieves the computed Handover of Work SNA metric and returns it.

   In a frontend-compatible format.


.. py:function:: get_subcontracting_metric(job_id: str, request: fastapi.Request) -> Dict[str, List[Dict[str, List[Any]]]]
   :async:


   Returns subcontracting metric in table/graph format.


.. py:function:: get_working_together_metric(job_id: str, request: fastapi.Request) -> Dict[str, List[Dict[str, List[Any]]]]
   :async:


   Returns working together metric in table/graph format.


.. py:function:: get_similar_activities_metric(job_id: str, request: fastapi.Request) -> Dict[str, List[Dict[str, List[Any]]]]
   :async:


   Returns similar activities metric in table/graph format.


.. py:function:: get_organizational_roles_result(job_id: str, request: fastapi.Request) -> List[backend.api.models.schemas.resource_based_models.OrganizationalRole]
   :async:


   Retrieves the computed organizational roles.

   :param job_id: The ID of the job to retrieve the organizational roles for.
   :param request: The FastAPI request object.

   :returns: A list of OrganizationalRole objects representing the discovered roles.


.. py:function:: get_distinct_activities(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time.'), end_time: str = Query(..., description='End time.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of distinct activities.

   :param start_time: The start time of the range.
   :param end_time: The end time of the range.
   :param resource: The resource for which to calculate the number of
                    distinct activities.
   :param celonis: The Celonis connection manager instance.

   :returns: The number of distinct activities for the specified resource.


.. py:function:: get_distinct_activities_pql(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time.'), end_time: str = Query(..., description='End time.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of distinct activities via a pql query.

   :param start_time: The start time of the range.
   :param end_time: The end time of the range.
   :param resource: The resource for which to calculate the number of
                    distinct activities.
   :param celonis: The Celonis connection manager instance.

   :returns: The number of distinct activities for the specified resource.


.. py:function:: get_resource_activity_frequency(resource: str = Query(..., description='The resource identifier.'), activity: str = Query(..., description='The specific activity name.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the activity frequency for a given resource and activity.

   :param resource: The resource for which to calculate the activity frequency.
   :param activity: The activity for which to calculate the frequency.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the activity frequency.


.. py:function:: get_resource_activity_frequency_pql(resource: str = Query(..., description='The resource identifier.'), activity: str = Query(..., description='The specific activity name.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the activity frequency for an activity via a PQL query.

   :param resource: The resource for which to calculate the activity frequency.
   :param activity: The activity for which to calculate the frequency.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the activity frequency.


.. py:function:: get_resource_activity_completions(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of activity instances completed by a resource.

   :param resource: The resource for which to calculate activity completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: An integer indicating the number of activity completions.


.. py:function:: get_resource_activity_completions_pql(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of activity instances completed via a PQL query.

   :param resource: The resource for which to calculate activity completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: An integer indicating the number of activity completions.


.. py:function:: get_resource_case_completions(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of cases completed by a resource.

   :param resource: The resource for which to calculate case completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: An integer indicating the number of case completions involving the resource.


.. py:function:: get_resource_case_completions_pql(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> int
   :async:


   Retrieves the number of cases completed by a resource via a PQL query.

   :param resource: The resource for which to calculate case completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: An integer indicating the number of case completions involving the resource.


.. py:function:: get_resource_fraction_case_completions(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the fraction of cases completed by a resource.

   :param resource: The resource for which to calculate the fraction of case completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the fraction of case completions involving the resource.


.. py:function:: get_resource_fraction_case_completions_pql(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the fraction of cases completed by a resource via a PQL query.

   :param resource: The resource for which to calculate the fraction of case completions.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the fraction of case completions involving the resource.


.. py:function:: get_resource_average_workload(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the average workload for a given resource in a time interval.

   :param resource: The resource for which to calculate the average workload.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the average workload.


.. py:function:: get_resource_average_workload_pql(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the average workload for a resource via a PQL query.

   :param resource: The resource for which to calculate the average workload.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the average workload.


.. py:function:: get_resource_multitasking(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the multitasking metric for a given resource.

   :param resource: The resource for which to calculate multitasking.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the multitasking metric.


.. py:function:: get_resource_average_activity_duration(resource: str = Query(..., description='The resource identifier.'), activity: str = Query(..., description='The specific activity name.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the average duration for an activity completed by a resource.

   :param resource: The resource involved.
   :param activity: The activity name.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the average duration of the activity for the resource.


.. py:function:: get_resource_average_case_duration(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the average duration of cases completed by a resource.

   :param resource: The resource involved.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the average duration of cases involving the resource.


.. py:function:: get_interaction_of_two_resources(resource1: str = Query(..., description='The first resource identifier.'), resource2: str = Query(..., description='The second resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the interaction between two resources.

   :param resource1: The first resource.
   :param resource2: The second resource.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the interaction (number of common cases) between the two resources.


.. py:function:: get_interaction_of_two_resources_pql(resource1: str = Query(..., description='The first resource identifier.'), resource2: str = Query(..., description='The second resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the interaction between two resources via a PQL query.

   :param resource1: The first resource.
   :param resource2: The second resource.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the interaction (number of common cases) between the two resources.


.. py:function:: get_resource_social_position(resource: str = Query(..., description='The resource identifier.'), start_time: str = Query(..., description='Start time of the interval.'), end_time: str = Query(..., description='End time of the interval.'), celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> float
   :async:


   Retrieves the social position of a given resource in a time interval.

   :param resource: The resource for which to calculate the social position.
   :param start_time: The start time of the interval.
   :param end_time: The end time of the interval.
   :param celonis: The Celonis connection manager instance.

   :returns: A float indicating the social position of the resource.


.. py:function:: get_group_relative_focus_metric(job_id: str, request: fastapi.Request) -> Dict[str, Dict[str, float]]
   :async:


   Retrieves the Group Relative Focus metric.

   :param job_id: The ID of the job to retrieve the metric for.
   :param request: The FastAPI request object.

   :returns: A dictionary containing the Group Relative Focus metric.


.. py:function:: get_group_relative_stake_metric(job_id: str, request: fastapi.Request) -> Dict[str, Dict[str, float]]
   :async:


   Retrieves the Group Relative Stake metric.

   :param job_id: The ID of the job to retrieve the metric for.
   :param request: The FastAPI request object.

   :returns: A dictionary containing the Group Relative Stake metric.


.. py:function:: get_group_coverage_metric(job_id: str, request: fastapi.Request) -> Dict[str, Dict[str, float]]
   :async:


   Retrieves the Group Coverage metric.

   :param job_id: The ID of the job to retrieve the metric for.
   :param request: The FastAPI request object.

   :returns: A dictionary containing the Group Coverage metric.


.. py:function:: get_group_member_contribution_metric(job_id: str, request: fastapi.Request) -> Dict[str, Dict[str, Dict[str, int]]]
   :async:


   Retrieves the Group Member Contribution metric.

   :param job_id: The ID of the job to retrieve the metric for.
   :param request: The FastAPI request object.

   :returns: A dictionary containing the Group Member Contribution metric.


