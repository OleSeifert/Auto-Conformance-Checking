"""Contains functionality for declarative conformance checking.

This module defines the DeclerativeConstraints class which uses PM4Py to
discover declarative profiles from event logs and checks conformance
based on the discovered declarative profiles.
"""

import pandas as pd
import pm4py
from pm4py.algo.conformance.declare import algorithm as declare_conformance
from typing import Dict, List, Optional, Any


class DeclarativeConstraints:
    """Represents the declarative constraints of an event log.

    Attributes :
        log : The main event log.
        min_support_ratio : The minimum support ratio for discovering rules.
        min_confidence_ratio : The minimum confidence ratio for discovering rules.
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
            log : The main event log.
            min_support_ratio : The minimum support ratio for discovering rules.
                                Defaults to 0.3.
            min_confidence_ratio :  The minimum confidence ratio for discovering rules.
                                    Defaults to 0.75.
            case_id_col : The name of the column containing case IDs.
            activity_col : The name of the column containing activity names.
            timestamp_col : The name of the column containing timestamps.
        """
        self.log = log
        self.min_support_ratio = min_support_ratio
        self.min_confidence_ratio = min_confidence_ratio
        self.declare_model = None
        self.case_id_col: Optional[str] = case_id_col
        self.activity_col: Optional[str] = activity_col
        self.timestamp_col: Optional[str] = timestamp_col
        self.valid_rules = [
            "existence",
            "absence",
            "exactly_one",
            "init",
            "responded_existence",
            "coexistence",
            "response",
            "precedence",
            "succession",
            "altprecedence",
            "altsuccession",
            "chainresponse",
            "chainprecedence",
            "chainsuccession",
            "noncoexistence",
            "nonsuccession",
            "nonchainsuccession",
        ]
        self.conf_results_memory = {rule: None for rule in self.valid_rules}

    # ************************* Running Model *************************

    def run_model(
        self,
        log: Optional[pd.DataFrame] = None,
        min_support_ratio: Optional[float] = None,
        min_confidence_ratio: Optional[float] = None,
    ) -> None:
        """Runs the declarative model on the event log and stores the result in memory.

        Args:
            log (Optional[pd.DataFrame]) : The event log to use.
            min_support_ratio (Optional[float]) : The minimum support ratio for discovering rules.
            min_confidence_ratio (Optional[float]) : The minimum confidence ratio for discovering rules.
        """
        if log is None:
            log = self.log
        if min_support_ratio is None:
            min_support_ratio = self.min_support_ratio
        if min_confidence_ratio is None:
            min_confidence_ratio = self.min_confidence_ratio
        self.declare_model = pm4py.discover_declare(
            log,
            min_support_ratio=min_support_ratio,
            min_confidence_ratio=min_confidence_ratio,
        )
        self.conf_results_memory = {rule: None for rule in self.valid_rules}

    # ************************* Getting Violations & Graphs Data *************************

    def rule_specific_violation_summary(
        self,
        declare_model: Optional[Dict] = None,
        log: Optional[pd.DataFrame] = None,
        rule_name: Optional[str] = None,
        verbose: bool = False,
    ) -> Dict:
        """Summarizes number of violations in the event log for a specified declarative rule.

        This function does not access memory variable, so it runs the rule from scratch even if results are pre-computed and stored.

        Args:
            declare_model (Optional[Dict]) :  The Declare model.
                                                        If None, uses the default model.
            log (Optional[EventLog]) :  The event log.
                                        If None, uses the default log.
            rule_name (Optional[str]) : Name of the rule to check.
            verbose (bool) : Whether to print details for debugging.

        Returns:
            Dict: Summary with graph and table information of rule violations.

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

        rule_dict : Dict = declare_model.get(rule_name, {})

        graph_nodes : List = []
        graph_edges : List = []
        table_rows : List = []
        table_headers : List = None
        output : Dict = {"graphs": [], "tables": []}

        try : 
            for rule_key, rule_info in rule_dict.items():
                if isinstance(rule_key, tuple):
                    A, B = rule_key
                else:
                    A, B = rule_key, None
                diagnostics = declare_conformance.apply(
                    log, {rule_name: {(A, B): rule_info}}
                )
                violated = [d for d in diagnostics if d["dev_fitness"] < 1.0]
                violation_count = len(violated)

                if B is not None : 
                    table_headers = ["First Activity", "Second Activity", "# Violations"]
                    graph_nodes.append(A)
                    graph_nodes.append(B)
                    graph_edges.append({"from": A, "to": B, "label": str(violation_count)})
                    table_rows.append([A, B, str(violation_count)])
                else: 
                    table_headers = ["Activity", "# Violations"]
                    table_rows.append([A, str(violation_count)])
            graph_nodes = [{"id": node} for node in list(set(list(graph_nodes)))]

            if table_headers is not None : 
                output["tables"] = [{"headers": table_headers, "rows": table_rows}]
            if len(graph_nodes) > 0 and len(graph_edges) > 0 :
                output['graphs'] = [{"nodes": graph_nodes, "edges": graph_edges}]
            return output

        except Exception as e :
            if verbose:
                print(f"Error processing rule '{rule_name}': {e}")

    def get_declarative_conformance_diagnostics(
        self, rule_name: str, run_from_scratch: Optional[bool] = False
    ) -> Dict:
        """The main function to get the conformance diagnostics for a specified declarative rule.

        Check for results stored in memory and runs conformance checking of any rule only if results previously not stored in memory.

        Args:
            rule_name (str) : The name of the declarative rule to analyze.
            run_from_scratch (bool) : If True, re-evaluates the rule even if results stored.

        Returns:
            Dict: Cached or newly generated rule violation summary.

        Raises:
            ValueError: If the rule name is not supported.
        """
        rule_name = str(rule_name).lower()
        if rule_name not in self.valid_rules:
            raise ValueError(f"Unsupported rule: '{rule_name}'")
        if (self.conf_results_memory[rule_name] is None) or (run_from_scratch is True):
            self.conf_results_memory[rule_name] = self.rule_specific_violation_summary(
                declare_model=self.declare_model, log=self.log, rule_name=rule_name
            )
        return self.conf_results_memory[rule_name]

    # ************************* Getting Violations for All/Each Rule *************************

    def declarative_conformance_for_existance(self) -> Dict:
        """The function to get results of existance rule.

        Returns:
            Dict: For existance rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="existence")

    def declarative_conformance_for_absence(self) -> Dict:
        """The function to get results of absence rule.

        Returns:
            Dict: For absence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="absence")

    def declarative_conformance_for_exactly_one(self) -> Dict[str, Any]:
        """The function to get results of exactly_one rule.

        Returns:
            Dict: For exactly_one rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="exactly_one")

    def declarative_conformance_for_init(self) -> Dict:
        """The function to get results of init rule.

        Returns:
            Dict: For init rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="init")

    def declarative_conformance_for_responded_existence(self) -> Dict[str, Any]:
        """The function to get results of responded_existence rule.

        Returns:
            Dict: For responded_existence rule.
        """
        return self.get_declarative_conformance_diagnostics(
            rule_name="responded_existence"
        )

    def declarative_conformance_for_coexistence(self) -> Dict:
        """The function to get results of coexistence rule.

        Returns:
            Dict: For coexistence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="coexistence")

    def declarative_conformance_for_response(self) -> Dict:
        """The function to get results of response rule.

        Returns:
            Dict: For response rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="response")

    def declarative_conformance_for_precedence(self) -> Dict:
        """The function to get results of precedence rule.

        Returns:
            Dict: For precedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="precedence")

    def declarative_conformance_for_succession(self) -> Dict:
        """The function to get results of succession rule.

        Returns:
            Dict: For succession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="succession")

    def declarative_conformance_for_altprecedence(self) -> Dict:
        """The function to get results of altprecedence rule.

        Returns:
            Dict: For altprecedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="altprecedence")

    def declarative_conformance_for_altsuccession(self) -> Dict:
        """The function to get results of altsuccession rule.

        Returns:
            Dict: For altsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="altsuccession")

    def declarative_conformance_for_chainresponse(self) -> Dict:
        """The function to get results of chainresponse rule.

        Returns:
            Dict: For chainresponse rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainresponse")

    def declarative_conformance_for_chainprecedence(self) -> Dict:
        """The function to get results of chainprecedence rule.

        Returns:
            Dict: For chainprecedence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainprecedence")

    def declarative_conformance_for_chainsuccession(self) -> Dict:
        """The function to get results of chainsuccession rule.

        Returns:
            Dict: For chainsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="chainsuccession")

    def declarative_conformance_for_noncoexistence(self) -> Dict:
        """The function to get results of noncoexistence rule.

        Returns:
            Dict: For noncoexistence rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="noncoexistence")

    def declarative_conformance_for_nonsuccession(self) -> Dict:
        """The function to get results of nonsuccession rule.

        Returns:
            Dict: For nonsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(rule_name="nonsuccession")

    def declarative_conformance_for_nonchainsuccession(self) -> Dict:
        """The function to get results of nonchainsuccession rule.

        Returns:
            Dict: For nonchainsuccession rule.
        """
        return self.get_declarative_conformance_diagnostics(
            rule_name="nonchainsuccession"
        )

    def run_all_rules(
        self,
        list_of_rules: Optional[list] = None,
        run_from_scratch: Optional[bool] = False,
    ) -> Any:
        """Runs conformance checking for all rules and stores results in memory.

        Useful for poling when all rules need to be pre-computed in the background.

        Args:
            list_of_rules (Optional[list]) : List of rule names to check. If None, runs for all valid rules.
            run_from_scratch (Optional[bool]) : If True, re-evaluates all rules even if results stored.

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
