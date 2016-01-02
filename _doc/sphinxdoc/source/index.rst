.. project_name documentation documentation master file, created by
   sphinx-quickstart on Fri May 10 18:35:14 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pysqllike documentation
=======================


.. image:: https://travis-ci.org/sdpython/pysqllike.svg?branch=master
    :target: https://travis-ci.org/sdpython/pysqllike
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/67ljkgh36klak07a?svg=true
    :target: https://ci.appveyor.com/project/sdpython/pysqllike
    :alt: Build Status Windows
    
.. image:: https://badge.fury.io/py/pysqllike.svg
    :target: http://badge.fury.io/py/pysqllike
       
.. image:: http://img.shields.io/pypi/dm/pysqllike.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/pysqllike

.. image:: http://img.shields.io/github/issues/sdpython/pysqllike.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pysqllike/issues
    
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT
    
.. image:: https://landscape.io/github/sdpython/pysqllike/master/landscape.svg?style=flat
   :target: https://landscape.io/github/sdpython/pysqllike/master
   :alt: Code Health
    
.. image:: https://requires.io/github/sdpython/pysqllike/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/pysqllike/requirements/?branch=master
     :alt: Requirements Status      

.. image:: https://codecov.io/github/codecov/pysqllike/coverage.svg?branch=master
    :target: https://codecov.io/github/codecov/pysqllike?branch=master
    

   
**Links:** `pypi <https://pypi.python.org/pypi/pysqllike/>`_,
`github <https://github.com/sdpython/pysqllike/>`_,
`documentation <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/index.html>`_,
`wheel <http://www.xavierdupre.fr/site2013/index_code.html#pysqllike>`_,
:ref:`l-README`,
:ref:`blog <ap-main-0>`


What is it?
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
        return wher
        
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

Installation
------------

``pip install pysqllike``

Functionalities
---------------

* not yet ready
    

Quick start
-----------

.. toctree::
    :maxdepth: 1
    
    all_example
    all_notebooks
            
        
Indices and tables
------------------

+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`l-modules`     |  :ref:`l-functions` | :ref:`l-classes`    | :ref:`l-methods`   | :ref:`l-staticmethods` | :ref:`l-properties`                            |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`modindex`      |  :ref:`l-example`   | :ref:`search`       | :ref:`l-license`   | :ref:`l-changes`       | :ref:`l-README`                                |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+
| :ref:`genindex`      |  :ref:`l-FAQ`       | :ref:`l-notebooks`  |                    | :ref:`l-statcode`      | `Unit Test Coverage <coverage/index.html>`_    |
+----------------------+---------------------+---------------------+--------------------+------------------------+------------------------------------------------+

Navigation
----------

.. toctree::
    :maxdepth: 1
    
    indexmenu

    