"""Contains the API routes to handle logs and log-related operations.

This module defines the FastAPI routes for managing logs, including
retrieving logs, filtering logs by date, and deleting logs. It also
includes utility functions for handling log data and formatting
responses. In case of and log upload, it also includes the necessary
metadata to create a celonis connection.
"""

import json
import os
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status

import backend.utils.file_handlers as file_handlers
from backend.api.celonis import get_celonis_connection
from backend.celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)

router = APIRouter(prefix="/api/logs", tags=["Logs"])


@router.post("/upload-log")
async def upload_log(
    file: UploadFile,
    metadata: Optional[str] = Form(None),
    celonis_conn: CelonisConnectionManager = Depends(get_celonis_connection),
) -> Dict[str, str]:
    """Uploads an event log file to Celonis.

    Args:
        file: The event log to be uploaded. This should be a .csv of .xes file.
        metadata (optional): The metadata required for the Celonis connection.
          Defaults to None.
        celonis_conn (optional): The dependency injection for the celonis
          connection. User does not need to provide this. Defaults to
          Depends(get_celonis_connection).

    Returns:
        A dictionary containing a message indicating the success of the
        operation.
    """
    # Enforce .csv or .xes file
    if file.filename:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in (".csv", ".xes"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only .csv and .xes are allowed.",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required.",
        )
    # Parse metadata if provided
    meta: Dict[Any, Any] = {}
    if metadata:
        meta = json.loads(metadata)

    # Get uploaded content
    content = await file.read()

    try:
        # Process the XES file using the utility function
        result = file_handlers.process_xes_file(content)
    except ValueError as e:
        # The file could not be processed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error processing file: {str(e)}",
        )

    # Access metadata
    try:
        data_table_name = meta["dataTableName"]
    except KeyError:
        data_table_name = None

    # Upload to Celonis
    celonis_conn.add_dataframe(result)
    if data_table_name is not None:
        celonis_conn.create_table(table_name=data_table_name)
    else:
        celonis_conn.create_table()
    return {"Message": "Table created successfully"}
