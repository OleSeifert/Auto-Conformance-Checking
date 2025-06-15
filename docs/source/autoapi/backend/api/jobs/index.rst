backend.api.jobs
================

.. py:module:: backend.api.jobs

.. autoapi-nested-parse::

   Contains the router for handling jobs.



Attributes
----------

.. autoapisummary::

   backend.api.jobs.router


Functions
---------

.. autoapisummary::

   backend.api.jobs.get_jobs
   backend.api.jobs.verify_correct_job_module


Module Contents
---------------

.. py:data:: router

.. py:function:: get_jobs(job_id: str, request: fastapi.Request) -> backend.api.models.schemas.job_models.JobStatus
   :async:


   Fetches the status of a job via its ID.

   :param job_id: The ID of the job to be fetched.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.

   :raises HTTPException: If the job with the given ID is not found in the
   :raises application state.:

   :returns: The status of the job as a JobStatus object.


.. py:function:: verify_correct_job_module(job_id: str, request: fastapi.Request, module: str)

   Verifies if a job belongs to the module.

   Helper funciton used for the request of job states.

   :param job_id: The ID of the job to be fetched.
   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`.
   :param module: The name of the module that the job is checked against

   :raises HTTPException: If the job with the given ID does not belong to the module


