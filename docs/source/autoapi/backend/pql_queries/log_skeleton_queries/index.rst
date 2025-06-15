backend.pql_queries.log_skeleton_queries
========================================

.. py:module:: backend.pql_queries.log_skeleton_queries

.. autoapi-nested-parse::

   Queries that can be used to get log-skeleton related data from celonis.



Functions
---------

.. autoapisummary::

   backend.pql_queries.log_skeleton_queries.get_always_before_relation
   backend.pql_queries.log_skeleton_queries.get_always_after_relation
   backend.pql_queries.log_skeleton_queries.get_equivalance_relation
   backend.pql_queries.log_skeleton_queries.get_exclusive_choice_relaion
   backend.pql_queries.log_skeleton_queries.get_never_together_relation
   backend.pql_queries.log_skeleton_queries.get_directly_follows_relation_and_count
   backend.pql_queries.log_skeleton_queries.get_act_freq


Module Contents
---------------

.. py:function:: get_always_before_relation(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Caculates which pairs of Activity always occurr before each other.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A dataframe that contains for pairs of Activities whether
             they always occurr before each other.


.. py:function:: get_always_after_relation(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Caculates which pairs of Activity always occurr after each other.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A dataframe that contains for pairs of Activities whether
             they always occurr after each other.


.. py:function:: get_equivalance_relation(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Caculates which pairs of Activity are equivalent.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A dataframe that contains for pairs of Activities whether
             they are equivalent.


.. py:function:: get_exclusive_choice_relaion(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Caculates which pairs of Activity are exclusive choice.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A dataframe that contains for pairs of Activities whether
             they are exclusive choice.


.. py:function:: get_never_together_relation(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Caculates which pairs of Activity never occurr together.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A dataframe that contains for pairs of Activities whether
             they are never together in a trace


.. py:function:: get_directly_follows_relation_and_count(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Gets the directly follows relation and count.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A pandas dataframe that contains a statement whether the
             dirctly follows relation is true and the count for each


.. py:function:: get_act_freq(celonis: backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager) -> pandas.DataFrame

   Gets the activity frequencies.

   :param celonis: the celonis connection
   :type celonis: CelonisConnectionManager

   :returns: A pandas dataframe that contains the activity frequencies


