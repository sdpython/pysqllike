# coding: latin-1
"""
@file
@brief An class which iterates on any set.
"""

from .iter_exceptions import IterException
from .column_type import ColumnType, ColumnTableType


class IterRow(object):
    """
    defines an iterator which mimic SQL behavior
    """
    
    def __init__ (self, schema = None, anyset = None, as_dict = True):
        """
        initiates the iterator
        
        @param      schema      list of tuple [ (name, type) ], type can be None id it is unknown or a list of @see cl ColumnType
        @param      anyset      any set or iterator following the previous schema (or None if there is not any)
        @param      as_dict     in that case, the class iterator returns a list of dictionaries for each row

        schema can be None if anyset if a list of dictionaries [ {"col1":value1, ... } ].
        In that case, the construction will build the schema from the first row.
        
        @example(IterRow with a list of dictionaries)
        @code
        l = [ {"nom": 10}, {"jean": 40} ]
        tbl = IterRow (None, l)
        @endcode
        @endexample
        
        @example(IterRow with a schema)
        @code
        l = [ ("nom", 10), ("jean", 40) ]
        schema = [ ("nom", str), ("age", int) ]
        tbl = IterRow (schema, l)
        @endcode
        @endexample
        """
        if schema == None :
            if len(anyset) == 0:
                raise ValueError("unable to guess a schema from an empty list")
            firstrow = anyset[0]
            if not isinstance(firstrow,dict):
                raise ValueError("the first row must be a dictionary, otherwise, the schema cannot be guessed")
            schema = [ (k,type(v)) for k,v in firstrow.items() ]

        if len(schema) == 0 :
            raise IterException("schema is empty")

        truesch = [ ]
        for _ in schema:
            if isinstance(_,ColumnType):
                c = _.copy(new_owner = self)
            elif isinstance(_,str):
                c = ColumnTableType( _, None, owner = self)
            elif isinstance(_,tuple) :
                if len(_) == 1:
                    c = ColumnTableType( _[0], None, owner = self)
                elif len(_) == 2:
                    c = ColumnTableType( _[0], _[1], owner = self)
                else:
                    raise IterException("schema is not properly defined {0}".format(str(_)))
            else :
                raise IterException("schema is not properly defined {0}".format(str(_)))
            truesch.append(c)
            
        names = set([ _.Name for _ in truesch] )
        if len(names) < len(truesch) :
            raise IterException("some columns share the same name: " + str(truesch))
        
        self._schema  = truesch
        self._thisset = anyset
        self._as_dict = as_dict
        
        for sch in self._schema:
            if sch.Name in self.__dict__ :
                raise IterException("a column has a wrong name: {0}".format(sch))
            self.__dict__[sch.Name] = sch
    
    @property
    def Schema(self):
        """
        return _schema
        """
        return self._schema
        
    def __str__(self):
        """
        usual
        """
        return ";".join( [ str(_) for _ in self._schema ] )
        
    def __call__(self):
        """
        evaluate
        """
        return [ _() for _ in self._schema ]
        
    def __iter__(self):
        """
        iterator, returns this row,
        it always outputs a list of list
        """
        if self._thisset is None :
            raise IterException("this class contains no iterator")

        if self._as_dict:
            for _ in self._thisset :
                if isinstance(_,dict):
                    yield { k.Name:_[k.Name]  for k in self._schema }
                else :
                    yield { k.Name:v for k,v in zip(self._schema,_) }
        else :
            for _ in self._thisset :
                if isinstance(_,dict):
                    yield tuple([ _[k.Name] for k in self._schema ])
                else :
                    yield _

        for _ in self._schema :
            _.set_none()

    def print_schema(self):
        """
        calls @see me print_parent on each column
        """
        rows = [ "number of columns={0}".format(len(self._schema))]
        for i,sch in enumerate(self._schema):
            rows.append(sch.print_parent())
        return "\n".join(rows)

    def select(self, *nochange, as_dict = True, **changed) :
        """
        This function takes an undefined number of arguments. 
        It can be used the following way:
        
        @example(simple select)
        @code
        tbl = IterRow( ... )
        it  = tbl.select ( tbl.name, tbl.age * 2, old = tbl.age )
        @endcode
        @endexample

        @example(chained select)
        @code
        tbl = IterRow ( ... )
        iter = tbl.select(tbl.nom, age2=tbl.age, age3= tbl.age*0.5)
        iter2 = iter.select(iter.nom, age4=iter.age2*iter.age3)
        l = list ( iter2 )
        @endcode
        @endexample
        
        @param      nochange    list of fields to keep
        @param      changed     list of custom fields
        @param      as_dict     returns results as a list of dictionaries [ { "colname": value, ... } ]
        @return                 IterRow

        @warning The function does not guarantee the order of the output columns.
        
        @example(example with a function)
        @code
        def myf(x,y) : 
            return x*2.5 + y
        tbl = IterRow ( ... )
        iter = tbl.select(tbl.nom, age0= CFT(myf, tbl.age, tbl.age) )
        res = list(iter)
        @endcode
        @endexample
        """
        newschema = list(nochange) + [ (k,None) for k in changed.keys() ]
        
        for el in nochange :
            if not isinstance(el, ColumnType):
                raise IterException("expecting a ColumnType here not: {0}".format(str(el)))
            if el._owner != self:
                raise IterException("mismatch: all columns should belong to this view, check all columns come from this instance")

        arow = [ v.copy(None) for v in nochange ]  # we do not know the owner yet
        for k,v in changed.items():
            if not isinstance(v, ColumnType):
                raise IterException("expecting a ColumnType here not: {0}-{1}".format(type(v),str(v)))
            v = v.copy(None)  # we do not know the owner yet
            v.set_name(k)
            arow.append(v)
            
        schema = arow

        for _ in schema:
            if not isinstance(_, ColumnType):
                raise TypeError("we expect a ColumnType for column")
        
        def itervalues():
            for row in self._thisset :
                if isinstance(row,dict):
                    for col in self._schema :
                        col.set(row[col.Name])
                else :
                    for col,r in zip(self._schema, row) :
                        col.set(r)
                        
                if as_dict :
                    yield {_.Name:  _() for _ in schema }
                else :
                    yield tuple([ _() for _ in schema ])

        tbl = IterRow(schema, anyset = itervalues(), as_dict = as_dict )
        for c in schema :
            c.set_owner (tbl)
        return tbl

    def where(self, condition, as_dict = True, append_condition = False) :
        """
        This function filters elements from an IterRow instance.
        
        @param      condition           a ColumnType or an expression of ColumnType
        @param      append_condition    append the condition to the schema (for debugging purpose)
        @param      as_dict             returns results as a list of dictionaries [ { "colname": value, ... } ]
        @return                         IterRow
        
        @example(where)
        @code
        tbl = IterRow ( ... )
        iter = tbl.where(tbl.age == 40)
        res = list(iter)
        @endcode
        @endexample
        
        @warning For operator ``or``, ``and``, ``not``, the syntax is different because they cannot be overriden in Python.
        
        @example(where with or)
        @code
        tbl = IterRow ( ... )
        iter = tbl.where( ( tbl.age == 2).Or( tbl.age == 40))
        iter2 = tbl.where((tbl.age == 10).Not())
        @endcode
        @endexample
        """
        if not isinstance(condition,ColumnType):
            raise TypeError("condition should a ColumnType: {0}".format(str(condition)))
        
        schema = [ v.copy(None) for v in self._schema ]  # we do not know the owner yet
        if append_condition :
            schema.append ( condition )

        def itervalues():
            for row in self._thisset :
                if isinstance(row,dict):
                    for col in self._schema :
                        col.set(row[col.Name])
                else :
                    for col,r in zip(self._schema, row) :
                        col.set(r)
                    
                if condition() :
                    if as_dict :
                        yield  {_.Name:  _() for _ in schema  }
                    else :
                        yield tuple([ _() for _ in schema ])

        tbl = IterRow(schema, anyset = itervalues(), as_dict = as_dict )
        for c in schema :
            c.set_owner (tbl)
        return tbl

    def orderby(self, *nochange, as_dict = True, ascending = True) :
        """
        This function sorts elements from an IterRow instance.
        
        @param      nochange            list of columns used to sort
        @param      ascending           order
        @param      as_dict             returns results as a list of dictionaries [ { "colname": value, ... } ]
        @return                         IterRow
        """
        schema = [ v.copy(None) for v in self._schema ]  # we do not know the owner yet

        def itervalues():
            colsi = None
            for row in self._thisset :
                if isinstance(row,dict):
                    for col in self._schema :
                        col.set(row[col.Name])
                    key = tuple ( row [k.Name] for k in nochange )
                else :
                    for col,r in zip(self._schema, row) :
                        col.set(r)
                    if colsi is None:
                        colsi = [ self._schema.index(k.Name) for k in nochange ]
                    key = tuple ( row [k] for k in colsi)
                    
                if as_dict :
                    yield key, { _.Name: _() for _ in schema  }
                else :
                    yield key, tuple([ _() for _ in schema ])

        def itervalues_sort():
            for key,row in sorted(itervalues(), reverse = not ascending):
                yield row
        
        tbl = IterRow(schema, anyset = itervalues_sort(), as_dict = as_dict )
        for c in schema :
            c.set_owner (tbl)
        return tbl

