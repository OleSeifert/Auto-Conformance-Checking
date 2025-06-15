backend.api.setup
=================

.. py:module:: backend.api.setup

.. autoapi-nested-parse::

   Contains a router for the setup of the application.

   It contains several 'utility' endpoints that are used in the setup of
   the application and the general configuration for event logs.



Attributes
----------

.. autoapisummary::

   backend.api.setup.router
   backend.api.setup.ENV_PATH
   backend.api.setup.LOCK_PATH


Functions
---------

.. autoapisummary::

   backend.api.setup.celonis_credentials
   backend.api.setup.get_column_names


Module Contents
---------------

.. py:data:: router

.. py:data:: ENV_PATH

.. py:data:: LOCK_PATH

.. py:function:: celonis_credentials(credentials: backend.api.models.schemas.setup_models.CelonisCredentials)
   :async:


   Saves the Celonis credentials to the .env file.

   :param credentials: The Celonis credentials to be saved. This should be a
                       CelonisCredentials object.

   :returns: A dictionary containing a message indicating the success of the
             operation.


.. py:function:: get_column_names(request: fastapi.Request) -> Dict[str, List[str]]
   :async:


   Provides the column names of the current log.

   :param request: The FastAPI request object. This is used to access the app state
                   and retrieve the current log columns.

   :returns: A dictionary containing the column names of the current log.

   :raises HTTPException: If no log columns are found in the app state, a 400 error is raised
   :raises with a message indicating that no log columns were found. The user should:
   :raises upload a log first.:


