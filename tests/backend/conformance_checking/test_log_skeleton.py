"""Tests the LogSkeleton class."""

import pm4py  # type: ignore
import pytest
from conformance_checking.log_skeleton import LogSkeleton


@pytest.fixture
def sample_log():
    """Fixture to read a sample event log."""
    return pm4py.read_xes("tests/input_data/running-example.xes")


@pytest.fixture
def log_skeleton(sample_log):
    """Fixture to create a LogSkeleton instance based on the sample_log."""
    return LogSkeleton(sample_log)


def test_compute_skeleton(log_skeleton):
    """Test the compute_skeleton method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    assert log_skeleton._skeleton is not None
    assert "equivalence" in log_skeleton._skeleton
    assert "always_after" in log_skeleton._skeleton
    assert "always_before" in log_skeleton._skeleton
    assert "never_together" in log_skeleton._skeleton
    assert "activ_freq" in log_skeleton._skeleton


def test_get_equivalence_relation(log_skeleton):
    """Test the get_equivalence_relation method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    equivalence = log_skeleton.get_equivalence_relation()
    assert isinstance(equivalence, set)

    solution_equivalence = {
        ("examine thoroughly", "register request"),
        ("pay compensation", "examine casually"),
        ("decide", "check ticket"),
        ("reject request", "register request"),
        ("check ticket", "decide"),
        ("pay compensation", "register request"),
    }
    assert equivalence == solution_equivalence


def test_get_always_after_relation(log_skeleton):
    """Test the get_always_after_relation method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    always_after = log_skeleton.get_always_after_relation()
    assert isinstance(always_after, set)


def test_get_always_before_relation(log_skeleton):
    """Test the get_always_before_relation method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    always_before = log_skeleton.get_always_before_relation()
    assert isinstance(always_before, set)


def test_get_never_together_relation(log_skeleton):
    """Test the get_never_together_relation method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    never_together = log_skeleton.get_never_together_relation()
    assert isinstance(never_together, set)


def test_get_activity_frequencies(log_skeleton):
    """Test the get_activity_frequencies method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    activity_frequencies = log_skeleton.get_activity_frequencies()
    assert isinstance(activity_frequencies, dict)


def test_check_conformance_traces(log_skeleton, sample_log):
    """Test the check_conformance_traces method."""
    log_skeleton.compute_skeleton(noise_thr=0.0)
    conformance_results = log_skeleton.check_conformance_traces(sample_log)
    assert isinstance(conformance_results, list)
