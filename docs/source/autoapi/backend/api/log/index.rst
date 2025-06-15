backend.api.log
===============

.. py:module:: backend.api.log

.. autoapi-nested-parse::

   Contains the API routes to handle logs and log-related operations.

   This module defines the FastAPI routes for managing logs, including
   retrieving logs, filtering logs by date, and deleting logs. It also
   includes utility functions for handling log data and formatting
   responses. In case of and log upload, it also includes the necessary
   metadata to create a celonis connection.



Attributes
----------

.. autoapisummary::

   backend.api.log.router


Functions
---------

.. autoapisummary::

   backend.api.log.upload_log
   backend.api.log.commit_log_to_celonis


Module Contents
---------------

.. py:data:: router

.. py:function:: upload_log(file: fastapi.UploadFile, request: fastapi.Request) -> Dict[str, List[str]]
   :async:


   Uploads an event log file and retrieves its columns.

   The file gets stored in a temporary file for the later upload to Celonis.

   :param file: The event log file to be uploaded. This should be a .csv or .xes file.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :returns: The columns of the uploaded log file as a dictionary.

   :raises HTTPException: If the file name is not provided or if the file type is
   :raises invalid, or if there is an error processing the file.:


.. py:function:: commit_log_to_celonis(request: fastapi.Request, payload: Optional[backend.api.models.schemas.setup_models.ColumnMapping] = None, celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager = Depends(get_celonis_connection)) -> Dict[str, str]
   :async:


   Uploads the log file to Celonis and creates a table.

   :param payload: The column mapping for the event log. This should be a
                   ColumnMapping object containing the case ID, activity, and timestamp
                   columns. It is only needed if the log is a csv file.
   :type payload: optional
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.
   :param celonis: The Celonis Connection DI. Defaults to
                   Depends(get_celonis_connection).
   :type celonis: optional

   :raises HTTPException: If no log file is found in the app state, or if there is an
   :raises error processing the file.:

   :returns: A dictionary containing a message indicating the success of the
             operation.


