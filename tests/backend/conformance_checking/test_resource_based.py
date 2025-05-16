"""Tests the ResourceBased class."""

import pm4py  # type: ignore
import pytest
from conformance_checking.resource_based import ResourceBased
from pm4py.objects.org.sna.obj import SNA  # type: ignore


@pytest.fixture
def sample_log():
    """Fixture to read a sample event log."""
    return pm4py.read_xes("tests/input_data/running-example.xes")  # type: ignore


@pytest.fixture
def resource_based(sample_log):  # type: ignore
    """Fixture to create a ResourceBased instance based on the sample_log."""
    return ResourceBased(sample_log)  # type: ignore


# **************** Social Network Analysis Testing ****************


def test_compute_handover_of_work(resource_based):  # type: ignore
    """Test the compute_handover_of_work method."""
    resource_based.compute_handover_of_work()  # type: ignore
    assert resource_based._handover_of_work is not None  # type: ignore
    assert isinstance(resource_based._handover_of_work, SNA)  # type: ignore


def test_get_handover_of_work_values(resource_based):  # type: ignore
    """Test the get_handover_of_work_values method."""
    resource_based.compute_handover_of_work()  # type: ignore
    handover_of_work = resource_based.get_handover_of_work_values()  # type: ignore
    assert isinstance(handover_of_work, dict)


def test_is_handover_of_work_directed(resource_based):  # type: ignore
    """Test the is_handover_of_work_directed method."""
    resource_based.compute_handover_of_work()  # type: ignore
    handover_of_work = resource_based.is_handover_of_work_directed()  # type: ignore
    assert isinstance(handover_of_work, bool)


def test_compute_subcontracting(resource_based):  # type: ignore
    """Test the compute_subcontracting method."""
    resource_based.compute_subcontracting()  # type: ignore
    assert resource_based._subcontracting is not None  # type: ignore
    assert isinstance(resource_based._subcontracting, SNA)  # type: ignore


def test_get_subcontracting_values(resource_based):  # type: ignore
    """Test the get_subcontracting_values method."""
    resource_based.compute_subcontracting()  # type: ignore
    subcontracting = resource_based.get_subcontracting_values()  # type: ignore
    assert isinstance(subcontracting, dict)


def test_is_subcontracting_directed(resource_based):  # type: ignore
    """Test the is_subcontracting_directed method."""
    resource_based.compute_subcontracting()  # type: ignore
    subcontracting = resource_based.is_subcontracting_directed()  # type: ignore
    assert isinstance(subcontracting, bool)


def test_compute_working_together(resource_based):  # type: ignore
    """Test the compute_working_together method."""
    resource_based.compute_working_together()  # type: ignore
    assert resource_based._working_together is not None  # type: ignore
    assert isinstance(resource_based._working_together, SNA)  # type: ignore


def test_get_working_together_values(resource_based):  # type: ignore
    """Test the get_working_together_values method."""
    resource_based.compute_working_together()  # type: ignore
    working_together = resource_based.get_working_together_values()  # type: ignore
    assert isinstance(working_together, dict)


def test_is_working_together_directed(resource_based):  # type: ignore
    """Test the is_working_together_directed method."""
    resource_based.compute_working_together()  # type: ignore
    working_together = resource_based.is_working_together_directed()  # type: ignore
    assert isinstance(working_together, bool)


def test_compute_similar_activities(resource_based):  # type: ignore
    """Test the compute_similar_activities method."""
    resource_based.compute_similar_activities()  # type: ignore
    assert resource_based._similar_activities is not None  # type: ignore
    assert isinstance(resource_based._similar_activities, SNA)  # type: ignore


def test_get_similar_activities_values(resource_based):  # type: ignore
    """Test the get_similar_activities_values method."""
    resource_based.compute_similar_activities()  # type: ignore
    similar_activities = resource_based.get_similar_activities_values()  # type: ignore
    assert isinstance(similar_activities, dict)


def test_is_similar_activities_directed(resource_based):  # type: ignore
    """Test the is_similar_activities_directed method."""
    resource_based.compute_similar_activities()  # type: ignore
    similar_activities = resource_based.is_similar_activities_directed()  # type: ignore
    assert isinstance(similar_activities, bool)


# **************** Role Discovery Testing ****************


def test_compute_organizational_roles(resource_based):  # type: ignore
    """Test the compute_organizational_roles method."""
    resource_based.compute_organizational_roles()  # type: ignore
    assert resource_based._organizational_roles is not None  # type: ignore
    assert isinstance(resource_based._organizational_roles, list)  # type: ignore


def test_get_organizational_roles(resource_based):  # type: ignore
    """Test the get_organizational_roles method."""
    resource_based.compute_organizational_roles()  # type: ignore
    organizational_roles = resource_based.get_organizational_roles()  # type: ignore
    assert isinstance(organizational_roles, list)


# **************** Resource Profiles Testing ****************


