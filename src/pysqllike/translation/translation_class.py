"""
@file
@brief One class which visits a syntax tree.
"""

import ast
import inspect
from .code_exception import CodeException
from .node_visitor_translator import CodeNodeVisitor


class TranslateClass:

    """
    Interface for a class which translates a code
    written in pseudo-SQL syntax into another language.
    """

    def __init__(self, code_func):
        """
        Constructor.

        @param  code_func   code (str) or function(func)
        """
        if isinstance(code_func, str):
            code = code_func
        else:
            code = inspect.getsource(code_func)
        self.init(code)

    def init(self, code):
        """
        Parses the function code and add it the class,
        it complements the constructor.

        @param  code        function code
        """
        node = ast.parse(code)
        v = CodeNodeVisitor()
        v.visit(node)

        self._rows = v.Rows
        self._code = code

    def __str__(self):
        """
        Returns a string representing a tree.
        """
        return self.to_str()

    def to_str(self, fields=None):
        """
        Returns a string representing a tree.

        @param      fields      additional fields to add at the end of each row
        @return                 string
        """
        if fields is None:
            fields = []
        if len(fields) == 0:
            rows = ["{0}{1}: {2} - nbch {3}".format("    " * r["indent"], r["type"], r["str"], len(r.get("children", [])))
                    for r in self._rows]
        else:
            rows = ["{0}{1}: {2} - nbch {3}".format("    " * r["indent"], r["type"], r["str"], len(r.get("children", [])))
                    + " --- " + ",".join(["%s=%s" %
                                          (_, r.get(_, "")) for _ in fields])
                    for r in self._rows]

        return "\n".join(rows)

    def Code(self):
        """
        Returns the code of the initial Python function
        into another language.

        @return     str
        """
        # we add a field "processed" in each rows to tell it was interpreted
        for row in self._rows:
            row["processed"] = row["type"] == "Module"

        code_rows = []

        for row in self._rows:
            if row["processed"]:
                continue

            if row["type"] == "FunctionDef":
                res = self.interpretFunction(row)
                if res is not None and len(res) > 0:
                    code_rows.extend(res)

        for row in self._rows:
            if not row["processed"]:
                return self.RaiseCodeException(
                    "the function was unable to interpret all the lines",
                    code_rows=code_rows)

        return "\n".join(code_rows)

    def RaiseCodeException(self, message, field="processed", code_rows=None):
        """
        Raises an exception when interpreting the code.

        @param  field       field to add to the message exception
        @param  code_rows   list of rows to display

        :raises: CodeException
        """
        if code_rows is None:
            code_rows = []
        if len(code_rows) > 0:
            if "_status" in self.__dict__ and len(self._status) > 0:
                code_rows = code_rows + ["", "-- STATUS --", ""] + self._status
            raise CodeException(message + "\n---tree:\n"
                                + self.to_str(["processed"]) +
                                "\n\n---so far:\n"
                                + "\n".join(code_rows))
        elif "_status" in self.__dict__:
            raise CodeException(message + "\n---tree:\n"
                                + self.to_str(["processed"]) +
                                "\n\n-- STATUS --\n"
                                + "\n".join(self._status))
        else:
            raise CodeException(message + "\n---tree:\n"
                                + self.to_str(["processed"]))

    def interpretFunction(self, obj):
        """
        Starts the interpretation of node which begins a function.

        @param      obj     obj to begin with (a function)
        @return             list of strings
        """
        if "children" not in obj:
            return self.RaiseCodeException("children key is missing")
        if "name" not in obj:
            return self.RaiseCodeException("name is missing")

        obj["processed"] = True
        chil = obj["children"]
        code_rows = []

        # signature
        name = obj["name"]
        argus = [_ for _ in chil if _["type"] == "arguments"]
        args = []
        for a in argus:
            a["processed"] = True
            for ch in a["children"]:
                if ch["type"] == "arg":
                    ch["processed"] = True
                    args.append(ch)
        names = [_["str"] for _ in args]

        sign = self.Signature(name, names)
        if sign is not None and len(sign) > 0:
            code_rows.extend(sign)

        # the rest
        self._status = code_rows  # for debugging purpose
        # assi = [_ for _ in chil if _["type"] == "Assign"]
        for an in chil:
            if an["type"] == "Assign":
                one = self.Intruction(an)
                if one is not None and len(one) > 0:
                    code_rows.extend(one)
            elif an["type"] == "Return":
                one = self.interpretReturn(an)
                if one is not None and len(one) > 0:
                    code_rows.extend(one)
            elif an["type"] == "arguments":
                pass
            else:
                return self.RaiseCodeException("unexpected type: " + an["type"])
        return code_rows

    def Signature(self, name, rows):
        """
        Build the signature of a function based on its name and its children.

        @param      name        name
        @param      rows        node where type == arguments
        @return                 list of strings (code)
        """
        return self.RaiseCodeException("not implemented")

    def Intruction(self, rows):
        """
        Builds an instruction of a function based on its name and its children.

        @param      rows        node where type == Assign
        @return                 list of strings (code)
        """
        rows["processed"] = True
        chil = rows["children"]
        name = [_ for _ in chil if _["type"] == "Name"]
        if len(name) != 1:
            return self.RaiseCodeException(
                "expecting only one row not %d" %
                len(chil))
        call = [_ for _ in chil if _["type"] == "Call"]
        if len(call) != 1:
            return self.RaiseCodeException(
                "expecting only one row not %d" %
                len(call))

        name = name[0]
        name["processed"] = True

        call = call[0]
        call["processed"] = True

        varn = name["str"]
        kind = call["str"]

        # the first attribute gives the name the table
        method = call["children"][0]
        method["processed"] = True
        table, meth = method["str"].split(".")
        if meth != kind:
            return self.RaiseCodeException(
                "cannot go further, expects: {0}=={1}".format(
                    kind,
                    meth))

        if kind == "select":
            top = call["children"][1:]
            return self.Select(varn, table, top)
        elif kind == "where":
            top = call["children"][1:]
            return self.Where(varn, table, top)
        elif kind == "groupby":
            top = call["children"][1:]
            return self.GroupBy(varn, table, top)
        else:
            return self.RaiseCodeException("not implemented for: " + kind)

    def Select(self, name, table, rows):
        """
        Interprets a select statement.

        @param      name        name of the table which receives the results
        @param      table       name of the table it applies to
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        return self.RaiseCodeException("not implemented")

    def Where(self, name, table, rows):
        """
        Interprets a select statement.

        @param      name        name of the table which receives the results
        @param      table       name of the table it applies to
        @param      rows        rows to consider
        @return                 list of strings (code)
        """
        return self.RaiseCodeException("not implemented")

    _symbols = {"Lt": "<", "Gt": ">", "Mult": "*", }

    def ResolveExpression(self, node, prefixAtt):
        """
        Produces an expression based on a a node and its children.

        @param      node        node
        @param      prefixAtt   prefix to add before an attribute (usually _)
        @return                 a string, the used fields, the called functions
        """
        if node["type"] == "keyword":
            chil = node["children"]
            if len(chil) == 1:
                node["processed"] = True
                return self.ResolveExpression(chil[0], prefixAtt)
            else:
                return self.RaiseCodeException(
                    "not implemented for type: "
                    + node["type"])

        elif node["type"] == "BinOp" or node["type"] == "Compare":
            chil = node["children"]
            if len(chil) == 3:
                node["processed"] = True
                ex1, fi1, fu1 = self.ResolveExpression(chil[0], prefixAtt)
                ex2, fi2, fu2 = self.ResolveExpression(chil[1], prefixAtt)
                ex3, fi3, fu3 = self.ResolveExpression(chil[2], prefixAtt)
                fi1.update(fi2)
                fi1.update(fi3)
                fu1.update(fu2)
                fu1.update(fu3)
                ex = "{0}{1}{2}".format(ex1, ex2, ex3)
                return ex, fi1, fu1
            else:
                return self.RaiseCodeException(
                    "not implemented for type: "
                    + node["type"])

        elif node["type"] in TranslateClass._symbols:
            node["processed"] = True
            return TranslateClass._symbols[node["type"]], {}, {}

        elif node["type"] == "Attribute":
            node["processed"] = True
            return prefixAtt + node["str"], {node["str"]: node}, {}

        elif node["type"] == "Num":
            node["processed"] = True
            return node["str"], {}, {}

        elif node["type"] == "Call":
            node["processed"] = True

            expre = []
            field = {}
            funcs = {}

            if node["str"] in ["Or", "And", "Not"]:
                for chil in node["children"]:
                    if chil["type"] == "Attribute":
                        if chil["str"] != node["str"]:
                            return self.RaiseCodeException("incoherence")
                        elif len(chil["children"]) != 1:
                            return self.RaiseCodeException("incoherence")
                        else:
                            chil["processed"] = True
                            ex, fi, fu = self.ResolveExpression(
                                chil["children"][0], prefixAtt)
                            expre.append("({0})".format(ex))
                            field.update(fi)
                            funcs.update(funcs)
                            expre.append(node["str"].lower())
                    else:
                        ex, fi, fu = self.ResolveExpression(chil, prefixAtt)
                        expre.append("({0})".format(ex))
                        field.update(fi)
                        funcs.update(funcs)

            elif node["str"] == "CFT":
                # we need to look further as CFT is a way to call a function
                funcName = None
                subexp = []
                for chil in node["children"]:
                    if chil["type"] == "Attribute":
                        chil["processed"] = True
                        ex, fi, fu = self.ResolveExpression(chil, prefixAtt)
                        subexp.append(ex)
                        field.update(fi)
                        funcs.update(funcs)
                    elif chil["type"] == "Name" and chil["str"] == "CFT":
                        pass
                    elif chil["type"] == "Name":
                        # we call function chil["str"]
                        funcName = chil["str"]
                        funcs[chil["str"]] = chil["str"]
                    else:
                        return self.RaiseCodeException(
                            "unexpected configuration: "
                            + node["type"])
                    chil["processed"] = True
                expre.append("{0}({1})".format(funcName, ",".join(subexp)))

            elif node["str"] == "len":
                # aggregated function
                funcName = None
                subexp = []
                for chil in node["children"]:
                    if chil["type"] == "Attribute":
                        chil["processed"] = True
                        ex, fi, fu = self.ResolveExpression(chil, prefixAtt)
                        subexp.append(ex)
                        field.update(fi)
                        funcs.update(funcs)
                    elif chil["type"] == "Name" and chil["str"] == "CFT":
                        pass
                    elif chil["type"] == "Name":
                        # we call function chil["str"]
                        funcName = chil["str"]
                        funcs[chil["str"]] = chil["str"]
                    else:
                        return self.RaiseCodeException(
                            "unexpected configuration: "
                            + node["type"])
                    chil["processed"] = True
                expre.append("{0}({1})".format(funcName, ",".join(subexp)))
            else:
                return self.RaiseCodeException(
                    "not implemented for function: "
                    + node["str"])
            return " ".join(expre), field, funcs

        else:
            return self.RaiseCodeException(
                "not implemented for type: "
                + node["type"])

    def interpretReturn(self, obj):
        """
        Starts the interpretation of a node which sets a return.

        @param      obj     obj to begin with (a function)
        @return             list of strings
        """
        if "children" not in obj:
            return self.RaiseCodeException("children key is missing")
        allret = []
        obj["processed"] = True
        for node in obj["children"]:
            if node["type"] == "Name":
                allret.append(node)
            else:
                return self.RaiseCodeException("unexpected type: " + node["type"])
        return self.setReturn(allret)

    def setReturn(self, nodes):
        """
        Indicates all nodes containing information about returned results.

        @param      node        list of nodes
        @return                 list of string
        """
        return self.RaiseCodeException("not implemented")
