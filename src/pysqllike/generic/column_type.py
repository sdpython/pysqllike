# -*- coding: utf-8 -*-
"""
@file
@brief Classes which defines column for class @see cl IterRow
"""
from inspect import isfunction
from .iter_exceptions import IterException, NotAllowedOperation
from .others_types import long, NA, EmptyGroup, GroupByContainer

from .column_operator import OperatorId, OperatorMul, ColumnOperator, OperatorAdd
from .column_operator import OperatorDiv, OperatorPow, OperatorSub, OperatorDivN, OperatorMod
from .column_operator import OperatorEq, OperatorNe, OperatorGe, OperatorLe, OperatorGt, OperatorLt
from .column_operator import OperatorNot, OperatorOr, OperatorAnd
from .column_operator import OperatorFunc

from .column_group_operator import OperatorGroupLen, OperatorGroupAvg


def private_function_type():
    "no documentation"
    pass


class ColumnType:

    """
    Defines a column of a table.
    """

    _default_name = "__unk__"
    _str_type = {int: 'int', long: 'long', NA: 'NA',
                 float: 'float', str: 'str',
                 type(private_function_type): 'func',
                 }

    def IsColumnType(self):
        """
        checks it is a column type which used by an operator
        """
        return True

    @property
    def ShortName(self):
        """
        a short name (tells the column type)
        """
        return "any"

    @property
    def Name(self):
        """
        property
        """
        return self._name

    @property
    def Type(self):
        """
        property
        """
        return self._type

    @property
    def Parent(self):
        """
        property
        """
        return self._parent

    @property
    def Func(self):
        """
        property
        """
        return self._func

    def __init__(
            self, name, typ, func=None, parent=tuple(), op=None, owner=None):
        """
        initiates the column

        @param      name        name of the column
        @param      typ         type of the data it will contain (can be None)
        @param      func        a function, if None, if will be the identity
        @param      parent      precise a list of parents if this column was part of a formula
        @param      op          operator to apply between the column
        @param      owner       table which contains the column (only for further validation)

        function is a function: ``f: x --> y``
        """
        self._name = name
        self._type = typ
        self._value = None
        self._parent = parent
        self._op = op
        self._owner = owner

        if not isinstance(op, ColumnOperator):
            raise IterException(
                "op should be a ColumnOperator not: {0}".format(
                    type(op)))

        if not isinstance(parent, tuple):
            raise TypeError("we expect a tuple for parameter parent")
        for p in parent:
            p.IsColumnType()

        if typ not in [int, float, long, str, None, NA,
                       type(private_function_type)]:
            raise IterException(
                "type should in [int,float,str,long,function]: " +
                str(typ))

        if isfunction(func):
            self._func = func
        elif func is None:
            self._func = None
        else:
            raise IterException(
                "type of func should in [int,float,str,long,function]: {0}".format(
                    str(func)))

        if "_func" not in self.__dict__:
            raise IterException("this column is missing a function")

    def __str__(self):
        """
        usual
        """
        ps = "|".join([_.ShortName for _ in self._parent])
        if self._value is not None:
            return "CT({0},<{1}>,op:{2},#P={3})={4}".format(
                self._name, ColumnType._str_type[self._type], str(self._op), ps, self())
        else:
            return "CT({0},<{1}>,op:{2},#P={3}) [no loop started]".format(
                self._name, ColumnType._str_type[self._type], str(self._op), ps)

    def __call__(self):
        """
        returns func(value)
        """
        if self._func is None:
            if len(self._parent) == 0:
                if self._value is None:
                    raise ValueError(
                        "method set must be called before for column {0}".format(
                            str(self)))
                else:
                    res = self._value
            elif self._op is None:
                raise ValueError(
                    "there are parents but no operator for column {0}\nParents:\n{1}".format(
                        str(self),
                        self.print_parent()))
            else:
                try:
                    res = self._op(self._parent)
                except TypeError as e:
                    raise IterException(
                        "unable(1) to apply an operator for column op=<{0}>, col={1}, TYPE={2} TYPE_OP={3} TYPE_PARENT={4}".format(
                            str(
                                self._op), str(self), type(self), type(
                                self._op), type(
                                self._parent))) from e
                except AttributeError as ee:
                    raise IterException(
                        "unable(2) to apply an operator for column op=<{0}>, col={1}, TYPE={2} TYPE_OP={3} TYPE_PARENT={4}".format(
                            str(
                                self._op), str(self), type(self), type(
                                self._op), type(
                                self._parent))) from ee

                if isinstance(res, ColumnType):
                    raise IterException(
                        "this evaluation(*) cannot return a ColumnType for this column: {0}".format(str(self)))
        else:
            # we use a shortcut
            try:
                res = self._func(self._value)
            except TypeError as e:
                raise IterException(
                    "unable to compute the value of {0}\n{1}".format(
                        str(self),
                        self.print_parent())) from e

        if isinstance(res, ColumnType):
            raise IterException(
                "this evaluation cannot return a ColumnType for this column: {0}".format(
                    str(self)))

        self.set(res)
        return res

    def set(self, value):
        """
        Sets a value for this column.

        @param      value       anything in ``[int, float, long, str, function]``
        """
        if isinstance(value, (int, str, float, long, NA)):
            self._value = value
        elif isinstance(value, EmptyGroup):
            # for an empty group
            self._value = value
        elif isinstance(value, list):
            # for a group
            self._value = value
        else:
            raise IterException(
                "type of value should be in [int,float,str,long] not {0} for the column {1}".format(
                    type(value),
                    str(self)))

    def set_none(self):
        """
        After a loop on a database, we should put None back as a value.
        """
        for p in self._parent:
            p.set_none()
            self._value = None

    def set_name(self, new_name):
        """
        Changes the name of the column.

        @param      newname     new name
        """
        self._name = new_name

    def set_owner(self, new_owner):
        """
        Changes the owner of the column.

        @param      newname     new name
        """
        self._owner = new_owner

    def print_parent(self):
        """
        Returns a string showing the dependencies of this columns.

        Example:
        @code
        this_columns
            parent1
                parent11
                parent12
            parent2
        @endcode
        """
        if self._parent is None:
            return self.__str__()
        else:
            rows = [self.__str__()]
            for p in self._parent:
                rs = ["    " + _ for _ in p.print_parent().split("\n")]
                rows.extend(rs)
            return "\n".join(rows)

    ######################################
    # functions which create other columns
    ######################################

    def copy(self, new_owner):
        """
        Returns a copy of this class.

        @param      new_owner       new owner
        @return                     ColumnType
        """
        return ColumnType(self._name, self._type, func=None, parent=(
            self,), op=OperatorId(), owner=new_owner)

    #######################################
    # operations
    #######################################

    def __mul__(self, column):
        """
        These operators should be able to translate an expression
        into function operating on the values.

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorMul())
        else:
            return self.__mul__(ColumnConstantType(column))

    def __add__(self, column):
        """
        These operators should be able to translate an expression
        into function operating on the values.

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorAdd())
        else:
            return self.__add__(ColumnConstantType(column))

    def __sub__(self, column):
        """
        These operators should be able to translate an expression
        into function operating on the values.

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorSub())
        else:
            return self.__sub__(ColumnConstantType(column))

    def __truediv__(self, column):
        """
        These operators should be able to translate an expression
        into function operating on the values.

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorDiv())
        else:
            return self.__truediv__(ColumnConstantType(column))

    def __floordiv__(self, column):
        """
        These operators should be able to translate an expression
        into function operating on the values.

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorDivN())
        else:
            return self.__floordiv__(ColumnConstantType(column))

    def __mod__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorMod())
        else:
            return self.__mod__(ColumnConstantType(column))

    def __pow__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorPow())
        else:
            return self.__pow__(ColumnConstantType(column))

    #######################################
    # test
    #######################################

    def __eq__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorEq())
        else:
            return self.__eq__(ColumnConstantType(column))

    def __lt__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorLt())
        else:
            return self.__lt__(ColumnConstantType(column))

    def __le__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorLe())
        else:
            return self.__le__(ColumnConstantType(column))

    def __gt__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorGt())
        else:
            return self.__gt__(ColumnConstantType(column))

    def __ge__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorGe())
        else:
            return self.__ge__(ColumnConstantType(column))

    def __ne__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorNe())
        else:
            return self.__ne__(ColumnConstantType(column))

    #######################################
    # logical
    #######################################

    def Not(self):
        """
        ``not`` cannot be overriden
        """
        return self.__not__()

    def __not__(self):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @return                 a ColumnType
        """
        return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
            self,), op=OperatorNot())

    def Or(self, column):
        """
        ``or`` cannot be overriden
        """
        return self.__or__(column)

    def __or__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorOr())
        else:
            return self.__or__(ColumnConstantType(column))

    def And(self, column):
        """
        ``and`` cannot be overriden
        """
        return self.__and__(column)

    def __and__(self, column):
        """
        these operators should be able to translate an expression
        into function operating on the values

        @param      column      a function or an int or a float or a long or a str or a ColumnType
        @return                 a ColumnType
        """
        if isinstance(column, ColumnType):
            return ColumnType(ColumnType._default_name, self._type, func=None, parent=(
                self, column), op=OperatorAnd())
        else:
            return self.__and__(ColumnConstantType(column))

    #######################################
    # group function
    #######################################

    def len(self):
        """
        returns a group columns to count the number of observations
        """
        return ColumnGroupType(
            ColumnType._default_name, int, parent=(self,), op=OperatorGroupLen())

    def count(self):
        """
        returns a group columns to count the number of observations
        """
        return self.len()

    def avg(self):
        """
        returns a group columns to return an average
        """
        return ColumnGroupType(
            ColumnType._default_name, float, parent=(self,), op=OperatorGroupAvg())


