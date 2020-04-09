# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys


sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'TFE network simulation'
copyright = '2020, UCLouvain - EPL - T. Beckers & M. Beugoms'
author = 'T. Beckers & M. Beugoms'

# The full version, including alpha/beta/rc tags
release = '0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

autodoc_mock_imports = ["docker", "sphinx_bootstrap_theme"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_templates']

# (Optional) Logo. Should be small enough to fit the navbar (ideally 24x24).
# Path should be relative to the ``_static`` files directory.
html_logo = "_static/logo_tfe.jpg"

# Theme options are theme-specific and customize the look and feel of a
# theme further.
html_theme_options = {
    # color
    # dark blue : rgb(0,45,98)
    # light blue : rgb(79,177,228)
    # sky blue : rgb(142,176,205)
    'footerbgcolor': 'rgb(0,45,98)',
    'sidebarbgcolor': 'rgb(142,176,205)',
    'footertextcolor': 'white',
    'sidebarlinkcolor': 'white',
    'relbarbgcolor': 'rgb(0,45,98)',
}