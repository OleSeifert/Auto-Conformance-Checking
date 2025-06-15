"""Tests the Log Skeleton Router."""

import uuid

import pandas as pd
import pytest
from pytest_mock import MockerFixture

import backend.api.modules.log_skeleton_router as log_skeleton_router
from backend.api.models.schemas.job_models import JobStatus
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)
from backend.main import app

# **************** Fixtures for testing ****************


@pytest.fixture
def fake_celonis_manager(mocker: MockerFixture):
    """Creates a fake CelonisConnectionManager for testing."""
    manager = mocker.create_autospec(
        CelonisConnectionManager,
        instance=True,
        spec_set=True,
        name="CelonisConnectionManager",
    )
    yield manager


@pytest.fixture
def client(mocker: MockerFixture, fake_celonis_manager):
    """Creates a fake FastAPI client for testing."""
    app.dependency_overrides[log_skeleton_router.get_celonis_connection] = (
        lambda: fake_celonis_manager
    )
    from fastapi.testclient import TestClient

    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.fixture
def fake_uuid():
    """Creates a fake UUID for testing."""
    return str(uuid.UUID("12345678-1234-5678-1234-567812345678"))


@pytest.fixture
def rows():
    """Creates a fixture for equivalence rows."""
    return [["A", "B"], ["C", "D"]]


@pytest.fixture
def populate_equivalence_job(client, fake_uuid, rows):
    """Creates a finished job with equivalence rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"equivalence": rows},
        )
    }


@pytest.fixture
def populate_always_after_job(client, fake_uuid, rows):
    """Creates a finished job with always after rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"always_after": rows},
        )
    }


@pytest.fixture
def populate_always_before_job(client, fake_uuid, rows):
    """Creates a finished job with always before rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"always_before": rows},
        )
    }


@pytest.fixture
def populate_never_together_job(client, fake_uuid, rows):
    """Creates a finished job with never together rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"never_together": rows},
        )
    }


@pytest.fixture
def populate_directly_follows_job(client, fake_uuid, rows):
    """Creates a finished job with directly follows rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"directly_follows": rows},
        )
    }


@pytest.fixture
def populate_activity_frequencies_job(client, fake_uuid, rows):
    """Creates a finished job with activity frequencies rows."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"activ_freq": {"hello": {1, 2, 3}, "world": {4, 5, 6}}},
        )
    }


# **************** Tests ****************

# ******** Tests for compute_log_skeleton ********


def test_compute_log_skeleton(client, mocker, fake_celonis_manager, fake_uuid) -> None:
    """Tests the compute_log_skeleton endpoint."""
    mocker.patch(
        "backend.api.modules.log_skeleton_router.uuid.uuid4", return_value=fake_uuid
    )

    dummy_task = mocker.Mock(name="dummy_task")
    mocker.patch(
        "backend.api.modules.log_skeleton_router.compute_and_store_log_skeleton",
        dummy_task,
    )

    app_state = client.app.state
    app_state.jobs = {}

    response = client.post("/api/log-skeleton/compute-skeleton")

    # Assert HTTP calls
    assert response.status_code == 202
    assert response.json() == {"job_id": fake_uuid}

    # Assert side effects
    job = app.state.jobs[fake_uuid]
    assert job.module == log_skeleton_router.MODULE_NAME
    assert job.status == "pending"

    dummy_task.assert_called_once_with(client.app, fake_uuid, fake_celonis_manager)


# ******** Tests for get_equivalence ********


def test_get_equivalence_okay(client, fake_uuid, populate_equivalence_job, rows):
    """Tests the get_equivalence endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_equivalence/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [{"headers": ["Activity A", "Activity B"], "rows": rows}],
        "graphs": [],
    }


def test_get_equivalence_empty(client, fake_uuid):
    """Tests the get_equivalence endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"equivalence": []},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_equivalence/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# ******** Tests for get_equivalence PQL ********


