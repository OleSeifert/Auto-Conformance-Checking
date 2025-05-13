"""Contains the main entry point for the FastAPI backend.

This module initializes the FastAPI application, sets up middleware, and
includes the API routers.
"""

import json

import pandas as pd
from celonis_connection.celonis_connection_manager import (
    CelonisConnectionManager,
)  # type: ignore
from fastapi import APIRouter, FastAPI, Form, UploadFile
from pm4py.objects.conversion.log.variants import (  # type: ignore
    to_data_frame as log_to_df,
)
from pm4py.objects.log.importer.xes import importer as xes_importer  # type: ignore

app = FastAPI()

upload_to_celonis_router = APIRouter()
my_celonis: CelonisConnectionManager


@upload_to_celonis_router.post("/upload-log-and-metadata")
async def upload_log(file: UploadFile, metadata: str = Form(...)):
    """Uploads a log file and its metadata to Celonis.

    Args:
        file: The event log that is to be uploaded.
        metadata: The metadata required for the Celonis connection.

    Returns:
        dict: A response indicating the success or failure of the upload.
    """
    # Step 1: Parse metadata
    meta = json.loads(metadata)

    # Step 2: Read uploaded file
    content = await file.read()

    # Step 3: For now, assume file is a XES file
    result = xes_importer.apply(content)  # type: ignore
    result = log_to_df.apply(result)  # type: ignore

    # Step 4: Access metadata
    api_url = meta["apiURL"]
    data_pool_name = meta["dataPoolName"]
    data_model_name = meta["dataModelName"]
    try:
        data_table_name = meta["dataTableName"]
    except KeyError:
        data_table_name = None
    try:
        api_token = meta["token"]
    except KeyError:
        api_token = None

    # Step 5: Create a Celonis connection
    if api_token is not None:
        my_celonis = CelonisConnectionManager(
            base_url=api_url,
            data_pool_name=data_pool_name,
            data_model_name=data_model_name,
            api_token=api_token,
        )
    else:
        my_celonis = CelonisConnectionManager(
            base_url=api_url,
            data_pool_name=data_pool_name,
            data_model_name=data_model_name,
        )
    # Step 6: Add the event log to the data model
    if isinstance(result, pd.DataFrame):
        my_celonis.add_dataframe(result)
        if data_table_name is not None:
            my_celonis.create_table(table_name=data_table_name)
        else:
            my_celonis.create_table()
        return {"status": "success", "message": "Table created in Celoni"}
    else:
        return {"status": "error", "message": "Failed to read the log file."}


# Include routers from other modules
app.include_router(upload_to_celonis_router)
