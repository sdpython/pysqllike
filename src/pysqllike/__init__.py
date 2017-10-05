#-*- coding: utf-8 -*-
"""
@file
@brief Module *pysqllike*.
Parses :epkg:`Python` and produces equivalent
code in other languages in a map reduce logic.
"""

__version__ = "0.1"
__author__ = "Xavier Dupré"
__github__ = "https://github.com/sdpython/pysqllike"
__url__ = "http://www.xavierdupre.fr/app/pysqllike/helpsphinx/index.html"
__license__ = "MIT License"


def _setup_hook():
    """
    does nothing
    """
    pass


def check(log=False):
    """
    Checks the library is working.
    It raises an exception.
    If you want to disable the logs:

    @param      log     if True, display information, otherwise
    @return             0 or exception
    """
    return True
