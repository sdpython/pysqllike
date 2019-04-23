# coding: latin-1
"""
@brief      test log(time=1s)
"""
import unittest
from pysqllike.generic.iter_rows import IterRow, IterException


class TestSelect (unittest.TestCase):

    def test_iter_simple(self):
        lr = [("nom", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)
        lr = list(tbl)
        assert len(lr) == 2
        if lr != [{'nom': 'nom', 'age': 10}, {'nom': 'jean', 'age': 40}]:
            raise ValueError(str(lr))

        tbl = IterRow(schema, lr, as_dict=False)
        lr = list(tbl)
        assert len(lr) == 2
        if lr != [('nom', 10), ('jean', 40)]:
            raise ValueError(str(lr))

    def test_iter_simple_dict(self):
        l0 = [{"nom": "jean", "age": 10},
              {"nom": "j", "age": 20}]
        tbl = IterRow(None, l0)
        lr = list(tbl)
        assert len(lr) == 2
        if lr != l0:
            raise ValueError(str(lr))

    def test_iter_simple_dict2(self):
        l0 = [{"nom": "jean", "age": 10},
              {"nom": "j", "age": 20}]
        tbl = IterRow(None, l0)
        tbl2 = tbl.select(tbl.nom)
        lr = list(tbl2)
        assert len(lr) == 2
        if lr != [{"nom": "jean"}, {"nom": "j"}]:
            raise ValueError(str(lr))

    def test_select_simple(self):
        lr = [("jake", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)
        lr = list(tbl.select(tbl.nom, tbl.age))
        if lr != [{'age': 10, 'nom': 'jake'}, {'age': 40, 'nom': 'jean'}]:
            raise Exception(str(lr))

    def test_select_simple2(self):
        lr = [("nom", 10), ("jean", 40)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.select(tbl.nom, age2=tbl.age * 2, age3=tbl.age * 3)

        lr = list(iter)
        assert len(lr) == 2
        if lr != [{'nom': 'nom', 'age2': 20, 'age3': 30},
                  {'nom': 'jean', 'age2': 80, 'age3': 120}]:
            raise Exception(str(lr))

        iter = tbl.select(tbl.nom, age2=tbl.age * 2)
        sch = iter.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age2"

    def test_select_simple3(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.select(tbl.nom, age2=tbl.age * 2)
        iter2 = iter.select(iter.nom, age4=iter.age2 * 2)

        lr = list(iter2)
        assert len(lr) == 3
        if lr != [{'age4': 40, 'nom': 'nom'}, {
                'age4': 160, 'nom': 'jean'}, {'age4': 8, 'nom': 'jeanne'}]:
            raise Exception(str(lr))

        sch = iter2.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age4"

    def test_select_simple_square(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.select(tbl.nom, age2=tbl.age, age3=tbl.age * 0.5)
        iter2 = iter.select(iter.nom, age4=iter.age2 * iter.age3)

        lr = list(iter2)
        assert len(lr) == 3
        if lr != [{'age4': 50.0, 'nom': 'nom'}, {
                'age4': 800.0, 'nom': 'jean'}, {'age4': 2.0, 'nom': 'jeanne'}]:
            raise Exception(str(lr))

        sch = iter2.Schema
        assert sch[0].Name == "nom"
        assert sch[1].Name == "age4"

    def test_select_mismatch(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.select(tbl.nom, age2=tbl.age, age3=tbl.age * 0.5)
        try:
            iter.select(iter.nom, tbl.age)
            raise TypeError(
                "we should not be able to reach this code due to confusion between iter and tbl")
        except IterException as e:
            assert "mismatch" in str(e)
        # however we do not check formulas...

    def test_select_operators(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

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
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.select(tbl.nom, formula=tbl.age + (tbl.age + 2) / 3)

        res = list(iter)

        exp = [{'formula': 14.0, 'nom': 'nom'},
               {'formula': 54.0, 'nom': 'jean'},
               {'formula': 3.333333333333333, 'nom': 'jeanne'}]

        if res != exp:
            raise ValueError(str(res))

    def test_where(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

        iter = tbl.where(tbl.age == 40)
        res = list(iter)

        exp = [{'nom': "jean", 'age': 40}]

        if res != exp:
            raise ValueError(str(res))

    def test_where2(self):
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)

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
        lr = [("nom", 10), ("jean", 40), ("jeanne", 2)]
        schema = [("nom", str), ("age", int)]
        tbl = IterRow(schema, lr)
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
