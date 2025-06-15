"""Tests for the Resource Based Router."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.models.schemas.job_models import JobStatus


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
