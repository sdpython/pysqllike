"""
@brief      test log(time=1s)
"""
import unittest
from pysqllike.generic.iter_rows import IterRow


class TestSelectOrderBy (unittest.TestCase):

    def test_select_orderby(self):
        le = [{"nom": "j", "age": 10, "gender": "M"},
              {"nom": "jean", "age": 40, "gender": "M"},
              {"nom": "jeanne", "age": 2, "gender": "F"}]
        tbl = IterRow(None, le)

        iter = tbl.orderby(tbl.nom, tbl.age, ascending=False)
        res = list(iter)

        exp = [{'gender': 'F', 'nom': 'jeanne', 'age': 2},
               {'gender': 'M', 'nom': 'jean', 'age': 40},
               {'gender': 'M', 'nom': 'j', 'age': 10}]

        if res != exp:
            raise ValueError(str(res))


if __name__ == "__main__":
    unittest.main()
