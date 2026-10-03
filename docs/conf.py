import os
import sys

sys.path.insert(0, os.path.abspath('..'))

project = 'School Management System'
copyright = '2026, Leen Bechara'
author = 'Leen Bechara'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

autodoc_mock_imports = ['tkinter']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']