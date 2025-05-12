"""Contains the resource-based conformance checking part.

The implementation is based on PM4Py.
"""

from typing import Optional

import pandas as pd


class ResourceBased:
    """The ResourceBased class.

    It is used for resource-based conformance checking.

    Attributes:
        log: The event log as a pandas DataFrame.
        resource_col: The name of the resource column.
    """

    def __init__(self, log: pd.DataFrame, resource_col: Optional[str] = None) -> None:
        """Initializes the ResourceBased class.

        Args:
            log: The event log as a pandas DataFrame.
            resource_col (optional): The name of the resource column. Defaults
              to None.
        """
        self.log = log
        self.resource_col = resource_col  # not sure if needed

    # **************** Social Network Analysis ****************

    def get_handover_of_work(self):
        """Calculates the handover of work.

        The Handover of Work metric measures how many times an
        individual is followed by another individual in the execution of
        a business process.
        """
        pass

    def get_subcontracting(self):
        """Calculates the subcontracting.

        The subcontracting metric calculates how many times the work of
        an individual is interleaved by the work of another individual,
        only to eventually “return” to the original individual.
        """
        pass

    def get_working_together(self):
        """Calculates the working together.

        The Working Together metric calculates how many times two
        individuals work together to resolve a process instance.
        """
        pass

    def get_similar_activities(self):
        """Calculates the similar activities.

        The Similar Activities metric calculates how similar the work
        patterns are between two individuals.
        """
        pass

    # **************** Role Discovery ****************

    def get_organizational_roles(self):
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
        """
        pass

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
