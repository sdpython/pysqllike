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
from src.pysqllike.generic.column_type import NA


class TestSelectUnion (unittest.TestCase):

    def test_select_union(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        lr = [{"nom": "j", "age": 10, "gender": "M"},
              {"nom": "jean", "age": 40, "gender": "M"},
              {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, lr)

        iter = tbl.unionall(tbl)
        res = list(iter)

        exp = [{"nom": "j", "age": 10, "gender": "M"},
               {"nom": "jean", "age": 40, "gender": "M"},
               {"nom": "jeanne", "age": 2, "gender": "F"},
               {"nom": "j", "age": 10, "gender": "M"},
               {"nom": "jean", "age": 40, "gender": "M"},
               {"nom": "jeanne", "age": 2, "gender": "F"},
               ]

        if res != exp:
            raise ValueError(str(res))

    def test_select_union_notin(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        le = [{"nom": "j", "age": 10, "gender": "M"},
              {"nom": "jean", "age": 40, "gender": "M"},
              {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, le)

        le = [{"nom": "j", "newage": 10, "gender": "M"},
              {"nom": "jean", "newage": 40, "gender": "M"},
              {"nom": "jeanne", "newage": 2, "gender": "F"}]
        tbl2 = IterRow(None, le)

        iter = tbl.unionall(tbl2, merge_schema=True)
        res = list(iter)

        exp = [{'gender': 'M', 'nom': 'j', 'newage': 'NA()', 'age': 10},
               {'gender': 'M', 'nom': 'jean', 'newage': 'NA()', 'age': 40},
               {'gender': 'F', 'nom': 'jeanne', 'newage': 'NA()', 'age': 2},
               {'gender': 'F', 'nom': 'jeanne', 'newage': 10, 'age': 'NA()'},
               {'gender': 'F', 'nom': 'jeanne', 'newage': 40, 'age': 'NA()'},
               {'gender': 'F', 'nom': 'jeanne', 'newage': 2, 'age': 'NA()'}]

        def repl(d):
            return {k: repla(v) for k, v in d.items()}

        def repla(v):
            if isinstance(v, NA):
                return 'NA()'
            else:
                return v
        res = [repl(r) for r in res]

        if res != exp:
            raise ValueError(str(res))


if __name__ == "__main__":
    unittest.main()
