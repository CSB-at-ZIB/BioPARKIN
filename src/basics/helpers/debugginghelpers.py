"""
This file provides some helper methods dealing with debugging.
"""

import logging
import time

__author__ = 'Moritz Wade'

def print_timing(func):
    """
    This method can be used as a decorator on any method and will provide
    run time information in the debug log.

    E.g.:

    @print_timing
    def some_method(self, x, y):
        ...


    """
    def wrapper(*arg, **args):
        t1 = time.time()
        res = func(*arg, **args)
        t2 = time.time()
        #print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        logging.debug('%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0))
        return res
    return wrapper
  