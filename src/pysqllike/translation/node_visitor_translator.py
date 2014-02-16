"""     
@file
@brief This file was inspired by the following one `transbits.py <https://github.com/chrishumphreys/p2j/blob/master/translator/>`_
"""

import ast


class CodeNodeVisitor(ast.NodeVisitor):
    """
    Defines a visitor which walks though the syntax tree of the code.
    
    @example(get the tree of a simple function)
    @code
    def myjob(input):
        iter = input.select (input.age, input.nom, age2 = input.age2*input.age2)
        wher = iter.where( (iter.age > 60).Or(iter.age < 25))
        return where    
    
    code = inspect.getsource(myjob)
    node = ast.parse(code)
    v = CodeNodeVisitor()
    v.visit(node)
    for r in v.Rows :
        print("{0}{1}: {2}".format("    " * r["indent"], r["type"], r["str"]))
    @endcode
    
    The previous will produce the following:
    
    @code
    Module: 
        FunctionDef: myjob
            arguments: 
                arg: input
            Assign: 
                Name: iter
                Call: select
                    Attribute: input.select
                    Attribute: input.age
                    Attribute: input.nom
                    keyword: age2
                        BinOp: 
                            Attribute: input.age2
                            Mult: 
                            Attribute: input.age2
            Assign: 
                Name: wher
                Call: where
                    Attribute: iter.where
                    Call: Or
                        Attribute: age.Or
                        Compare: 
                            Attribute: iter.age
                            Lt: 
                            Num: 25
            Return: 
                Name: where
    @endcode
    @endexample
    
    
    """
    def __init__(self):
        """
        constructor
        """
        ast.NodeVisitor.__init__(self)
        self._rows = []
        self._indent = 0
        self._stack = [ ]
        
    def push(self,row):
        """
        push an element into a list
        """
        self._rows.append(row)
        
    def generic_visit(self, node):
        """
        override generic_visit to keep track of the indentation
        and the node parent
        """
        self._indent += 1
        res = ast.NodeVisitor.generic_visit(self,node)
        self._indent -= 1
        return res
        
    def visit(self, node):
        """
        Visit a node, a method must exist for every object class
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor == None :
            raise TypeError("unable to find a method: " + method)
        return visitor(node)        
        
    @property
    def Rows(self):
        """
        returns a list of dictionaries with all the elements of the code
        """
        return self._rows
        
    def visit_Str(self, node):
        cont = { "indent":self._indent, "type": "Str", "str":node.s, "node":node, "value":node.s } 
        self.push(cont)
        return self.generic_visit(node)
        
    def visit_Name(self, node):
        cont = { "indent":self._indent, "type": "Name", "str":node.id,  "node":node, "id":node.id , "ctx":node.ctx } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Module(self, node):
        cont = { "indent":self._indent, "type": "Module", "str": "" , "body":node.body, "node":node } 
        self.push(cont)
        return self.generic_visit(node)
        
    def visit_FunctionDef(self, node):
        cont = { "indent":self._indent, "type": "FunctionDef", "str": node.name , "name":node.name, "body":node.body,
                    "node":node, "returns":node.returns} 
        self.push(cont)
        return self.generic_visit(node)

    def visit_arguments(self, node):
        cont = { "indent":self._indent, "type": "arguments", "str": "" , 
                     "node":node,   "args":node.args } 
        self.push(cont)
        return self.generic_visit(node)
        
    def visit_arg(self, node):
        cont = { "indent":self._indent, "type": "arg", "str": node.arg , 
                    "node":node,
                        "arg":node.arg, "annotation":node.annotation } 
        self.push(cont)
        return self.generic_visit(node)
        
    def visit_Assign(self, node):
        cont = { "indent":self._indent, "type": "Assign", "str": "" , "node":node,
                        "targets":node.targets, "value":node.value } 
        self.push(cont)
        return self.generic_visit(node)
        
    def visit_Store(self, node):
        #cont = { "indent":self._indent, "type": "Store", "str": "" } 
        #self.push(cont)
        return self.generic_visit(node)

    def visit_Call(self, node):
        cont = { "indent":self._indent, "type": "Call", "str": node.func.attr , 
                    "node":node, "func":node.func } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Attribute(self, node):
        cont = { "indent":self._indent, "type": "Attribute", "str": node.attr , 
                    "node":node, "value":node.value, "ctx":node.ctx, "attr":node.attr } 
        self.push(cont)
        last = len(self._rows)
        res = self.generic_visit(node)
        
        cont["belongs"] = self._rows[last:]
        del self._rows[last:]
        
        names = [ r for r in cont["belongs"] if r["type"] in ("Name", "Attribute") ]
        names = [ (r["node"].id if r["type"]=="Name" else r["node"].attr) for r in names ]
        names.reverse()
        cont["str"] = "{0}.{1}".format(".".join(names), cont["str"])
        
        return res

    def visit_Load(self, node):
        #cont = { "indent":self._indent, "type": "Load", "str": "" } 
        #self.push(cont)
        return self.generic_visit(node)

    def visit_keyword(self, node):
        cont = { "indent":self._indent, "type": "keyword", "str": "{0}".format(node.arg) , 
                        "node":node, "arg":node.arg, "value":node.value } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_BinOp(self, node):
        cont = { "indent":self._indent, "type": "BinOp", "str": "", "node":node } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Mult(self, node):
        cont = { "indent":self._indent, "type": "Mult", "str": "", "node":node } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Compare(self, node):
        cont = { "indent":self._indent, "type": "Compare", "str": "", "node":node } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Gt(self, node):
        cont = { "indent":self._indent, "type": "Gt", "str": "", "node":node } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Lt(self, node):
        cont = { "indent":self._indent, "type": "Lt", "str": "", "node":node } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Num(self, node):
        cont = { "indent":self._indent, "type": "Num", "node":node, "str": "{0}".format(node.n), 'n':node.n } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_Return(self, node):
        cont = { "indent":self._indent, "type": "Return", "node":node, "str": "", 
                        'value':node.value } 
        self.push(cont)
        return self.generic_visit(node)

    def visit_(self, node):
        help(node)
        assert False




