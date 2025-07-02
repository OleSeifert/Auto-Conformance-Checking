backend.api.celonis
===================

.. py:module:: backend.api.celonis

.. autoapi-nested-parse::

   Contains the dependency injection for the CelonisConnectionManager.

   This module contains one function, which is used to return a
   CelonisConnectionManager instance. The function is used as a dependency
   in the FastAPI application.



Classes
-------

.. autoapisummary::

   backend.api.celonis.CelonisSettings


Functions
---------

.. autoapisummary::

   backend.api.celonis.get_celonis_connection


Module Contents
---------------

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


.. py:function:: get_celonis_connection(request: fastapi.Request) -> backend.celonis_connection.celonis_connection_manager.CelonisConnectionManager

   Returns a CelonisConnectionManager instance.

   It tries to get the CelonisConnectionManager instance from the
   application state. If it is not present, it creates a new instance
   using the settings from the environment variables. The instance is
   then stored in the application state for later use.
   This function is used as a dependency in the FastAPI application.

   :param request: The FastAPI request object. This is used to access the
                   application state via `request.app.state`. The application state
                   contains the `CelonisConnectionManager` instance, which is created
                   during application startup and stored for later use.

   :returns: The CelonisConnectionManager instance. This is used to connect to the
             Celonis API and perform operations on the data pool.


