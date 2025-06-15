"""Comprehensive tests for backend/api/log.py endpoints."""

import io
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest
from fastapi import status
from fastapi.testclient import TestClient


class TestUploadLogEndpoint:
    """Test cases for /api/logs/upload-log endpoint."""

    def test_upload_csv_file_success(self, test_client: TestClient) -> None:
        """Test successful CSV file upload."""
        csv_content = "case_id,activity,timestamp\n1,A,2023-01-01\n1,B,2023-01-02"
        csv_file = io.BytesIO(csv_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame(
                {
                    "case_id": [1, 1],
                    "activity": ["A", "B"],
                    "timestamp": ["2023-01-01", "2023-01-02"],
                }
            )
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/test_file.csv"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("test.csv", csv_file, "text/csv")},
                )

                assert response.status_code == status.HTTP_201_CREATED
                assert response.json() == {
                    "columns": ["case_id", "activity", "timestamp"]
                }

                # Verify app state was updated
                assert test_client.app.state.current_log == "/tmp/test_file.csv"  # type: ignore
                assert test_client.app.state.current_log_columns == [  # type: ignore
                    "case_id",
                    "activity",
                    "timestamp",
                ]

    def test_upload_xes_file_success(self, test_client: TestClient) -> None:
        """Test successful XES file upload."""
        xes_content = b"<?xml version='1.0' encoding='UTF-8'?><log></log>"
        xes_file = io.BytesIO(xes_content)

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame(
                {
                    "case:concept:name": [1],
                    "concept:name": ["A"],
                    "time:timestamp": ["2023-01-01"],
                }
            )
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/test_file.xes"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("test.xes", xes_file, "application/xml")},
                )

                assert response.status_code == status.HTTP_201_CREATED
                assert response.json() == {
                    "columns": ["case:concept:name", "concept:name", "time:timestamp"]
                }

    def test_upload_invalid_file_type(self, test_client: TestClient) -> None:
        """Test upload with invalid file type."""
        txt_content = "This is a text file"
        txt_file = io.BytesIO(txt_content.encode())

        response = test_client.post(
            "/api/logs/upload-log", files={"file": ("test.txt", txt_file, "text/plain")}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "detail": "Invalid file type. Only .csv and .xes are allowed."
        }

    def test_upload_case_insensitive_file_extensions(
        self, test_client: TestClient
    ) -> None:
        """Test that file extensions are case-insensitive."""
        csv_content = "case_id,activity\n1,A"
        csv_file = io.BytesIO(csv_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame({"case_id": [1], "activity": ["A"]})
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/test_file.CSV"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("test.CSV", csv_file, "text/csv")},
                )

                assert response.status_code == status.HTTP_201_CREATED

    def test_upload_file_processing_error(self, test_client: TestClient) -> None:
        """Test error during file processing."""
        csv_content = "invalid,csv,content"
        csv_file = io.BytesIO(csv_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_process.side_effect = ValueError("Invalid file format")

            response = test_client.post(
                "/api/logs/upload-log",
                files={"file": ("test.csv", csv_file, "text/csv")},
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {
                "detail": "Error processing file: Invalid file format"
            }

    def test_upload_empty_file(self, test_client: TestClient) -> None:
        """Test upload of empty file."""
        empty_file = io.BytesIO(b"")

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_process.side_effect = ValueError("Empty file")

            response = test_client.post(
                "/api/logs/upload-log",
                files={"file": ("test.csv", empty_file, "text/csv")},
            )

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {"detail": "Error processing file: Empty file"}

    def test_upload_large_file(self, test_client: TestClient) -> None:
        """Test upload of large file."""
        # Create a large CSV content
        large_content = "case_id,activity,timestamp\n" + "\n".join(
            [f"{i},Activity_{i},2023-01-{i % 30 + 1:02d}" for i in range(10000)]
        )
        large_file = io.BytesIO(large_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame(
                {
                    "case_id": list(range(10000)),
                    "activity": [f"Activity_{i}" for i in range(10000)],
                }
            )
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/large_file.csv"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("large.csv", large_file, "text/csv")},
                )

                assert response.status_code == status.HTTP_201_CREATED

    def test_upload_unicode_filename(self, test_client: TestClient) -> None:
        """Test upload with Unicode characters in filename."""
        csv_content = "case_id,activity\n1,A"
        csv_file = io.BytesIO(csv_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame({"case_id": [1], "activity": ["A"]})
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/tëst_fïlë.csv"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("tëst_fïlë.csv", csv_file, "text/csv")},
                )

                assert response.status_code == status.HTTP_201_CREATED

    def test_upload_multiple_dots_in_filename(self, test_client: TestClient) -> None:
        """Test upload with multiple dots in filename."""
        csv_content = "case_id,activity\n1,A"
        csv_file = io.BytesIO(csv_content.encode())

        with patch("backend.utils.file_handlers.process_file") as mock_process:
            mock_df = pd.DataFrame({"case_id": [1], "activity": ["A"]})
            mock_process.return_value = mock_df

            with patch("tempfile.NamedTemporaryFile") as mock_temp:
                mock_temp_instance = MagicMock()
                mock_temp_instance.name = "/tmp/test.backup.csv"
                mock_temp.return_value = mock_temp_instance

                response = test_client.post(
                    "/api/logs/upload-log",
                    files={"file": ("test.backup.csv", csv_file, "text/csv")},
                )

                assert response.status_code == status.HTTP_201_CREATED

    def test_upload_file_no_filename(self, test_client: TestClient) -> None:
        """Test upload with no filename provided."""
        csv_content = "case_id,activity\n1,A"
        csv_file = io.BytesIO(csv_content.encode())

        response = test_client.post(
            "/api/logs/upload-log",
            files={"file": ("", csv_file, "text/csv")},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCommitLogToCelonisEndpoint:
    """Test cases for /api/logs/commit-log-to-celonis endpoint."""

    def test_commit_csv_log_success(self, test_client: TestClient) -> None:
        """Test successful CSV log commit to Celonis."""
        from fastapi import Request

        from backend.api.celonis import get_celonis_connection

        # Set up app state with a log file
        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        column_mapping = {
            "case_id_column": "case_id",
            "activity_column": "activity",
            "timestamp_column": "timestamp",
            "resource_1_column": "resource",
        }

        csv_content = "case_id,activity,timestamp,resource\n1,A,2023-01-01,User1\n1,B,2023-01-02,User2"

        # Mock Celonis connection
        mock_celonis = MagicMock()

        # Mock the dependency directly
        def mock_get_celonis_connection(request: Request):
            return mock_celonis

        # Override the dependency
        test_client.app.dependency_overrides[get_celonis_connection] = (  # type: ignore
            mock_get_celonis_connection
        )

        try:
            with (
                patch("os.path.exists", return_value=True),
                patch("builtins.open", mock_open(read_data=csv_content)),
                patch("backend.utils.file_handlers.process_file") as mock_process,
                patch("os.unlink") as mock_unlink,
            ):
                mock_df = pd.DataFrame(
                    {
                        "case_id": [1, 1],
                        "activity": ["A", "B"],
                        "timestamp": ["2023-01-01", "2023-01-02"],
                        "resource": ["User1", "User2"],
                    }
                )
                mock_process.return_value = mock_df

                response = test_client.post(
                    "/api/logs/commit-log-to-celonis", json=column_mapping
                )

                assert response.status_code == status.HTTP_200_OK
                assert response.json() == {"message": "Table created successfully"}

                # Verify Celonis methods were called
                mock_celonis.add_dataframe.assert_called_once()
                mock_celonis.create_table.assert_called_once()

                # Verify cleanup
                mock_unlink.assert_called_once_with("/tmp/test.csv")
                assert test_client.app.state.current_log is None  # type: ignore
                assert test_client.app.state.current_log_columns == []  # type: ignore
        finally:
            # Clean up dependency override
            test_client.app.dependency_overrides.clear()  # type: ignore

    def test_commit_xes_log_success(self, test_client: TestClient) -> None:
        """Test successful XES log commit to Celonis."""
        from fastapi import Request

        from backend.api.celonis import get_celonis_connection

        # Set up app state with an XES log file
        test_client.app.state.current_log = "/tmp/test.xes"  # type: ignore

        xes_content = b"<?xml version='1.0' encoding='UTF-8'?><log></log>"

        # Mock Celonis connection
        mock_celonis = MagicMock()

        # Mock the dependency directly
        def mock_get_celonis_connection(request: Request):
            return mock_celonis

        # Override the dependency
        test_client.app.dependency_overrides[get_celonis_connection] = (  # type: ignore
            mock_get_celonis_connection
        )

        try:
            with (
                patch("os.path.exists", return_value=True),
                patch("builtins.open", mock_open(read_data=xes_content)),
                patch("backend.utils.file_handlers.process_file") as mock_process,
                patch("os.unlink") as mock_unlink,
            ):
                mock_df = pd.DataFrame(
                    {
                        "case:concept:name": [1, 1],
                        "concept:name": ["A", "B"],
                        "time:timestamp": ["2023-01-01", "2023-01-02"],
                    }
                )
                mock_process.return_value = mock_df

                # XES files don't need column mapping
                response = test_client.post("/api/logs/commit-log-to-celonis")

                assert response.status_code == status.HTTP_200_OK
                assert response.json() == {"message": "Table created successfully"}

                # Verify Celonis methods were called
                mock_celonis.add_dataframe.assert_called_once()
                mock_celonis.create_table.assert_called_once()

                # Verify file cleanup was performed
                mock_unlink.assert_called_once_with("/tmp/test.xes")
        finally:
            # Clean up dependency override
            test_client.app.dependency_overrides.clear()  # type: ignore

    def test_commit_csv_without_column_mapping(self, test_client: TestClient) -> None:
        """Test CSV commit without required column mapping."""
        # Set up app state with a CSV log file
        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        csv_content = "case_id,activity,timestamp\n1,A,2023-01-01"

        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=csv_content)),
            patch("backend.utils.file_handlers.process_file") as mock_process,
        ):
            mock_df = pd.DataFrame(
                {"case_id": [1], "activity": ["A"], "timestamp": ["2023-01-01"]}
            )
            mock_process.return_value = mock_df

            response = test_client.post("/api/logs/commit-log-to-celonis")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {
                "detail": "Column mapping is required for CSV files."
            }

    def test_commit_no_log_file_uploaded(self, test_client: TestClient) -> None:
        """Test commit when no log file has been uploaded."""
        # Ensure no log file in app state
        test_client.app.state.current_log = None  # type: ignore

        response = test_client.post("/api/logs/commit-log-to-celonis")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "detail": "No log file found. Please upload a log first."
        }

    def test_commit_log_file_not_exists(self, test_client: TestClient) -> None:
        """Tests commit when log file path exists in state but file doesn't."""
        # Set up app state with non-existent file
        test_client.app.state.current_log = "/tmp/non_existent.csv"  # type: ignore

        with patch("os.path.exists", return_value=False):
            response = test_client.post("/api/logs/commit-log-to-celonis")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {
                "detail": "No log file found. Please upload a log first."
            }

    def test_commit_file_processing_error(self, test_client: TestClient) -> None:
        """Test commit when file processing fails."""
        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        csv_content = "invalid,content"

        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=csv_content)),
            patch("backend.utils.file_handlers.process_file") as mock_process,
        ):
            mock_process.side_effect = ValueError("Invalid file format")

            response = test_client.post("/api/logs/commit-log-to-celonis")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {
                "detail": "Error processing file: Invalid file format"
            }

    def test_commit_csv_with_timestamp_conversion(
        self, test_client: TestClient
    ) -> None:
        """Test CSV commit with timestamp conversion."""
        from fastapi import Request

        from backend.api.celonis import get_celonis_connection

        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        column_mapping = {
            "case_id_column": "case_id",
            "activity_column": "activity",
            "timestamp_column": "timestamp",
            "resource_1_column": "resource",
        }

        csv_content = (
            "case_id,activity,timestamp,resource\n1,A,2023-01-01 10:00:00,User1"
        )

        # Mock Celonis connection
        mock_celonis = MagicMock()

        # Mock the dependency directly
        def mock_get_celonis_connection(request: Request):
            return mock_celonis

        # Override the dependency
        test_client.app.dependency_overrides[get_celonis_connection] = (  # type: ignore
            mock_get_celonis_connection
        )

        try:
            with (
                patch("os.path.exists", return_value=True),
                patch("builtins.open", mock_open(read_data=csv_content)),
                patch("backend.utils.file_handlers.process_file") as mock_process,
                patch("os.unlink") as mock_unlink,
                patch("pandas.to_datetime") as mock_to_datetime,
            ):
                mock_df = pd.DataFrame(
                    {
                        "case_id": [1],
                        "activity": ["A"],
                        "timestamp": ["2023-01-01 10:00:00"],
                        "resource": ["User1"],
                    }
                )
                mock_process.return_value = mock_df
                mock_to_datetime.return_value = pd.to_datetime(["2023-01-01 10:00:00"])  # type: ignore

                response = test_client.post(
                    "/api/logs/commit-log-to-celonis", json=column_mapping
                )

                assert response.status_code == status.HTTP_200_OK

                # Verify timestamp conversion was called (it might be called multiple times during processing)
                assert mock_to_datetime.call_count >= 1

                # Verify Celonis methods were called
                mock_celonis.add_dataframe.assert_called_once()
                mock_celonis.create_table.assert_called_once()

                # Verify file cleanup was performed
                mock_unlink.assert_called_once_with("/tmp/test.csv")
        finally:
            # Clean up dependency override
            test_client.app.dependency_overrides.clear()  # type: ignore

    def test_commit_csv_invalid_column_mapping(self, test_client: TestClient) -> None:
        """Test CSV commit with invalid column mapping."""
        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        invalid_mapping = {
            "case_id_column": "case_id",
            # Missing required fields
        }

        response = test_client.post(
            "/api/logs/commit-log-to-celonis", json=invalid_mapping
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_commit_empty_log_file(self, test_client: TestClient) -> None:
        """Test commit with empty log file."""
        test_client.app.state.current_log = "/tmp/empty.csv"  # type: ignore

        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data="")),
            patch("backend.utils.file_handlers.process_file") as mock_process,
        ):
            mock_process.side_effect = ValueError("Empty file")

            response = test_client.post("/api/logs/commit-log-to-celonis")

            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.json() == {"detail": "Error processing file: Empty file"}

    def test_commit_csv_with_partial_column_mapping(
        self, test_client: TestClient
    ) -> None:
        """Test CSV commit with only required columns in mapping."""
        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        minimal_mapping = {
            "case_id_column": "case_id",
            "activity_column": "activity",
            "timestamp_column": "timestamp",
            "resource_1_column": "",  # Empty resource column
        }

        csv_content = "case_id,activity,timestamp\n1,A,2023-01-01"

        # Mock Celonis connection
        mock_celonis = MagicMock()

        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=csv_content)),
            patch("backend.utils.file_handlers.process_file") as mock_process,
            patch("os.unlink") as mock_unlink,
            patch("backend.api.log.get_celonis_connection", return_value=mock_celonis),
            patch(
                "backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager",
                return_value=mock_celonis,
            ),
        ):
            mock_df = pd.DataFrame(
                {"case_id": [1], "activity": ["A"], "timestamp": ["2023-01-01"]}
            )
            mock_process.return_value = mock_df

            response = test_client.post(
                "/api/logs/commit-log-to-celonis", json=minimal_mapping
            )

            assert response.status_code == status.HTTP_200_OK
            # Verify cleanup was performed
            mock_unlink.assert_called_once_with("/tmp/test.csv")

    def test_commit_celonis_connection_error(self, test_client: TestClient) -> None:
        """Test commit when Celonis connection fails."""
        from fastapi import Request

        from backend.api.celonis import get_celonis_connection

        test_client.app.state.current_log = "/tmp/test.csv"  # type: ignore

        column_mapping = {
            "case_id_column": "case_id",
            "activity_column": "activity",
            "timestamp_column": "timestamp",
            "resource_1_column": "resource",
        }

        csv_content = "case_id,activity,timestamp,resource\n1,A,2023-01-01,User1"

        # Mock the dependency to raise an exception
        def mock_get_celonis_connection(request: Request):
            raise Exception("Connection failed")

        # Override the dependency
        test_client.app.dependency_overrides[get_celonis_connection] = (  # type: ignore
            mock_get_celonis_connection
        )

        try:
            with (
                patch("os.path.exists", return_value=True),
                patch("builtins.open", mock_open(read_data=csv_content)),
                patch("backend.utils.file_handlers.process_file") as mock_process,
            ):
                mock_df = pd.DataFrame({"case_id": [1], "activity": ["A"]})
                mock_process.return_value = mock_df

                # The exception should be raised during the request
                with pytest.raises(Exception, match="Connection failed"):
                    test_client.post(
                        "/api/logs/commit-log-to-celonis", json=column_mapping
                    )
        finally:
            # Clean up dependency override
            test_client.app.dependency_overrides.clear()  # type: ignore
