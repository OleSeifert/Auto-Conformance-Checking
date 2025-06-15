backend.api.models.schemas.setup_models
=======================================

.. py:module:: backend.api.models.schemas.setup_models

.. autoapi-nested-parse::

   Contains the Pydantic models for the setup API.

   This module defines the Pydantic models used for validating the input
   data for the setup API endpoints. It includes models for Celonis
   credentials, and column mapping.



Classes
-------

.. autoapisummary::

   backend.api.models.schemas.setup_models.CelonisCredentials
   backend.api.models.schemas.setup_models.ColumnMapping


Module Contents
---------------

.. py:class:: CelonisCredentials(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Defines the Celonis credentials required for the connection.


   .. py:attribute:: celonis_base_url
      :type:  str


   .. py:attribute:: celonis_data_pool_name
      :type:  str


   .. py:attribute:: celonis_data_model_name
      :type:  str


   .. py:attribute:: api_token
      :type:  str


.. py:class:: ColumnMapping(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Defines the column mapping for the event log.


   .. py:attribute:: case_id_column
      :type:  str


   .. py:attribute:: activity_column
      :type:  str


   .. py:attribute:: timestamp_column
      :type:  str


   .. py:attribute:: resource_1_column
      :type:  Optional[str]
      :value: None



   .. py:attribute:: group_column
      :type:  Optional[str]
      :value: None



