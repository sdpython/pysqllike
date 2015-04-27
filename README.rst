
.. _l-README:

README / Changes
================

.. image:: https://travis-ci.org/sdpython/pysqllike.svg?branch=master
    :target: https://travis-ci.org/sdpython/pysqllike
    :alt: Build status

.. image:: https://badge.fury.io/py/pysqllike.svg
    :target: http://badge.fury.io/py/pysqllike   
   
.. image:: http://img.shields.io/pypi/dm/pysqllike.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/pysqllike

              
**Links:**
    * `pypi/pysqllike <https://pypi.python.org/pypi/pysqllike/>`_
    * `GitHub/pysqllike <https://github.com/sdpython/pysqllike>`_
    * `documentation <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/index.html>`_
    * `Windows Setup <http://www.xavierdupre.fr/site2013/index_code.html#pysqllike>`_
    * `Travis <https://travis-ci.org/sdpython/pysqllike>`_
    * `Blog <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/blog/main_0000.html#ap-main-0>`_


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


Design
------

This project contains various helper about logging functions, unit tests and help generation.
   * a source folder: ``src``
   * a unit test folder: ``_unittests``, go to this folder and run ``run_unittests.py``
   * a _doc folder: ``_doc``, it will contains the documentation
   * a file ``setup.py`` to build and to install the module
   * a file ``make_help.py`` to build the sphinx documentation

Versions
--------

* **v0.1 - 2014/??/??**
    * **new:** first version
    * **fix:** the setup does not need the file ``README.rst`` anymore
    
    
