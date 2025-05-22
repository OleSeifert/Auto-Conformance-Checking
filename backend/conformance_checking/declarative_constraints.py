"""Contains functionality for declarative conformance checking.

This module defines the DeclarativeConstraints class which uses PM4Py to
discover declarative profiles from event logs and checks conformance based
on the discovered declarative profiles.
"""

from typing import Dict, Optional, Any
import pandas as pd
import pm4py
from pm4py.algo.conformance.declare import algorithm as declare_conformance


class DeclerativeConstraints:
    """
    A class to handle the conformance checking of declarative constraints
    in an event log using the PM4Py library.

    Attributes :
        log : The main event log
        min_support_ratio : The minimum support ratio for discovering rules
        min_confidence_ratio : The minimum confidence ratio for discovering rules
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
        """
        Initializes the DeclerativeConstraints class with an event log.
        Also defines the model and the memory for all results

        Args:
            log : The main event log.
            min_support_ratio : The minimum support ratio for discovering rules
                                Defaults to 0.3
            min_confidence_ratio :  The minimum confidence ratio for discovering rules
                                    Defaults to 0.75
        """
        self.log = log
        self.declare_model = pm4py.discover_declare(
            log,
            min_support_ratio=min_support_ratio,
            min_confidence_ratio=min_confidence_ratio,
        )
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

    def rule_specific_violation_summary(
        self,
        declare_model: Optional[Dict[str, Any]] = None,
        log: Optional[pd.DataFrame] = None,
        rule_name: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Summarizes number of violations in the event log for a specified declarative rule.

        Args:
            declare_model (Optional[Dict[str, Any]]) :  The Declare model.
                                                        If None, uses the default model.
            log (Optional[EventLog]) :  The event log.
                                        If None, uses the default log.
            rule_name (Optional[str]) : Name of the rule to check.
            verbose (bool) : Whether to print details for debugging.

        Returns:
            Dict[str, Any]: Summary with graph and table information of rule violations.

        Raises:
            ValueError: If an unsupported rule name is provided.
        """

        if declare_model is None:
            declare_model = self.declare_model
        if log is None:
            log = self.log

        if str(rule_name) not in self.valid_rules:
            raise ValueError(
                f"Unsupported rule: '{rule_name}'. Must be one of: {valid_rules}"
            )

        rule_dict = declare_model.get(rule_name, {})

        output = {"graph": {"nodes": [], "edges": []}, "table": []}

        nodes_set = list([])

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

            nodes_set.append(A)
            if B is not None:
                output["table"].append(
                    {
                        "First Activity": A,
                        "Second Activity": B,
                        "# Violations": str(violation_count),
                    }
                )
                nodes_set.append(B)
                output["graph"]["edges"].append(
                    {"from": A, "to": B, "label": str(violation_count)}
                )
            else:
                output["table"].append(
                    {
                        "First Activity": A,
                        "Second Activity": "-",
                        "# Violations": str(violation_count),
                    }
                )
                output["graph"]["edges"].append(
                    {"from": A, "to": A, "label": str(violation_count)}
                )
        output["graph"]["nodes"] = list(set(list(nodes_set)))
        return output

    def get_declarative_conformance_diagnostics(
        self, rule_name: str, run_from_scratch: Optional[bool] = False
    ) -> Dict[str, Any]:
        """
        The main function to get the conformance diagnostics for a specified declarative rule.
        Check for results stored in memory and runs conformance checking of any rule only if results previously not stored in memory.

        Args:
            rule_name (str) : The name of the declarative rule to analyze.
            run_from_scratch (bool) : If True, re-evaluates the rule even if results stored.

        Returns:
            Dict[str, Any]: Cached or newly generated rule violation summary.

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
