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
from src.pysqllike.generic.iter_rows import IterRow, IterException


class TestSelect (unittest.TestCase):

    def test_iter_simple(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        l = [("nom", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)
        l = list(tbl)
        assert len(l) == 2
        if l != [{'nom': 'nom', 'age': 10}, {'nom': 'jean', 'age': 40}]:
            raise ValueError(str(l))

        tbl = IterRow(schema, l, as_dict=False)
        l = list(tbl)
        assert len(l) == 2
        if l != [('nom', 10), ('jean', 40)]:
            raise ValueError(str(l))

    def test_iter_simple_dict(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        l0 = [{"nom": "jean", "age": 10},
              {"nom": "j", "age": 20}]
        tbl = IterRow(None, l0)
        l = list(tbl)
        assert len(l) == 2
        if l != l0:
            raise ValueError(str(l))

    def test_iter_simple_dict2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        l0 = [{"nom": "jean", "age": 10},
              {"nom": "j", "age": 20}]
        tbl = IterRow(None, l0)
        tbl2 = tbl.select(tbl.nom)
        l = list(tbl2)
        assert len(l) == 2
        if l != [{"nom": "jean"}, {"nom": "j"}]:
            raise ValueError(str(l))

    def test_select_simple(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        l = [("jake", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)
        l = list(tbl.select(tbl.nom, tbl.age))
        for _ in l:
            fLOG("+", _)
        if l != [{'age': 10, 'nom': 'jake'}, {'age': 40, 'nom': 'jean'}]:
            raise Exception(str(l))

    def test_select_simple2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, age2=tbl.age * 2, age3=tbl.age * 3)

        l = list(iter)
        assert len(l) == 2
        if l != [{'nom': 'nom', 'age2': 20, 'age3': 30},
                 {'nom': 'jean', 'age2': 80, 'age3': 120}]:
            raise Exception(str(l))

        iter = tbl.select(tbl.nom, age2=tbl.age * 2)
        sch = iter.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age2"

    def test_select_simple3(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, age2=tbl.age * 2)
        iter2 = iter.select(iter.nom, age4=iter.age2 * 2)

        l = list(iter2)
        assert len(l) == 3
        fLOG(";".join([str(_) for _ in iter2.Schema]))
        fLOG(l)
        if l != [{'age4': 40, 'nom': 'nom'}, {
                'age4': 160, 'nom': 'jean'}, {'age4': 8, 'nom': 'jeanne'}]:
            raise Exception(str(l))

        sch = iter2.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age4"

    def test_select_simple_square(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, age2=tbl.age, age3=tbl.age * 0.5)
        iter2 = iter.select(iter.nom, age4=iter.age2 * iter.age3)

        l = list(iter2)
        assert len(l) == 3
        fLOG(";".join([str(_) for _ in iter2.Schema]))
        fLOG(l)
        if l != [{'age4': 50.0, 'nom': 'nom'}, {
                'age4': 800.0, 'nom': 'jean'}, {'age4': 2.0, 'nom': 'jeanne'}]:
            raise Exception(str(l))

        sch = iter2.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age4"

    def test_select_mismatch(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, age2=tbl.age, age3=tbl.age * 0.5)
        try:
            iter.select(iter.nom, tbl.age)
            raise TypeError(
                "we should not be able to reach this code due to confusion between iter and tbl")
        except IterException as e:
            fLOG(e)
            assert "mismatch" in str(e)
        # however we do not check formulas...

    def test_select_operators(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, age0=tbl.age,
                          agem=tbl.age * 0.5,
                          agea=tbl.age + 0.5,
                          ages=tbl.age - 0.5,
                          agep=tbl.age ** 0.5, agedd=tbl.age // 3, agemod=tbl.age % 3
                          )

        res = list(iter)

        exp = [{'age0': 10, 'ages': 9.5, 'agemod': 1, 'agem': 5.0, 'agep': 3.1622776601683795, 'agea': 10.5, 'agedd': 3, 'nom': 'nom'},
               {'age0': 40,
                'ages': 39.5,
                'agemod': 1,
                'agem': 20.0,
                'agep': 6.324555320336759,
                'agea': 40.5,
                'agedd': 13,
                'nom': 'jean'},
               {'age0': 2, 'ages': 1.5, 'agemod': 2, 'agem': 1.0, 'agep': 1.4142135623730951, 'agea': 2.5, 'agedd': 0, 'nom': 'jeanne'}]

        if res != exp:
            raise ValueError(str(res))

    def test_select_bracket(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.select(tbl.nom, formula=tbl.age + (tbl.age + 2) / 3)

        res = list(iter)

        exp = [{'formula': 14.0, 'nom': 'nom'},
               {'formula': 54.0, 'nom': 'jean'},
               {'formula': 3.333333333333333, 'nom': 'jeanne'}]

        if res != exp:
            raise ValueError(str(res))

    def test_where(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.where(tbl.age == 40)
        res = list(iter)

        exp = [{'nom': "jean", 'age': 40}]

        if res != exp:
            raise ValueError(str(res))

    def test_where2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)

        iter = tbl.where(tbl.age >= 40)
        res = list(iter)
        exp = [{'nom': "jean", 'age': 40}]
        if res != exp:
            raise ValueError(str(res))

        iter = tbl.where(tbl.age <= 2)
        res = list(iter)
        exp = [{'nom': "jeanne", 'age': 2}]
        if res != exp:
            raise ValueError(str(res))

        iter = tbl.where(tbl.age < 2)
        res = list(iter)
        exp = []
        if res != exp:
            raise ValueError(str(res))

        iter = tbl.where(tbl.age > 20)
        res = list(iter)
        exp = [{'nom': "jean", 'age': 40}]
        if res != exp:
            raise ValueError(str(res))

        iter = tbl.where(tbl.age != 10)
        res = list(iter)
        assert len(res) == 2

    def test_where_or(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        l = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, l)
        iter = tbl.where(
            (tbl.age == 2).Or(
                tbl.age == 40),
            append_condition=True)
        res = list(iter)
        exp = [{'nom': 'jean', 'age': 40, '__unk__': True},
               {'nom': "jeanne", 'age': 2, '__unk__': True}, ]
        if res != exp:
            raise ValueError(str(res) + "\n\n" + iter.print_schema())

        iter = tbl.where((tbl.age == 10).Not())
        res = list(iter)
        assert len(res) == 2


if __name__ == "__main__":
    unittest.main()
