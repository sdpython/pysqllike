
.. image:: https://github.com/sdpython/pysqllike/blob/master/_doc/sphinxdoc/source/phdoc_static/project_ico.png?raw=true
    :target: https://github.com/sdpython/pysqllike/

.. _l-README:

pysqllike: pseudo map/reduce in python
======================================

.. image:: https://travis-ci.org/sdpython/pysqllike.svg?branch=master
    :target: https://travis-ci.org/sdpython/pysqllike
    :alt: Build status

.. image:: https://ci.appveyor.com/api/projects/status/rrpks1pgivea23js?svg=true
    :target: https://ci.appveyor.com/project/sdpython/pysqllike
    :alt: Build Status Windows

.. image:: https://circleci.com/gh/sdpython/pysqllike/tree/master.svg?style=svg
    :target: https://circleci.com/gh/sdpython/pysqllike/tree/master

.. image:: https://badge.fury.io/py/pysqllike.svg
    :target: http://badge.fury.io/py/pysqllike

.. image:: http://img.shields.io/github/issues/sdpython/pysqllike.png
    :alt: GitHub Issues
    :target: https://github.com/sdpython/pysqllike/issues

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License
    :target: http://opensource.org/licenses/MIT

.. image:: https://requires.io/github/sdpython/pysqllike/requirements.svg?branch=master
     :target: https://requires.io/github/sdpython/pysqllike/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://codecov.io/github/sdpython/pysqllike/coverage.svg?branch=master
    :target: https://codecov.io/github/sdpython/pysqllike?branch=master

.. image:: https://pepy.tech/badge/pysqllike/month
    :target: https://pepy.tech/project/pysqllike/month
    :alt: Downloads

.. image:: https://img.shields.io/github/forks/sdpython/pysqllike.svg
    :target: https://github.com/sdpython/pysqllike/
    :alt: Forks

.. image:: https://img.shields.io/github/stars/sdpython/pysqllike.svg
    :target: https://github.com/sdpython/pysqllike/
    :alt: Stars

*The project is not actively developed.*

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
job:

::

    input = LOAD '...' USING PigStorage('\t') AS (nom, age);
    iter = FOREACH input GENERATE age, nom, age*age AS age2 ;
    wher = FILTER iter BY age > 60 or age < 25 ;
    STORE wher INTO '...' USING PigStorage();

It should also be translated into
`SQL <http://fr.wikipedia.org/wiki/Structured_Query_Language>`_.

**Links:**

* `GitHub/pysqllike <https://github.com/sdpython/pysqllike>`_
* `documentation <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/index.html>`_
* `Blog <http://www.xavierdupre.fr/app/pysqllike/helpsphinx/blog/main_0000.html#ap-main-0>`_
