"""Tests for the Temporal Profile Router."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.api.models.schemas.job_models import JobStatus
from backend.conformance_checking.temporal_profile import ConformanceResultType


class TestComputeTemporalProfileEndpoint:
    """Tests for the api/temporal-profile/compute-result endpoint."""

    def test_compute_temporal_conformance_result(self, test_client: TestClient):
        """Test successful job ID creation for temporal conformance."""
        with patch(
            "backend.api.tasks.temporal_profile_tasks.compute_and_store_temporal_conformance_result"
        ) as mock_task:
            mock_task.return_value = None
            response = test_client.post(
                "/api/temporal-profile/compute-result", params={"zeta": 0.5}
            )

            assert response.status_code == 202
            assert "job_id" in response.json()
            assert isinstance(response.json()["job_id"], str)
            assert len(response.json()["job_id"]) > 0


class TestGetTemporalConformanceResultEndpoint:
    """Tests for the api/temporal-profile/get-result endpoint."""

    def test_get_temporal_conformance_result_success(self, test_client: TestClient):
        """Test successful retrieval of temporal conformance result."""
        dummy_conformance_result: ConformanceResultType = [
            [
                ("activity_a", "activity_b", 5.0, 1.5),
                ("activity_b", "activity_c", 3.0, 0.5),
                ("activity_c", "activity_d", 2.0, 0.0),
                ("activity_d", "activity_e", 4.0, 1.0),
            ],
            [
                ("activity_a", "activity_b", 6.0, 2.0),
                ("activity_b", "activity_c", 4.0, 1.0),
            ],
        ]

        test_client.app.state.jobs = {  # type: ignore
            "test_job_id": JobStatus(
                module="temporal",
                status="complete",
                result={
                    "temporal_conformance_result": dummy_conformance_result,
                },
            )
        }

        response = test_client.get("/api/temporal-profile/get-result/test_job_id")

        assert response.status_code == 200
        response_data = response.json()

        assert "graphs" in response_data
        assert "tables" in response_data

        assert len(response_data["graphs"]) == 1
        assert len(response_data["tables"]) == 1

    def test_get_temporal_conformance_result_job_belongs_to_different_module(
        self, test_client: TestClient
    ):
        """Test temporal result retrieval with different module's job ID."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="resource_based",
                status="complete",
                result={},
            )
        }

        response = test_client.get("/api/temporal-profile/get-result/job_id")
        assert response.status_code == 400
        assert response.json() == {"detail": "Job ID belongs to a different module"}

    def test_get_temporal_conformance_result_missing_result(
        self, test_client: TestClient
    ):
        """Test temporal conformance result retrieval with missing result."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result=None,
            )
        }

        response = test_client.get("/api/temporal-profile/get-result/job_id")
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Job 'job_id' is complete, but result data is missing internally."
        }

    def test_get_temporal_conformance_result_data_not_found(
        self, test_client: TestClient
    ):
        """Test retrieval of temporal conformance result with no data found."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={"temporal_conformance_result": None},
            )
        }

        response = test_client.get("/api/temporal-profile/get-result/job_id")
        assert response.status_code == 404
        assert response.json() == {
            "detail": "Temporal conformance result data not found for completed job 'job_id'."
        }

    def test_get_temporal_conformance_result_empty_data(self, test_client: TestClient):
        """Test retrieval of temporal conformance result with empty data."""
        test_client.app.state.jobs = {  # type: ignore
            "job_id": JobStatus(
                module="temporal",
                status="complete",
                result={"temporal_conformance_result": []},
            )
        }

        response = test_client.get("/api/temporal-profile/get-result/job_id")
        assert response.status_code == 200
        assert response.json() == {"tables": [], "graphs": []}
