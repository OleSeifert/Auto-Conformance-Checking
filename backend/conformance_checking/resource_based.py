"""Contains functionality for resource-based conformance checking.

This module defines the ResourceBased class which uses PM4Py to discover
resource-based conformance checking metrics from event logs.
"""

from typing import Any, Dict, List, Optional, Tuple, TypeAlias

import pandas as pd
import pm4py  # type: ignore
from pm4py.algo.organizational_mining.local_diagnostics import (  # type: ignore
    algorithm as org_algorithm,  # type: ignore
)
from pm4py.algo.organizational_mining.resource_profiles import (  # type: ignore
    algorithm as rp_algorithm,  # type: ignore
)
from pm4py.objects.org.sna.obj import SNA  # type: ignore

SocialNetworkAnalysisType: TypeAlias = Dict[Tuple[str, str], float]


class ResourceBased:
    """Represents the resource-based conformance checking metrics of a log.

    Attributes:
        log: The event log.
        case_id_col (optional): The name of the Case ID column. Only needed if
            the log is read as a csv file.
        activity_col (optional): The name of the Activity column. Only needed if
            the log is read as a csv file.
        timestamp_col (optional): The name of the Timestamp column. Only needed if
            the log is read as a csv file.
        resource_col (optional): The name of the Resource column. Only needed if
            the log is read as a csv file.
        _handover_of_work: The Handover of Work metric. Defaults to None.
        _subcontracting: The Subcontracting metric. Defaults to None.
        _working_together: The Working Together metric. Defaults to None.
        _similar_activities: The Similar Activities metric. Defaults to None.
        _organizational_roles: The Organizational Roles of the log. Defaults
            to None.
        _organizational_diagnostics: The Organizational Diagnostics of the log.
            Defaults to None.
    """

    def __init__(
        self,
        log: pd.DataFrame,
        case_id_col: Optional[str] = None,
        activity_col: Optional[str] = None,
        timestamp_col: Optional[str] = None,
        resource_col: Optional[str] = None,
        group_col: Optional[str] = None,
    ) -> None:
        """Initializes the ResourceBased class with an event log.

        Args:
            log: The event log.
            case_id_col (optional): The name of the Case ID column. Defaults
              to None.
            activity_col (optional): The name of the Activity column. Defaults
              to None.
            timestamp_col (optional): The name of the Timestamp column. Defaults
              to None.
            resource_col (optional): The name of the Resource column. Defaults
              to None.
            group_col (optional): The name of the Group column. Defaults to None.
        """
        self.log = log
        self._handover_of_work: Optional[SNA] = None
        self._subcontracting: Optional[SNA] = None
        self._working_together: Optional[SNA] = None
        self._similar_activities: Optional[SNA] = None
        self._organizational_roles: Optional[List[Any]] = None
        self._organizational_diagnostics: Optional[Dict[str, Any]] = None
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col
        self.resource_col: Optional[str] = resource_col
        self.group_col: Optional[str] = group_col

    # **************** Social Network Analysis ****************

    def compute_handover_of_work(self) -> None:
        """Calculates the Handover of Work metric.

        The Handover of Work metric measures how many times an
        individual is followed by another individual in the execution of
        a business process. It is stored in a dictionary where the keys
        are tuples of two individuals and the values are the number of
        times the first individual is followed by the second individual
        in the execution of a business process.
        """
        self._handover_of_work = pm4py.discover_handover_of_work_network(self.log)

    def get_handover_of_work_values(self) -> SocialNetworkAnalysisType:
        """Returns the Handover of Work metric.

        The Handover of Work metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the first individual is followed by the second individual
        in the execution of a business process.

        Returns:
            The Handover of Work metric.

        Raises:
            ValueError: If the Handover of Work values have not been calculated yet.
        """
        if self._handover_of_work is None:
            raise ValueError(
                "Handover of Work values have not been calculated yet. "
                "Please call compute_handover_of_work() first."
            )
        return self._handover_of_work.connections

    def is_handover_of_work_directed(self) -> bool:
        """Checks if the Handover of Work metric is directed.

        Returns:
            True if the Handover of Work metric is directed, False otherwise.
        """
        if self._handover_of_work is None:
            raise ValueError(
                "Handover of Work values have not been calculated yet. "
                "Please call compute_handover_of_work() first."
            )
        return self._handover_of_work.is_directed

    def compute_subcontracting(self) -> None:
        """Calculates the Subcontracting metric.

        The Subcontracting metric calculates how many times the work of
        an individual is interleaved by the work of another individual,
        only to eventually “return” to the original individual. It is
        stored in a dictionary where the keys are tuples of two
        individuals and the values are the number of times the first
        individual is  interleaved by the second individual in the
        execution of a business process.
        """
        self._subcontracting = pm4py.discover_subcontracting_network(self.log)

    def get_subcontracting_values(self) -> SocialNetworkAnalysisType:
        """Returns the Subcontracting metric.

        The Subcontracting metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the first individual is interleaved by the second individual
        in the execution of a business process.

        Returns:
            The Subcontracting metric.

        Raises:
            ValueError: If the Subcontracting values have not been calculated yet.
        """
        if self._subcontracting is None:
            raise ValueError(
                "Subcontracting values have not been calculated yet. "
                "Please call compute_subcontracting() first."
            )
        return self._subcontracting.connections

    def is_subcontracting_directed(self) -> bool:
        """Checks if the Subcontracting metric is directed.

        Returns:
            True if the Subcontracting metric is directed, False otherwise.

        Raises:
            ValueError: If the Subcontracting values have not been calculated yet.
        """
        if self._subcontracting is None:
            raise ValueError(
                "Subcontracting values have not been calculated yet. "
                "Please call compute_subcontracting() first."
            )
        return self._subcontracting.is_directed

    def compute_working_together(self) -> None:
        """Calculates the Working Together metric.

        The Working Together metric calculates how many times two
        individuals work together to resolve a process instance. It is
        stored in a dictionary where the keys are tuples of two
        individuals and the values are the number of times the two
        individuals worked together to resolve a process instance.
        """
        self._working_together = pm4py.discover_working_together_network(self.log)

    def get_working_together_values(self) -> SocialNetworkAnalysisType:
        """Returns the Working Together metric.

        The Working Together metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the two individuals worked together to resolve a process instance.

        Returns:
            The Working Together metric.

        Raises:
            ValueError: If the Working Together values have not been calculated yet.
        """
        if self._working_together is None:
            raise ValueError(
                "Working Together values have not been calculated yet. "
                "Please call compute_working_together() first."
            )
        return self._working_together.connections

    def is_working_together_directed(self) -> bool:
        """Checks if the Working Together metric is directed.

        Returns:
            True if the Working Together metric is directed, False otherwise.

        Raises:
            ValueError: If the Working Together values have not been calculated yet.
        """
        if self._working_together is None:
            raise ValueError(
                "Working Together values have not been calculated yet. "
                "Please call compute_working_together() first."
            )
        return self._working_together.is_directed

    def compute_similar_activities(self) -> None:
        """Calculates the Similar Activities metric.

        The Similar Activities metric calculates how similar the work
        patterns are between two individuals. It is stored in a
        dictionary where the keys are tuples of two individuals and the
        values are the similarity score between the two individuals.
        """
        self._similar_activities = pm4py.discover_activity_based_resource_similarity(
            self.log
        )

    def get_similar_activities_values(self) -> SocialNetworkAnalysisType:
        """Returns the Similar Activities metric.

        The Similar Activities metric is a dictionary where the keys are
        tuples of two individuals and the values are the similarity score
        between the two individuals.

        Returns:
            The Similar Activities metric.

        Raises:
            ValueError: If the Similar Activities values have not been calculated yet.
        """
        if self._similar_activities is None:
            raise ValueError(
                "Similar Activities values have not been calculated yet. "
                "Please call compute_similar_activities() first."
            )
        return self._similar_activities.connections

    def is_similar_activities_directed(self) -> bool:
        """Checks if the Similar Activities metric is directed.

        Returns:
            True if the Similar Activities metric is directed, False otherwise.

        Raises:
            ValueError: If the Similar Activities values have not been calculated yet.
        """
        if self._similar_activities is None:
            raise ValueError(
                "Similar Activities values have not been calculated yet. "
                "Please call compute_similar_activities() first."
            )
        return self._similar_activities.is_directed

    # **************** Role Discovery ****************

    def compute_organizational_roles(self) -> None:
        """Calculates the organizational roles.

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
        """
        self._organizational_roles = pm4py.discover_organizational_roles(self.log)

    def get_organizational_roles(self) -> List[Dict[str, Any]]:
        """Returns the organizational roles.

        The organizational roles are stored as a semi-structured list of
        activity groups, where each group associates a list of activities
        with a dictionary of originators and their corresponding
        importance scores.

        Returns:
            A list of dictionaries, where each dictionary
            contains the activities and their corresponding originators' importance
            scores.
            Each dictionary has the following structure:
            {
                "activities": List[str],    # List of activities in the role
                "originators_importance": Dict[str, float]
                    # Dictionary of originators and their importance scores
            }

        Raises:
            ValueError: If the organizational roles have not been calculated yet.
        """
        if self._organizational_roles is None:
            raise ValueError(
                "Organizational roles have not been calculated yet. "
                "Please call compute_organizational_roles() first."
            )
        structured_roles = [
            {
                "activities": role.activities,
                "originators_importance": role.originator_importance,
            }
            for role in self._organizational_roles
        ]
        return structured_roles

    # **************** Resource Profiles ****************

    def get_number_of_distinct_activities(
        self, start_time: str, end_time: str, resource: str
    ) -> int:
        """Calculates the number of distinct activities.

        Number of distinct activities done by a resource in a given time
        interval [t1, t2).

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the number of
                distinct activities.

        Returns:
            An integer indicating the number of distinct activities done by
            the resource in the given time interval.
        """
        return rp_algorithm.distinct_activities(
            self.log, start_time, end_time, resource
        )

    def get_activity_frequency(
        self, start_time: str, end_time: str, resource: str, activity: str
    ) -> float:
        """Calculates the activity frequency.

        Fraction of completions of a given activity a by a given
        resource r during a given time slot [t1, t2), with respect to
        the total number of activity completions by resource r during
        [t1, t2).

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the activity
                frequency.
            activity (str): The activity for which to calculate the frequency.

        Returns:
            A float indicating the activity frequency of the given activity
            by the resource in the given time interval.
        """
        return rp_algorithm.activity_frequency(
            self.log, start_time, end_time, resource, activity
        )

    def get_activity_completions(
        self, start_time: str, end_time: str, resource: str
    ) -> int:
        """Calculates the activity completions.

        The number of activity instances completed by a given resource
        during a given time slot.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the activity
                completions.

        Returns:
            An integer indicating the number of activity instances completed
            by the resource in the given time interval.
        """
        return rp_algorithm.activity_completions(
            self.log, start_time, end_time, resource
        )

    def get_case_completions(
        self, start_time: str, end_time: str, resource: str
    ) -> int:
        """Calculates the case completion.

        The number of cases completed during a given time slot in which
        a given resource was involved.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the case
                completions.

        Returns:
            An integer indicating the number of cases completed by the
            resource in the given time interval.
        """
        return rp_algorithm.case_completions(self.log, start_time, end_time, resource)

    def get_fraction_case_completions(
        self, start_time: str, end_time: str, resource: str
    ) -> float:
        """Calculates the fraction case completion.

        The fraction of cases completed during a given time slot in
        which a given resource was involved with respect to the total
        number of cases completed during the time slot.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the
                fraction case completions.

        Returns:
            A float indicating the fraction of cases completed by the
            resource in the given time interval.
        """
        return rp_algorithm.fraction_case_completions(
            self.log, start_time, end_time, resource
        )

    def get_average_workload(
        self, start_time: str, end_time: str, resource: str
    ) -> float:
        """Calculates the average workload.

        The average number of activities started by a given resource but
        not completed at a moment in time.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the average
                workload.

        Returns:
            A float indicating the average workload of the given resource
            in the given time interval.
        """
        return rp_algorithm.average_workload(self.log, start_time, end_time, resource)

    def get_multitasking(self, start_time: str, end_time: str, resource: str) -> float:
        """Calculates the multitasking.

        The fraction of active time during which a given resource is
        involved in more than one activity with respect to the
        resource's active time.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the
                multitasking.

        Returns:
            A float indicating the multitasking of the given resource
            in the given time interval.
        """
        return rp_algorithm.multitasking(self.log, start_time, end_time, resource)

    def get_average_activity_duration(
        self, start_time: str, end_time: str, resource: str, activity: str
    ) -> float:
        """Calculates the average activity duration.

        The average duration of instances of a given activity completed
        during a given time slot by a given resource.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the average
                activity duration.
            activity (str): The activity for which to calculate the average
                duration.

        Returns:
            A float indicating the average duration of the given activity
            by the resource in the given time interval.
        """
        return rp_algorithm.average_duration_activity(
            self.log, start_time, end_time, resource, activity
        )

    def get_average_case_duration(
        self, start_time: str, end_time: str, resource: str
    ) -> float:
        """Calculates the average case duration.

        The average duration of cases completed during a given time slot
        in which a given resource was involved.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the average
                case duration.

        Returns:
            A float indicating the average duration of cases completed
            by the resource in the given time interval.
        """
        return rp_algorithm.average_case_duration(
            self.log, start_time, end_time, resource
        )

    def get_interaction_two_resources(
        self, start_time: str, end_time: str, resource1: str, resource2: str
    ) -> float:
        """Calculates the interaction between two resources.

        The number of cases completed during a given time slot in which
        two given resources were involved.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource1 (str): The first resource for which to calculate the
                interaction.
            resource2 (str): The second resource for which to calculate the
                interaction.

        Returns:
            A float indicating the interaction between the two resources
            in the given time interval.
        """
        return float(
            rp_algorithm.interaction_two_resources(
                self.log, start_time, end_time, resource1, resource2
            )
        )

    def get_social_position(
        self, start_time: str, end_time: str, resource: str
    ) -> float:
        """Calculates the social position.

        The fraction of resources involved in the same cases with a
        given resource during a given time slot with respect to the
        total number of resources active during the time slot.

        Args:
            start_time (str): The start time of the interval.
            end_time (str): The end time of the interval.
            resource (str): The resource for which to calculate the
                social position.

        Returns:
            A float indicating the social position of the given resource
            in the given time interval.
        """
        return rp_algorithm.social_position(self.log, start_time, end_time, resource)

    # **************** Organizational Mining ****************

    def compute_organizational_diagnostics(self) -> None:
        """Calculates the organizational diagnostics.

        Provides the local diagnostics for the organizational model
        starting from a log object and considering the resource group
        specified by the attribute. It is stored in a dictionary where the keys are
        the names of the group-related metrics and the values are the
        corresponding diagnostic values.

        Raises:
            ValueError: If the resource column name is not provided.
        """
        if self.resource_col is None:
            raise ValueError(
                "Resource column name is not provided. "
                "Please provide a resource column name."
            )
        if self.group_col is None:
            raise ValueError(
                "Group column name is not provided. Please provide a group column name."
            )

        self._organizational_diagnostics = org_algorithm.apply_from_group_attribute(
            self.log,
            parameters={
                org_algorithm.Parameters.GROUP_KEY: self.group_col,
            },
        )

    def get_group_relative_focus(self) -> Dict[str, Dict[str, float]]:
        """Returns the Group Relative Focus metric.

         The Group Relative Focus metric specifies for a given work how
         much a resource group performed this type of work compared to
         the overall workload of the group. It can be used to measure how
         the workload of a resource group is distributed over different
         types of work, i.e., work diversification of the group.

        Returns:
            A dictionary where the keys are the names of the resources
            and the values are dictionaries containing activity names
            and the Group Relative Focus metric.

        Raises:
            ValueError: If the organizational diagnostics have not been
            calculated yet.
        """
        if self._organizational_diagnostics is None:
            raise ValueError(
                "Organizational diagnostics have not been calculated yet. "
                "Please call compute_organizational_diagnostics() first."
            )
        return self._organizational_diagnostics["group_relative_focus"]

    def get_group_relative_stake(self) -> Dict[str, Dict[str, float]]:
        """Returns the Group Relative Stake metric.

        The Group Relative Stake metric specifies for a given work how much
        this type of work was performed by a certain resource group among
        all groups. It can be used to measure how the workload devoted to
        a certain type of work is distributed over resource groups in an
        organizational model, i.e., work participation by different groups.

        Returns:
            A dictionary where the keys are the names of the resources and
            the values are dictionaries containing activity names and the
            Group Relative Stake metric.

        Raises:
            ValueError: If the organizational diagnostics have not been
            calculated yet.
        """
        if self._organizational_diagnostics is None:
            raise ValueError(
                "Organizational diagnostics have not been calculated yet. "
                "Please call compute_organizational_diagnostics() first."
            )
        return self._organizational_diagnostics["group_relative_stake"]

    def get_group_coverage(self) -> Dict[str, Dict[str, float]]:
        """Returns the Group Coverage metric.

        The Group Coverage metric with respect to a given type of work,
        specifies the proportion of members of a resource group that
        performed this type of work.

        Returns:
            A dictionary where the keys are the names of the resources
            and the values are dictionaries containing resources and the
            Group Coverage metric.

        Raises:
            ValueError: If the organizational diagnostics have not been
            calculated yet.
        """
        if self._organizational_diagnostics is None:
            raise ValueError(
                "Organizational diagnostics have not been calculated yet. "
                "Please call compute_organizational_diagnostics() first."
            )
        return self._organizational_diagnostics["group_coverage"]

    def get_group_member_contribution(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """Returns the Group Member Contribution metric.

        The Group Member Contribution metric of a member of a resource group
        with respect to a given type of work specifies how much of this type
        of work by the group was performed by the member. It can be used to
        measure how the workload of the entire group devoted to a certain
        type of work is distributed over the group members.

        Returns:
            A dictionary where the keys are the names of the resources and
            the values are dictionaries containing resources and the Group
            Member Contribution metric.

        Raises:
            ValueError: If the organizational diagnostics have not been
            calculated yet.
        """
        if self._organizational_diagnostics is None:
            raise ValueError(
                "Organizational diagnostics have not been calculated yet. "
                "Please call compute_organizational_diagnostics() first."
            )
        return self._organizational_diagnostics["group_member_contribution"]
