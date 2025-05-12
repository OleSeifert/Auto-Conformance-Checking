"""Tests the TemporalProfile class."""

import pm4py  # type: ignore
import pytest
import pandas as pd
from pandas.io.formats.style import Styler
from conformance_checking.temporal_profile import TemporalProfile


@pytest.fixture
def sample_log():
    """Fixture to read a sample event log."""
    return pm4py.read_xes("tests/input_data/running-example.xes")  # type: ignore


@pytest.fixture
def temporal_profile(sample_log):  # type: ignore
    """Fixture to create a TemporalProfile instance based on the sample_log."""
    return TemporalProfile(sample_log)  # type: ignore


def test_discover_temporal_profile(temporal_profile):  # type: ignore
    """Test the discover_temporal_profile method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    assert temporal_profile._temporal_profile is not None  # type: ignore
    assert isinstance(temporal_profile._temporal_profile, dict)  # type: ignore


def test_check_temporal_conformance(temporal_profile):  # type: ignore
    """Test the check_temporal_conformance method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    assert temporal_profile._temporal_conformance_result is not None  # type: ignore
    assert isinstance(temporal_profile._temporal_conformance_result, list)  # type: ignore


def test_get_temporal_profile(temporal_profile):  # type: ignore
    """Test the get_temporal_profile method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    temporal_profile_result = temporal_profile.get_temporal_profile()  # type: ignore
    assert temporal_profile_result is not None
    assert isinstance(temporal_profile_result, dict)


def test_get_temporal_conformance_result(temporal_profile):  # type: ignore
    """Test the get_temporal_conformance_result method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    conformance_result = temporal_profile.get_temporal_conformance_result()  # type: ignore
    assert conformance_result is not None
    assert isinstance(conformance_result, list)


def test_get_zeta(temporal_profile):  # type: ignore
    """Test the get_zeta method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    zeta = temporal_profile.get_zeta()  # type: ignore
    assert zeta is not None
    assert isinstance(zeta, float)
    assert zeta >= 0


def test_get_conformance_diagnostics(temporal_profile):  # type: ignore
    """Test the get_conformance_diagnostics method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    diagnostics = temporal_profile.get_conformance_diagnostics()  # type: ignore
    assert diagnostics is not None
    assert isinstance(diagnostics, pd.DataFrame)


def test_get_sorted_coloured_diagnostics(temporal_profile):  # type: ignore
    """Test the get_sorted_coloured_diagnostics method."""
    temporal_profile.discover_temporal_profile()  # type: ignore
    temporal_profile.check_temporal_conformance()  # type: ignore
    sorted_coloured_diagnostics = temporal_profile.get_sorted_coloured_diagnostics()  # type: ignore
    assert sorted_coloured_diagnostics is not None
    assert isinstance(sorted_coloured_diagnostics, Styler)
