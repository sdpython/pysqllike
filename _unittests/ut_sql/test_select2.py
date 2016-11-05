# coding: latin-1
"""
@brief      test log(time=1s)
"""

import sys
import os
import unittest


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
    import pyquickhelper as skip_
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
    import pyquickhelper as skip_


from pyquickhelper.loghelper import fLOG
from src.pysqllike.generic.iter_rows import IterRow
from src.pysqllike.generic.column_type import CFT


class TestSelect2 (unittest.TestCase):

    def test_select_function(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        def myf(x, y):
            return x * 2.5 + y
        iter = tbl.select(tbl.nom, age0=CFT(myf, tbl.age, tbl.age))
        res = list(iter)

        exp = [{'nom': 'nom', 'age0': 35.0},
               {'nom': 'jean', 'age0': 140.0},
               {'nom': 'jeanne', 'age0': 7.0}]

        if res != exp:
            raise ValueError(str(res))

    def test_select_function2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        lr = [{"nom": "j", "age": 10},
              {"nom": "jean", "age": 40},
              {"nom": "jeanne", "age": 2}]
        tbl = IterRow(None, lr)

        def myf(x, y):
            return x * 2.5 + y
        iter = tbl.select(tbl.nom, age0=CFT(myf, tbl.age, tbl.age))
        res = list(iter)

        exp = [{'nom': 'j', 'age0': 35.0},
               {'nom': 'jean', 'age0': 140.0},
               {'nom': 'jeanne', 'age0': 7.0}]

        if res != exp:
            raise ValueError(str(res))


if __name__ == "__main__":
    unittest.main()
