"""
@brief      test log(time=2s)
"""
import unittest
from pysqllike.generic.iter_rows import IterRow
from pysqllike.translation.translation_to_python import Translate2Python
from pysqllike.generic.column_type import CFT


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

                try:
                    co = exec(code)
                except Exception as e:
                    raise Exception("unable to compile code\n" + code) from e

                assert co is None

                try:
                    exe = eval("%s(it)" % fname)
                except Exception as e:
                    raise Exception("unable to execute\n" + code) from e

                if exe != exp:
                    exe.reverse()
                    self.assertEqual(exe, exp)

                nb += 1
        assert nb > 0


if __name__ == "__main__":
    unittest.main()
