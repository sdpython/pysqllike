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
        
    def Select(self, name, table, rows):
        """
        interpret a select statement
        
        @param      name        name of the table which receives the results
        @param      table       name of the table it applies to
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        code_rows = [ ]
        code_rows.append("{0} = [ ]".format(name))
        code_rows.append("for row in {0}:".format(table))

        done = { }
        code_exp = []
        code_exp.append("    newr = {")
        for r in rows :
            if r["type"] == "Attribute" :
                tbl,att = r["str"].split(".")
                if tbl != table :
                    self.RaiseCodeException("an attribute comes from an unexpected table {0}!={1}".format(table,tbl))
                if att not in done :
                    code_rows.append("    _{0}=row['{0}']".format(att))
                    done[att] = att
                code_exp.append("      '{0}':_{0},".format(att))
            elif r["type"] == "keyword" :
                # it has to be an expression
                att0 = r["str"]
                exp, fields, functions = self.ResolveExpression( r, "_" )
                
                if len(functions) > 0 :
                    # we do nothing here, we assume the function is known
                    # when it will be called
                    pass
                    
                for att_ in fields:
                    spl = att_.split(".")
                    if len(spl) != 2 :
                        self.RaiseCodeException("unexpected field name: " + att)
                    if spl[0] != table :
                        self.RaiseCodeException("unexpected table name: " + att)
                    att = spl[1]
                    if att not in done :
                        code_rows.append("    _{0}=row['{0}']".format(att))
                        done[att] = att
                    exp = exp.replace(att_,att)
                code_exp.append("      '{0}':{1},".format(att0, exp))
            else :
                self.RaiseCodeException("type expected {0}".format(r["type"]))
            r["processed"] = True
                
        code_rows.extend(code_exp)
        code_rows.append("      }")
        code_rows.append("    {0}.append(newr)".format(name))
        return [ "    " + _ for _ in code_rows ]
        
    def Where(self, name, table, rows):
        """
        interpret a select statement
        
        @param      name        name of the table which receives the results
        @param      table       name of the table it applies to
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        """
        interpret a select statement
        
        @param      name        name of the table which receives the results
        @param      table       name of the table it applies to
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        code_rows = [ ]
        code_rows.append("{0} = [ ]".format(name))
        code_rows.append("for row in {0}:".format(table))

        done = { }
        first = True
        for r in rows :
            if not first:
                self.RaiseCodeException("SyntaxError, only one clause where is allowed")
            att0 = r["str"]
            exp, fields, functions = self.ResolveExpression( r, "_")
            for att_ in fields:
                spl = att_.split(".")
                if len(spl) != 2 :
                    self.RaiseCodeException("unexpected field name: " + att)
                if spl[0] != table :
                    self.RaiseCodeException("unexpected table name: " + att)
                att = spl[1]
                if att not in done :
                    code_rows.append("    _{0}=row['{0}']".format(att))
                    done[att] = att
                exp = exp.replace(att_,att)
            code_rows.append("    _exp={0}".format(exp))
            code_rows.append("    if _exp: {0}.append(row)".format(name))
            r["processed"] = True
            first = False
                
        return [ "    " + _ for _ in code_rows ]
        
    def setReturn(self, nodes):
        """
        indicates all nodes containing information about returned results
        
        @param      node        list of nodes
        @return                 list of string
        """
        for node in nodes :
            node["processed"] = True
        names = [ node["str"] for node in nodes ]
        return [ "    return " + ",".join(names) ]
        

