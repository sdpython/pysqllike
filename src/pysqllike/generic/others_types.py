"""
@file
@brief defines custom types
"""

class long:
    """
    defines the long type as int
    """
    def __init__(self, v) : self._v = int(v)
    def __mul__(self, y) : return long(self._v*y._v)
    def __add__(self, y) : return long(self._v+y._v)
    def __sub__(self, y) : return long(self._v-y._v)
    def __div__(self, y) : return long(self._v/y._v)
    def __str__(self): return "%d"%self._v
    def __int__(self): return self._v
    def __float__(self): return float(self._v)

class NA :
    """
    defines the missing type
    """
    def __init__(self) : pass
    def __mul__(self, y) : return NA()
    def __add__(self, y) : return NA()
    def __sub__(self, y) : return NA()
    def __div__(self, y) : return NA()

class EmptyGroup :
    """
    defines an empty group
    """
    def __init__(self) : pass

class NoSortClass:
    """
    container which overloads the sort operator to return 0 all the times
    """
    def __init__(self, value):
        """
        any value
        """
        self.value = value
        
    def __lt__(self, o):
        """
        operator __lt__
        """
        return -1
        
    def __str__(self):
        """
        usual
        """
        return "NSC:{0}".format(str(self.value))
        
class GroupByContainer (list):
    """
    to differiate between a list and a list introduced by a groupby
    """
    pass
    