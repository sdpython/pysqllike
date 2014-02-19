# coding: latin-1
"""
@brief      test log(time=1s)
"""

import sys, os, unittest, inspect, ast, inspect, _ast

try :
    import src
except ImportError :
    path = os.path.normpath(os.path.abspath( os.path.join( os.path.split(__file__)[0], "..", "..")))
    if path not in sys.path : sys.path.append (path)
    import src
    
try :
    import pyquickhelper
except ImportError :
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", "..", "..", "pyquickhelper", "src"))
    sys.path.append(path)
    import pyquickhelper
    

from pyquickhelper import fLOG
from src.pysqllike.generic.iter_rows import IterRow, IterException
from src.pysqllike.translation.node_visitor_translator import CodeNodeVisitor
from src.pysqllike.translation.translation_class import TranslateClass
from src.pysqllike.translation.translation_to_python import Translate2Python
from src.pysqllike.translation.code_exception import CodeException


def myjob(input):
    iter = input.select (input.age, input.nom, age2 = input.age2*input.age2)
    wher = iter.where( (iter.age > 60).Or(iter.age < 25))
    return where

class TestCode (unittest.TestCase):
    
    def test_tree_job(self) :
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        code = inspect.getsource(myjob)
        node = ast.parse(code)
        inode = 0
        stack = [(0,node)]
        
        return
        while len(stack) > 0 :
            ind,n = stack[-1]
            del stack[-1]
            att = { name:ch for name,ch in ast.iter_fields(n) }
            print ("  " * ind,type(n), att.get("name","--"), att)
            for ch in ast.iter_child_nodes(n) :
                stack.append( (ind+1,ch) )
                
    def test_translation(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        code = inspect.getsource(myjob)
        node = ast.parse(code)
        v = CodeNodeVisitor()
        v.visit(node)        
        assert len(v.Rows)==27
        
    def test_translate_class(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        trans = TranslateClass(myjob)
        #fLOG(trans)
        s = str(trans)
        assert len(s)>0
        assert "input.age2" in s

    def test_translate_class_code(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        trans = TranslateClass(myjob)
        try :
            code = trans.Code()
            assert False
        except CodeException as e :
            assert "not implemented" in str(e)
        
    def test_translate_2_python(self):
        fLOG (__file__, self._testMethodName, OutputPrint = __name__ == "__main__")
        trans = Translate2Python(myjob)
        code = trans.Code()
        assert "def myjob(input)" in code


if __name__ == "__main__"  :
    unittest.main ()    
