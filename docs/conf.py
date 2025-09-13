import os
import sys
sys.path.insert(0, os.path.abspath('..'))



project = 'Makcu Python Library'
copyright = '2025, SleepyTotem'
author = 'SleepyTotem'
release = '2.2.0'
version = '2.2.0'



extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.todo',
    'sphinx_rtd_theme',
    'sphinx_copybutton',
    'sphinx_autodoc_typehints',
    'myst_parser',
]


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']




html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',

    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

html_logo = '_static/makcu_logo.png' 
html_favicon = '_static/favicon.ico' 



autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'show-inheritance': True,
    'inherited-members': True,
}

autodoc_typehints = 'description'
autodoc_class_signature = 'mixed'



napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None
napoleon_attr_annotations = True



intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pyserial': ('https://pyserial.readthedocs.io/en/latest/', None),
}



todo_include_todos = True



copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True



def setup(app):
    app.add_css_file('custom.css')