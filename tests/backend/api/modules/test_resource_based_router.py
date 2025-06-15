"""Tests for the Resource Based Router."""

from unittest.mock import patch

import pandas as pd
from fastapi.testclient import TestClient

from backend.api.models.schemas.job_models import JobStatus
from backend.main import app


class TestComputeResourceBasedEndpoint:
    """Tests for the api/resource-based/compute endpoint."""

    def test_compute_resource_based_metrics(self, test_client: TestClient):
        """Test successful job ID creation for resource-based metrics."""
        with patch(
            "backend.api.modules.resource_based_router.compute_and_store_resource_based_metrics"
        ) as mock_task:
            mock_task.return_value = None
            response = test_client.post("/api/resource-based/compute")

            assert response.status_code == 202
            assert "job_id" in response.json()
            assert isinstance(response.json()["job_id"], str)
            assert len(response.json()["job_id"]) > 0


# *****************Social Network Analysis (SNA) Tests*****************


class TestGetHandoverOfWorkEndpoint:
    """Tests for the api/resource-based/sna/handover-of-work endpoint."""

    def test_get_handover_of_work_success(self, test_client: TestClient):
        """Test successful retrieval of handover of work metric."""
        dummy_result = {  # type: ignore
            "handover_of_work": {
                "values": [
                    {"source": "user1", "target": "user2", "value": 0.75},
                    {"source": "user2", "target": "user3", "value": 0.50},
                ]
            }
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get(
            "/api/resource-based/sna/handover-of-work/test_job_id"
        )

        assert response.status_code == 200
        response_data = response.json()

        assert "graphs" in response_data
        assert "tables" in response_data
        assert len(response_data["graphs"]) == 1
        assert len(response_data["tables"]) == 1

    def test_get_handover_of_work_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test handover of work retrieval with different module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/resource-based/sna/handover-of-work/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}


class TestGetSubcontractingEndpoint:
    """Tests for the api/resource-based/sna/subcontracting endpoint."""

    def test_get_subcontracting_success(self, test_client: TestClient):
        """Test successful retrieval of subcontracting metric."""
        dummy_result = {  # type: ignore
            "subcontracting": {
                "values": [
                    {"source": "dept1", "target": "dept2", "value": 0.80},
                    {"source": "dept2", "target": "dept3", "value": 0.60},
                ]
            }
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get("/api/resource-based/sna/subcontracting/test_job_id")

        assert response.status_code == 200
        response_data = response.json()

        assert "graphs" in response_data
        assert "tables" in response_data
        assert len(response_data["graphs"]) == 1
        assert len(response_data["tables"]) == 1

    def test_get_subcontracting_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test subcontracting retrieval with different module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/resource-based/sna/subcontracting/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}


class TestGetWorkingTogetherEndpoint:
    """Tests for the api/resource-based/sna/working-together endpoint."""

    def test_get_working_together_success(self, test_client: TestClient):
        """Test successful retrieval of working together metric."""
        dummy_result = {  # type: ignore
            "working_together": {
                "values": [
                    {"source": "team1", "target": "team2", "value": 0.90},
                    {"source": "team2", "target": "team3", "value": 0.70},
                ]
            }
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get(
            "/api/resource-based/sna/working-together/test_job_id"
        )

        assert response.status_code == 200
        response_data = response.json()

        assert "graphs" in response_data
        assert "tables" in response_data
        assert len(response_data["graphs"]) == 1
        assert len(response_data["tables"]) == 1

    def test_get_working_together_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test working together retrieval with different module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/resource-based/sna/working-together/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}


class TestGetSimilarActivitiesEndpoint:
    """Tests for the api/resource-based/sna/similar-activities endpoint."""

    def test_get_similar_activities_success(self, test_client: TestClient):
        """Test successful retrieval of similar activities metric."""
        dummy_result = {  # type: ignore
            "similar_activities": {
                "values": [
                    {"source": "activity1", "target": "activity2", "value": 0.85},
                    {"source": "activity2", "target": "activity3", "value": 0.65},
                ]
            }
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get(
            "/api/resource-based/sna/similar-activities/test_job_id"
        )

        assert response.status_code == 200
        response_data = response.json()

        assert "graphs" in response_data
        assert "tables" in response_data
        assert len(response_data["graphs"]) == 1
        assert len(response_data["tables"]) == 1

    def test_get_similar_activities_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test similar activities retrieval with different module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/resource-based/sna/similar-activities/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}

    # *****************Role Discovery Tests*****************


