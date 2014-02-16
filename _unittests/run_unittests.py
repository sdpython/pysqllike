# coding: latin-1
"""
@file
@brief run all unit tests
"""

import unittest, os, sys, io

try :
    import pyquickhelper
except ImportError :
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", "pyquickhelper", "src" ))
    sys.path.append(path)
    import pyquickhelper
    

from pyquickhelper import fLOG
from pyquickhelper.unittests.utils_tests import main 



if __name__ == "__main__" :
    fLOG(OutputPrint = True)
        
    runner  = unittest.TextTestRunner(verbosity=0, stream = io.StringIO ())
    path    = os.path.abspath(os.path.join(os.path.split(__file__) [0]))
    res     = main(runner, path_test = path, skip = -1)
    for r in res :
        k = str (r [1])
        if "errors=0" not in k or "failures=0" not in k :
            print ("*", r[1], r[0])