def test_get_equivalence_pql_okay(client, mocker):
    """Tests the get_equivalence_pql endpoint with valid data."""
    # Patch the helper functions
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_equivalance_relation",
        return_value=_equiv_df(),
    )
    mocker.patch(
        "backend.api.modules.log_skeleton_router.general_queries.get_activities",
        return_value=pd.DataFrame(
            {"Activity": ["A", "B", "C"], "Activity Count": [10, 20, 30]}
        ),
    )

    # Call the endpoint
    response = client.get("/api/log-skeleton/get_equivalence")
    assert response.status_code == 200
    body = response.json()

    # Expected structures
    expected_table = {
        "headers": [
            "Activity A",
            "Activity B",
        ],
        "rows": [["A", "B"]],
    }

    expected_graph = {
        "nodes": [{"id": act} for act in ["A", "B", "C"]],
        "edges": [{"from": "A", "to": "B", "label": "equals_to"}],
    }

    assert body == {"tables": [expected_table], "graphs": [expected_graph]}


def test_get_equivalence_pql_empty(client, mocker):
    """Tests the get_equivalence_pql endpoint with no data."""
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_equivalance_relation",
        return_value=pd.DataFrame(columns=["Activity A", "Activity B", "Rel"]),
    )

    response = client.get("/api/log-skeleton/get_equivalence/")
    assert response.status_code == 200
    assert response.json() == {"tables": [], "graphs": []}


# ******** Tests for get_always_after ********


def test_get_always_after_okay(client, rows, populate_always_after_job, fake_uuid):
    """Tests the get_always_after endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_always_after/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [
            {
                "headers": ["Activity A", "Always After Activity B"],
                "rows": rows,
            }
        ],
        "graphs": [],
    }


def test_get_always_after_empty(client, fake_uuid):
    """Tests the get_always_after endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"always_after": []},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_always_after/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# ******** Tests for get_always_after PQL ********


def test_get_always_after_pql_okay(client, mocker):
    """Tests the get_always_after_pql endpoint with valid data."""
    # Patch the helper functions
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_always_after_relation",
        return_value=_always_after_df(),
    )
    mocker.patch(
        "backend.api.modules.log_skeleton_router.general_queries.get_activities",
        return_value=pd.DataFrame(
            {"Activity": ["A", "B", "C"], "Activity Count": [10, 20, 30]}
        ),
    )

    # Call the endpoint
    response = client.get("/api/log-skeleton/get_always_after")
    assert response.status_code == 200
    body = response.json()

    # Expected structures
    expected_table = {
        "headers": [
            "Activity A",
            "Activity B always after A",
        ],
        "rows": [["A", "B"]],
    }
    expected_graph = {
        "nodes": [{"id": act} for act in ["A", "B", "C"]],
        "edges": [{"from": "A", "to": "B", "label": "always_after"}],
    }

    assert body == {"tables": [expected_table], "graphs": [expected_graph]}


def test_get_always_after_pql_empty(client, mocker):
    """Tests the get_always_after_pql endpoint with no data."""
    # Patch the helper function
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_always_after_relation",
        return_value=pd.DataFrame(
            columns=["Activity A", "Activity B always after A", "Rel"]
        ),
    )

    response = client.get("/api/log-skeleton/get_always_after/")
    assert response.status_code == 200
    assert response.json() == {"tables": [], "graphs": []}


# ******** Tests for get_always_before ********


def test_get_always_before_okay(client, fake_uuid, populate_always_before_job, rows):
    """Tests the get_always_before endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_always_before/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [
            {
                "headers": ["Activity A", "Always Before Activity B"],
                "rows": rows,
            }
        ],
        "graphs": [],
    }


def test_get_always_before_empty(client, fake_uuid):
    """Tests the get_always_before endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"always_before": []},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_always_before/{fake_uuid}")
    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# ******** Tests for get_always_before PQL ********


