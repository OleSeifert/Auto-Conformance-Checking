"""Tests the DeclerativeConstraints class."""

import pm4py  # type: ignore
import pytest
import pandas as pd
from pandas.io.formats.style import Styler
from declarative_constraints import DeclarativeConstraints


# @pytest.fixture
def get_sample_log():
    """Fixture to read a sample event log."""
    return pm4py.read_xes("tests/input_data/running-example.xes")


# @pytest.fixture
def get_declarative_constraints_obj():
    """Fixture to create a DeclarativeConstraints instance based on the sample_log."""
    sample_log = get_sample_log()
    return DeclarativeConstraints(sample_log)


# Test function where user input is passed (general function)
def test_get_declarative_conformance_diagnostics(rule_name="response"):
    """Test the get_declarative_conformance_diagnostics method."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name=rule_name)
    assert declarative_profile.conf_results_memory[rule_name] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory[rule_name], dict)  # type: ignore


# Test function for response rule
def test_get_declarative_conformance_diagnostics_for_response():
    """Test the get_declarative_conformance_diagnostics method for response rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="response")
    assert declarative_profile.conf_results_memory["response"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["response"], dict)  # type: ignore


# Test function for precedence rule
def test_get_declarative_conformance_diagnostics_for_precedence():
    """Test the get_declarative_conformance_diagnostics method for precedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="precedence")
    assert declarative_profile.conf_results_memory["precedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["precedence"], dict)  # type: ignore


# Test function for existence rule
def test_get_declarative_conformance_diagnostics_for_existence():
    """Test the get_declarative_conformance_diagnostics method for existence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="existence")
    assert declarative_profile.conf_results_memory["existence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["existence"], dict)  # type: ignore


# Test function for absence rule
def test_get_declarative_conformance_diagnostics_for_absence():
    """Test the get_declarative_conformance_diagnostics method for absence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="absence")
    assert declarative_profile.conf_results_memory["absence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["absence"], dict)  # type: ignore


# Test function for exactly_one rule
def test_get_declarative_conformance_diagnostics_for_exactly_one():
    """Test the get_declarative_conformance_diagnostics method for exactly_one rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="exactly_one")
    assert declarative_profile.conf_results_memory["exactly_one"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["exactly_one"], dict)  # type: ignore


# Test function for init rule
def test_get_declarative_conformance_diagnostics_for_init():
    """Test the get_declarative_conformance_diagnostics method for init rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="init")
    assert declarative_profile.conf_results_memory["init"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["init"], dict)  # type: ignore


# Test function for responded_existence rule
def test_get_declarative_conformance_diagnostics_for_responded_existence():
    """Test the get_declarative_conformance_diagnostics method for responded_existence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="responded_existence"
    )
    assert declarative_profile.conf_results_memory["responded_existence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["responded_existence"], dict)  # type: ignore


# Test function for coexistence rule
def test_get_declarative_conformance_diagnostics_for_coexistence():
    """Test the get_declarative_conformance_diagnostics method for coexistence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="coexistence")
    assert declarative_profile.conf_results_memory["coexistence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["coexistence"], dict)  # type: ignore


# Test function for succession rule
def test_get_declarative_conformance_diagnostics_for_succession():
    """Test the get_declarative_conformance_diagnostics method for succession rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="succession")
    assert declarative_profile.conf_results_memory["succession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["succession"], dict)  # type: ignore


# Test function for altresponse rule
def test_get_declarative_conformance_diagnostics_for_altresponse():
    """Test the get_declarative_conformance_diagnostics method for altresponse rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(rule_name="altresponse")
    assert declarative_profile.conf_results_memory["altresponse"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["altresponse"], dict)  # type: ignore


# Test function for altprecedence rule
def test_get_declarative_conformance_diagnostics_for_altprecedence():
    """Test the get_declarative_conformance_diagnostics method for altprecedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="altprecedence"
    )
    assert declarative_profile.conf_results_memory["altprecedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["altprecedence"], dict)  # type: ignore


# Test function for altsuccession rule
def test_get_declarative_conformance_diagnostics_for_altsuccession():
    """Test the get_declarative_conformance_diagnostics method for altsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="altsuccession"
    )
    assert declarative_profile.conf_results_memory["altsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["altsuccession"], dict)  # type: ignore


# Test function for chainresponse rule
def test_get_declarative_conformance_diagnostics_for_chainresponse():
    """Test the get_declarative_conformance_diagnostics method for chainresponse rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="chainresponse"
    )
    assert declarative_profile.conf_results_memory["chainresponse"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainresponse"], dict)  # type: ignore


# Test function for chainprecedence rule
def test_get_declarative_conformance_diagnostics_for_chainprecedence():
    """Test the get_declarative_conformance_diagnostics method for chainprecedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="chainprecedence"
    )
    assert declarative_profile.conf_results_memory["chainprecedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainprecedence"], dict)  # type: ignore


# Test function for chainsuccession rule
def test_get_declarative_conformance_diagnostics_for_chainsuccession():
    """Test the get_declarative_conformance_diagnostics method for chainsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="chainsuccession"
    )
    assert declarative_profile.conf_results_memory["chainsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainsuccession"], dict)  # type: ignore


# Test function for noncoexistence rule
def test_get_declarative_conformance_diagnostics_for_noncoexistence():
    """Test the get_declarative_conformance_diagnostics method for noncoexistence rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="noncoexistence"
    )
    assert declarative_profile.conf_results_memory["noncoexistence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["noncoexistence"], dict)  # type: ignore


# Test function for nonsuccession rule
def test_get_declarative_conformance_diagnostics_for_nonsuccession():
    """Test the get_declarative_conformance_diagnostics method for nonsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="nonsuccession"
    )
    assert declarative_profile.conf_results_memory["nonsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["nonsuccession"], dict)  # type: ignore


# Test function for nonchainsuccession rule
def test_get_declarative_conformance_diagnostics_for_nonchainsuccession():
    """Test the get_declarative_conformance_diagnostics method for nonchainsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    declarative_profile.get_declarative_conformance_diagnostics(
        rule_name="nonchainsuccession"
    )
    assert declarative_profile.conf_results_memory["nonchainsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["nonchainsuccession"], dict)  # type: ignore
