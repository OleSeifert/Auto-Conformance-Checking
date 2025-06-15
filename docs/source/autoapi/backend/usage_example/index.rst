backend.usage_example
=====================

.. py:module:: backend.usage_example

.. autoapi-nested-parse::

   The file is an example of how to use the CelonisConnection Class.

   It contains examples of how to create a Celonis connection, add a
   dataframe to the data model, create a table, and get a dataframe from
   Celonis.



Attributes
----------

.. autoapisummary::

   backend.usage_example.EVENT_LOG_LOC
   backend.usage_example.cfg
   backend.usage_example.my_celonis
   backend.usage_example.starttime
   backend.usage_example.result


Classes
-------

.. autoapisummary::

   backend.usage_example.CelonisSettings


Module Contents
---------------

.. py:data:: EVENT_LOG_LOC
   :value: '/home/rene/MyProjects/Auto_CC/conformance_checking_spp/tests/input_data/running-example.xes'


.. py:class:: CelonisSettings(_case_sensitive: bool | None = None, _nested_model_default_partial_update: bool | None = None, _env_prefix: str | None = None, _env_file: pydantic_settings.sources.DotenvType | None = ENV_FILE_SENTINEL, _env_file_encoding: str | None = None, _env_ignore_empty: bool | None = None, _env_nested_delimiter: str | None = None, _env_nested_max_split: int | None = None, _env_parse_none_str: str | None = None, _env_parse_enums: bool | None = None, _cli_prog_name: str | None = None, _cli_parse_args: bool | list[str] | tuple[str, Ellipsis] | None = None, _cli_settings_source: pydantic_settings.sources.CliSettingsSource[Any] | None = None, _cli_parse_none_str: str | None = None, _cli_hide_none_type: bool | None = None, _cli_avoid_json: bool | None = None, _cli_enforce_required: bool | None = None, _cli_use_class_docs_for_groups: bool | None = None, _cli_exit_on_error: bool | None = None, _cli_prefix: str | None = None, _cli_flag_prefix_char: str | None = None, _cli_implicit_flags: bool | None = None, _cli_ignore_unknown_args: bool | None = None, _cli_kebab_case: bool | None = None, _secrets_dir: pydantic_settings.sources.PathType | None = None, **values: Any)

   Bases: :py:obj:`pydantic_settings.BaseSettings`


   Settings for the Celonis connection.

   This class is used to load the Celonis connection settings from the
   environment variables. The settings are loaded from a .env file
   using the `pydantic_settings` library. The settings include the
   Celonis base URL, data pool name, data model name, and API token.


   .. py:attribute:: CELONIS_BASE_URL
      :type:  str


   .. py:attribute:: CELONIS_DATA_POOL_NAME
      :type:  str


   .. py:attribute:: CELONIS_DATA_MODEL_NAME
      :type:  str


   .. py:attribute:: API_TOKEN
      :type:  str


   .. py:attribute:: model_config

      Configuration for the model, should be a dictionary conforming to [`ConfigDict`][pydantic.config.ConfigDict].


.. py:data:: cfg

.. py:data:: my_celonis

.. py:data:: starttime

.. py:data:: result

