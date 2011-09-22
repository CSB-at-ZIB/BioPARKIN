__author__ = 'Moritz Wade'


class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass

class InitError(Error):
    """
    Exception raised for errors while initializing the integrator.

    @param msg: Explanation of the error
    @type msg: str
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)