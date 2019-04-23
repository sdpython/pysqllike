# coding: latin-1
"""
@brief      test log(time=1s)
"""
import unittest
from pysqllike.generic.iter_rows import IterRow
from pysqllike.generic.column_type import CFT


class TestSelect2 (unittest.TestCase):

    def test_select_function(self):
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
