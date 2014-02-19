"""     
@file
@brief One class which visits a syntax tree.
"""

import ast, inspect
from .code_exception import CodeException
from .node_visitor_translator import CodeNodeVisitor


class TranslateClass :
    """
    interface for a class which translates a code
    written in pseudo-SQL syntax into another language
    """
    def __init__(self, code_func):
        """
        constructor
        
        @param  code_func   code (str) or function(func)
        """
        if isinstance(code_func, str) :
            code = code_func
        else :
            code = inspect.getsource(code_func)
        self.init(code)
        
    def init(self, code):
        """
        parse the function code and add it the class,
        it complements the constructor
        
        @param  code        function code
        """
        node = ast.parse(code)
        v = CodeNodeVisitor()
        v.visit(node)
        
        self._rows = v.Rows
        self._code = code
        
    def __str__(self):
        """
        return a string representing a tree
        """
        return self.to_str()
        
    def to_str(self, fields = []) :
        """
        return a string representing a tree
        
        @param      fields      additional fields to add at the end of each row
        @return                 string
        """
        if len(fields) == 0 :
            rows = ["{0}{1}: {2} - nbch {3}".format("    " * r["indent"], r["type"], r["str"], len(r.get("children",[]))) \
                        for r in self._rows ]
        else :
            rows = ["{0}{1}: {2} - nbch {3}".format("    " * r["indent"], r["type"], r["str"], len(r.get("children",[]))) + \
                        " --- " + ",".join( [ "%s=%s" % (_,r.get(_,"")) for _ in fields ] ) \
                        for r in self._rows ]
            
        return "\n".join(rows)
        
    def Code(self):
        """
        returns the code of the initial Python function
        into another language
        
        @return     str
        """
        # we add a field "processed" in each rows to tell it was interpreted
        for row in self._rows :
            row["processed"] = row["type"] == "Module"
            
        code_rows = [ ]
            
        for row in self._rows :
            if row["processed"] :
                continue
                
            if row["type"] == "FunctionDef":
                res = self.interpretFunction(row)
                if res is not  None and len(res) > 0 : code_rows.extend( res )
                
        for row in self._rows :
            if not row["processed"] :
                self.RaiseCodeException("the function was unable to interpret all the lines", code_rows = code_rows)
                
        return "\n".join(code_rows)
                                
    def RaiseCodeException(self, message, field = "processed", code_rows = []):
        """
        raises an exception when interpreting the code
        
        @param  field       field to add to the message exception
        @param  code_rows   list of rows to display
        
        :raises: CodeException
        """
        raise CodeException(message + "\n---tree:\n" + \
                        self.to_str(["processed"]) + "\n\n---so far:\n" + \
                        "\n".join(code_rows))
                                
    def interpretFunction(self, obj):
        """
        starts the interpretation of node which begins a function
        
        @param      obj     obj to begin with (a function)
        @return             list of strings
        """
        if "children" not in obj : self.RaiseCodeException("children key is missing")
        if "name" not in obj : self.RaiseCodeException("name is missing")
        
        obj["processed"] = True
        chil = obj["children"]        
        code_rows = []
        
        # signature
        name = obj["name"]
        argus = [ _ for _ in chil if _["type"] == "arguments" ]
        args = []
        for a in argus :
            a["processed"] = True
            for ch in a["children"] :
                if ch["type"] == "arg" :
                    ch["processed"] = True
                    args.append(ch)
        names = [ _["str"] for _ in args ]
        
        sign = self.Signature(name, names)
        if sign is not  None and len(sign) > 0 : code_rows.extend(sign)
        
        # the rest
        assi = [ _ for _ in chil if _["type"] == "Assign" ]
        for an in assi :
            one = self.Intruction(an)
            if one is not None and len(one) > 0 : code_rows.extend(one)
        
        return code_rows
        
    def Signature(self, name, rows):
        """
        build the signature of a function based on its name and its children
        
        @param      name        name
        @param      rows        node where type == arguments
        @return                 list of strings (code)
        """
        self.RaiseCodeException("not implemented")
        
    def Intruction(self, rows):
        """
        build an instruction of a function based on its name and its children
        
        @param      rows        node where type == Assign
        @return                 list of strings (code)
        """
        rows["processed"] = True
        chil = rows["children"]
        name = [ _ for _ in chil if _["type"] == "Name"]
        if len(name)!=1 : self.RaiseCodeException("expecting only one row not %d" % len(call))
        call = [ _ for _ in chil if _["type"] == "Call"]
        if len(call)!=1 : self.RaiseCodeException("expecting only one row not %d" % len(call))
        
        name = name[0]
        name["processed"] = True
        
        call = call[0]
        call["prcessed"] = True
        
        varn = name["str"]
        kind = call["str"]
        if kind == "select":
            return self.Select(varn, call["children"])
        elif kind == "where":
            return self.Where(varn, call["children"])
        else:
            self.RaiseCodeException("not implemented for: " + kind) 
        
    def Select(self, name, rows):
        """
        interpret a select statement
        
        @param      name        name of the table to consider
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        self.RaiseCodeException("not implemented")
        
    def Where(self, name, rows):
        """
        interpret a select statement
        
        @param      name        name of the table to consider
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        self.RaiseCodeException("not implemented")
        

