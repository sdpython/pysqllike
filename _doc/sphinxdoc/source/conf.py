#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  documentation build configuration file, created by
# sphinx-quickstart on Fri May 10 18:35:14 2013.
#

import sys, os, datetime, re
import cloud_sptheme as csp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0])))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], "pysqllike")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", "..", "..", "pyquickhelper", "src")))

from pyquickhelper.helpgen.default_conf import set_sphinx_variables
set_sphinx_variables(   __file__,
                        "pysqllike",
                        "Xavier Dupré",
                        2014,
                        "cloud",
                        csp.get_theme_dir(),
                        locals(),
                        add_extensions = ['cloud_sptheme'])
