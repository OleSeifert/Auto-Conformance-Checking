Installation
============

This page describes how to install the package.
There exist two ways to install the application: manually or via Docker.

.. tip::

  We recommend using Docker for installation, as it is the easiest way to get started with the application.

Manual Installation
-------------------

Manually installing the application requires setting up both the backend and frontend dependencies.
To install the application manually, you need to follow these steps:

Backend Dependencies
^^^^^^^^^^^^^^^^^^^^

For installing the project's backend dependencies, we recommend using `uv <https://docs.astral.sh/uv/>`_ as it operates very quickly.
To install the project's backend dependencies using uv, follow these steps:

1. Ensure that you have uv installed on your system (see `here <https://docs.astral.sh/uv/getting-started/installation/>`_ for installation instructions).
2. Clone the repository to your local machine using ``git clone``.
3. Navigate to the root directory of the repository.
4. Run ``uv sync``. uv will then install all necessary dependencies and create a virtual environment in the ``.venv`` folder at the root of the project.
5. Activate the environment by running ``source ./.venv/bin/activate`` on Mac and Linux, or ``.venv\Scripts\activate`` on Windows.

Frontend Dependencies
^^^^^^^^^^^^^^^^^^^^^

To install the project's frontend dependencies, you need to have `Node.js <https://nodejs.org/en/download/>`_ and `npm <https://docs.npmjs.com/downloading-and-installing-node-js-and-npm>`_ installed on your system.
To install the project's frontend dependencies, follow these steps:

1. Ensure that you have Node.js and npm installed on your system.
2. Navigate to the ``frontend`` directory of the repository.
3. Run ``npm install``. This will install all necessary frontend dependencies.


Running the project
^^^^^^^^^^^^^^^^^^^

To run the project, locally you have to start the **backend server** and the **frontend server**.
To start the backend server, open the shell of your choice and run the following command:

.. code-block:: shell

  uv run uvicorn backend.main:app

This runs the backend server on port ``8000`` by default.

To start the frontend server, open another shell, navigate to the ``frontend`` directory and run the following command:

.. code-block:: shell

  npm run frontend

This runs the frontend server on port ``3000`` by default.

To access the application, open your web browser and navigate to `<http://localhost:3000>`_.

Docker Installation
-------------------

Installing the application via Docker is the easiest way to get started.
To install the application via Docker, follow these steps:

1. Ensure that you have Docker installed on your system (see `here <https://docs.docker.com/get-docker/>`_ for installation instructions).
2. Clone the repository to your local machine using ``git clone``.
3. Navigate to the root directory of the repository.
4. Build the Docker image by running the following command (make sure **Docker is running**):

.. code-block:: shell

  docker compose up --build

5. Once the build is complete, the application will be running on port ``3000`` by default.