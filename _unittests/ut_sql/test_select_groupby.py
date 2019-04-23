"""
@brief      test log(time=1s)
"""
import unittest
from pysqllike.generic.iter_rows import IterRow
from pysqllike.generic.iter_exceptions import NotAllowedOperation


class TestSelectGroupBy (unittest.TestCase):

    def test_select_function2(self):
        lr = [{"nom": "j", "age": 10, "gender": "M"},
              {"nom": "jean", "age": 40, "gender": "M"},
              {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, lr)

        iter = tbl.groupby(
            tbl.gender,
            len_nom=tbl.nom.len(),
            avg_age=tbl.age.avg())
        res = list(iter)

        exp = [{'gender': 'F', 'len_nom': 1, 'avg_age': 2.0},
               {'gender': 'M', 'len_nom': 2, 'avg_age': 25.0},
               ]

        if res != exp:
            raise ValueError(str(res))

        try:
            tbl.groupby(
                tbl.gender,
                len_nom=tbl.nom.len() * 2,
                avg_age=tbl.age.avg())
            raise Exception("unexpected, it should raise an exception")
        except NotAllowedOperation:
            pass

    def test_select_function3(self):
        le = [{"nom": "j", "age": 10, "gender": "M"},
              {"nom": "jean", "age": 40, "gender": "M"},
              {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, le)

        iter = tbl.groupby(tbl.gender, tbl.nom, nbs=tbl.age.len())
        res = list(iter)

        exp = [{'nbs': 1, 'gender': 'F', 'nom': 'jeanne'},
               {'nbs': 1, 'gender': 'M', 'nom': 'j'},
               {'nbs': 1, 'gender': 'M', 'nom': 'jean'}]

        if res != exp:
            raise ValueError(str(res))

        try:
            tbl.groupby(
                tbl.gender,
                len_nom=tbl.nom.len() * 2,
                avg_age=tbl.age.avg())
            raise Exception("unexpected, it should raise an exception")
        except NotAllowedOperation:
            pass


if __name__ == "__main__":
    unittest.main()
