from __future__ import annotations

import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))
import hcloud  # noqa

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Hetzner Cloud Python"
author = "Hetzner Cloud GmbH"
copyright = f"{datetime.now().year}, {author}"

version = hcloud.__version__
release = hcloud.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# A boolean that decides whether module names are prepended to all object names (for
# object types where a “module” of some kind is defined), e.g. for py:function
# directives. Default is True.
add_module_names = False

# Myst Parser
myst_enable_extensions = ["colon_fence"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_logo = "_static/logo-hetzner.svg"
html_favicon = "_static/favicon.png"
# Theme options are theme-specific and customize the look and feel of a theme further.
# For a list of options available for each theme, see the documentation.
html_theme_options = {
    "logo_only": True,
    "style_nav_header_background": "#fff",
}
html_css_files = [
    "custom.css",
]
