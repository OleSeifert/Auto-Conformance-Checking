"""Test CelonisConnectionManager class."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)


@pytest.fixture
def dummy_df():
    """Create a dummy DataFrame for testing.

    :return: DataFrame with dummy data.
    """
    return pd.DataFrame(
        {
            "case:concept:name": [1, 2],
            "concept:name": ["A", "B"],
            "time:timestamp": ["2023-01-01", "2023-01-02"],
        }
    )


@pytest.fixture
def mock_acquire_api_token():
    """Create a mock acquire_api_token function for testing.

    :return: Mock acquire_api_token function.
    """
    return "mock-token"


@pytest.fixture
def mock_celonis_connection_manager():
    """Create a mock CelonisConnectionManager for testing.

    :return: Mock CelonisConnectionManager object.
    """
    with patch(
        "backend.celonis_connection.celonis_connection_manager.get_celonis"
    ) as mock_get_celonis:
        mock_celonis = MagicMock()
        mock_get_celonis.return_value = mock_celonis

        manager = CelonisConnectionManager(
            base_url="http://mock-url",
            data_pool_name="mock-pool",
            data_model_name="mock-model",
            api_token="mock-token",
        )
        return manager


def test_find_data_pool_existing(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test finding an existing data pool.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_pool = MagicMock()
    mock_data_pool.name = "mock-pool"
    mock_celonis_connection_manager.find_data_pool = MagicMock(
        return_value=mock_data_pool
    )
    result = mock_celonis_connection_manager.find_data_pool("mock-pool")
    assert result.name == "mock-pool"


def test_find_data_pool_non_existing(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test finding a non-existing data pool.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_pool = MagicMock()
        mock_data_pool.name = "non-existing-pool"

        mock_celonis_connection_manager.celonis.data_integration.get_data_pools().find = MagicMock(
            side_effect=Exception("Data pool not found")
        )
        mock_celonis_connection_manager.celonis.data_integration.create_data_pool = (
            MagicMock(return_value=mock_data_pool)
        )
        result = mock_celonis_connection_manager.find_data_pool("non-existing-pool")
        assert result.name == "non-existing-pool"
        mock_celonis_connection_manager.celonis.data_integration.create_data_pool.assert_called_once_with(
            "non-existing-pool"
        )


def test_find_data_model_existing(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test finding an existing data model.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_data_model.name = "mock-model"
    mock_celonis_connection_manager.find_data_model = MagicMock(
        return_value=mock_data_model
    )
    result = mock_celonis_connection_manager.find_data_model("mock-model")
    assert result.name == "mock-model"


def test_find_data_model_non_existing(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test finding a non-existing data model.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_model = MagicMock()
        mock_data_model.name = "non-existing-model"

        mock_celonis_connection_manager.data_pool.get_data_models().find = MagicMock(
            side_effect=Exception("Data model not found")
        )
        mock_celonis_connection_manager.data_pool.create_data_model = MagicMock(
            return_value=mock_data_model
        )
        result = mock_celonis_connection_manager.find_data_model("non-existing-model")
        assert result is not None
        assert result.name == "non-existing-model"
        mock_celonis_connection_manager.data_pool.create_data_model.assert_called_once_with(
            "non-existing-model"
        )


def test_find_data_model_no_data_pool(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test finding a data model when the data pool is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_pool = None  # type: ignore
    result = mock_celonis_connection_manager.find_data_model("mock-model")
    assert result is None


def test_create_table_that_does_not_exist(
    mock_celonis_connection_manager: CelonisConnectionManager,
    dummy_df: pd.DataFrame,
):
    """Test creating a table that does not exist.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_pool = MagicMock()
        mock_data_model = MagicMock()
        mock_data_model.get_tables().find = MagicMock(
            side_effect=Exception("Table not found")
        )
        mock_celonis_connection_manager.data_model = mock_data_model
        mock_celonis_connection_manager.data_pool = mock_data_pool
        mock_celonis_connection_manager.data_frame = dummy_df
        mock_celonis_connection_manager.create_table()
        mock_data_pool.create_table.assert_called_once()
        mock_data_model.add_table.assert_called_once()
        mock_data_model.create_process_configuration.assert_called_once()
        mock_data_model.reload.assert_called_once()


def test_create_table_that_exists(
    mock_celonis_connection_manager: CelonisConnectionManager,
    dummy_df: pd.DataFrame,
):
    """Test creating a table that exists.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_pool = MagicMock()
    mock_data_model = MagicMock()
    mock_data_model.get_tables().find = MagicMock(
        return_value=MagicMock(name="mock-table")
    )
    mock_celonis_connection_manager.data_model = mock_data_model
    mock_celonis_connection_manager.data_pool = mock_data_pool
    mock_celonis_connection_manager.data_frame = dummy_df
    mock_celonis_connection_manager.create_table()
    mock_data_pool.create_table.assert_called_once()
    mock_data_model.add_table.assert_called_once()
    mock_data_model.create_process_configuration.assert_called_once()
    mock_data_model.reload.assert_called_once()


def test_create_table_no_data_pool(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test creating a table when the data pool is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_pool = None  # type: ignore
    result = mock_celonis_connection_manager.create_table()
    assert result is None


def test_create_table_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test creating a table when the data model is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.create_table()
    assert result is None


def test_create_table_no_data_frame(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test creating a table when the data frame is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    result = mock_celonis_connection_manager.create_table()
    assert result is None


def test_add_dataframe(
    mock_celonis_connection_manager: CelonisConnectionManager,
    dummy_df: pd.DataFrame,
):
    """Test adding a DataFrame to the CelonisConnectionManager.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.add_dataframe(dummy_df)
    assert mock_celonis_connection_manager.data_frame is not None
    assert mock_celonis_connection_manager.data_frame.equals(dummy_df)  # type: ignore


def test_get_basic_dataframe_from_celonis(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a basic DataFrame from Celonis.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_data_model.get_tables().find = MagicMock(
        return_value=MagicMock(name="mock-table")
    )
    mock_celonis_connection_manager.get_basic_dataframe_from_celonis = MagicMock(
        return_value=pd.DataFrame()
    )
    mock_celonis_connection_manager.data_model = mock_data_model
    result = mock_celonis_connection_manager.get_basic_dataframe_from_celonis()
    assert result is not None
    assert isinstance(result, pd.DataFrame)


def test_get_basic_dataframe_from_celonis_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a basic DataFrame from Celonis when the data model is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.get_basic_dataframe_from_celonis()
    assert result is None


def test_get_basic_dataframe_from_celonis_table_not_found(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a basic DataFrame from Celonis when the table is not found.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_model = MagicMock()
        mock_data_model.get_tables().find = MagicMock(
            side_effect=Exception("Table not found")
        )
        mock_celonis_connection_manager.data_model = mock_data_model
        result = mock_celonis_connection_manager.get_basic_dataframe_from_celonis()
        assert result is None


def test_get_dataframe_from_celonis(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a DataFrame from Celonis.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_data_model.get_tables().find = MagicMock(
        return_value=MagicMock(name="mock-table")
    )
    mock_celonis_connection_manager.get_dataframe_from_celonis = MagicMock(
        return_value=pd.DataFrame()
    )
    mock_celonis_connection_manager.data_model = mock_data_model
    result = mock_celonis_connection_manager.get_dataframe_from_celonis()
    assert result is not None
    assert isinstance(result, pd.DataFrame)


def test_get_dataframe_from_celonis_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a DataFrame from Celonis when the data model is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_query = MagicMock()
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.get_dataframe_from_celonis(
        pql_query=mock_query
    )
    assert result is None


def test_get_dataframe_from_celonis_no_pql_query(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a DataFrame from Celonis when the PQL query is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = MagicMock()
    result = mock_celonis_connection_manager.get_dataframe_from_celonis(pql_query=None)  # type: ignore
    assert result is None


def test_get_table_that_exists(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a table that exists.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_data_model.get_tables().find = MagicMock(
        return_value=MagicMock(name="mock-table")
    )
    mock_celonis_connection_manager.data_model = mock_data_model
    result = mock_celonis_connection_manager.get_table("mock-table")
    assert result is not None
    assert isinstance(result, MagicMock)


def test_get_table_that_does_not_exist(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a table that does not exist.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_model = MagicMock()
        mock_data_model.get_tables().find = MagicMock(
            side_effect=Exception("Table not found")
        )
        mock_celonis_connection_manager.data_model = mock_data_model
        result = mock_celonis_connection_manager.get_table("non-existing-table")
        assert result is None


def test_get_table_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting a table when the data model is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.get_table("mock-table")
    assert result is None


def test_get_table_columns(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting table columns.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_data_model.get_tables().find = MagicMock(
        return_value=MagicMock(name="mock-table")
    )
    table = MagicMock()
    table.get_columns = MagicMock(return_value=MagicMock(name="mock-columns"))
    mock_celonis_connection_manager.data_model = mock_data_model
    result = mock_celonis_connection_manager.get_table_columns("mock-table")
    assert result is not None
    assert isinstance(result, MagicMock)


def test_get_table_columns_table_not_found(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting table columns when the table is not found.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    with pytest.raises(Exception):
        mock_data_model = MagicMock()
        mock_data_model.get_tables().find = MagicMock(
            side_effect=Exception("Table not found")
        )
        mock_celonis_connection_manager.data_model = mock_data_model
        result = mock_celonis_connection_manager.get_table_columns("non-existing-table")
        assert result is None


def test_get_table_columns_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting table columns when the data model is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.get_table_columns("mock-table")
    assert result is None


def test_get_data_pool(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting the data pool.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_pool = MagicMock()
    mock_celonis_connection_manager.data_pool = mock_data_pool
    result = mock_celonis_connection_manager.get_data_pool()
    assert result is not None
    assert isinstance(result, MagicMock)


def test_get_data_pool_no_data_pool(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting the data pool when it is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_pool = None  # type: ignore
    result = mock_celonis_connection_manager.get_data_pool()
    assert result is None


def test_get_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting the data model.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_data_model = MagicMock()
    mock_celonis_connection_manager.data_model = mock_data_model
    result = mock_celonis_connection_manager.get_data_model()
    assert result is not None
    assert isinstance(result, MagicMock)


def test_get_data_model_no_data_model(
    mock_celonis_connection_manager: CelonisConnectionManager,
):
    """Test getting the data model when it is None.

    :param mock_celonis_connection_manager: Mock
        CelonisConnectionManager object.
    """
    mock_celonis_connection_manager.data_model = None  # type: ignore
    result = mock_celonis_connection_manager.get_data_model()
    assert result is None
