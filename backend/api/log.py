# """Contains the API routes to handle logs and log-related operations.

# This module defines the FastAPI routes for managing logs, including
# retrieving logs, filtering logs by date, and deleting logs. It also
# includes utility functions for handling log data and formatting
# responses. In case of and log upload, it also includes the necessary
# metadata to create a celonis connection.
# """

# import json
# import os
# from typing import Any, Dict, Optional

# from fastapi import APIRouter, Depends, Form, HTTPException, Request, UploadFile, status

# import backend.utils.file_handlers as file_handlers
# from backend.api.celonis import get_celonis_connection
# from backend.celonis_connection.celonis_connection_manager import (
#     CelonisConnectionManager,
# )

# router = APIRouter(prefix="/api/logs", tags=["Logs"])


# @router.post("/upload-log")
# async def upload_log(
#     file: UploadFile,
#     request: Request,
#     metadata: Optional[str] = Form(None),
#     celonis_conn: CelonisConnectionManager = Depends(get_celonis_connection),
# ) -> Dict[str, str]:
#     """Uploads an event log file to Celonis.

#     Only allows .csv and .xes files.

#     Args:
#         file: The event log to be uploaded. This should be a .csv of .xes file.
#         request: The FastAPI request object. This is used to access the
#           application state via `request.app.state`.
#         metadata (optional): The metadata required for the Celonis connection.
#           Defaults to None.
#         celonis_conn (optional): The dependency injection for the celonis
#           connection. User does not need to provide this. Defaults to
#           Depends(get_celonis_connection).

#     Returns:
#         A dictionary containing a message indicating the success of the
#         operation.
#     """
#     # Enforce .csv or .xes file
#     if file.filename:
#         ext = os.path.splitext(file.filename)[1].lower()
#         if ext not in (".csv", ".xes"):
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Invalid file type. Only .csv and .xes are allowed.",
#             )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="File name is required.",
#         )
#     # Parse metadata if provided
#     meta: Dict[Any, Any] = {}
#     if metadata:
#         meta = json.loads(metadata)

#     # Get uploaded content
#     content = await file.read()

#     try:
#         # Process the XES file using the utility function
#         result = file_handlers.process_xes_file(content)
#     except ValueError as e:
#         # The file could not be processed
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Error processing file: {str(e)}",
#         )

#     # Store the log columns in the app state
#     request.app.state.current_log_columns = result.columns.tolist()

#     # Access metadata
#     try:
#         data_table_name = meta["dataTableName"]
#     except KeyError:
#         data_table_name = None

#     # Upload to Celonis
#     celonis_conn.add_dataframe(result)
#     if data_table_name is not None:
#         celonis_conn.create_table(table_name=data_table_name)
#     else:
#         celonis_conn.create_table()
#     return {"Message": "Table created successfully"}
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
# from backend.api.models.schemas.setup_models import ColumnMapping
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
