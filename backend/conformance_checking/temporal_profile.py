"""Contains functionality for temporal conformance checking.

This module defines the TemporalProfile class which uses PM4Py to
discover temporal profiles from event logs and checks conformance based
on the discovered temporal profiles.
"""

from typing import Dict, Optional, Tuple, List

import pandas as pd
from pm4py.algo.discovery.temporal_profile import algorithm as tp_discovery  # type: ignore
from pm4py.algo.conformance.temporal_profile import algorithm as tp_conformance  # type: ignore


class TemporalProfile:
    """Represents the temporal profile of an event log.

    Attributes:
        log: The event log.
        _temporal_profile: The temporal profile.
        case_id_col (optional): The name of the Case ID column. Only needed if
        the log is read as a csv file.
        activity_col (optional): The name of the Activity column. Only needed if
          the log is read as a csv file.
        timestamp_col (optional): The name of the Timestamp column. Only needed if
          the log is read as a csv file.
    """

    def __init__(
        self,
        log: pd.DataFrame,
        case_id_col: Optional[str] = None,
        activity_col: Optional[str] = None,
        timestamp_col: Optional[str] = None,
    ) -> None:
        """Initializes the TemporalProfile class with an event log.

        Args:
            log: The event log.
            case_id_col (optional): The name of the Case ID column. Defaults
              to None.
            activity_col (optional): The name of the Activity column. Defaults
              to None.
            timestamp_col (optional): The name of the Timestamp column. Defaults
              to None.
        """
        self.log: pd.DataFrame = log
        self._temporal_profile: Dict[Tuple[str, str], Tuple[float, float]]
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col

    def discover_temporal_profile(self) -> None:
        """Discovers the temporal profile from the event log."""
        self._temporal_profile = tp_discovery.apply(self.log)

    def check_temporal_conformance(
        self, zeta: float = 0.0
    ) -> List[List[Tuple[float, float, float, float]]]:
        """Check conformance of the log against the temporal profile.

        Args:
            zeta: Multiplier for the standard deviation.

        Returns:
            A list containing, for each trace, all the deviations. Each deviation is
            a tuple with four elements:
                1. The source activity of the recorded deviation.
                2. The target activity of the recorded deviation.
                3. The time passed between the occurrence of the source activity and the
                   target activity.
                4. The value of (time passed - mean)/std for this occurrence (zeta).
        """
        temporal_conformance_result = tp_conformance.apply(
            self.log, self._temporal_profile, parameters={"zeta": zeta}
        )
        return temporal_conformance_result
