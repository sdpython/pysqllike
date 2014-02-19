"""     
@file
@brief One class which visits a syntax tree.
"""

from .translation_class import TranslateClass

class Translate2Python(TranslateClass) :
    """
    translate a code into Python
    
    """
    def __init__(self, code_func):
        """
        constructor
        
        @param  code_func   code (str) or function(func)
        """
        TranslateClass.__init__(self,code_func)
        
    def Signature(self, name, args):
        """
        build the signature of a function based on its name and its children
        
        @param      name        name
        @param      args        list of argumens
        @return                 list of strings (code)
        """
        code_rows = [ "def {0}({1}):".format (name, ", ".join(args)) ]
        return code_rows
        
    def Select(self, name, rows):
        """
        interpret a select statement
        
        @param      name        name of the table to consider
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        #self.RaiseCodeException("not implemented")
        pass
        
    def Where(self, name, rows):
        """
        interpret a select statement
        
        @param      name        name of the table to consider
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        #self.RaiseCodeException("not implemented")
        pass
        

