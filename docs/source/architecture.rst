System Architecture
===================

This page explains the architecture of the system.
It explains the overall structure of the backend and how the the backend interacts with the Celonis platform via `PyCelonis <https://celonis.github.io/pycelonis/2.13.0/>`_.

Backend Architecture
--------------------

The overall backend architecture is shown in the following diagram:

.. _backend-architecture:

.. figure:: ../_static/img/backend.svg

  Backend Architecture

In the following, we explain the key components of the backend.

Celonis Connection
^^^^^^^^^^^^^^^^^^
The :py:mod:`celonis_connection_manager <backend.celonis_connection.celonis_connection_manager>` module houses the :py:class:`CelonisConnectionManager <backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager>` class.
This class is responsible for managing the connection to the Celonis platform.
For this it uses the `PyCelonis <https://celonis.github.io/pycelonis/2.13.0/>`_ library to connect.

It offers mechanisms to upload event logs to the Celonis platform, and run arbitrary PQL queries on the platform against the uploaded data.
In the :py:mod:`API <backend.api>` module, we use this class as a dependency to connect to Celonis.
This is done in the :py:mod:`celonis <backend.api.celonis>` module.

Conformance Checking
^^^^^^^^^^^^^^^^^^^^

The :py:mod:`conformance_checking <backend.conformance_checking>` package contains modules for the four different conformance checking techniques.
Each module defines a class that implements the conformance checking technique.
These implementations are based on `PM4Py <https://processintelligence.solutions/pm4py>`_.

These were built in a first iteration of the application.
The application also allows to run the conformance techniques based on **PQL queries** instead of the PM4Py implementations.

PQL Queries
^^^^^^^^^^^

The :py:mod:`pql_queries <backend.pql_queries>` package contains modules that define the PQL queries for the conformance checking techniques.
As :ref:`backend-architecture` shows this package mirrors the strucuture of the :py:mod:`conformance_checking <backend.conformance_checking>` package.

Each module defines PQL queries that can be used to run the conformance checking techniques on the Celonis platform.

API
^^^

The :py:mod:`API <backend.api>` package contains the API endpoints for the application.
It is probably the biggest package in the backend.
It houses all the API relevant code.

The backend API is built using the `FastAPI <https://fastapi.tiangolo.com/>`_ framework.
The main application is defined in the :py:mod:`main <backend.api.main>` module.

The API endpoints are split-up into different routers, each responsible for a specific functionality.
The routers have the following functionality:

* :py:mod:`setup <backend.api.setup>`: Contains endpoints for setting up the application, such as inserting Celonis credentials.
* :py:mod:`log <backend.api.log>`: Contains endpoints for uploading event logs to the application and commiting them to the Celonis platform.
* :py:mod:`jobs <backend.api.jobs>`: Contains endpoints for getting the status of jobs for conformance checking techniques.
* :py:mod:`modules <backend.api.modules>`: Contains a module each, which defines a router, for each conformance checking technique.
  These routers contain endpoints for running the conformance checking techniques and getting the results.

Remaining Modules
^^^^^^^^^^^^^^^^^

The remaining modules in the backend contain code for various utilities and configurations.
All modules are well documented and we refer the reader to the code itself and the :doc:`autoapi/index` for more details.

Interaction with Celonis
------------------------

All conformance checking techniques use the Celonis platform to store the event logs.
The basic implementations that are based on `PM4Py <https://processintelligence.solutions/pm4py>`_ (see :py:mod:`conformance_checking <backend.conformance_checking>`) download a basic variant of the event log from the Celonis platform.
They then run all the conformance checking locally using PM4Py.

The PQL-based implementations (see :py:mod:`pql_queries <backend.pql_queries>`) perform pre-computations on the event logs on the Celonis platform using `PQL <https://docs.celonis.com/en/pql---process-query-language.html>`_.
They then fetch the results of these pre-computations and process them locally to compute the wanted results.