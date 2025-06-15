"""Test utilities and fixtures for API testing."""

import os
import tempfile
from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from fastapi import Request
from fastapi.testclient import TestClient

from backend.api.celonis import get_celonis_connection
from backend.main import app


class MockCelonisConnectionManager:
    """Simple mock for CelonisConnectionManager that avoids HTTP calls."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize mock with minimal setup."""
        self.data_frame = pd.DataFrame()
        self.add_dataframe = MagicMock()
        self.create_table = MagicMock()
        self.get_basic_dataframe_from_celonis = MagicMock()
        self.get_dataframe_with_resource_group_from_celonis = MagicMock()
        self.get_dataframe_from_celonis = MagicMock()


def mock_get_celonis_connection(request: Request) -> MockCelonisConnectionManager:
    """Mock dependency injection function for get_celonis_connection."""
    return MockCelonisConnectionManager()


@pytest.fixture
def mock_celonis_manager():
    """Create a mock CelonisConnectionManager instance for direct use."""
    return MockCelonisConnectionManager()


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as client:
        app.dependency_overrides[get_celonis_connection] = mock_get_celonis_connection
        yield client
        app.dependency_overrides.clear()


@pytest.fixture
def sample_celonis_credentials():
    """Sample Celonis credentials for testing."""
    return {
        "celonis_base_url": "https://test.celonis.cloud",
        "celonis_data_pool_name": "test_pool",
        "celonis_data_model_name": "test_model",
        "api_token": "test_token_123",
    }


@pytest.fixture
def sample_column_mapping():
    """Sample column mapping for testing."""
    return {
        "case_id_column": "case:concept:name",
        "activity_column": "concept:name",
        "timestamp_column": "time:timestamp",
        "resource_1_column": "org:resource",
    }


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
        temp_path = f.name

    # Patch the .env file path to use our temporary file
    with (
        patch("backend.api.setup.set_key") as mock_set_key,
        patch("backend.api.setup.dotenv_values") as mock_dotenv_values,
    ):
        # Store original env content
        original_env: Dict[str, str] = {}

        def mock_set_key_func(
            path: str, key: str, value: str, quote_mode: Optional[str] = None
        ) -> None:
            if path == ".env":
                original_env[key] = value

        def mock_dotenv_values_func(path: str) -> Dict[str, str]:
            if path == ".env":
                return original_env.copy()
            return {}

        mock_set_key.side_effect = mock_set_key_func
        mock_dotenv_values.side_effect = mock_dotenv_values_func

        yield temp_path, mock_set_key, mock_dotenv_values

    # Cleanup
    try:
        os.unlink(temp_path)
    except FileNotFoundError:
        pass
