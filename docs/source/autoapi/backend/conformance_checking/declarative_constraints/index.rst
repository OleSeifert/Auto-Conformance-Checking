backend.conformance_checking.declarative_constraints
====================================================

.. py:module:: backend.conformance_checking.declarative_constraints

.. autoapi-nested-parse::

   Contains functionality for declarative conformance checking.

   This module defines the DeclerativeConstraints class which uses PM4Py to
   discover declarative profiles from event logs and checks conformance
   based on the discovered declarative profiles.



Attributes
----------

.. autoapisummary::

   backend.conformance_checking.declarative_constraints.DeclareModelType
   backend.conformance_checking.declarative_constraints.ReturnGraphType


Classes
-------

.. autoapisummary::

   backend.conformance_checking.declarative_constraints.DeclarativeConstraints


Module Contents
---------------

.. py:type:: DeclareModelType
   :canonical: Dict[str, Dict[Any, Dict[str, int]]]


.. py:type:: ReturnGraphType
   :canonical: Dict[str, List[Dict[str, List[Union[str, Dict[str, str]]]]]]


.. py:class:: DeclarativeConstraints(log: pandas.DataFrame, min_support_ratio: Optional[float] = 0.3, min_confidence_ratio: Optional[float] = 0.75, case_id_col: Optional[str] = None, activity_col: Optional[str] = None, timestamp_col: Optional[str] = None)

   Represents the declarative constraints of an event log.

   Attributes :
       log: The main event log.
       min_support_ratio: The minimum support ratio for discovering rules.
       min_confidence_ratio: The minimum confidence ratio for discovering rules.


   .. py:attribute:: log


   .. py:attribute:: min_support_ratio
      :value: 0.3



   .. py:attribute:: min_confidence_ratio
      :value: 0.75



   .. py:attribute:: declare_model
      :type:  Optional[DeclareModelType]
      :value: None



   .. py:attribute:: case_id_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: activity_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: timestamp_col
      :type:  Optional[str]
      :value: None



   .. py:attribute:: valid_rules
      :value: ['existence', 'absence', 'exactly_one', 'init', 'responded_existence', 'coexistence',...



   .. py:attribute:: conf_results_memory
      :type:  Dict[str, None]


   .. py:method:: run_model(log: Optional[pandas.DataFrame] = None, min_support_ratio: Optional[float] = None, min_confidence_ratio: Optional[float] = None) -> None

      Runs the declarative model on the event log.

      It stores the result in memory.

      :param log: The event log to use.
      :param min_support_ratio: The minimum support ratio for discovering rules.
      :param min_confidence_ratio: The minimum confidence ratio for discovering rules.



   .. py:method:: rule_specific_violation_summary(declare_model: Optional[DeclareModelType] = None, log: Optional[pandas.DataFrame] = None, rule_name: Optional[str] = None, verbose: bool = False) -> ReturnGraphType

      Summarizes number of violations for a declarative rule.

      This function does not access memory variable, so it runs the rule from
      scratch even if results are pre-computed and stored.

      :param declare_model: The Declare model. If None, uses the default model.
      :param log: The event log. If None, uses the default log.
      :param rule_name: Name of the rule to check.
      :param verbose: Whether to print details for debugging.

      :returns: Summary with graph and table information of rule violations.

      :raises ValueError: If an unsupported rule name is provided.



   .. py:method:: get_declarative_conformance_diagnostics(rule_name: str, run_from_scratch: Optional[bool] = False) -> ReturnGraphType

      Gets conformance diagnostics for a specific declarative rule.

      Check for results stored in memory and runs conformance checking of any
      rule only if results previously not stored in memory.

      :param rule_name: The name of the declarative rule to analyze.
      :param run_from_scratch: If True, re-evaluates the rule even if results
                               stored.

      :returns: Cached or newly generated rule violation summary.

      :raises ValueError: If the rule name is not supported.



   .. py:method:: declarative_conformance_for_existence() -> ReturnGraphType

      Gets results for the existence rule.

      :returns: For existance rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_absence() -> ReturnGraphType

      Gets results for the absence rule.

      :returns: For absence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_exactly_one() -> ReturnGraphType

      Gets results for the exactly_one rule.

      :returns: For exactly_one rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_init() -> ReturnGraphType

      Gets results for the init rule.

      :returns: For init rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_responded_existence() -> ReturnGraphType

      Gets results for the responded existence rule.

      :returns: For responded existence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_coexistence() -> ReturnGraphType

      Gets results for the coexistence rule.

      :returns: For coexistence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_response() -> ReturnGraphType

      Gets results for the response rule.

      :returns: For response rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_precedence() -> ReturnGraphType

      Gets results for the precedence rule.

      :returns: For precedence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_succession() -> ReturnGraphType

      Gets results for the succession rule.

      :returns: For succession rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_altprecedence() -> ReturnGraphType

      Gets results for the altprecedence rule.

      :returns: For altprecedence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_altsuccession() -> ReturnGraphType

      Gets results for the altsuccession rule.

      :returns: For altsuccession rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_chainresponse() -> ReturnGraphType

      Gets results for the chainresponse rule.

      :returns: For chainresponse rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_chainprecedence() -> ReturnGraphType

      Gets results for the chainprecedence rule.

      :returns: For chainprecedence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_chainsuccession() -> ReturnGraphType

      Gets results for the chainsuccession rule.

      :returns: For chainsuccession rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_noncoexistence() -> ReturnGraphType

      Gets results for the noncoexistence rule.

      :returns: For noncoexistence rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_nonsuccession() -> ReturnGraphType

      Gets results for the nonsuccession rule.

      :returns: For nonsuccession rule.
      :rtype: Dict



   .. py:method:: declarative_conformance_for_nonchainsuccession() -> ReturnGraphType

      Gets results for the nonchainsuccession rule.

      :returns: For nonchainsuccession rule.
      :rtype: Dict



   .. py:method:: run_all_rules(list_of_rules: Optional[List[str]] = None, run_from_scratch: Optional[bool] = False) -> Any

      Runs conformance checking for all rules.

      It stores results in memory.
      Useful for poling when all rules need to be pre-computed in the background.

      :param list_of_rules: List of rule names to check. If None, runs for all
                            valid rules.
      :param run_from_scratch: If True, re-evaluates all rules even if results
                               stored.

      :returns: Dictionary of all violations.



