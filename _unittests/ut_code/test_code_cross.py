"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest
import inspect
import ast
import inspect
import _ast

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
from src.pysqllike.translation.node_visitor_translator import CodeNodeVisitor
from src.pysqllike.translation.translation_class import TranslateClass
from src.pysqllike.translation.translation_to_python import Translate2Python
from src.pysqllike.translation.code_exception import CodeException
from src.pysqllike.generic.column_type import CFT


def myjob1(input):
    iter = input.select(input.ext, input.num, num2=input.num * input.num)
    wher = iter.where((iter.num2 < 8).And(iter.num2 > 1))
    return wher


def cube(x): return x * x * x


def myjob2(input):
    iter = input.select(input.ext, input.num, num2=input.num * input.num)
    sele = iter.select(iter.ext, iter.num, iter.num2, num3=CFT(cube, iter.num))
    return sele


def myjob3(input):
    iter = input.groupby(input.year, size=input.ext.len())
    return iter

data1 = [{"ext": "pysqllike", "num": 3, "year": 2014},
         {"ext": "pyquickhelper", "num": 1, "year": 2013},
         {"ext": "pyensae", "num": 2, "year": 2013},
         {"ext": "pyrsslocal", "num": 3, "year": 2014}
         ]


class TestCodeCross (unittest.TestCase):

    def test_translation(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        data = [data1]
        functions = [myjob1, myjob2, myjob3]
        translate = [Translate2Python]

        nb = 0
        for i, f in enumerate(functions):
            fname = "myjob%d" % (i + 1)

            it = IterRow(None, data1)
            res = f(it)
            exp = list(res)

            for tr in translate:
                obj = tr(f)
                code = obj.Code()

                if i == len(functions) - 1:
                    fLOG("\n" + code)

                try:
                    co = exec(code)
                except Exception as e:
                    raise Exception("unable to compile code\n" + code) from e

                try:
                    exe = eval("%s(it)" % fname)
                except Exception as e:
                    raise Exception("unable to execute\n" + code) from e

                if i == len(functions) - 1:
                    fLOG("\nEXE:\n", exe, "\nEXP:\n", exp)
                assert exe == exp

                nb += 1
        assert nb > 0


if __name__ == "__main__":
    unittest.main()
