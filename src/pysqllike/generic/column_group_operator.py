# -*- coding: utf-8 -*-
"""
@file
@brief Creates custom classes to interpret Python expression as column operations.
"""

from .column_operator import ColumnOperator
from .others_types import NA


class ColumnGroupOperator(ColumnOperator):
    """
    Defines an operation between two columns.
    """

    def __init__(self):
        """
        Initiates the operator.

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


class OperatorGroupLen(ColumnGroupOperator):

    """
    defines the group function ``len``
    """

    def __str__(self):
        """
        usual
        """
        return "len"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns
        """
        return len(columns)


class OperatorGroupAvg(ColumnGroupOperator):

    """
    defines the group function ``avg``, the default value when the set is empty is None
    """

    def __str__(self):
        """
        usual
        """
        return "avg"

    def __call__(self, columns):
        """
        returns the results of this operation between a list of columns,
        it returns @see cl NA for a null set
        """
        # we walk through the set only once
        nb = 0
        for val in columns:
            if nb == 0:
                s = val
            else:
                s += val
            nb += 1

        if nb == 0:
            return NA
        else:
            return s / nb
