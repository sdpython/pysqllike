# pylint: disable=R1721
"""
@brief      test log(time=0s)
"""

import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8
from pyquickhelper.pycode.utils_tests_helper import _extended_refactoring


class TestCodeStyle(unittest.TestCase):

    def test_code_style_src(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG, extended=[("fLOG", _extended_refactoring)],
                   pylint_ignore=('C0103', 'C1801', 'R1705', 'W0108', 'W0613',
                                  'W0231', 'W0212', 'C0111', 'W0107', 'R1728',
                                  'C0209'),
                   skip=["Redefining built-in 'iter'",
                         "iter_rows.py:340",
                         "translation_class.py",
                         "translation_to_python.py:118",
                         "translation_to_python.py:185",
                         "translation_to_python.py:244",
                         "node_visitor_translator.py:74: E1111",
                         "R1720",
                         ]
                   )

    def test_code_style_test(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0111', 'C0103', 'W0622', 'C1801', 'C0412',
                                  'W0122', 'W0123', 'E1101', 'R1705',
                                  'W0107', 'R1720', 'C0209', 'R1721'),
                   skip=[],
                   extended=[("fLOG", _extended_refactoring)])


if __name__ == "__main__":
    unittest.main()
