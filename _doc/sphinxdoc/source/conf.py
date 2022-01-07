# -*- coding: utf-8 -*-
import sys
import os
import alabaster
from pyquickhelper.helpgen.default_conf import set_sphinx_variables

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))

set_sphinx_variables(__file__, "pysqllike", "Xavier Dupré", 2022,
                     "alabaster", alabaster.get_path(), locals(), add_extensions=['alabaster'],
                     extlinks=dict(issue=('https://github.com/sdpython/pysqllike/issues/%s', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/sqllike/helpsphinx/"
