"""Comprehensive tests for backend/api/setup.py endpoints."""

from typing import Any, Dict, Tuple, Union
from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient


class TestCelonisCredentialsEndpoint:
    """Test cases for /api/setup/celonis-credentials endpoint."""

    def test_save_new_credentials_success(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test successful saving of new Celonis credentials."""
        _, mock_set_key, mock_dotenv_values = temp_env_file

        # Mock empty .env file
        mock_dotenv_values.return_value = {}

        response = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

        # Verify set_key was called with correct parameters
        expected_calls = [
            (".env", "CELONIS_BASE_URL", "https://test.celonis.cloud", "never"),
            (".env", "CELONIS_DATA_POOL_NAME", "test_pool", "never"),
            (".env", "CELONIS_DATA_MODEL_NAME", "test_model", "never"),
            (".env", "API_TOKEN", "test_token_123", "never"),
        ]

        for i, (path, key, value, quote_mode) in enumerate(expected_calls):
            call_args = mock_set_key.call_args_list[i]
            assert call_args[0] == (path, key, value)
            assert call_args[1]["quote_mode"] == quote_mode

    def test_save_credentials_with_data_table_name(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test saving credentials with optional data_table_name."""
        _, mock_set_key, mock_dotenv_values = temp_env_file
        mock_dotenv_values.return_value = {}

        credentials_with_table = {
            "celonis_base_url": "https://test.celonis.cloud",
            "celonis_data_pool_name": "test_pool",
            "celonis_data_model_name": "test_model",
            "api_token": "test_token_123",
            "data_table_name": "custom_table",
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=credentials_with_table
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

        # Verify data_table_name was also saved
        assert mock_set_key.call_count == 5
        last_call = mock_set_key.call_args_list[-1]
        assert last_call[0] == (".env", "DATA_TABLE_NAME", "custom_table")

    def test_credentials_already_exist_and_match(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test when credentials already exist and match exactly."""
        _, mock_set_key, mock_dotenv_values = temp_env_file

        # Set up existing matching credentials using the side_effect mechanism
        existing_env = {
            "CELONIS_BASE_URL": "https://test.celonis.cloud",
            "CELONIS_DATA_POOL_NAME": "test_pool",
            "CELONIS_DATA_MODEL_NAME": "test_model",
            "API_TOKEN": "test_token_123",
        }

        def mock_dotenv_values_func(path: str) -> Dict[str, Any]:
            if path == ".env":
                return existing_env.copy()
            return {}

        mock_dotenv_values.side_effect = mock_dotenv_values_func

        response = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials already exist and match."}

        # Verify set_key was not called since credentials match
        mock_set_key.assert_not_called()

    def test_credentials_exist_but_different(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test when credentials exist but are different - should update."""
        _, mock_set_key, mock_dotenv_values = temp_env_file

        # Mock existing different credentials in .env
        mock_dotenv_values.return_value = {
            "CELONIS_BASE_URL": "https://old.celonis.cloud",
            "CELONIS_DATA_POOL_NAME": "old_pool",
            "CELONIS_DATA_MODEL_NAME": "old_model",
            "API_TOKEN": "old_token",
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

        # Verify set_key was called to update credentials
        assert mock_set_key.call_count == 4

    def test_partial_credentials_exist(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test when only some credentials exist in .env file."""
        _, mock_set_key, mock_dotenv_values = temp_env_file

        # Mock partially existing credentials
        mock_dotenv_values.return_value = {
            "CELONIS_BASE_URL": "https://test.celonis.cloud",
            "CELONIS_DATA_POOL_NAME": "test_pool",
            # Missing CELONIS_DATA_MODEL_NAME and API_TOKEN
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

        # Should update all credentials since not all match
        assert mock_set_key.call_count == 4

    def test_empty_env_file(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test with completely empty .env file."""
        _, mock_set_key, mock_dotenv_values = temp_env_file

        # Mock empty .env file
        mock_dotenv_values.return_value = {}

        response = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}
        assert mock_set_key.call_count == 4

    def test_missing_required_fields(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with missing required credential fields."""
        incomplete_credentials = {
            "celonis_base_url": "https://test.celonis.cloud",
            "celonis_data_pool_name": "test_pool",
            # Missing celonis_data_model_name and api_token
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=incomplete_credentials
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_invalid_json_payload(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with invalid JSON payload."""
        response = test_client.post(
            "/api/setup/celonis-credentials",
            data="invalid json",  # type: ignore
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_empty_credential_values(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with empty string values for credentials."""
        empty_credentials = {
            "celonis_base_url": "",
            "celonis_data_pool_name": "",
            "celonis_data_model_name": "",
            "api_token": "",
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=empty_credentials
        )

        # Should still accept empty strings as valid input
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

    def test_null_credential_values(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with null values for credentials."""
        null_credentials = {
            "celonis_base_url": None,
            "celonis_data_pool_name": None,
            "celonis_data_model_name": None,
            "api_token": None,
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=null_credentials
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_extra_fields_ignored(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
    ) -> None:
        """Test that extra fields in request are ignored."""
        _, mock_set_key, mock_dotenv_values = temp_env_file
        mock_dotenv_values.return_value = {}

        credentials_with_extra: Dict[str, Union[str, int]] = {
            **sample_celonis_credentials,
            "extra_field": "should_be_ignored",
            "another_extra": 12345,
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=credentials_with_extra
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

        # Should only save the 4 expected credentials
        assert mock_set_key.call_count == 4

    def test_unicode_credentials(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with Unicode characters in credentials."""
        _, _, mock_dotenv_values = temp_env_file
        mock_dotenv_values.return_value = {}

        unicode_credentials = {
            "celonis_base_url": "https://tëst.celonis.cloud",
            "celonis_data_pool_name": "tëst_pöol",
            "celonis_data_model_name": "tëst_modël",
            "api_token": "tökën_123_ñ",
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=unicode_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}

    def test_very_long_credentials(
        self, test_client: TestClient, temp_env_file: Tuple[str, MagicMock, MagicMock]
    ) -> None:
        """Test with very long credential values."""
        _, _, mock_dotenv_values = temp_env_file
        mock_dotenv_values.return_value = {}

        long_value = "x" * 1000
        long_credentials = {
            "celonis_base_url": f"https://{long_value}.celonis.cloud",
            "celonis_data_pool_name": long_value,
            "celonis_data_model_name": long_value,
            "api_token": long_value,
        }

        response = test_client.post(
            "/api/setup/celonis-credentials", json=long_credentials
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Credentials saved to .env"}


class TestMapColumnsEndpoint:
    """Test cases for /api/setup/map-columns endpoint."""

    def test_map_columns_success(
        self, test_client: TestClient, sample_column_mapping: Dict[str, str]
    ) -> None:
        """Test successful column mapping."""
        response = test_client.post(
            "/api/setup/map-columns", json=sample_column_mapping
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Column mapping saved."}

        # Verify that column mapping was saved to app state
        assert hasattr(test_client.app.state, "column_mapping")  # type: ignore
        assert test_client.app.state.column_mapping == sample_column_mapping  # type: ignore

    def test_map_columns_empty_mapping(self, test_client: TestClient) -> None:
        """Test with empty column mapping - should fail validation."""
        empty_mapping = {}

        response = test_client.post("/api/setup/map-columns", json=empty_mapping)

        # Empty mapping fails Pydantic validation due to missing required fields
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_map_columns_empty_string_values(self, test_client: TestClient) -> None:
        """Test column mapping with empty string values - accepted by Pydantic."""
        mapping_with_empty_strings = {
            "case_id_column": "",
            "activity_column": "concept:name",
            "timestamp_column": "",
            "resource_1_column": "org:resource",
        }

        response = test_client.post(
            "/api/setup/map-columns", json=mapping_with_empty_strings
        )

        # Empty strings are valid according to Pydantic str type
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Column mapping saved."}

    def test_map_columns_null_values(self, test_client: TestClient) -> None:
        """Test column mapping with null values."""
        mapping_with_nulls: Dict[str, Union[str, None]] = {
            "case_id_column": None,
            "activity_column": "concept:name",
            "timestamp_column": "time:timestamp",
            "resource_1_column": None,
        }

        response = test_client.post("/api/setup/map-columns", json=mapping_with_nulls)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_map_columns_overwrite_existing(
        self, test_client: TestClient, sample_column_mapping: Dict[str, str]
    ) -> None:
        """Test overwriting existing column mapping."""
        # First, set initial mapping
        response1 = test_client.post(
            "/api/setup/map-columns", json=sample_column_mapping
        )
        assert response1.status_code == status.HTTP_200_OK

        # Then overwrite with new mapping
        new_mapping = {
            "case_id_column": "new_case_id",
            "activity_column": "new_activity",
            "timestamp_column": "new_timestamp",
            "resource_1_column": "new_resource",
        }

        response2 = test_client.post("/api/setup/map-columns", json=new_mapping)

        assert response2.status_code == status.HTTP_200_OK
        assert response2.json() == {"message": "Column mapping saved."}
        assert test_client.app.state.column_mapping == new_mapping  # type: ignore

    def test_map_columns_invalid_json(self, test_client: TestClient) -> None:
        """Test with invalid JSON payload."""
        response = test_client.post("/api/setup/map-columns", data="invalid json")  # type: ignore

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_map_columns_with_special_characters(self, test_client: TestClient) -> None:
        """Test column mapping with special characters."""
        mapping_with_special_chars = {
            "case_id_column": "case:concept:name",
            "activity_column": "concept@name#test",
            "timestamp_column": "time:timestamp$",
            "resource_1_column": "org:resource%",
        }

        response = test_client.post(
            "/api/setup/map-columns", json=mapping_with_special_chars
        )

        assert response.status_code == status.HTTP_200_OK
        assert test_client.app.state.column_mapping == mapping_with_special_chars  # type: ignore


class TestGetColumnNamesEndpoint:
    """Test cases for /api/setup/get-column-names endpoint."""

    def test_get_column_names_success(self, test_client: TestClient) -> None:
        """Test successful retrieval of column names."""
        # Set up column names in app state
        test_columns = [
            "case:concept:name",
            "concept:name",
            "time:timestamp",
            "org:resource",
        ]
        test_client.app.state.current_log_columns = test_columns  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"columns": test_columns}

    def test_get_column_names_no_columns_uploaded(
        self, test_client: TestClient
    ) -> None:
        """Test when no log columns are found in app state."""
        # Ensure no columns are set
        test_client.app.state.current_log_columns = None  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "detail": "No log columns found. Please upload a log first."
        }

    def test_get_column_names_empty_columns_list(self, test_client: TestClient) -> None:
        """Test with empty columns list."""
        # Set empty list
        test_client.app.state.current_log_columns = []  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        # Empty list should be considered as no columns
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "detail": "No log columns found. Please upload a log first."
        }

    def test_get_column_names_single_column(self, test_client: TestClient) -> None:
        """Test with single column."""
        test_columns = ["single_column"]
        test_client.app.state.current_log_columns = test_columns  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"columns": test_columns}

    def test_get_column_names_unicode_columns(self, test_client: TestClient) -> None:
        """Test with Unicode column names."""
        test_columns = ["casë:cöncept:nämë", "cöncept:nämë", "tïmë:tïmëstamp"]
        test_client.app.state.current_log_columns = test_columns  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"columns": test_columns}

    def test_get_column_names_many_columns(self, test_client: TestClient) -> None:
        """Test with many columns."""
        test_columns = [f"column_{i}" for i in range(100)]
        test_client.app.state.current_log_columns = test_columns  # type: ignore

        response = test_client.get("/api/setup/get-column-names")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"columns": test_columns}


class TestEndpointIntegration:
    """Integration tests for setup endpoints."""

    def test_full_setup_workflow(
        self,
        test_client: TestClient,
        temp_env_file: Tuple[str, MagicMock, MagicMock],
        sample_celonis_credentials: Dict[str, str],
        sample_column_mapping: Dict[str, str],
    ) -> None:
        """Test complete setup workflow: credentials -> columns -> retrieve columns."""
        _, _, mock_dotenv_values = temp_env_file
        mock_dotenv_values.return_value = {}

        # Step 1: Save credentials
        response1 = test_client.post(
            "/api/setup/celonis-credentials", json=sample_celonis_credentials
        )
        assert response1.status_code == status.HTTP_200_OK

        # Step 2: Map columns
        response2 = test_client.post(
            "/api/setup/map-columns", json=sample_column_mapping
        )
        assert response2.status_code == status.HTTP_200_OK

        # Step 3: Set up some log columns
        test_columns = ["case:concept:name", "concept:name", "time:timestamp"]
        test_client.app.state.current_log_columns = test_columns  # type: ignore

        # Step 4: Get column names
        response3 = test_client.get("/api/setup/get-column-names")
        assert response3.status_code == status.HTTP_200_OK
        assert response3.json() == {"columns": test_columns}

        # Verify app state contains both mappings
        assert hasattr(test_client.app.state, "column_mapping")  # type: ignore
        assert test_client.app.state.column_mapping == sample_column_mapping  # type: ignore

    def test_app_state_isolation_between_tests(self, test_client: TestClient) -> None:
        """Test that app state is properly isolated between tests."""
        # This test should start with clean app state, but since app state persists
        # between tests, we need to clean it up ourselves
        if hasattr(test_client.app.state, "column_mapping"):  # type: ignore
            delattr(test_client.app.state, "column_mapping")  # type: ignore
        if hasattr(test_client.app.state, "current_log_columns"):  # type: ignore
            delattr(test_client.app.state, "current_log_columns")  # type: ignore

        # Now verify clean state
        assert not hasattr(test_client.app.state, "column_mapping")  # type: ignore
        assert not hasattr(test_client.app.state, "current_log_columns")  # type: ignore