def test_get_always_before_pql_okay(client, mocker):
    """Tests the get_always_before_pql endpoint with valid data."""
    # Patch the helper functions
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_always_before_relation",
        return_value=_always_before_df(),
    )
    mocker.patch(
        "backend.api.modules.log_skeleton_router.general_queries.get_activities",
        return_value=pd.DataFrame(
            {"Activity": ["A", "B", "C"], "Activity Count": [10, 20, 30]}
        ),
    )

    # Call the endpoint
    response = client.get("/api/log-skeleton/get_always_before")
    assert response.status_code == 200
    body = response.json()

    # Expected structures
    expected_table = {
        "headers": [
            "Activity A always before",
            "Activity B",
        ],
        "rows": [["A", "B"]],
    }
    expected_graph = {
        "nodes": [{"id": act} for act in ["A", "B", "C"]],
        "edges": [{"from": "A", "to": "B", "label": "always_before"}],
    }
    assert body == {"tables": [expected_table], "graphs": [expected_graph]}


def test_get_always_before_pql_empty(client, mocker):
    """Tests the get_always_before_pql endpoint with no data."""
    # Patch the helper function
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_always_before_relation",
        return_value=pd.DataFrame(
            columns=["Activity A always before", "Activity B", "Rel"]
        ),
    )

    response = client.get("/api/log-skeleton/get_always_before/")
    assert response.status_code == 200
    assert response.json() == {"tables": [], "graphs": []}


# ******** Tests for get_never_together ********


def test_get_never_together_okay(client, fake_uuid, populate_never_together_job, rows):
    """Tests the get_never_together endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_never_together/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [
            {
                "headers": ["Activity A", "Activity B (Never Together)"],
                "rows": rows,
            }
        ],
        "graphs": [],
    }


def test_get_never_together_empty(client, fake_uuid):
    """Tests the get_never_together endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"never_together": []},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_never_together/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# ******** Tests for get_never_together PQL ********


def test_get_never_together_pql_okay(client, mocker):
    """Tests the get_never_together_pql endpoint with valid data."""
    # Path the helper functions
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_never_together_relation",
        return_value=pd.DataFrame(
            {
                "Activity A": ["A", "B"],
                "Activity B": ["B", "C"],
                "Rel": ["true", "false"],
            }
        ),
    )
    mocker.patch(
        "backend.api.modules.log_skeleton_router.general_queries.get_activities",
        return_value=pd.DataFrame(
            {"Activity": ["A", "B", "C"], "Activity Count": [10, 20, 30]}
        ),
    )

    # Call the endpoint
    response = client.get("/api/log-skeleton/get_never_together")
    assert response.status_code == 200
    body = response.json()

    # Expected structures
    expected_table = {
        "headers": [
            "Activity A",
            "Activity B",
        ],
        "rows": [["A", "B"]],
    }
    expected_graph = {
        "nodes": [{"id": act} for act in ["A", "B", "C"]],
        "edges": [{"from": "A", "to": "B", "label": "never_together"}],
    }
    assert body == {"tables": [expected_table], "graphs": [expected_graph]}


def test_get_never_together_pql_empty(client, mocker):
    """Tests the get_never_together_pql endpoint with no data."""
    # Patch the helper function
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_never_together_relation",
        return_value=pd.DataFrame(columns=["Activity A", "Activity B", "Rel"]),
    )
    response = client.get("/api/log-skeleton/get_never_together/")
    assert response.status_code == 200
    assert response.json() == {"tables": [], "graphs": []}


# ******** Tests for get_directly_follows ********


def test_get_directly_follows_okay(
    client, fake_uuid, populate_directly_follows_job, rows
):
    """Tests the get_directly_follows endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_directly_follows/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [
            {
                "headers": ["Preceding Activity", "Following Activity"],
                "rows": rows,
            }
        ],
        "graphs": [],
    }


def test_get_directly_follows_empty(client, fake_uuid):
    """Tests the get_directly_follows endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"directly_follows": []},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_directly_follows/{fake_uuid}")
    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# ******** Tests for get_directly_follows PQL ********


