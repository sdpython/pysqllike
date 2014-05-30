.. project_name documentation documentation master file, created by
   sphinx-quickstart on Fri May 10 18:35:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pysqllike documentation
=======================

   
   
**Links:**
    * `pypi/pysqllike <https://pypi.python.org/pypi/pysqllike/>`_
    * `GitHub/pysqllike <https://github.com/sdpython/pysqllike/>`_
    * `documentation <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pysqllike>`_


Description
-----------

Writing a map/reduce job
(using `PIG <https://pig.apache.org/>`_ for example),
usually requires to switch from local files to remote files
(on `Hadoop <http://hadoop.apache.org/>`_). 
On way to work is extract a small sample of the data which will be processed
by a map/reduce job. The job is then locally developped. And when it works,
it is run on a parallized environment.

The goal of this extension is allow the implementation of 
this job using Python syntax as follows:


::

    def myjob(input):
        iter = input.select (input.age, input.nom, age2 = input.age2*input.age2)
        wher = iter.where( (iter.age > 60).Or(iter.age < 25))
        return where 
        
    input = IterRow (None, [ {"nom": 10}, {"jean": 40} ] )
    output = myjob(input)
    
When the job is ready, it can be translated into a `PIG <https://pig.apache.org/>`_
job::

    input = LOAD '...' USING PigStorage('\t') AS (nom, age);
    iter = FOREACH input GENERATE age, nom, age*age AS age2 ;
    wher = FILTER iter BY age > 60 or age < 25 ;
    STORE wher INTO '...' USING PigStorage();

It should also be translated into 
`SQL <http://fr.wikipedia.org/wiki/Structured_Query_Language>`_.

Functionalities
---------------

* not yet ready
    

Indices and tables
==================

+------------------+---------------------+---------------------+------------------+------------------------+---------------------+
| :ref:`l-modules` |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods` | :ref:`l-staticmethods` | :ref:`l-properties` |
+------------------+---------------------+---------------------+------------------+------------------------+---------------------+
| :ref:`genindex`  |  :ref:`modindex`    | :ref:`search`       | :ref:`l-license` | :ref:`l-changes`       | :ref:`l-README`     |
+------------------+---------------------+---------------------+------------------+------------------------+---------------------+
| :ref:`l-example` |  :ref:`l-FAQ`       | :ref:`l-notebooks`  |                  |                        |                     |
+------------------+---------------------+---------------------+------------------+------------------------+---------------------+

Navigation
==========

.. toctree::
    :maxdepth: 1

    doctestunit
    generatedoc
    generatesetup
    installation
    all_example
    all_FAQ
    all_notebooks
    glossary
    index_module
    license
    filechanges
    README
    all_indexes
    