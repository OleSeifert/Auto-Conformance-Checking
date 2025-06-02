"""Tests the DeclerativeConstraints class."""

import pm4py  # type: ignore
from declarative_constraints import DeclarativeConstraints


def get_sample_log():
    """Fixture to read a sample event log."""
    return pm4py.read_xes("tests/input_data/running-example.xes")


def get_declarative_constraints_obj():
    """Fixture to create a DeclarativeConstraints instance based on the sample_log."""
    sample_log = get_sample_log()
    return DeclarativeConstraints(sample_log)


def test_get_declarative_conformance_diagnostics_for_response():
    """Test the get_declarative_conformance_diagnostics method for response rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_response()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["response"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["response"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_precedence():
    """Test the get_declarative_conformance_diagnostics method for precedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_precedence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["precedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["precedence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_existence():
    """Test the get_declarative_conformance_diagnostics method for existence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_existence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["existence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["existence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_absence():
    """Test the get_declarative_conformance_diagnostics method for absence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_absence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["absence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["absence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_exactly_one():
    """Test the get_declarative_conformance_diagnostics method for exactly_one rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_exactly_one()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["exactly_one"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["exactly_one"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_init():
    """Test the get_declarative_conformance_diagnostics method for init rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_init()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["init"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["init"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_responded_existence():
    """Test the get_declarative_conformance_diagnostics method for responded_existence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_responded_existence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["responded_existence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["responded_existence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_coexistence():
    """Test the get_declarative_conformance_diagnostics method for coexistence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_coexistence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["coexistence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["coexistence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_succession():
    """Test the get_declarative_conformance_diagnostics method for succession rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_succession()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["succession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["succession"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_altprecedence():
    """Test the get_declarative_conformance_diagnostics method for altprecedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_altprecedence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["altprecedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["altprecedence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_altsuccession():
    """Test the get_declarative_conformance_diagnostics method for altsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_altsuccession()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["altsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["altsuccession"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_chainresponse():
    """Test the get_declarative_conformance_diagnostics method for chainresponse rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_chainresponse()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["chainresponse"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainresponse"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_chainprecedence():
    """Test the get_declarative_conformance_diagnostics method for chainprecedence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_chainprecedence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["chainprecedence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainprecedence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_chainsuccession():
    """Test the get_declarative_conformance_diagnostics method for chainsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_chainsuccession()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["chainsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["chainsuccession"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_noncoexistence():
    """Test the get_declarative_conformance_diagnostics method for noncoexistence rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_noncoexistence()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["noncoexistence"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["noncoexistence"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_nonsuccession():
    """Test the get_declarative_conformance_diagnostics method for nonsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_nonsuccession()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["nonsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["nonsuccession"], dict)  # type: ignore


def test_get_declarative_conformance_diagnostics_for_nonchainsuccession():
    """Test the get_declarative_conformance_diagnostics method for nonchainsuccession rules."""
    declarative_profile = get_declarative_constraints_obj()
    result = declarative_profile.declarative_conformance_for_nonchainsuccession()
    assert result is not None # type: ignore
    assert declarative_profile.conf_results_memory["nonchainsuccession"] is not None  # type: ignore
    assert isinstance(declarative_profile.conf_results_memory["nonchainsuccession"], dict)  # type: ignore
