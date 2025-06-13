"""Contains functionality for declarative conformance checking.

This module defines the DeclerativeConstraints class which uses PM4Py to
discover declarative profiles from event logs and checks conformance
based on the discovered declarative profiles.
"""

from typing import Any, Dict, List, Optional, TypeAlias, Union

import pandas as pd  # type: ignore
import pm4py  # type: ignore
from pm4py.algo.conformance.declare import algorithm as decl_conf  # type: ignore

# **************** Type Aliases ****************

DeclareModelType: TypeAlias = Dict[str, Dict[Any, Dict[str, int]]]

TableType: TypeAlias = Dict[str, Union[List[str], List[List[str]]]]
GraphType: TypeAlias = Dict[str, List[Dict[str, str]]]
ReturnGraphType: TypeAlias = Dict[str, Union[List[TableType], List[GraphType]]]


class DeclarativeConstraints:
    """Represents the declarative constraints of an event log.

    Attributes :
        log: The main event log.
        min_support_ratio: The minimum support ratio for discovering rules.
        min_confidence_ratio: The minimum confidence ratio for discovering rules.
    """

    def __init__(
        self,
        log: pd.DataFrame,
        min_support_ratio: Optional[float] = 0.3,
        min_confidence_ratio: Optional[float] = 0.75,
        case_id_col: Optional[str] = None,
        activity_col: Optional[str] = None,
        timestamp_col: Optional[str] = None,
    ) -> None:
        """Initializes the DeclarativeConstraints class with an event log.

        Also defines the model and the memory for all results.

        Args:
            log: The main event log.
            min_support_ratio: The minimum support ratio for discovering rules.
              Defaults to 0.3.
            min_confidence_ratio: The minimum confidence ratio for discovering rules.
              Defaults to 0.75.
            case_id_col : The name of the column containing case IDs.
            activity_col : The name of the column containing activity names.
            timestamp_col : The name of the column containing timestamps.
        """
        self.log = log
        self.min_support_ratio = min_support_ratio
        self.min_confidence_ratio = min_confidence_ratio
        self.declare_model: Optional[DeclareModelType] = None
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col
        self.valid_rules = list({
            "Existence" : "existance", 
            "Never" : "absence", 
            "Exactly Once" : "exactly_one", 
            "Initially" : "init", 
            "Responded Existence" : "responded_existence",
            "Co-Existence" : "coexistence",
            "Always After" : "response",
            "Always Before" : "precedence",
            "Succession" : "succession",
            "Alternate Precedence" : "altprecedence",
            "Alternate Succession" : "altsuccession",
            "Immediately After" : "chainresponse",
            "Immediately Before" : "chainprecedence",
            "Chain Succession" : "chainsuccession",
            "Non Co-Existence" : "noncoexistence",
            "Not Succession" : "nonsuccession",
            "Not Chain Succession" : "nonchainsuccession",
        }.values())
        self.conf_results_memory: Dict[str, None] = {
            rule: None for rule in self.valid_rules
        }

    # ************************* Running Model *************************

    def run_model(
        self,
        log: Optional[pd.DataFrame] = None,
        min_support_ratio: Optional[float] = None,
        min_confidence_ratio: Optional[float] = None,
    ) -> None:
        """Runs the declarative model on the event log.

        It stores the result in memory.

        Args:
            log: The event log to use.
            min_support_ratio: The minimum support ratio for discovering rules.
            min_confidence_ratio: The minimum confidence ratio for discovering rules.
        """
        if log is None:
            log = self.log
        if min_support_ratio is None:
            min_support_ratio = self.min_support_ratio
        if min_confidence_ratio is None:
            min_confidence_ratio = self.min_confidence_ratio
        self.declare_model = pm4py.discover_declare(  # type: ignore
            log,
            min_support_ratio=min_support_ratio,
            min_confidence_ratio=min_confidence_ratio,
        )
        self.conf_results_memory = {rule: None for rule in self.valid_rules}

    # ************************* Getting Violations & Graphs Data *************************

    def rule_specific_violation_summary(
        self,
        declare_model: Optional[DeclareModelType] = None,
        log: Optional[pd.DataFrame] = None,
        rule_name: Optional[str] = None,
        verbose: bool = False,
    ) -> ReturnGraphType:
        """Summarizes number of violations for a declarative rule.

        This function does not access memory variable, so it runs the rule from
        scratch even if results are pre-computed and stored.

        Args:
            declare_model: The Declare model. If None, uses the default model.
            log: The event log. If None, uses the default log.
            rule_name: Name of the rule to check.
            verbose: Whether to print details for debugging.

        Returns:
            Summary with graph and table information of rule violations.

        Raises:
            ValueError: If an unsupported rule name is provided.
        """
        if self.declare_model is None:
            self.run_model()
        if declare_model is None:
            declare_model = self.declare_model
        if log is None:
            log = self.log

        if str(rule_name) not in self.valid_rules:
            raise ValueError(
                f"Unsupported rule: '{rule_name}'. Must be one of: {self.valid_rules}"
            )

        if declare_model is None:
            raise ValueError("Declare model is stil None. Something has gone wrong.")
        rule_dict: Dict[str, Dict[str, int]] = (
            declare_model[rule_name] if rule_name in declare_model else {}
        )

        graph_nodes: List[Dict[str, str]] = []
        graph_edges: List[Dict[str, str]] = []
        table_rows: List[str] = []
        table_headers: List[str] = []
        output: ReturnGraphType = {"graphs": [], "tables": []}

        try:
            for rule_key, rule_info in rule_dict.items():
                if isinstance(rule_key, tuple):
                    A, B = rule_key  # type: ignore
                else:
                    A, B = rule_key, None  # type: ignore
                diagnostics = decl_conf.apply(log, {rule_name: {(A, B): rule_info}})  # type: ignore
                violated = [d for d in diagnostics if d["dev_fitness"] < 1.0]  # type: ignore
                violation_count = len(violated)  # type: ignore

                if violation_count > 0:
                    if rule_name not in ["existence", "absence", "init", "exactly_one"]:
                        table_headers = [
                            "First Activity",
                            "Second Activity",
                            "# Violations",
                        ]
                        graph_nodes.append(A)  # type: ignore
                        graph_nodes.append(B)  # type: ignore
                        graph_edges.append(
                            {"from": A, "to": B, "label": str(violation_count)}  # type: ignore
                        )
                        table_rows.append([A, B, str(violation_count)])  # type: ignore
                    else:
                        table_headers = ["Activity", "# Violations"]
                        table_rows.append([A, str(violation_count)])  # type: ignore
            graph_nodes = [{"id": node} for node in list(set(list(graph_nodes)))]  # type: ignore

            if table_headers != []:
                output["tables"] = [{"headers": table_headers, "rows": table_rows}]  # type: ignore
            if len(graph_nodes) > 0 and len(graph_edges) > 0:
                output["graphs"] = [{"nodes": graph_nodes, "edges": graph_edges}]  # type: ignore
            return output

        except Exception as e:
            if verbose:
                print(f"Error processing rule '{rule_name}': {e}")
            return {}

    def get_declarative_conformance_diagnostics(
        self, rule_name: str, run_from_scratch: Optional[bool] = False
    ) -> ReturnGraphType:
        """Gets conformance diagnostics for a specific declarative rule.

        Check for results stored in memory and runs conformance checking of any
        rule only if results previously not stored in memory.

        Args:
            rule_name: The name of the declarative rule to analyze.
            run_from_scratch: If True, re-evaluates the rule even if results
              stored.

        Returns:
            Cached or newly generated rule violation summary.

        Raises:
            ValueError: If the rule name is not supported.
        """
        rule_name = str(rule_name).lower()
        if rule_name not in self.valid_rules:
            raise ValueError(f"Unsupported rule: '{rule_name}'")
        if (self.conf_results_memory[rule_name] is None) or (run_from_scratch is True):
            self.conf_results_memory[rule_name] = self.rule_specific_violation_summary(  # type: ignore
                declare_model=self.declare_model, log=self.log, rule_name=rule_name
            )
        if self.conf_results_memory[rule_name] is None:
            raise ValueError(
                f"Conformance results for rule '{rule_name}' are still None. "
                "Something has gone wrong."
            )
        return self.conf_results_memory[rule_name]  # type: ignore

    # ************************* Getting Violations for All/Each Rule *************************

    def declarative_conformance_for_existence(self) -> ReturnGraphType:
        """Gets results for the existence rule.

        Returns:
            Dict: For existance rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="existence")

    def declarative_conformance_for_absence(self) -> ReturnGraphType:
        """Gets results for the absence rule.

        Returns:
            Dict: For absence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="absence")

    def declarative_conformance_for_exactly_one(self) -> ReturnGraphType:
        """Gets results for the exactly_one rule.

        Returns:
            Dict: For exactly_one rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="exactly_one")

    def declarative_conformance_for_init(self) -> ReturnGraphType:
        """Gets results for the init rule.

        Returns:
            Dict: For init rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="init")

    def declarative_conformance_for_responded_existence(self) -> ReturnGraphType:
        """Gets results for the responded existence rule.

        Returns:
            Dict: For responded existence rule.
        """
        return self.get_declarative_conformance_diagnostics(
            rule_name="responded_existence"
        )

    def declarative_conformance_for_coexistence(self) -> ReturnGraphType:
        """Gets results for the coexistence rule.

        Returns:
            Dict: For coexistence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="coexistence")

    def declarative_conformance_for_response(self) -> ReturnGraphType:
        """Gets results for the response rule.

        Returns:
            Dict: For response rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="response")

    def declarative_conformance_for_precedence(self) -> ReturnGraphType:
        """Gets results for the precedence rule.

        Returns:
            Dict: For precedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="precedence")

    def declarative_conformance_for_succession(self) -> ReturnGraphType:
        """Gets results for the succession rule.

        Returns:
            Dict: For succession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="succession")

    def declarative_conformance_for_altprecedence(self) -> ReturnGraphType:
        """Gets results for the altprecedence rule.

        Returns:
            Dict: For altprecedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="altprecedence")

    def declarative_conformance_for_altsuccession(self) -> ReturnGraphType:
        """Gets results for the altsuccession rule.

        Returns:
            Dict: For altsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="altsuccession")

    def declarative_conformance_for_chainresponse(self) -> ReturnGraphType:
        """Gets results for the chainresponse rule.

        Returns:
            Dict: For chainresponse rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainresponse")

    def declarative_conformance_for_chainprecedence(self) -> ReturnGraphType:
        """Gets results for the chainprecedence rule.

        Returns:
            Dict: For chainprecedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainprecedence")

    def declarative_conformance_for_chainsuccession(self) -> ReturnGraphType:
        """Gets results for the chainsuccession rule.

        Returns:
            Dict: For chainsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainsuccession")

    def declarative_conformance_for_noncoexistence(self) -> ReturnGraphType:
        """Gets results for the noncoexistence rule.

        Returns:
            Dict: For noncoexistence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="noncoexistence")

    def declarative_conformance_for_nonsuccession(self) -> ReturnGraphType:
        """Gets results for the nonsuccession rule.

        Returns:
            Dict: For nonsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="nonsuccession")

    def declarative_conformance_for_nonchainsuccession(self) -> ReturnGraphType:
        """Gets results for the nonchainsuccession rule.

        Returns:
            Dict: For nonchainsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(
            rule_name="nonchainsuccession"
        )

    def run_all_rules(
        self,
        list_of_rules: Optional[List[str]] = None,
        run_from_scratch: Optional[bool] = False,
    ) -> Any:
        """Runs conformance checking for all rules.

        It stores results in memory.
        Useful for poling when all rules need to be pre-computed in the background.

        Args:
            list_of_rules: List of rule names to check. If None, runs for all
              valid rules.
            run_from_scratch: If True, re-evaluates all rules even if results
              stored.

        Returns:
            Dictionary of all violations.
        """
        if list_of_rules is None:
            list_of_rules = self.valid_rules
        for rule in list_of_rules:
            self.temp = self.get_declarative_conformance_diagnostics(
                rule_name=rule, run_from_scratch=run_from_scratch
            )
        return self.conf_results_memory

    def update_model_and_run_all_rules(
        self,
        log: Optional[pd.DataFrame] = None,
        min_support_ratio: Optional[float] = None,
        min_confidence_ratio: Optional[float] = None,
        list_of_rules: Optional[List[str]] = None,
        run_from_scratch: Optional[bool] = False,
    ) -> Any:
        """Updates the model and runs all rules.

        Args:
            log: The event log to use.
            min_support_ratio: The minimum support ratio for discovering rules.
            min_confidence_ratio: The minimum confidence ratio for discovering rules.
            list_of_rules: List of rule names to check. If None, runs for all
              valid rules.
            run_from_scratch: If True, re-evaluates all rules even if results
              stored.

        Returns:
            Dictionary of all violations.
        """
        if log is None:
            log = self.log
        if min_support_ratio is None:
            min_support_ratio = self.min_support_ratio
        if min_confidence_ratio is None:
            min_confidence_ratio = self.min_confidence_ratio
        if list_of_rules is None:
            list_of_rules = self.valid_rules

        self.run_model(
            log=log,
            min_support_ratio=min_support_ratio,
            min_confidence_ratio=min_confidence_ratio,
        )
        for rule in list_of_rules:
            self.temp = self.get_declarative_conformance_diagnostics(
                rule_name=rule, run_from_scratch=run_from_scratch
            )
        return self.conf_results_memory