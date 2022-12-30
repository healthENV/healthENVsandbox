# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath('../app/'))
sys.path.append(os.path.abspath('../app/static'))
sys.path.append(os.path.abspath('../launcher/'))
sys.path.append(os.path.abspath('/logs/'))
"""

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join(__file__, "../../app/static/")))
sys.path.append(os.path.abspath(os.path.join(__file__, "../../app")))
sys.path.append(os.path.abspath(os.path.join(__file__, "../../launcher")))
sys.path.append(os.path.abspath(os.path.join(__file__, "../../logs")))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'healthENV'
copyright = '2022, M Bailey'
author = 'M Bailey'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'launcher.txt']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_favicon = 'favicon.png'