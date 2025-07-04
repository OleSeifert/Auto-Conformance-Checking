backend.conformance_checking.temporal_profile
=============================================

.. py:module:: backend.conformance_checking.temporal_profile

.. autoapi-nested-parse::

   Contains functionality for temporal conformance checking.

   This module defines the TemporalProfile class which uses PM4Py to
   discover temporal profiles from event logs and checks conformance based
   on the discovered temporal profiles.



Attributes
----------

.. autoapisummary::

   backend.conformance_checking.temporal_profile.TemporalProfileType
   backend.conformance_checking.temporal_profile.ConformanceResultType


Classes
-------

.. autoapisummary::

   backend.conformance_checking.temporal_profile.TemporalProfile


Module Contents
---------------

.. py:type:: TemporalProfileType
   :canonical: Dict[Tuple[str, str], Tuple[float, float]]


.. py:type:: ConformanceResultType
   :canonical: List[List[Tuple[Any, ...]]]


.. py:class:: TemporalProfile(log: pandas.DataFrame, case_id_col: Optional[str] = None, activity_col: Optional[str] = None, timestamp_col: Optional[str] = None)

   Represents the temporal profile of an event log.

   .. attribute:: log

      The event log.

   .. attribute:: _temporal_profile

      The discovered temporal profile.

   .. attribute:: _temporal_conformance_result

      The result of temporal conformance checking.

   .. attribute:: _zeta

      The zeta value used for temporal conformance checking.

   .. attribute:: case_id_col

      The name of the Case ID column. Only needed if

      :type: optional

   .. attribute:: the log is read as a csv file.



   .. attribute:: activity_col

      The name of the Activity column. Only needed if
      the log is read as a csv file.

      :type: optional

   .. attribute:: timestamp_col

      The name of the Timestamp column. Only needed if
      the log is read as a csv file.

      :type: optional


   .. py:attribute:: log
      :type:  pandas.DataFrame


   .. py:attribute:: case_id_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: activity_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: timestamp_col
      :type:  Optional[str]
      :value: None



   .. py:method:: discover_temporal_profile() -> None

      Discovers the temporal profile from the log.

      The result is stored in _temporal_profile which is a dictionary
      where each key is a tuple of two activity names (source, target),
      and the value is a tuple containing:
          1. The mean duration between the two activities
          2. The standard deviation of those durations.



   .. py:method:: check_temporal_conformance(zeta: float = 0.5) -> None

      Checks conformance of the log against the temporal profile.

      The result is stored in _temporal_conformance_result which is a list containing,
      for each trace, all the deviations. Each deviation is a tuple containing:
          1. The source activity of the recorded deviation.
          2. The target activity of the recorded deviation.
          3. The time passed between the occurrence of the source activity and the
              target activity.
          4. The value of (time passed - mean)/std for this occurrence (zeta).

      :param zeta: Multiplier for the standard deviation.

      :raises ValueError: If the temporal profile has not been discovered yet.



   .. py:method:: get_temporal_profile() -> TemporalProfileType

      Returns the discovered temporal profile.

      :returns: A dictionary where each key is a tuple of two activity names (source, target),
                and the value is a tuple containing:
                    1. The mean duration between the two activities
                    2. The standard deviation of those durations.

      :raises ValueError: If the temporal profile has not been discovered yet.



   .. py:method:: get_temporal_conformance_result() -> ConformanceResultType

      Returns the result of temporal conformance checking.

      :returns:     1. The source activity of the recorded deviation.
                    2. The target activity of the recorded deviation.
                    3. The time passed between the occurrence of the source activity and the
                       target activity.
                    4. The value of (time passed - mean)/std for this occurrence (zeta).
      :rtype: A list containing, for each trace, all the deviations. Each deviation is a tuple containing

      :raises ValueError: If the temporal conformance result has not been computed yet.



   .. py:method:: get_zeta() -> Optional[float]

      Returns the zeta value used for temporal conformance checking.

      :returns: The zeta value used for temporal conformance checking.



   .. py:method:: get_conformance_diagnostics() -> pandas.DataFrame

      Returns the result of temporal conformance checking as a DataFrame.

      :returns:     1. The Case ID of the recorded deviation.
                    2. The source activity of the recorded deviation.
                    3. The target activity of the recorded deviation.
                    4. The time passed between the occurrence of the source activity and the
                       target activity.
                    5. The value of (time passed - mean)/std for this occurrence (zeta).
      :rtype: A DataFrame containing the deviations for each trace. Each row contains

      :raises ValueError: If the temporal conformance result has not been computed yet.



   .. py:method:: get_sorted_coloured_diagnostics() -> pandas.io.formats.style.Styler

      Returns the diagnostics DataFrame with sorting and styling.

      Sorts the diagnostics DataFrame in descending order of the number of standard deviations (num_st_devs)
      and applies a colour-coded strip to the rows based on the value of num_st_devs - zeta:
          - Green: If the value is less than 0.5
          - Yellow: If the value is between 0.5 and 1.0
          - Red: If the value is greater than 1.0

      :returns: A styled DataFrame containing the sorted diagnostics with colour-coding.



