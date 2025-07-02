backend.pql_queries.resource_based_queries
==========================================

.. py:module:: backend.pql_queries.resource_based_queries

.. autoapi-nested-parse::

   Queries that can be used to get resource related data from celonis.



Functions
---------

.. autoapisummary::

   backend.pql_queries.resource_based_queries.get_number_of_resources
   backend.pql_queries.resource_based_queries.get_number_of_groups
   backend.pql_queries.resource_based_queries.get_resource_for_activity
   backend.pql_queries.resource_based_queries.get_handover_of_work_values
   backend.pql_queries.resource_based_queries.get_subcontracting_values
   backend.pql_queries.resource_based_queries.get_working_together_values
   backend.pql_queries.resource_based_queries.get_similar_activities_values
   backend.pql_queries.resource_based_queries.get_organizational_roles
   backend.pql_queries.resource_based_queries.get_number_of_distinct_activities
   backend.pql_queries.resource_based_queries.get_activity_frequency
   backend.pql_queries.resource_based_queries.get_activity_completions
   backend.pql_queries.resource_based_queries.get_case_completions
   backend.pql_queries.resource_based_queries.get_fraction_case_completions
   backend.pql_queries.resource_based_queries.get_average_workload
   backend.pql_queries.resource_based_queries.get_average_activity_duration
   backend.pql_queries.resource_based_queries.get_average_case_duration
   backend.pql_queries.resource_based_queries.get_interaction_two_resources
   backend.pql_queries.resource_based_queries.get_social_position
   backend.pql_queries.resource_based_queries.get_group_relative_focus
   backend.pql_queries.resource_based_queries.get_group_relative_stake
   backend.pql_queries.resource_based_queries.get_group_coverage
   backend.pql_queries.resource_based_queries.get_group_member_interaction


Module Contents
---------------

