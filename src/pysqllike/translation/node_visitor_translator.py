"""
@file
@brief One class which visits a syntax tree.
"""

import ast


class CodeNodeVisitor(ast.NodeVisitor):

    """
    Defines a visitor which walks though the syntax tree of the code.

    .. exref::
        :title: Get the tree of a simple function

        The following code uses Python syntax but follows a SQL logic.

        .. runpython::
            :showcode:
            :process:

            import ast
            import inspect
            import textwrap
            from pysqllike.translation.node_visitor_translator import CodeNodeVisitor

            def myjob(input):
                iter = input.select (input.age, input.nom, age2 = input.age2*input.age2)
                wher = iter.where( (iter.age > 60).Or(iter.age < 25))
                return wher

            code = textwrap.dedent(inspect.getsource(myjob))
            node = ast.parse(code)
            v = CodeNodeVisitor()
            v.visit(node)
            for r in v.Rows :
                print("{0}{1}: {2}".format("    " * r["indent"], r["type"], r["str"]))
    """

    def __init__(self):
        """
        constructor
        """
        ast.NodeVisitor.__init__(self)
        self._rows = []
        self._indent = 0
        self._stack = []

    def push(self, row):
        """
        Pushes an element into a list.
        """
        self._rows.append(row)

    def generic_visit(self, node, row):
        """
        Overrides ``generic_visit`` to keep track of the indentation
        and the node parent. The function will add field
        ``row["children"] = visited`` nodes from here.

        @param      node        node which needs to be visited
        @param      row         row (a dictionary)
        @return                 See ``ast.NodeVisitor.generic_visit``
        """
        self._indent += 1
        last = len(self._rows)
        res = ast.NodeVisitor.generic_visit(self, node)
        row["children"] = [
            _ for _ in self._rows[
                last:] if _["indent"] == self._indent]
        self._indent -= 1
        return res

    def visit(self, node):
        """
        Visits a node, a method must exist for every object class.
        """
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, None)
        if visitor is None:
            raise TypeError("unable to find a method: " + method)
        res = visitor(node)
        # print(method, CodeNodeVisitor.print_node(node))
        return res

    @staticmethod
    def print_node(node):
        """
        Debugging purpose.
        """
        r = []
        for att in ["s", "name", "str", "id", "body", "n",
                    "arg", "targets", "attr", "returns", "ctx"]:
            if att in node.__dict__:
                r.append("{0}={1}".format(att, str(node.__dict__[att])))
        return " ".join(r)

    def print_tree(self):
        """
        Displays the tree of instructions.

        @return     string
        """
        rows = []
        for r in self.Rows:
            rows.append(
                ("{0}{1}: {2}".format(
                    "    " *
                    r["indent"],
                    r["type"],
                    r["str"])))
        return "\n".join(rows)

    @property
    def Rows(self):
        """
        returns a list of dictionaries with all the elements of the code
        """
        return [_ for _ in self._rows if not _.get("remove", False)]

    def visit_Str(self, node):
        cont = {
            "indent": self._indent,
            "type": "Str",
            "str": node.s,
            "node": node,
            "value": node.s}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Name(self, node):
        cont = {
            "indent": self._indent,
            "type": "Name",
            "str": node.id,
            "node": node,
            "id": node.id,
            "ctx": node.ctx}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Module(self, node):
        cont = {
            "indent": self._indent,
            "type": "Module",
            "str": "",
            "body": node.body,
            "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_FunctionDef(self, node):
        cont = {"indent": self._indent, "type": "FunctionDef", "str": node.name, "name": node.name, "body": node.body,
                "node": node, "returns": node.returns}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_arguments(self, node):
        cont = {"indent": self._indent, "type": "arguments", "str": "",
                "node": node, "args": node.args}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_arg(self, node):
        cont = {"indent": self._indent, "type": "arg", "str": node.arg,
                "node": node,
                "arg": node.arg, "annotation": node.annotation}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Assign(self, node):
        cont = {"indent": self._indent, "type": "Assign", "str": "", "node": node,
                "targets": node.targets, "value": node.value}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Store(self, node):
        #cont = { "indent":self._indent, "type": "Store", "str": "" }
        # self.push(cont)
        cont = {}
        return self.generic_visit(node, cont)

    def visit_Call(self, node):
        if "attr" in node.func.__dict__:
            cont = {"indent": self._indent, "type": "Call", "str": node.func.attr,
                    "node": node, "func": node.func}
        else:
            cont = {"indent": self._indent, "type": "Call", "str": node.func.id,
                    "node": node, "func": node.func}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Attribute(self, node):
        cont = {"indent": self._indent, "type": "Attribute", "str": node.attr,
                "node": node, "value": node.value, "ctx": node.ctx, "attr": node.attr}
        self.push(cont)
        # last = len(self._rows)
        res = self.generic_visit(node, cont)

        if len(cont["children"]) > 0:
            fir = cont["children"][0]
            if fir["type"] == "Name":
                parent = fir["node"].id
                cont["str"] = "{0}.{1}".format(parent, cont["str"])
                cont["children"][0]["remove"] = True
        return res

    def visit_Load(self, node):
        #cont = { "indent":self._indent, "type": "Load", "str": "" }
        # self.push(cont)
        cont = {}
        return self.generic_visit(node, cont)

    def visit_keyword(self, node):
        cont = {"indent": self._indent, "type": "keyword", "str": "{0}".format(node.arg),
                "node": node, "arg": node.arg, "value": node.value}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_BinOp(self, node):
        cont = {
            "indent": self._indent,
            "type": "BinOp",
            "str": "",
            "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Mult(self, node):
        cont = {
            "indent": self._indent,
            "type": "Mult",
            "str": "",
            "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Compare(self, node):
        cont = {
            "indent": self._indent,
            "type": "Compare",
            "str": "",
            "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Gt(self, node):
        cont = {"indent": self._indent, "type": "Gt", "str": "", "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Lt(self, node):
        cont = {"indent": self._indent, "type": "Lt", "str": "", "node": node}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Num(self, node):
        cont = {
            "indent": self._indent,
            "type": "Num",
            "node": node,
            "str": "{0}".format(
                node.n),
            'n': node.n}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_Return(self, node):
        cont = {"indent": self._indent, "type": "Return", "node": node, "str": "",
                'value': node.value}
        self.push(cont)
        return self.generic_visit(node, cont)

    def visit_(self, node):
        help(node)
        assert False
