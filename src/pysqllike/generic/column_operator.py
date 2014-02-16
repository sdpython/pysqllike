# coding: latin-1
"""
@file
@brief An class which iterates on any set.
"""


class ColumnOperator :
    """
    defines an operation between two columns
    """
    
    def __init__ (self) :
        """
        initiates the operator
        
        @param      name        name of the column
        """
        pass

    def __str__(self):
        """
        usual
        """
        raise NotImplementedError()

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        raise NotImplementedError()

class OperatorId(ColumnOperator):
    """
    defines a constant
    """
    def __str__(self):
        """
        usual
        """
        return "="

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns) != 1 : raise ValueError("we expect a single value in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns:c.IsColumnType()
        return columns[0]()

class OperatorMul(ColumnOperator):
    """
    defines the multiplication
    """
    def __str__(self):
        """
        usual
        """
        return "*"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)==0 : raise ValueError("we expect at least a value in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()

        r = columns[0]()
        for c in columns[1:] :
            r *= c()
        return r

class OperatorAdd(ColumnOperator):
    """
    defines the addition
    """
    def __str__(self):
        """
        usual
        """
        return "+"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)==0 : raise ValueError("we expect at least a value in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()

        r = columns[0]()
        for c in columns[1:] :
            r += c()
        return r

class OperatorDiv(ColumnOperator):
    """
    defines the division
    """
    def __str__(self):
        """
        usual
        """
        return "/"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() / columns[1]()

class OperatorSub(ColumnOperator):
    """
    defines the subtraction
    """
    def __str__(self):
        """
        usual
        """
        return "-"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() - columns[1]()

class OperatorPow(ColumnOperator):
    """
    defines the power
    """
    def __str__(self):
        """
        usual
        """
        return "**"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()

        return columns[0]() **columns[1]()

class OperatorMod(ColumnOperator):
    """
    defines the operator mod
    """
    def __str__(self):
        """
        usual
        """
        return "%"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()

        return columns[0]()  % columns[1]()

class OperatorDivN(ColumnOperator):
    """
    defines the division //
    """
    def __str__(self):
        """
        usual
        """
        return "//"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()

        return columns[0]()  // columns[1]()

class OperatorEq(ColumnOperator):
    """
    defines ==
    """
    def __str__(self):
        """
        usual
        """
        return "=="

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() == columns[1]()

class OperatorNe(ColumnOperator):
    """
    defines !=
    """
    def __str__(self):
        """
        usual
        """
        return "!="

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() != columns[1]()

class OperatorLt(ColumnOperator):
    """
    defines <
    """
    def __str__(self):
        """
        usual
        """
        return "<"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() < columns[1]()

class OperatorGt(ColumnOperator):
    """
    defines >
    """
    def __str__(self):
        """
        usual
        """
        return ">"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() > columns[1]()

class OperatorLe(ColumnOperator):
    """
    defines <=
    """
    def __str__(self):
        """
        usual
        """
        return "<="

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() <= columns[1]()

class OperatorGe(ColumnOperator):
    """
    defines >=
    """
    def __str__(self):
        """
        usual
        """
        return ">="

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() >= columns[1]()

class OperatorOr(ColumnOperator):
    """
    defines ``or``
    """
    def __str__(self):
        """
        usual
        """
        return "or"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() or columns[1]()

class OperatorAnd(ColumnOperator):
    """
    defines ``and``
    """
    def __str__(self):
        """
        usual
        """
        return "and"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=2 : raise ValueError("we expect two values in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return columns[0]() and columns[1]()

class OperatorNot(ColumnOperator):
    """
    defines ``not``
    """
    def __str__(self):
        """
        usual
        """
        return "not"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        if len(columns)!=1 : raise ValueError("we expect one value in a array here: {0}".format(str(columns)))
        if not isinstance(columns,tuple): raise TypeError("we expect a tuple here")
        for c in columns: c.IsColumnType()
        return not (columns[0]())












