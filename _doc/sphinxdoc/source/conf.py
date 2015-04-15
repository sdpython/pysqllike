import sys
import os
import datetime
import re
import cloud_sptheme as csp

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
set_sphinx_variables(__file__,
                     "pysqllike",
                     "Xavier Dupré",
                     2014,
                     "cloud",
                     csp.get_theme_dir(),
                     locals(),
                     add_extensions=['cloud_sptheme'])
