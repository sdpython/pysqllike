# -*- coding: utf-8 -*-
"""
@file
@brief An class which iterates on any set.
"""

from .iter_exceptions import IterException, NotAllowedOperation, SchemaException
from .column_type import ColumnType, ColumnTableType, ColumnGroupType
from .others_types import NoSortClass, GroupByContainer, NA

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
        if schema is None :
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
        
        @example(order by)
        @code
        l = [   { "nom":"j", "age": 10, "gender":"M"} , 
                {"nom":"jean", "age":40, "gender":"M"}, 
                {"nom":"jeanne", "age":2, "gender":"F"} ]
        tbl = IterRow (None, l)
        
        iter = tbl.orderby(tbl.nom, tbl.age, ascending=False )
        @endcode
        @endexample
        
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
                        colsi = [ self._findschema(self._schema, k.Name) for k in nochange ]
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
        
    def _findschema(self, schema, name):
        """
        look for column index whose name is name
        
        @param      name    column name to search
        @param      schema  schama
        @return             position
        """
        for i,col in enumerate(schema):
            if col.Name == name : return i
        raise IndexError()

    def groupby(self, *nochange, as_dict = True, **changed) :
        """
        This function applies a groupby (same behavior as SQL's version)
        
        @param      nochange    list of fields to keep
        @param      changed     list of custom fields
        @param      as_dict     returns results as a list of dictionaries [ { "colname": value, ... } ]
        @return                 IterRow

        @warning The function does not guarantee the order of the output columns.
        
        @example(group by)
        
        @code
        l = [   { "nom":"j", "age": 10, "gender":"M"} , 
                {"nom":"jean", "age":40, "gender":"M"}, 
                {"nom":"jeanne", "age":2, "gender":"F"} ]
        tbl = IterRow (None, l)
        
        iter = tbl.groupby(tbl.gender, len_nom=tbl.nom.len(), avg_age=tbl.age.avg())
        @endcode
        @endexample
        """
        selftbl = self.orderby(nochange, as_dict = as_dict)
        
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
            v.set_name(k)
            arow.append(v)
            
        schema = arow

        for _ in schema:
            if not isinstance(_, ColumnType):
                raise TypeError("we expect a ColumnType for column")
        
        def to_matrix(iter):
            mat = list(iter)
            if isinstance(mat[0],dict):
                res = {}
                for k in mat[0]:
                    i = self._findschema(schema, k)
                    col = schema[i]
                    if isinstance(col, ColumnGroupType):
                        temp = GroupByContainer( m[k] for m in mat )
                        col.set(temp)
                        res[k] = col()
                    else :
                        temp = mat[0][k]
                        col.set(temp)
                        res[k] = temp
                return res
            else:
                raise NotImplementedError()
                res = []
                for i in range(0,len(mat[0])) :
                    res.append ( GroupByContainer( m[i] for m in mat ) )
                    self._schema[i].set(res[-1])
                return res

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
                        colsi = [ self._findschema(self._schema, k.Name) for k in nochange ]
                    key = tuple ( row [k] for k in colsi)
                    
                if as_dict :
                    yield key, NoSortClass({ _.Name: _() for _ in schema  })
                else :
                    yield key, NoSortClass(tuple([ _() for _ in schema ]))
                    
        def itervalues_group():
            current = [ ]
            keycur = None
            for key,row in sorted(itervalues()):
                if key != keycur :
                    if len(current) > 0 :
                        tom = to_matrix(current)
                        yield tom
                    current = [ row.value ]
                    keycur = key
                else :
                    current.append(row.value)
            if len(current) > 0 :
                tom = to_matrix(current)
                yield tom
                
        tbl = IterRow(schema, anyset = itervalues_group(), as_dict = as_dict )
        for c in schema :
            c.set_owner (tbl)
        return tbl
        
    def unionall(self, iter, merge_schema = False, as_dict = True):
        """
        Concatenates this table with another one
        
        @param      iter            IterRow
        @param      merge_schema    if False, the function expects you find the same schema,
                                    otherwise, it merges them (same column name are not duplicated)
        @param      as_dict         returns results as a list of dictionaries [ { "colname": value, ... } ]
        @return                     IterRow
        
        @example(union all)
        @code
        l = [   { "nom":"j", "age": 10, "gender":"M"} , 
                {"nom":"jean", "age":40, "gender":"M"}, 
                {"nom":"jeanne", "age":2, "gender":"F"} ]
        tbl = IterRow (None, l)
        
        iter = tbl.unionall(tbl)
        @endcode
        @endexample
        
        @example(union all with different schema)
        @code
        l = [   { "nom":"j", "age": 10, "gender":"M"} , 
                {"nom":"jean", "age":40, "gender":"M"}, 
                {"nom":"jeanne", "age":2, "gender":"F"} ]
        tbl = IterRow (None, l)
        
        l = [   { "nom":"j", "newage": 10, "gender":"M"} , 
                {"nom":"jean", "newage":40, "gender":"M"}, 
                {"nom":"jeanne", "newage":2, "gender":"F"} ]
        tbl2 = IterRow (None, l)
        
        iter = tbl.unionall(tbl2, merge_schema = True)        
        @endcode
        @endexample
        """
            
        if merge_schema :
            names = set( a.Name for a in self._schema )
            name2 = set( a.Name for a in iter._schema )
            common = names & name2

            schema = []
            for c in common :
                i = self._findschema(self._schema, c)
                col = self._schema[i]
                schema.append ( col.copy(None) )
                
            for col in self._schema :
                if col.Name not in common :
                    schema.append ( col.copy(None) )
            for col in iter._schema :
                if col.Name not in common :
                    schema.append ( col.copy(None) )
                    
            not_in_self = set ( c.Name for c in iter._schema if c.Name not in common )
            not_in_iter = set ( c.Name for c in self._schema if c.Name not in common )
                    
        else :
            if len(self._schema) != len(self._schema):
                raise SchemaException("cannot concatenate, different schema length")
            names = sorted( a.Name for a in self._schema )
            name2 = sorted( a.Name for a in iter._schema )
            for a,b in zip(names, name2):
                if a != b :
                    raise SchemaException("cannot concatenate, different schema column: {0} != {1}".format(a,b))

            schema = [ v.copy(None) for v in self._schema ]  # we do not know the owner yet
            
            not_in_self = set()
            not_in_iter = set()
            
        not_in_self = [ iter._findschema(iter._schema, c) for c in not_in_self ]
        not_in_iter = [ self._findschema(self._schema, c) for c in not_in_iter ]
            
        def iter_union():
            for i in not_in_self :
                iter._schema[i].set(NA())
            for row in self._thisset :
                if isinstance(row,dict):
                    for col in self._schema :
                        col.set(row[col.Name])
                else :
                    for col,r in zip(self._schema, row) :
                        col.set(r)
                    
                if as_dict :
                    yield  {_.Name:  _() for _ in schema  }
                else :
                    yield tuple([ _() for _ in schema ])
                    
            for i in not_in_iter :
                self._schema[i].set(NA())
            for row in iter._thisset :
                if isinstance(row,dict):
                    for col in iter._schema :
                        col.set(row[col.Name])
                else :
                    for col,r in zip(iter._schema, row) :
                        col.set(r)
                    
                if as_dict :
                    yield  {_.Name:  _() for _ in schema  }
                else :
                    yield tuple([ _() for _ in schema ])
                    
        tbl = IterRow(schema, anyset = iter_union(), as_dict = as_dict )
        for c in schema :
            c.set_owner (tbl)
        return tbl
        
