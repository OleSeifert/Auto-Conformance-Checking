"""Contains the LogSkeleton class.

This module is used to create a log skeleton from a given event log and
to compute various metrics related to the log skeleton.
"""

from typing import Any, Dict, List, Optional, Set, Tuple

import pandas as pd
from pm4py.algo.conformance.log_skeleton import algorithm as lsk_conf  # type: ignore
from pm4py.algo.discovery.log_skeleton import algorithm as lsk_discovery  # type: ignore


class LogSkeleton:
    """Represents a log skeleton.

    Attributes:
        log: The event log.
        _skeleton: The log skeleton.
        case_id_col (optional): The name of the case ID column. Only needed if
          the log is read as csv file.
        activity_col (optional): The name of the activity column. Only needed if
          the log is read as csv file.
        timestamp_col (optional): The name of the timestamp column. Only needed if
          the log is read as csv file.
    """

    def __init__(
        self,
        log: pd.DataFrame,
        case_id_col: Optional[str] = None,
        activity_col: Optional[str] = None,
        timestamp_col: Optional[str] = None,
    ) -> None:
        """Initializes the LogSkeleton class.

        Args:
            log: The event log.
            case_id_col (optional): The name of the case ID column. Defaults
              to None.
            activity_col (optional): The name of the activity column. Defaults
              to None.
            timestamp_col (optional): The name of the timestamp column. Defaults
              to None.
        """
        self.log: pd.DataFrame = log
        self._skeleton: Dict[str, Any]
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col

    # **************** Compute log skeleton and conformance for traces ****************

    def compute_skeleton(self, noise_thr: float = 0.0) -> None:
        """Computes the log skeleton.

        Args:
            noise_thr: The noise threshold. Value between 0 and 1.
        """
        self._skeleton = lsk_discovery.apply(
            self.log,
            parameters={
                lsk_discovery.Variants.CLASSIC.value.Parameters.NOISE_THRESHOLD: noise_thr,
            },
        )

    def check_conformance_traces(self, traces: pd.DataFrame) -> List[Set[Any]]:
        """Computes the conformance of traces with the log skeleton.

        Args:
            traces: A DataFrame containing the traces to be checked.

        Returns:
            A list of sets containing the results of the conformance. The
            conformance checking results for each trace include:
            - Outputs.IS_FIT: boolean that tells if the trace is perfectly
              fit according to the model.
            - Outputs.DEV_FITNESS: deviation based fitness (between 0 and 1;
                the more the trace is near to 1 the more fit is).
            - Outputs.DEVIATIONS: list of deviations in the model.
        """
        conf_result = lsk_conf.apply(traces, self._skeleton)
        return conf_result

    # **************** Getters for attributes of log skeleton ****************

    def get_equivalence_relation(self) -> Set[Tuple[str, str]]:
        """Returns the equivalence relation of the log skeleton.

        Returns:
            A set of tuples representing two activities that are equivalent.
        """
        return self._skeleton["equivalence"]

    def get_always_after_relation(self) -> Set[Tuple[str, str]]:
        """Returns the always after relation of the log skeleton.

        Returns:
            A set of tuples representing two activities where the first
            activity always happens before the second activity.
        """
        return self._skeleton["always_after"]

    def get_always_before_relation(self) -> Set[Tuple[str, str]]:
        """Returns the always before relation of the log skeleton.

        Returns:
            A set of tuples representing two activities where the first
            activity always happens after the second activity.
        """
        return self._skeleton["always_before"]

    def get_never_together_relation(self) -> Set[Tuple[str, str]]:
        """Returns the never together relation of the log skeleton.

        Returns:
            A set of tuples representing two activities that never happen
            together.
        """
        return self._skeleton["never_together"]

    def get_activity_frequencies(self) -> Dict[str, Set[int]]:
        """Returns the activity frequencies.

        For each activity, it returns the number of possible occurences per
        trace.

        Returns:
            A dictionary where the keys are the activities and the values
            are sets of integers representing the number of possible
            occurences per trace.
        """
        return self._skeleton["activ_freq"]

    def get_skeleton(self) -> Dict[str, Any]:
        """Returns the log skeleton.

        Returns:
            The log skeleton.
        """
        return self._skeleton
