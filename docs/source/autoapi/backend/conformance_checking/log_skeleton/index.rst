backend.conformance_checking.log_skeleton
=========================================

.. py:module:: backend.conformance_checking.log_skeleton

.. autoapi-nested-parse::

   Contains the LogSkeleton class.

   This module is used to create a log skeleton from a given event log and
   to compute various metrics related to the log skeleton.



Classes
-------

.. autoapisummary::

   backend.conformance_checking.log_skeleton.LogSkeleton


Module Contents
---------------

.. py:class:: LogSkeleton(log: pandas.DataFrame, case_id_col: Optional[str] = None, activity_col: Optional[str] = None, timestamp_col: Optional[str] = None)

   Represents a log skeleton.

   .. attribute:: log

      The event log.

   .. attribute:: _skeleton

      The log skeleton.

   .. attribute:: case_id_col

      The name of the case ID column. Only needed if
      the log is read as csv file.

      :type: optional

   .. attribute:: activity_col

      The name of the activity column. Only needed if
      the log is read as csv file.

      :type: optional

   .. attribute:: timestamp_col

      The name of the timestamp column. Only needed if
      the log is read as csv file.

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



   .. py:method:: compute_skeleton(noise_thr: float = 0.0) -> None

      Computes the log skeleton.

      :param noise_thr: The noise threshold. Value between 0 and 1.



   .. py:method:: check_conformance_traces(traces: pandas.DataFrame) -> List[Set[Any]]

      Computes the conformance of traces with the log skeleton.

      :param traces: A DataFrame containing the traces to be checked.

      :returns: A list of sets containing the results of the conformance. The
                conformance checking results for each trace include:
                - Outputs.IS_FIT: boolean that tells if the trace is perfectly
                  fit according to the model.
                - Outputs.DEV_FITNESS: deviation based fitness (between 0 and 1;
                    the more the trace is near to 1 the more fit is).
                - Outputs.DEVIATIONS: list of deviations in the model.



   .. py:method:: get_equivalence_relation() -> Set[Tuple[str, str]]

      Returns the equivalence relation of the log skeleton.

      :returns: A set of tuples representing two activities that are equivalent.



   .. py:method:: get_always_after_relation() -> Set[Tuple[str, str]]

      Returns the always after relation of the log skeleton.

      :returns: A set of tuples representing two activities where the first
                activity always happens before the second activity.



   .. py:method:: get_always_before_relation() -> Set[Tuple[str, str]]

      Returns the always before relation of the log skeleton.

      :returns: A set of tuples representing two activities where the first
                activity always happens after the second activity.



   .. py:method:: get_never_together_relation() -> Set[Tuple[str, str]]

      Returns the never together relation of the log skeleton.

      :returns: A set of tuples representing two activities that never happen
                together.



   .. py:method:: get_activity_frequencies() -> Dict[str, Set[int]]

      Returns the activity frequencies.

      For each activity, it returns the number of possible occurences per
      trace.

      :returns: A dictionary where the keys are the activities and the values
                are sets of integers representing the number of possible
                occurences per trace.



   .. py:method:: get_skeleton() -> Dict[str, Any]

      Returns the log skeleton.

      :returns: The log skeleton.