class ColumnConstantType(ColumnType):

    """
    defines a constant as a column
    """

    def __init__(self, const):
        self._value = const
        self._func = lambda x, c=self._value: c
        self._parent = None
        self._op = None
        self._type = type(const)
        self._const = const
        self._owner = None

        if isinstance(const, (int, float, long, str, NA)):
            pass
        else:
            raise ValueError(
                "this value is not a constant: {0}".format(
                    str(const)))

    @property
    def ShortName(self):
        """
        a short name (tells the column type)
        """
        return "cst"

    def set_none(self):
        """
        do nothing (it is a constant)
        """
        pass

    def set(self, value):
        """
        do nothing (it is a constant)

        @param      value       anything in [int,float,long,str, function ]
        """
        pass

    def __call__(self):
        """
        return the constant
        """
        return self._const

    def __str__(self):
        """
        usual
        """
        return "cst({0})".format(self())


class ColumnTableType(ColumnType):

    """
    defines a table column (not coming from an expression)
    """

    def __init__(self, name, typ, owner):
        """
        constructor

        @param      name        name of the column
        @param      typ         type of the column
        @param      owner       owner of this column
        """
        self._name = name
        self._func = None
        self._parent = None
        self._op = None
        self._type = typ
        self._owner = owner

    @property
    def ShortName(self):
        """
        a short name (tells the column type)
        """
        return "col"

    def set_none(self):
        """
        after a loop on a database, we should put None back as a value
        """
        self._value = None

    def __call__(self):
        """
        returns the content
        """
        if self._value is None:
            raise IterException(
                "this column should contain a value: {0}".format(
                    str(self)))
        return self._value

    def __str__(self):
        """
        usual
        """
        return "col({0},{1})".format(
            self._name, ColumnType._str_type[self._type])


