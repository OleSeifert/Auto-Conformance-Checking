backend.main
============

.. py:module:: backend.main

.. autoapi-nested-parse::

   Contains the main entry point for the FastAPI backend.

   This module initializes the FastAPI application, sets up middleware, and
   includes the API routers.



Attributes
----------

.. autoapisummary::

   backend.main.app


Functions
---------

.. autoapisummary::

   backend.main.lifespan
   backend.main.home


Module Contents
---------------

.. py:function:: lifespan(app: fastapi.FastAPI)
   :async:


   Initializes the CelonisConnectionManager and stores it in the app state.

   This function is used as a context manager to ensure that the
   CelonisConnectionManager is properly initialized.

   :param app: The FastAPI application instance. This is used to store the
               CelonisConnectionManager instance in the application state.


.. py:data:: app

.. py:function:: home() -> Dict[str, str]

   Returns a simple message indicating that the API is running.


