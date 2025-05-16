"""Contains functionality for resource-based conformance checking.

This module defines the ResourceBased class which uses PM4Py to discover
resource-based conformance checking metrics from event logs.
"""

from typing import Any, Dict, List, Optional, Protocol, Tuple, TypeAlias

import numpy as np
import pandas as pd
import pm4py  # type: ignore

HandoverOfWorkType: TypeAlias = Dict[Tuple[str, str], float]
SubcontractingType: TypeAlias = Dict[Tuple[str, str], float]
WorkingTogetherType: TypeAlias = Dict[Tuple[str, str], float]
SimilarActivitiesType: TypeAlias = Dict[Tuple[str, str], np.float64]


class SNAProtocol(Protocol):
    """Protocol for Social Network Analysis (SNA) metrics.

    This protocol defines the structure of SNA metrics used in the
    ResourceBased class. It includes attributes for the connections and
    whether the metric is directed.
    """

    connections: Dict[Tuple[str, str], Any]
    is_directed: bool


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
    """

    def __init__(
        self,
        log: pd.DataFrame,
        case_id_col: Optional[str] = None,
        activity_col: Optional[str] = None,
        timestamp_col: Optional[str] = None,
        resource_col: Optional[str] = None,
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
        """
        self.log = log
        self._handover_of_work: Optional[SNAProtocol] = None
        self._subcontracting: Optional[SNAProtocol] = None
        self._working_together: Optional[SNAProtocol] = None
        self._similar_activities: Optional[SNAProtocol] = None
        self._organizational_roles: Optional[List[Any]] = None
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col
        self.resource_col: Optional[str] = resource_col

    # **************** Social Network Analysis ****************

    def compute_handover_of_work(self) -> None:
        """Calculates the Handover of Work metric.

        The Handover of Work metric measures how many times an
        individual is followed by another individual in the execution of
        a business process. It is stored in a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the first individual is followed by the second individual
        in the execution of a business process.

        Returns:
            None.
        """
        self._handover_of_work = pm4py.discover_handover_of_work_network(self.log)

    def get_handover_of_work_values(self) -> HandoverOfWorkType:
        """Returns the Handover of Work metric.

        The Handover of Work metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the first individual is followed by the second individual
        in the execution of a business process.

        Returns:
            HandoverOfWorkType: The Handover of Work metric.

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
            bool: True if the Handover of Work metric is directed, False otherwise.
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
        only to eventually “return” to the original individual. It is stored
        in a dictionary where the keys are tuples of two individuals and
        the values are the number of times the first individual is  interleaved
        by the second individual in the execution of a business process.

        Returns:
            None.
        """
        self._subcontracting = pm4py.discover_subcontracting_network(self.log)

    def get_subcontracting_values(self) -> SubcontractingType:
        """Returns the Subcontracting metric.

        The Subcontracting metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the first individual is interleaved by the second individual
        in the execution of a business process.

        Returns:
            SubcontractingType: The Subcontracting metric.

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
            bool: True if the Subcontracting metric is directed, False otherwise.

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
        individuals work together to resolve a process instance. It is stored
        in a dictionary where the keys are tuples of two individuals and
        the values are the number of times the two individuals worked
        together to resolve a process instance.

        Returns:
            None.
        """
        self._working_together = pm4py.discover_working_together_network(self.log)

    def get_working_together_values(self) -> WorkingTogetherType:
        """Returns the Working Together metric.

        The Working Together metric is a dictionary where the keys are
        tuples of two individuals and the values are the number of times
        the two individuals worked together to resolve a process instance.

        Returns:
            WorkingTogetherType: The Working Together metric.

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
            bool: True if the Working Together metric is directed, False otherwise.

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
        patterns are between two individuals. It is stored in a dictionary
        where the keys are tuples of two individuals and the values are the
        similarity score between the two individuals.

        Returns:
            None.
        """
        self._similar_activities = pm4py.discover_activity_based_resource_similarity(
            self.log
        )

    def get_similar_activities_values(self) -> SimilarActivitiesType:
        """Returns the Similar Activities metric.

        The Similar Activities metric is a dictionary where the keys are
        tuples of two individuals and the values are the similarity score
        between the two individuals.

        Returns:
            SimilarActivitiesType: The Similar Activities metric.

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
            bool: True if the Similar Activities metric is directed, False otherwise.

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

        Returns:
            None
        """
        self._organizational_roles = pm4py.discover_organizational_roles(self.log)

    def get_organizational_roles(self) -> List[Dict[str, Any]]:
        """Returns the organizational roles.

        The organizational roles are stored as a semi-structured list of
        activity groups, where each group associates a list of activities
        with a dictionary of originators and their corresponding
        importance scores.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary
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

    def get_number_of_distinct_activities(self):
        """Calculates the number of distinct activities.

        Number of distinct activities done by a resource in a given time
        interval [t1, t2).
        """
        pass

    def get_activity_frequency(self):
        """Calculates the activity frequency.

        Fraction of completions of a given activity a by a given
        resource r during a given time slot [t1, t2), with respect to
        the total number of activity completions by resource r during
        [t1, t2).
        """
        pass

    def get_activity_completions(self):
        """Calculates the activity completions.

        The number of activity instances completed by a given resource
        during a given time slot.
        """
        pass

    def get_case_completions(self):
        """Calculates the case completion.

        The number of cases completed during a given time slot in which
        a given resource was involved.
        """
        pass

    def get_fraction_case_completion(self):
        """Calculates the fraction case completion.

        The fraction of cases completed during a given time slot in
        which a given resource was involved with respect to the total
        number of cases completed during the time slot.
        """
        pass

    def get_average_workload(self):
        """Calculates the average workload.

        The average number of activities started by a given resource but
        not completed at a moment in time.
        """
        pass

    def get_multitasking(self):
        """Calculates the multitasking.

        The fraction of active time during which a given resource is
        involved in more than one activity with respect to the
        resource's active time.
        """
        pass

    def get_average_activity_duration(self):
        """Calculates the average activity duration.

        The average duration of instances of a given activity completed
        during a given time slot by a given resource.
        """
        pass

    def get_average_case_duration(self):
        """Calculates the average case duration.

        The average duration of cases completed during a given time slot
        in which a given resource was involved.
        """
        pass

    def get_interaction_two_resources(self):
        """Calculates the interaction between two resources.

        The number of cases completed during a given time slot in which
        two given resources were involved.
        """
        pass

    def get_social_position(self):
        """Calculates the social position.

        The fraction of resources involved in the same cases with a
        given resource during a given time slot with respect to the
        total number of resources active during the time slot.
        """
        pass

    # **************** Organizational Mining ****************

    # TODO: Figure out how to implement this and if this is suitable for our purposes