class TestGetOrganizationalRolesEndpoint:
    """Tests for the api/resource-based/role-discovery endpoint."""

    def test_get_organizational_roles_success(self, test_client: TestClient):
        """Test successful retrieval of organizational roles."""
        dummy_result = {  # type: ignore
            "organizational_roles": [
                {
                    "activities": ["Activity A"],
                    "originators_importance": {"Resource A": "0.85"},
                },
                {
                    "activities": ["Activity B"],
                    "originators_importance": {"Resource B": "0.72"},
                },
                {
                    "activities": ["Activity C"],
                    "originators_importance": {"Resource C": "0.93"},
                },
            ]
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get("/api/resource-based/role-discovery/test_job_id")

        assert response.status_code == 200
        response_data = response.json()

        assert "tables" in response_data
        assert "graphs" in response_data
        assert len(response_data["tables"]) == 1
        assert len(response_data["graphs"]) == 0

        table = response_data["tables"][0]
        assert table["headers"] == ["Activity", "Originator", "Importance"]
        assert len(table["rows"]) == 3
        assert table["rows"][0] == ["Activity A", "Resource A", "0.85"]
        assert table["rows"][1] == ["Activity B", "Resource B", "0.72"]
        assert table["rows"][2] == ["Activity C", "Resource C", "0.93"]

    def test_get_organizational_roles_empty_result(self, test_client: TestClient):
        """Test organizational roles retrieval with empty result."""
        dummy_result = {  # type: ignore
            "organizational_roles": []
        }

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get("/api/resource-based/role-discovery/test_job_id")

        assert response.status_code == 200
        response_data = response.json()

        assert "tables" in response_data
        assert "graphs" in response_data
        assert len(response_data["tables"]) == 1
        assert len(response_data["graphs"]) == 0

        table = response_data["tables"][0]
        assert table["headers"] == ["Activity", "Originator", "Importance"]
        assert len(table["rows"]) == 0

    def test_get_organizational_roles_missing_result_key(self, test_client: TestClient):
        """Test organizational roles retrieval with result key missing."""
        dummy_result = {}  # type: ignore

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="resource_based",
                status="complete",
                result=dummy_result,  # type: ignore
            )
        }

        response = test_client.get("/api/resource-based/role-discovery/test_job_id")

        assert response.status_code == 200
        response_data = response.json()

        assert "tables" in response_data
        assert "graphs" in response_data
        assert len(response_data["tables"]) == 1
        assert len(response_data["graphs"]) == 0

        table = response_data["tables"][0]
        assert table["headers"] == ["Activity", "Originator", "Importance"]
        assert len(table["rows"]) == 0

    def test_get_organizational_roles_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test getting organizational roles with wrong module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/resource-based/role-discovery/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}


