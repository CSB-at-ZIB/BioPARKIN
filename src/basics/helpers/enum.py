'''
Created on Feb 26, 2010

@author: moritz
'''

## {{{ Recipe 577024 (r5): Yet another 'enum' for Python 
def enum(typename, field_names):
    "Create a new enumeration type"

    if isinstance(field_names, str):
        field_names = field_names.replace(',', ' ').split()
    d = dict((reversed(nv) for nv in enumerate(field_names)), __slots__ = ())
    return type(typename, (object,), d)()
## End of recipe 577024 }}}


#class Enum(object):
#    '''
#    Simple enum data structure
#    '''
#
#
#    def __init__(self):
#        '''
#        Constructor
#        '''
#
