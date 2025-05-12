"""Contains functionality for temporal conformance checking.

This module defines the TemporalProfile class which uses PM4Py to
discover temporal profiles from event logs and checks conformance based
on the discovered temporal profiles.
"""

from typing import Dict, List, Optional, Tuple, TypeAlias

import pandas as pd
from pandas.io.formats.style import Styler
from pm4py.algo.conformance.temporal_profile import algorithm as tp_conformance  # type: ignore
from pm4py.algo.discovery.temporal_profile import algorithm as tp_discovery  # type: ignore

TemporalProfileType: TypeAlias = Dict[Tuple[str, str], Tuple[float, float]]
ConformanceResultType: TypeAlias = List[List[Tuple[float, float, float, float]]]


class TemporalProfile:
    """Represents the temporal profile of an event log.

    Attributes:
        log: The event log.
        _temporal_profile: The discovered temporal profile.
        _temporal_conformance_result: The result of temporal conformance checking.
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
        self._temporal_profile: Optional[TemporalProfileType] = None
        self._temporal_conformance_result: Optional[ConformanceResultType] = None
        self._zeta: Optional[float] = None
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col

    def discover_temporal_profile(self) -> None:
        """Discovers the temporal profile from the log.

        The result is stored in _temporal_profile which is a dictionary
        where each key is a tuple of two activity names (source, target),
        and the value is a tuple containing:
            1. The mean duration between the two activities
            2. The standard deviation of those durations.

        Returns:
            None.
        """
        self._temporal_profile = tp_discovery.apply(self.log)

    def check_temporal_conformance(self, zeta: float = 0.5) -> None:
        """Checks conformance of the log against the temporal profile.

        The result is stored in _temporal_conformance_result which is a list containing,
        for each trace, all the deviations. Each deviation is a tuple containing:
            1. The source activity of the recorded deviation.
            2. The target activity of the recorded deviation.
            3. The time passed between the occurrence of the source activity and the
                target activity.
            4. The value of (time passed - mean)/std for this occurrence (zeta).

        Args:
            zeta: Multiplier for the standard deviation.

        Returns:
            None.

        Raises:
            ValueError: If the temporal profile has not been discovered yet.
        """
        if not self._temporal_profile:
            raise ValueError(
                "Temporal Profile not discovered. Please run discover_temporal_profile() first."
            )
        self._zeta = zeta
        self._temporal_conformance_result = tp_conformance.apply(
            self.log, self._temporal_profile, parameters={"zeta": zeta}
        )

    def get_temporal_profile(self) -> TemporalProfileType:
        """Returns the discovered temporal profile.

        Returns:
            A dictionary where each key is a tuple of two activity names (source, target),
            and the value is a tuple containing:
                1. The mean duration between the two activities
                2. The standard deviation of those durations.

        Raises:
            ValueError: If the temporal profile has not been discovered yet.
        """
        if not self._temporal_profile:
            raise ValueError(
                "Temporal Profile not discovered. Please run discover_temporal_profile() first."
            )
        return self._temporal_profile

    def get_temporal_conformance_result(self) -> ConformanceResultType:
        """Returns the result of temporal conformance checking.

        Returns:
            A list containing, for each trace, all the deviations. Each deviation is a tuple containing:
                1. The source activity of the recorded deviation.
                2. The target activity of the recorded deviation.
                3. The time passed between the occurrence of the source activity and the
                   target activity.
                4. The value of (time passed - mean)/std for this occurrence (zeta).

        Raises:
            ValueError: If the temporal conformance result has not been computed yet.
        """
        if not self._temporal_conformance_result:
            raise ValueError(
                "Temporal Conformance Result not computed. Please run check_temporal_conformance() first."
            )
        return self._temporal_conformance_result

    def get_zeta(self) -> Optional[float]:
        """Returns the zeta value used for temporal conformance checking.

        Returns:
            The zeta value used for temporal conformance checking.
        """
        if self._zeta is None:
            raise ValueError(
                "Zeta value not set. Please run check_temporal_conformance() first."
            )
        return self._zeta

    def get_conformance_diagnostics(self) -> pd.DataFrame:
        """Returns the result of temporal conformance checking as a DataFrame.

        Returns:
            A DataFrame containing the deviations for each trace. Each row contains:
                1. The Case ID of the recorded deviation.
                2. The source activity of the recorded deviation.
                3. The target activity of the recorded deviation.
                4. The time passed between the occurrence of the source activity and the
                   target activity.
                5. The value of (time passed - mean)/std for this occurrence (zeta).

        Raises:
            ValueError: If the temporal conformance result has not been computed yet.
        """
        if not self._temporal_conformance_result:
            raise ValueError(
                "Temporal Conformance Result not computed. Please run check_temporal_conformance() first."
            )
        diagnostics_dataframe = tp_conformance.get_diagnostics_dataframe(
            self.log, self._temporal_conformance_result
        )
        return diagnostics_dataframe

    def get_sorted_coloured_diagnostics(self) -> Styler:
        """Returns the diagnostics DataFrame with sorting and styling.

        Sorts the diagnostics DataFrame in descending order of the number of standard deviations (num_st_devs)
        and applies a colour-coded strip to the rows based on the value of num_st_devs - zeta:
            - Green: If the value is less than 0.5
            - Yellow: If the value is between 0.5 and 1.0
            - Red: If the value is greater than 1.0

        Returns:
            pd.io.formats.style.Styler: A styled DataFrame containing the sorted diagnostics with colour-coding.
        """
        diagnostics_dataframe = self.get_conformance_diagnostics()
        sorted_diagnostics = diagnostics_dataframe.sort_values(  # type: ignore
            by=["num_st_devs"], ascending=False
        )

        def apply_color_strip(row):  # type: ignore
            diff = row["num_st_devs"] - self._zeta  # type: ignore
            strip_color = "green" if diff < 0.5 else "yellow" if diff < 1.0 else "red"
            return [f"border-left: 5px solid {strip_color};"] + [""] * (len(row) - 1)  # type: ignore

        return sorted_diagnostics.style.apply(apply_color_strip, axis=1)  # type: ignore
