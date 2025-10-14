# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'SynOmics'
copyright = '2025, Trinh'
author = 'The-Chuong Trinh, Guido Uguzzoni, Jean-Baptiste Woillard, Christophe Battail'

release = '0.1'
version = '0.1.0'

# -- Path setup: ensure package root is importable for autodoc
import os
import sys
THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, '..', '..'))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
]

# Mock heavy/optional imports to avoid RTD build failures
autodoc_mock_imports = [
    'pandas',
    'numpy',
    'sklearn',
    'mygene',
    'tqdm',
]

# Include both class and __init__ docstrings
autoclass_content = 'both'

# Autosummary generation
autosummary_generate = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