def test_get_directly_follows_pql_okay(client, mocker):
    """Tests the get_directly_follows_pql endpoint with valid data."""
    # Patch the helper functions
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_directly_follows_relation_and_count",
        return_value=pd.DataFrame(
            {
                "Activity A": ["A", "B"],
                "Activity B Directly-follows A": ["B", "C"],
                "Rel": ["true", "false"],
                "Count": [42, 6],
            }
        ),
    )
    mocker.patch(
        "backend.api.modules.log_skeleton_router.general_queries.get_activities",
        return_value=pd.DataFrame(
            {"Activity": ["A", "B", "C"], "Activity Count": [10, 20, 30]}
        ),
    )

    # Call the endpoint
    response = client.get("/api/log-skeleton/get_directly_follows_and_count")
    assert response.status_code == 200
    body = response.json()

    # Expected structures
    expected_table = {
        "headers": ["Activity A", "Activity B Directly-follows A", "Count"],
        "rows": [["A", "B", "42"]],
    }
    expected_graph = {
        "nodes": [{"id": act} for act in ["A", "B", "C"]],
        "edges": [{"from": "A", "to": "B", "label": "42"}],
    }
    assert body == {"tables": [expected_table], "graphs": [expected_graph]}


def test_get_directly_follows_pql_empty(client, mocker):
    """Tests the get_directly_follows_pql endpoint with no data."""
    # Patch the helper function
    mocker.patch(
        "backend.api.modules.log_skeleton_router.log_skeleton_queries.get_directly_follows_relation_and_count",
        return_value=pd.DataFrame(
            columns=["Activity A", "Activity B Directly-follows A", "Rel", "Count"]
        ),
    )

    response = client.get("/api/log-skeleton/get_directly_follows_and_count/")
    assert response.status_code == 200
    assert response.json() == {"tables": [], "graphs": []}


# ******** Test get_activity_frequencies ********


def test_get_activity_frequencies_okay(
    client,
    fake_uuid,
    populate_activity_frequencies_job,
):
    """Tests the get_activity_frequencies endpoint with valid data."""
    response = client.get(f"/api/log-skeleton/old/get_activity_frequencies/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [
            {
                "headers": ["Activity", "Frequency"],
                "rows": [["hello", "1, 2, 3"], ["world", "4, 5, 6"]],
            }
        ],
        "graphs": [],
    }


def test_get_activity_frequencies_empty(client, fake_uuid):
    """Tests the get_activity_frequencies endpoint with no data."""
    client.app.state.jobs = {
        fake_uuid: JobStatus(
            module=log_skeleton_router.MODULE_NAME,
            status="complete",
            result={"activ_freq": {}},
        )
    }

    response = client.get(f"/api/log-skeleton/old/get_activity_frequencies/{fake_uuid}")

    assert response.status_code == 200
    assert response.json() == {
        "tables": [],
        "graphs": [],
    }


# **************** Helper functions ****************


def _equiv_df() -> pd.DataFrame:
    """Returns a simple DataFrame for equivalence."""
    return pd.DataFrame(
        {
            "Activity A": ["A", "B"],
            "Activity B": ["B", "C"],
            "Rel": ["true", "false"],
        }
    )


def _always_after_df() -> pd.DataFrame:
    """Returns a simple DataFrame for always after."""
    return pd.DataFrame(
        {
            "Activity A": ["A", "B"],
            "Activity B always after A": ["B", "C"],
            "Rel": ["true", "false"],
        }
    )


def _always_before_df() -> pd.DataFrame:
    """Returns a simple DataFrame for always before."""
    return pd.DataFrame(
        {
            "Activity A always before": ["A", "B"],
            "Activity B": ["B", "C"],
            "Rel": ["true", "false"],
        }
    )
