"""Contains the API routes to handle logs and log-related operations.

This module defines the FastAPI routes for managing logs, including
retrieving logs, filtering logs by date, and deleting logs. It also
includes utility functions for handling log data and formatting
responses. In case of and log upload, it also includes the necessary
metadata to create a celonis connection.
"""

import os
import tempfile
from typing import Dict, List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile

import backend.utils.file_handlers as file_handlers
from backend.api.celonis import get_celonis_connection
from backend.api.models.schemas.setup_models import ColumnMapping
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.post("/upload-log", status_code=201)
async def upload_log(file: UploadFile, request: Request) -> Dict[str, List[str]]:
    """Uploads an event log file and retrieves its columns.

    The file gets stored in a temporary file for the later upload to Celonis.

    Args:
        file: The event log file to be uploaded. This should be a .csv or .xes file.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.

    Returns:
        The columns of the uploaded log file as a dictionary.

    Raises:
        HTTPException: If the file name is not provided or if the file type is
        invalid, or if there is an error processing the file.
    """
    # Only allow .csv and .xes files
    if not file.filename:
        raise HTTPException(400, "File name is required.")

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in (".csv", ".xes"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only .csv and .xes are allowed.",
        )

    content = await file.read()

    # Get the logs columns
    try:
        df = file_handlers.process_file(content, ext)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing file: {str(e)}",
        )

    # Store file to a tmp file for the later upload
    suffix = ext
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(content)
    tmp.close()

    # Store the path to the tmp file in the app state
    request.app.state.current_log = tmp.name
    request.app.state.current_log_columns = df.columns.tolist()

    return {"columns": df.columns.tolist()}


@router.post("/commit-log-to-celonis")
async def commit_log_to_celonis(
    request: Request,
    payload: Optional[ColumnMapping] = None,
    celonis: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Uploads the log file to Celonis and creates a table.

    Args:
        payload (optional): The column mapping for the event log. This should be a
          ColumnMapping object containing the case ID, activity, and timestamp
          columns. It is only needed if the log is a csv file.
        request: The FastAPI request object. This is used to access the
          application state via `request.app.state`.
        celonis (optional): The Celonis Connection DI. Defaults to
          Depends(get_celonis_connection).

    Raises:
        HTTPException: If no log file is found in the app state, or if there is an
        error processing the file.

    Returns:
        A dictionary containing a message indicating the success of the
        operation.
    """
    path = request.app.state.current_log  # Path to the temporary file with the log
    if not path or not os.path.exists(path):
        raise HTTPException(
            status_code=400,
            detail="No log file found. Please upload a log first.",
        )

    # Read the log file and convert it
    with open(path, "rb") as f:
        content = f.read()
    ext = os.path.splitext(path)[1].lower()
    try:
        df = file_handlers.process_file(content, ext)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error processing file: {str(e)}",
        )
    # CSV files must enforce a mapping
    if ext == ".csv":
        if not payload:
            raise HTTPException(
                status_code=400,
                detail="Column mapping is required for CSV files.",
            )
    # Rename the columns according to the mapping if specified
    if payload:
        df = df.rename(
            columns={
                payload.case_id_column: "case:concept:name",
                payload.activity_column: "concept:name",
                payload.timestamp_column: "time:timestamp",
                payload.resource_1_column: "org:resource",
                payload.group_column: "org:group",
            }
        )
        # Convert the timestamp column to datetime
        df["time:timestamp"] = pd.to_datetime(df["time:timestamp"], errors="coerce")  # type: ignore

    # Upload to Celonis
    celonis.add_dataframe(df)
    celonis.create_table()

    # Clean up the temporary file
    os.unlink(path)
    request.app.state.current_log = None
    request.app.state.current_log_columns = []

    return {"message": "Table created successfully"}