.. py:function:: get_number_of_resources(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the count of resources from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the count of resources


.. py:function:: get_number_of_groups(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that gets the count of groups from an event log.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the count of groups


.. py:function:: get_resource_for_activity(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   A query that maps activities to their related resources.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: a pandas Dataframe that contains the mapping between activities to their related resources


.. py:function:: get_handover_of_work_values(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Handover of Work metric.

   The Handover of Work metric is a dictionary where the keys are
   tuples of two individuals and the values are the number of times
   the first individual is followed by the second individual
   in the execution of a business process.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Handover of Work metric.


.. py:function:: get_subcontracting_values(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Subcontracting metric.

   The Subcontracting metric is a dictionary where the keys are
   tuples of two individuals and the values are the number of times
   the first individual is interleaved by the second individual
   in the execution of a business process.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Subcontracting metric.


.. py:function:: get_working_together_values(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Working Together metric.

   The Working Together metric is a dictionary where the keys are
   tuples of two individuals and the values are the number of times
   the two individuals worked together to resolve a process instance.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Working Together metric.


.. py:function:: get_similar_activities_values(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Similar Activities metric.

   The Similar Activities metric is a dictionary where the keys are
   tuples of two individuals and the values are the similarity score
   between the two individuals.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Similar Activities metric.


.. py:function:: get_organizational_roles(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the organizational roles.

   The organizational roles are stored as a semi-structured list of
   activity groups, where each group associates a list of activities
   with a dictionary of originators and their corresponding
   importance scores.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the organizational roles.


.. py:function:: get_number_of_distinct_activities(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> int

   Calculates the number of distinct activities.

   Number of distinct activities done by a resource in a given time
   interval [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the number of
                    distinct activities.
   :type resource: str

   :returns: An integer denoting the number of distinct activities.


.. py:function:: get_activity_frequency(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str, activity: str) -> float

   Calculates the activity frequency.

   Fraction of completions of a given activity a by a given
   resource r during a given time slot [t1, t2), with respect to
   the total number of activity completions by resource r during
   [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the activity
                    frequency.
   :type resource: str
   :param activity: The activity for which to calculate the frequency.
   :type activity: str

   :returns: A float indicating the activity frequency of the given activity
             by the resource in the given time interval.


.. py:function:: get_activity_completions(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> int

   Calculates the number of activity completions.

   Number of completions of a given activity by a given resource
   during a given time slot [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the number of
                    activity completions.
   :type resource: str

   :returns: An integer denoting the number of activity completions by the
             resource in the given time interval.


.. py:function:: get_case_completions(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> int

   Calculates the number of case completions.

   Number of completions of a given case by a given resource
   during a given time slot [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the number of
                    case completions.
   :type resource: str

   :returns: An integer denoting the number of case completions by the
             resource in the given time interval.


.. py:function:: get_fraction_case_completions(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> float

   Calculates the fraction of case completions.

   Fraction of completions of a case by a given resource r during
   a given time slot [t1, t2), with respect to the total number of
   case completions during [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the fraction
                    of case completions.
   :type resource: str

   :returns: A float indicating the fraction of case completions by the
             resource in the given time interval.


.. py:function:: get_average_workload(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> float

   Calculates the average workload.

   Average workload of a given resource r during a given time slot
   [t1, t2).

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the average
                    workload.
   :type resource: str

   :returns: A float indicating the average workload of the resource in the
             given time interval.


.. py:function:: get_average_activity_duration(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str, activity: str) -> float

   Calculates the average activity duration.

   The average duration of instances of a given activity completed
   during a given time slot by a given resource.

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the average
                    activity duration.
   :type resource: str
   :param activity: The activity for which to calculate the average
                    duration.
   :type activity: str

   :returns: A float indicating the average duration of the given activity
             by the resource in the given time interval.


.. py:function:: get_average_case_duration(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> float

   Calculates the average case duration.

   The average duration of cases completed during a given time slot
   in which a given resource was involved.

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the average
                    case duration.
   :type resource: str

   :returns: A float indicating the average duration of cases completed
             by the resource in the given time interval.


.. py:function:: get_interaction_two_resources(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource1: str, resource2: str) -> float

   Calculates the interaction between two resources.

   The number of cases completed during a given time slot in which
   two given resources were involved.

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource1: The first resource for which to calculate the
                     interaction.
   :type resource1: str
   :param resource2: The second resource for which to calculate the
                     interaction.
   :type resource2: str

   :returns: A float indicating the interaction between the two resources
             in the given time interval.


.. py:function:: get_social_position(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager, start_time: str, end_time: str, resource: str) -> float

   Calculates the social position of a resource.

   The social position is the fraction of resources that interacted
   with a given resource during a given time slot with respect to
   the total number of resources that were active during that time
   slot.

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager
   :param start_time: The start time of the interval.
   :type start_time: str
   :param end_time: The end time of the interval.
   :type end_time: str
   :param resource: The resource for which to calculate the social
                    position.
   :type resource: str

   :returns: A float indicating the social position of the resource in the
             given time interval.


.. py:function:: get_group_relative_focus(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Group Relative Focus.

   The Group Relative Focus metric specifies for a given work how
   much a resource group performed this type of work compared to
   the overall workload of the group. It can be used to measure how
   the workload of a resource group is distributed over different
   types of work, i.e., work diversification of the group.


   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Group Relative Focus for each group
             and activity.


.. py:function:: get_group_relative_stake(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns" the Group Relative Stake.

   The Group Relative Stake metric specifies for a given work how much
   this type of work was performed by a certain resource group among
   all groups. It can be used to measure how the workload devoted to
   a certain type of work is distributed over resource groups in an
   organizational model, i.e., work participation by different groups.


   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A DataFrame containing the Group Relative Stake for each group
             and activity.


.. py:function:: get_group_coverage(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Group Coverage metric.

   The Group Coverage metric with respect to a given type of work,
   specifies the proportion of members of a resource group that
   performed this type of work.

   :returns: A dictionary where the keys are the names of the resources
             and the values are dictionaries containing resources and the
             Group Coverage metric.


.. py:function:: get_group_member_interaction(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Returns the Group Member Contribution metric.

   The Group Member Contribution metric of a member of a resource group
   with respect to a given type of work specifies how much of this type
   of work by the group was performed by the member. It can be used to
   measure how the workload of the entire group devoted to a certain
   type of work is distributed over the group members.

   :param celonis: The Celonis connection
   :type celonis: CelonisConnectionManager


