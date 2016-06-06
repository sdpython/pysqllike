#-*- coding: utf-8 -*-
import sys
import os
import datetime
import re
import alabaster

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src")))

from pyquickhelper.helpgen.default_conf import set_sphinx_variables
set_sphinx_variables(__file__, "pysqllike", "Xavier Dupré", 2016,
                     "alabaster", alabaster.get_path(), locals(), add_extensions=['alabaster'],
                     extlinks=dict(issue=('https://github.com/sdpython/pysqllike/issues/%d', 'issue')))

blog_root = "http://www.xavierdupre.fr/app/sqllike/helpsphinx/"