class TestGetDistinctActivitiesEndpoint:
    """Tests for the api/resource-based/resource-profile/distinct-activities
    endpoint."""

    def test_get_distinct_activities_success(self):
        """Test successful retrieval of distinct activities count."""
        # Create a fresh test client without dependency overrides
        from fastapi.testclient import TestClient

        from backend.main import app

        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_number_of_distinct_activities"
                ) as mock_get_distinct:
                    mock_get_distinct.return_value = 5

                    response = client.get(
                        "/api/resource-based/resource-profile/distinct-activities",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    print(response.json())
                    assert response.status_code == 200
                    assert response.json() == 5


class TestGetResourceActivityFrequencyEndpoint:
    """Tests for the api/resource-based/resource-profile/activity-frequency
    endpoint."""

    def test_get_resource_activity_frequency_success(self):
        """Test successful retrieval of resource activity frequency."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_activity_frequency"
                ) as mock_get_frequency:
                    mock_get_frequency.return_value = 0.75

                    response = client.get(
                        "/api/resource-based/resource-profile/activity-frequency",
                        params={
                            "resource": "Resource A",
                            "activity": "Activity A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 0.75


class TestGetResourceActivityCompletionsEndpoint:
    """Tests for the api/resource-based/resource-profile/activity-completions
    endpoint."""

    def test_get_resource_activity_completions_success(self):
        """Test successful retrieval of resource activity completions."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_activity_completions"
                ) as mock_get_completions:
                    mock_get_completions.return_value = 15

                    response = client.get(
                        "/api/resource-based/resource-profile/activity-completions",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 15


class TestGetResourceCaseCompletionsEndpoint:
    """Tests for the api/resource-based/resource-profile/case-completions
    endpoint."""

    def test_get_resource_case_completions_success(self):
        """Test successful retrieval of resource case completions."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_case_completions"
                ) as mock_get_case_completions:
                    mock_get_case_completions.return_value = 8

                    response = client.get(
                        "/api/resource-based/resource-profile/case-completions",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 8


class TestGetResourceFractionCaseCompletionsEndpoint:
    """Tests for api/resource-based/resource-profile/fraction-case-
    completions."""

    def test_get_resource_fraction_case_completions_success(self):
        """Test successful retrieval of resource fraction case completions."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_fraction_git ccase_completions"
                ) as mock_get_fraction:
                    mock_get_fraction.return_value = 0.62

                    response = client.get(
                        "/api/resource-based/resource-profile/fraction-case-completions",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 0.62


class TestGetResourceAverageWorkloadEndpoint:
    """Tests for api/resource-based/resource-profile/average-workload."""

    def test_get_resource_average_workload_success(self):
        """Test successful retrieval of resource average workload."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_average_workload"
                ) as mock_get_workload:
                    mock_get_workload.return_value = 2.5

                    response = client.get(
                        "/api/resource-based/resource-profile/average-workload",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 2.5


class TestGetResourceMultitaskingEndpoint:
    """Tests for api/resource-based/resource-profile/multitasking."""

    def test_get_resource_multitasking_success(self):
        """Test successful retrieval of resource multitasking metric."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_multitasking"
                ) as mock_get_multitasking:
                    mock_get_multitasking.return_value = 1.8

                    response = client.get(
                        "/api/resource-based/resource-profile/multitasking",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 1.8


class TestGetInteractionOfTwoResourcesEndpoint:
    """Tests for api/resource-based/resource-profile/interaction-two-
    resources."""

    def test_get_interaction_of_two_resources_success(self):
        """Test successful retrieval of interaction between two resources."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_interaction_two_resources"
                ) as mock_get_interaction:
                    mock_get_interaction.return_value = 0.45

                    response = client.get(
                        "/api/resource-based/resource-profile/interaction-two-resources",
                        params={
                            "resource1": "Resource A",
                            "resource2": "Resource B",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 0.45


class TestGetResourceSocialPositionEndpoint:
    """Tests for api/resource-based/resource-profile/social-position."""

    def test_get_resource_social_position_success(self):
        """Test successful retrieval of resource social position."""
        with TestClient(app) as client:
            with patch(
                "backend.api.modules.resource_based_router.get_celonis_connection"
            ) as mock_celonis:
                mock_celonis_manager = mock_celonis.return_value
                mock_celonis_manager.get_dataframe_with_resource_group_from_celonis.return_value = pd.DataFrame(
                    {
                        "case:concept:name": ["Case 1", "Case 2", "Case 3"],
                        "org:resource": ["Resource A", "Resource B", "Resource C"],
                        "concept:name": ["Activity A", "Activity B", "Activity C"],
                        "time:timestamp": [
                            "2023-01-01 00:00:00",
                            "2023-06-01 00:00:00",
                            "2023-12-01 00:00:00",
                        ],
                        "org:group": ["Group 1", "Group 2", "Group 3"],
                    }
                )

                with patch(
                    "backend.conformance_checking.resource_based.ResourceBased.get_social_position"
                ) as mock_get_social_position:
                    mock_get_social_position.return_value = 0.78

                    response = client.get(
                        "/api/resource-based/resource-profile/social-position",
                        params={
                            "resource": "Resource A",
                            "start_time": "2023-01-01",
                            "end_time": "2023-12-31",
                        },
                    )

                    assert response.status_code == 200
                    assert response.json() == 0.78
