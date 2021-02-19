# -*- coding: utf-8 -*-
import sys
import os
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables, get_default_stylesheet


sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

local_template = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), "phdoc_templates")

set_sphinx_variables(__file__, "lightmlboard", "Xavier Dupré", 2021,
                     "alabaster", alabaster.get_path(),
                     locals(), extlinks=dict(
                         issue=('https://github.com/sdpython/lightmlboard/issues/%s', 'issue')),
                     title="lightmlboard", book=True)

blog_root = "http://www.xavierdupre.fr/app/lightmlboard/helpsphinx/"

html_context = {
    'css_files': get_default_stylesheet(['_static/my-styles.css']),
}

html_logo = "phdoc_static/project_ico.png"

html_sidebars = {}

language = "en"

mathdef_link_only = True

epkg_dictionary['L1'] = "https://en.wikipedia.org/wiki/Least_absolute_deviations"
