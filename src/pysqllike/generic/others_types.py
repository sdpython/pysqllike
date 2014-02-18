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

