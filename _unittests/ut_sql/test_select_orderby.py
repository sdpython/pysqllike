"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest
import operator

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

try:
    import pyquickhelper
except ImportError:
    path = os.path.abspath(
        os.path.join(
            os.path.split(__file__)[0],
            "..",
            "..",
            "..",
            "pyquickhelper",
            "src"))
    sys.path.append(path)
    import pyquickhelper


from pyquickhelper import fLOG
from src.pysqllike.generic.iter_rows import IterRow, IterException


class TestSelectOrderBy (unittest.TestCase):

    def test_select_orderby(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [{"nom": "j", "age": 10, "gender": "M"},
             {"nom": "jean", "age": 40, "gender": "M"},
             {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, l)

        iter = tbl.orderby(tbl.nom, tbl.age, ascending=False)
        res = list(iter)

        exp = [{'gender': 'F', 'nom': 'jeanne', 'age': 2},
               {'gender': 'M', 'nom': 'jean', 'age': 40},
               {'gender': 'M', 'nom': 'j', 'age': 10}]

        if res != exp:
            raise ValueError(str(res))


if __name__ == "__main__":
    unittest.main()