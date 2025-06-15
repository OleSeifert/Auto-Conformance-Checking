"""Configuration file for the Sphinx documentation builder."""
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

ROOT = os.path.abspath("../..")          # …/conformance_checking_spp
BACKEND = os.path.join(ROOT, "backend")

sys.path.insert(0, ROOT)                 #  <-- ADD THIS
sys.path.insert(0, BACKEND)

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Automatic Conformance Checking Insights in Celonis"
copyright = (
    "2025, Samadrita Saha, René Rockstedt, Ekansh Agarwal, Yash Raj, Ole Seifert"
)
author = "Samadrita Saha, René Rockstedt, Ekansh Agarwal, Yash Raj, Ole Seifert"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["autoapi.extension", "sphinx.ext.napoleon"]

autoclass_content = "both"

templates_path = ["_templates"]
exclude_patterns = []

# **************** AutoAPI Configuration ****************

autoapi_type = "python"
autoapi_dirs = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../backend"))]
autoapi_ignore = ["*tests/*", "*/backend/usage_2.py", "*backend/usage_2.*"]
autoapi_root = "autoapi"
# which things to include
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
# keep the generated files around (handy for debugging)
autoapi_keep_files = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "/img/light-logo.png",
    "dark_logo": "/img/dark-logo.png",
    "sidebar_hide_name": True,
}
