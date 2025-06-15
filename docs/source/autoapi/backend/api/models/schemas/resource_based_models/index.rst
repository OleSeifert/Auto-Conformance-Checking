backend.api.models.schemas.resource_based_models
================================================

.. py:module:: backend.api.models.schemas.resource_based_models

.. autoapi-nested-parse::

   Contains the Pydantic models for resource-based conformance checking.



Classes
-------

.. autoapisummary::

   backend.api.models.schemas.resource_based_models.SNAMetric
   backend.api.models.schemas.resource_based_models.OrganizationalRole


Module Contents
---------------

.. py:class:: SNAMetric(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents a single connection (edge) in an SNA graph.


   .. py:attribute:: source
      :type:  str


   .. py:attribute:: target
      :type:  str


   .. py:attribute:: value
      :type:  float


.. py:class:: OrganizationalRole(/, **data: Any)

   Bases: :py:obj:`pydantic.BaseModel`


   Represents an organizational role used for role discovery.


   .. py:attribute:: activities
      :type:  List[str]


   .. py:attribute:: originators_importance
      :type:  Dict[str, float]