class ColumnGroupType(ColumnType):

    """
    defines a column which processes a group of rows (after a groupby)
    """

    def __init__(self, name, typ, parent, op):
        """
        constructor

        @param      name        name of the column
        @param      typ         type of the column
        @param      owner       owner of this column
        @param      op          operator
        """
        self._name = name
        self._value = None
        self._parent = parent
        self._opgr = op
        self._op = OperatorId()
        self._type = typ
        self._owner = None
        self._func = None

    @property
    def ShortName(self):
        """
        a short name (tells the column type)
        """
        return "group"

    def set_none(self):
        """
        after a loop on a database, we should put None back as a value
        """
        self._value = None

    def __call__(self):
        """
        returns the content
        """
        if isinstance(self._value, GroupByContainer):
            try:
                return self._opgr(self._value)
            except TypeError as e:
                raise IterException(
                    "unable(1) to apply an operator for column op=<{0}>, col={1}, TYPE={2} TYPE_OP={3}".format(
                        str(
                            self._op), str(self), type(self), type(
                            self._op))) from e
            except AttributeError as ee:
                raise IterException(
                    "unable(2) to apply an operator for column op=<{0}>, col={1}, TYPE={2} TYPE_OP={3}".format(
                        str(
                            self._op), str(self), type(self), type(
                            self._op))) from ee
        else:
            return super().__call__()

    def __str__(self):
        """
        usual
        """
        return "CGT[{0}]({1})".format(str(self._opgr), self._name)

    def set(self, value):
        """
        sets a value for this column

        @param      value       anything in [int,float,long,str, function ]
        """
        self._value = value
        if not isinstance(value, str) and \
                not isinstance(value, GroupByContainer):
            raise IterException(
                "type of value should be GroupByContainer not {0} for the column {1}".format(
                    type(value),
                    str(self)))

    def __mul__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __add__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __sub__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __truediv__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __floordiv__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __mod__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()

    def __pow__(self, column):
        """
        forbidden
        """
        raise NotAllowedOperation()


class CFT(ColumnType):

    """
    defines a function
    """

    def __init__(self, func, *l):
        """
        constructor (a function cannot accept keywords)

        @param      func        contained function
        @param      l           list of ColumnType
        """
        self._name = None
        self._func = None
        self._parent = None
        self._op = OperatorFunc(func)
        self._type = type(private_function_type)
        self._owner = None
        self._thisfunc = func
        self._parent = tuple(l)

        for _ in l:
            if not isinstance(_, ColumnType):
                raise TypeError("expecting a column type, not " + str(type(_)))

    @property
    def ShortName(self):
        """
        a short name (tells the column type)
        """
        return "func"

    def set_none(self):
        """
        after a loop on a database, we should put None back as a value
        """
        self._value = None

    def __str__(self):
        """
        usual
        """
        return "func({0},{1})".format(
            self._name, ColumnType._str_type[self._type])
