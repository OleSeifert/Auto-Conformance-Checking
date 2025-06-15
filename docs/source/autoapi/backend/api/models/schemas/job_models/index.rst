backend.api.models.schemas.job_models
=====================================

.. py:module:: backend.api.models.schemas.job_models

.. autoapi-nested-parse::

   Contains the Pydantic model for a generic job.

   The job is used to represent a job in the system.



Classes
-------

.. autoapisummary::

   backend.api.models.schemas.job_models.JobStatus


Module Contents
---------------

.. py:class:: JobStatus(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   The job status model.

   This model is used to represent the status of a job in the system.
   It contains the module name, status, result, and error message.
   The status can be one of the following: "pending", "running",
   "completed", or "failed".
   The result is an optional dictionary containing the result of the job.
   The error is an optional string containing the error message if the
   job failed.


   .. py:attribute:: module
      :type:  str


   .. py:attribute:: status
      :type:  Literal['pending', 'running', 'complete', 'failed']


   .. py:attribute:: result
      :type:  Optional[Dict[str, Any]]
      :value: None



   .. py:attribute:: error
      :type:  Optional[str]
      :value: None



