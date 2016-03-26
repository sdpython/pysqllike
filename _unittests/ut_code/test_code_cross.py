"""
@brief      test log(time=2s)
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
from src.pysqllike.translation.translation_to_python import Translate2Python
from src.pysqllike.generic.column_type import CFT


def myjob1(input):
    iter = input.select(input.ext, input.num, num2=input.num * input.num)
    wher = iter.where((iter.num2 < 8).And(iter.num2 > 1))
    return wher


def cube(x):
    return x * x * x


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

                assert co is None

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
