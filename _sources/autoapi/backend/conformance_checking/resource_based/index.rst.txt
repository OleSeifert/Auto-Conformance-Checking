backend.conformance_checking.resource_based
===========================================

.. py:module:: backend.conformance_checking.resource_based

.. autoapi-nested-parse::

   Contains functionality for resource-based conformance checking.

   This module defines the ResourceBased class which uses PM4Py to discover
   resource-based conformance checking metrics from event logs.



Attributes
----------

.. autoapisummary::

   backend.conformance_checking.resource_based.SocialNetworkAnalysisType


Classes
-------

.. autoapisummary::

   backend.conformance_checking.resource_based.ResourceBased


Module Contents
---------------

.. py:type:: SocialNetworkAnalysisType
   :canonical: Dict[Tuple[str, str], float]


.. py:class:: ResourceBased(log: pandas.DataFrame, case_id_col: Optional[str] = None, activity_col: Optional[str] = None, timestamp_col: Optional[str] = None, resource_col: Optional[str] = None, group_col: Optional[str] = None)

   Represents the resource-based conformance checking metrics of a log.

   .. attribute:: log

      The event log.

   .. attribute:: case_id_col

      The name of the Case ID column. Only needed if
      the log is read as a csv file.

      :type: optional

   .. attribute:: activity_col

      The name of the Activity column. Only needed if
      the log is read as a csv file.

      :type: optional

   .. attribute:: timestamp_col

      The name of the Timestamp column. Only needed if
      the log is read as a csv file.

      :type: optional

   .. attribute:: resource_col

      The name of the Resource column. Only needed if
      the log is read as a csv file.

      :type: optional

   .. attribute:: _handover_of_work

      The Handover of Work metric. Defaults to None.

   .. attribute:: _subcontracting

      The Subcontracting metric. Defaults to None.

   .. attribute:: _working_together

      The Working Together metric. Defaults to None.

   .. attribute:: _similar_activities

      The Similar Activities metric. Defaults to None.

   .. attribute:: _organizational_roles

      The Organizational Roles of the log. Defaults
      to None.

   .. attribute:: _organizational_diagnostics

      The Organizational Diagnostics of the log.
      Defaults to None.


   .. py:attribute:: log


   .. py:attribute:: case_id_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: activity_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: timestamp_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: resource_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: group_col
      :type:  Optional[str]
      :value: None



   .. py:method:: compute_handover_of_work() -> None

      Calculates the Handover of Work metric.

      The Handover of Work metric measures how many times an
      individual is followed by another individual in the execution of
      a business process. It is stored in a dictionary where the keys
      are tuples of two individuals and the values are the number of
      times the first individual is followed by the second individual
      in the execution of a business process.



   .. py:method:: get_handover_of_work_values() -> SocialNetworkAnalysisType

      Returns the Handover of Work metric.

      The Handover of Work metric is a dictionary where the keys are
      tuples of two individuals and the values are the number of times
      the first individual is followed by the second individual
      in the execution of a business process.

      :returns: The Handover of Work metric.

      :raises ValueError: If the Handover of Work values have not been calculated yet.



   .. py:method:: is_handover_of_work_directed() -> bool

      Checks if the Handover of Work metric is directed.

      :returns: True if the Handover of Work metric is directed, False otherwise.



   .. py:method:: compute_subcontracting() -> None

      Calculates the Subcontracting metric.

      The Subcontracting metric calculates how many times the work of
      an individual is interleaved by the work of another individual,
      only to eventually “return” to the original individual. It is
      stored in a dictionary where the keys are tuples of two
      individuals and the values are the number of times the first
      individual is  interleaved by the second individual in the
      execution of a business process.



   .. py:method:: get_subcontracting_values() -> SocialNetworkAnalysisType

      Returns the Subcontracting metric.

      The Subcontracting metric is a dictionary where the keys are
      tuples of two individuals and the values are the number of times
      the first individual is interleaved by the second individual
      in the execution of a business process.

      :returns: The Subcontracting metric.

      :raises ValueError: If the Subcontracting values have not been calculated yet.



   .. py:method:: is_subcontracting_directed() -> bool

      Checks if the Subcontracting metric is directed.

      :returns: True if the Subcontracting metric is directed, False otherwise.

      :raises ValueError: If the Subcontracting values have not been calculated yet.



   .. py:method:: compute_working_together() -> None

      Calculates the Working Together metric.

      The Working Together metric calculates how many times two
      individuals work together to resolve a process instance. It is
      stored in a dictionary where the keys are tuples of two
      individuals and the values are the number of times the two
      individuals worked together to resolve a process instance.



   .. py:method:: get_working_together_values() -> SocialNetworkAnalysisType

      Returns the Working Together metric.

      The Working Together metric is a dictionary where the keys are
      tuples of two individuals and the values are the number of times
      the two individuals worked together to resolve a process instance.

      :returns: The Working Together metric.

      :raises ValueError: If the Working Together values have not been calculated yet.



   .. py:method:: is_working_together_directed() -> bool

      Checks if the Working Together metric is directed.

      :returns: True if the Working Together metric is directed, False otherwise.

      :raises ValueError: If the Working Together values have not been calculated yet.



   .. py:method:: compute_similar_activities() -> None

      Calculates the Similar Activities metric.

      The Similar Activities metric calculates how similar the work
      patterns are between two individuals. It is stored in a
      dictionary where the keys are tuples of two individuals and the
      values are the similarity score between the two individuals.



   .. py:method:: get_similar_activities_values() -> SocialNetworkAnalysisType

      Returns the Similar Activities metric.

      The Similar Activities metric is a dictionary where the keys are
      tuples of two individuals and the values are the similarity score
      between the two individuals.

      :returns: The Similar Activities metric.

      :raises ValueError: If the Similar Activities values have not been calculated yet.



   .. py:method:: is_similar_activities_directed() -> bool

      Checks if the Similar Activities metric is directed.

      :returns: True if the Similar Activities metric is directed, False otherwise.

      :raises ValueError: If the Similar Activities values have not been calculated yet.



   .. py:method:: compute_organizational_roles() -> None

      Calculates the organizational roles.

      A role is a set of activities in the log that are executed by a similar
      (multi)set of resources. Hence, it is a specific function within an
      organization. Grouping the activities into roles can help:

        - In understanding which activities are executed by which roles,
        - By understanding roles themselves (the numerosity of resources for
            a single activity may not provide enough explanation).

      Initially, each activity corresponds to a different role and is
      associated with the multiset of its originators. After that, roles are
      merged according to their similarity until no more merges are possible.

      The information about the roles is stored as a semi-structured list of
      activity groups, where each group associates a list of activities
      with a dictionary of originators and their corresponding
      importance scores.



   .. py:method:: get_organizational_roles() -> List[Dict[str, Any]]

      Returns the organizational roles.

      The organizational roles are stored as a semi-structured list of
      activity groups, where each group associates a list of activities
      with a dictionary of originators and their corresponding
      importance scores.

      :returns: A list of dictionaries, where each dictionary
                contains the activities and their corresponding originators' importance
                scores.
                Each dictionary has the following structure:
                {
                    "activities": List[str],    # List of activities in the role
                    "originators_importance": Dict[str, float]
                        # Dictionary of originators and their importance scores
                }

      :raises ValueError: If the organizational roles have not been calculated yet.



   .. py:method:: get_number_of_distinct_activities(start_time: str, end_time: str, resource: str) -> int

      Calculates the number of distinct activities.

      Number of distinct activities done by a resource in a given time
      interval [t1, t2).

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the number of
                       distinct activities.
      :type resource: str

      :returns: An integer indicating the number of distinct activities done by
                the resource in the given time interval.



   .. py:method:: get_activity_frequency(start_time: str, end_time: str, resource: str, activity: str) -> float

      Calculates the activity frequency.

      Fraction of completions of a given activity a by a given
      resource r during a given time slot [t1, t2), with respect to
      the total number of activity completions by resource r during
      [t1, t2).

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



   .. py:method:: get_activity_completions(start_time: str, end_time: str, resource: str) -> int

      Calculates the activity completions.

      The number of activity instances completed by a given resource
      during a given time slot.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the activity
                       completions.
      :type resource: str

      :returns: An integer indicating the number of activity instances completed
                by the resource in the given time interval.



   .. py:method:: get_case_completions(start_time: str, end_time: str, resource: str) -> int

      Calculates the case completion.

      The number of cases completed during a given time slot in which
      a given resource was involved.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the case
                       completions.
      :type resource: str

      :returns: An integer indicating the number of cases completed by the
                resource in the given time interval.



   .. py:method:: get_fraction_case_completions(start_time: str, end_time: str, resource: str) -> float

      Calculates the fraction case completion.

      The fraction of cases completed during a given time slot in
      which a given resource was involved with respect to the total
      number of cases completed during the time slot.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the
                       fraction case completions.
      :type resource: str

      :returns: A float indicating the fraction of cases completed by the
                resource in the given time interval.



   .. py:method:: get_average_workload(start_time: str, end_time: str, resource: str) -> float

      Calculates the average workload.

      The average number of activities started by a given resource but
      not completed at a moment in time.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the average
                       workload.
      :type resource: str

      :returns: A float indicating the average workload of the given resource
                in the given time interval.



   .. py:method:: get_multitasking(start_time: str, end_time: str, resource: str) -> float

      Calculates the multitasking.

      The fraction of active time during which a given resource is
      involved in more than one activity with respect to the
      resource's active time.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the
                       multitasking.
      :type resource: str

      :returns: A float indicating the multitasking of the given resource
                in the given time interval.



   .. py:method:: get_average_activity_duration(start_time: str, end_time: str, resource: str, activity: str) -> float

      Calculates the average activity duration.

      The average duration of instances of a given activity completed
      during a given time slot by a given resource.

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



   .. py:method:: get_average_case_duration(start_time: str, end_time: str, resource: str) -> float

      Calculates the average case duration.

      The average duration of cases completed during a given time slot
      in which a given resource was involved.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the average
                       case duration.
      :type resource: str

      :returns: A float indicating the average duration of cases completed
                by the resource in the given time interval.



   .. py:method:: get_interaction_two_resources(start_time: str, end_time: str, resource1: str, resource2: str) -> float

      Calculates the interaction between two resources.

      The number of cases completed during a given time slot in which
      two given resources were involved.

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



   .. py:method:: get_social_position(start_time: str, end_time: str, resource: str) -> float

      Calculates the social position.

      The fraction of resources involved in the same cases with a
      given resource during a given time slot with respect to the
      total number of resources active during the time slot.

      :param start_time: The start time of the interval.
      :type start_time: str
      :param end_time: The end time of the interval.
      :type end_time: str
      :param resource: The resource for which to calculate the
                       social position.
      :type resource: str

      :returns: A float indicating the social position of the given resource
                in the given time interval.



   .. py:method:: compute_organizational_diagnostics() -> None

      Calculates the organizational diagnostics.

      Provides the local diagnostics for the organizational model
      starting from a log object and considering the resource group
      specified by the attribute. It is stored in a dictionary where the keys are
      the names of the group-related metrics and the values are the
      corresponding diagnostic values.

      :raises ValueError: If the resource column name is not provided.



   .. py:method:: get_group_relative_focus() -> Dict[str, Dict[str, float]]

      Returns the Group Relative Focus metric.

       The Group Relative Focus metric specifies for a given work how
       much a resource group performed this type of work compared to
       the overall workload of the group. It can be used to measure how
       the workload of a resource group is distributed over different
       types of work, i.e., work diversification of the group.

      :returns: A dictionary where the keys are the names of the resources
                and the values are dictionaries containing activity names
                and the Group Relative Focus metric.

      :raises ValueError: If the organizational diagnostics have not been
      :raises calculated yet.:



   .. py:method:: get_group_relative_stake() -> Dict[str, Dict[str, float]]

      Returns the Group Relative Stake metric.

      The Group Relative Stake metric specifies for a given work how much
      this type of work was performed by a certain resource group among
      all groups. It can be used to measure how the workload devoted to
      a certain type of work is distributed over resource groups in an
      organizational model, i.e., work participation by different groups.

      :returns: A dictionary where the keys are the names of the resources and
                the values are dictionaries containing activity names and the
                Group Relative Stake metric.

      :raises ValueError: If the organizational diagnostics have not been
      :raises calculated yet.:



   .. py:method:: get_group_coverage() -> Dict[str, Dict[str, float]]

      Returns the Group Coverage metric.

      The Group Coverage metric with respect to a given type of work,
      specifies the proportion of members of a resource group that
      performed this type of work.

      :returns: A dictionary where the keys are the names of the resources
                and the values are dictionaries containing resources and the
                Group Coverage metric.

      :raises ValueError: If the organizational diagnostics have not been
      :raises calculated yet.:



   .. py:method:: get_group_member_contribution() -> Dict[str, Dict[str, Dict[str, int]]]

      Returns the Group Member Contribution metric.

      The Group Member Contribution metric of a member of a resource group
      with respect to a given type of work specifies how much of this type
      of work by the group was performed by the member. It can be used to
      measure how the workload of the entire group devoted to a certain
      type of work is distributed over the group members.

      :returns: A dictionary where the keys are the names of the resources and
                the values are dictionaries containing resources and the Group
                Member Contribution metric.

      :raises ValueError: If the organizational diagnostics have not been
      :raises calculated yet.:



