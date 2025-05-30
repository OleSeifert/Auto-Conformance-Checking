"""Contains utility functions for handling file uploads."""

import io
import os
import tempfile

import pandas as pd
import pm4py  # type: ignore
import pm4py.objects.conversion.log.variants as log_variants  # type: ignore


def process_xes_file(file_content: bytes) -> pd.DataFrame:
    """Processes XES file content and converts it to a DataFrame.

    This function is needed, as the transferred file via the API is in bytes,
    and pm4py does not support reading from bytes directly. Therefore, we
    create a temporary file to store the uploaded content and then read it
    using pm4py.

    Args:
        file_content: Binary content of the XES file.

    Returns:
        A pandas DataFrame containing the event log.

    Raises:
        ValueError: If the file cannot be processed.
    """
    # Create a temporary file to store the uploaded content
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xes")
    try:
        tmp_file.write(file_content)
        tmp_file.close()  # Close the file before reading it
        tmp_path = tmp_file.name
        
        # Read the XES file using pm4py
        log = pm4py.read_xes(tmp_path)  # type: ignore

        # Check if the log is already a DataFrame, if not convert it
        if not isinstance(log, pd.DataFrame):
            # Convert the log to a DataFrame
            log = log_variants.to_data_frame.apply(log)  # type: ignore

        return log  # type: ignore
    except Exception as e:
        raise ValueError(f"Failed to process XES file {str(e)}") from e
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_file.name):
            os.unlink(tmp_file.name)



def process_csv_file(file_content: bytes) -> pd.DataFrame:
    """Processes CSV file content and converts it to a Pandas DataFrame.

    Args:
        file_content: The binary content of the CSV file.

    Returns:
        A pandas DataFrame containing the CSV data.

    Raises:
        ValueError: If the file cannot be processed.
    """
    try:
        return pd.read_csv(io.BytesIO(file_content))  # type: ignore
    except Exception as e:
        raise ValueError(f"Failed to process CSV file: {str(e)}") from e


# **************** Generic Function for Dispatching ****************


def process_file(file_content: bytes, file_extension: str) -> pd.DataFrame:
    """Processes file content and converts it to a pandas DataFrame.

    This function acts as a dispatcher that directs the file processing
    to the appropriate handler based on the file extension.

    Args:
        file_content: Binary content of the file.
        file_extension: The file extension (e.g., ".csv" or ".xes").

    Returns:
        A pandas DataFrame containing the processed data.

    Raises:
        ValueError: If the file cannot be processed or if the file type is unsupported.
    """
    # Ensure the extension starts with a dot and is lowercase
    if not file_extension.startswith("."):
        file_extension = f".{file_extension}"
    file_extension = file_extension.lower()

    # Dispatch to the appropriate handler based on file extension
    if file_extension == ".csv":
        return process_csv_file(file_content)
    elif file_extension == ".xes":
        return process_xes_file(file_content)
    else:
        raise ValueError(
            f"Unsupported file extension: {file_extension}. "
            "Only .csv and .xes are supported."
        )