def test_get_number_of_distinct_activities(resource_based):  # type: ignore
    """Test the get_number_of_distinct_activities method."""
    num_activities = resource_based.get_number_of_distinct_activities(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(num_activities, int)
    assert num_activities >= 0


def test_get_activity_frequency(resource_based):  # type: ignore
    """Test the get_activity_frequency method."""
    activity_frequency = resource_based.get_activity_frequency(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara", "decide"
    )
    assert isinstance(activity_frequency, float)
    assert activity_frequency >= 0.0


def test_get_activity_completions(resource_based):  # type: ignore
    """Test the get_activity_completions method."""
    activity_completions = resource_based.get_activity_completions(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(activity_completions, int)
    assert activity_completions >= 0


def test_get_case_completions(resource_based):  # type: ignore
    """Test the get_case_completions method."""
    case_completions = resource_based.get_case_completions(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(case_completions, int)
    assert case_completions >= 0


def test_get_fraction_case_completions(resource_based):  # type: ignore
    """Test the get_fraction_case_completions method."""
    fraction_case_completions = resource_based.get_fraction_case_completions(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(fraction_case_completions, float)
    assert 0.0 <= fraction_case_completions <= 1.0


def test_get_average_workload(resource_based):  # type: ignore
    """Test the get_average_workload method."""
    average_workload = resource_based.get_average_workload(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(average_workload, float)
    assert 0.0 <= average_workload <= 1.0


def test_get_multitasking(resource_based):  # type: ignore
    """Test the get_multitasking method."""
    multitasking = resource_based.get_multitasking(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(multitasking, float)
    assert 0.0 <= multitasking <= 1.0


def test_get_average_activity_duration(resource_based):  # type: ignore
    """Test the get_average_activity_duration method."""
    average_activity_duration = resource_based.get_average_activity_duration(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara", "decide"
    )
    assert isinstance(average_activity_duration, float)
    assert average_activity_duration >= 0.0


def test_get_average_case_duration(resource_based):  # type: ignore
    """Test the get_average_case_duration method."""
    average_case_duration = resource_based.get_average_case_duration(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(average_case_duration, float)
    assert average_case_duration >= 0.0


def test_get_interaction_two_resources(resource_based):  # type: ignore
    """Test the get_interaction_two_resources method."""
    interaction = resource_based.get_interaction_two_resources(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara", "Mike"
    )
    assert isinstance(interaction, float)
    assert interaction >= 0.0


def test_get_social_position(resource_based):  # type: ignore
    """Test the get_social_position method."""
    social_position = resource_based.get_social_position(  # type: ignore
        "2010-12-30 00:00:00", "2011-01-25 00:00:00", "Sara"
    )
    assert isinstance(social_position, float)
    assert 0.0 <= social_position <= 1.0


# **************** Organizational Mining Testing ****************


def test_compute_organizational_diagnostics(resource_based):  # type: ignore
    """Test the compute_organizational_diagnostics method."""
    resource_based.resource_col = "Resource"  # type: ignore
    resource_based.compute_organizational_diagnostics()  # type: ignore

    diagnostics = resource_based._organizational_diagnostics  # type: ignore
    assert diagnostics is not None, "Organizational diagnostics returned None"
    assert isinstance(diagnostics, dict), "Organizational diagnostics is not a dict"

    expected_keys = {
        "group_relative_focus",
        "group_relative_stake",
        "group_coverage",
        "group_member_contribution",
    }
    for key in expected_keys:
        assert key in diagnostics, f"Missing key: {key}"


def test_get_group_relative_focus(resource_based):  # type: ignore
    """Test the get_group_relative_focus method."""
    resource_based.resource_col = "Resource"  # type: ignore
    resource_based.compute_organizational_diagnostics()  # type: ignore
    group_relative_focus = resource_based.get_group_relative_focus()  # type: ignore
    assert isinstance(group_relative_focus, dict)


def test_get_group_relative_stake(resource_based):  # type: ignore
    """Test the get_group_relative_stake method."""
    resource_based.resource_col = "Resource"  # type: ignore
    resource_based.compute_organizational_diagnostics()  # type: ignore
    group_relative_stake = resource_based.get_group_relative_stake()  # type: ignore
    assert isinstance(group_relative_stake, dict)


def test_get_group_coverage(resource_based):  # type: ignore
    """Test the get_group_coverage method."""
    resource_based.resource_col = "Resource"  # type: ignore
    resource_based.compute_organizational_diagnostics()  # type: ignore
    group_coverage = resource_based.get_group_coverage()  # type: ignore
    assert isinstance(group_coverage, dict)


def test_get_group_member_contribution(resource_based):  # type: ignore
    """Test the get_group_member_contribution method."""
    resource_based.resource_col = "Resource"  # type: ignore
    resource_based.compute_organizational_diagnostics()  # type: ignore
    group_member_contribution = resource_based.get_group_member_contribution()  # type: ignore
    assert isinstance(group_member_contribution, dict)
