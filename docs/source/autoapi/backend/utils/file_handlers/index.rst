backend.utils.file_handlers
===========================

.. py:module:: backend.utils.file_handlers

.. autoapi-nested-parse::

   Contains utility functions for handling file uploads.



Functions
---------

.. autoapisummary::

   backend.utils.file_handlers.process_xes_file
   backend.utils.file_handlers.process_csv_file
   backend.utils.file_handlers.process_file


Module Contents
---------------

.. py:function:: process_xes_file(file_content: bytes) -> pandas.DataFrame

   Processes XES file content and converts it to a DataFrame.

   This function is needed, as the transferred file via the API is in bytes,
   and pm4py does not support reading from bytes directly. Therefore, we
   create a temporary file to store the uploaded content and then read it
   using pm4py.

   :param file_content: Binary content of the XES file.

   :returns: A pandas DataFrame containing the event log.

   :raises ValueError: If the file cannot be processed.


.. py:function:: process_csv_file(file_content: bytes) -> pandas.DataFrame

   Processes CSV file content and converts it to a Pandas DataFrame.

   :param file_content: The binary content of the CSV file.

   :returns: A pandas DataFrame containing the CSV data.

   :raises ValueError: If the file cannot be processed.


.. py:function:: process_file(file_content: bytes, file_extension: str) -> pandas.DataFrame

   Processes file content and converts it to a pandas DataFrame.

   This function acts as a dispatcher that directs the file processing
   to the appropriate handler based on the file extension.

   :param file_content: Binary content of the file.
   :param file_extension: The file extension (e.g., ".csv" or ".xes").

   :returns: A pandas DataFrame containing the processed data.

   :raises ValueError: If the file cannot be processed or if the file type is unsupported.


