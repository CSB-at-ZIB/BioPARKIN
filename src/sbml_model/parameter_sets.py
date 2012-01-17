from collections import OrderedDict
import logging
from PySide.QtCore import QObject, Signal


"""
This file/module provides the data structures for storing multiple Parameter Sets
in one SBML file. (Note: Scroll down, there is more than one class defined here!)

It's modelled after a semi-official annotation for SBML:
http://www.sys-bio.org/sbwWiki/_media/sysbio/sysbio/parametersets/2010-02-22_-_managingmultipleparametersets.pdf

Objects of these classes will be saved as nested XML within a SBML Model's Annotation element.
"""

__author__ = "Moritz Wade"
__contact__ = "wade@zib.de"
__copyright__ = "Zuse Institute Berlin 2011"

class ListOfParameterSets(QObject):
    '''
    This is basically a Python list of ParameterSet objects with the additional information
    which of those Sets is active.

    @since: 2011-03-21
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    changed = Signal()

    def __init__(self, paramSet=None):
        super(ListOfParameterSets, self).__init__()
        self.activeSet = None
        self.defaultSet = None
        self.selectedSet = None
        self._list = []

        if paramSet:
            self._list.append(paramSet)
            self.activeSet = paramSet
            self.defaultSet = paramSet

    def createNewParameterSet(self, duplicate=False):
        baseSet = self.selectedSet if self.selectedSet else self.defaultSet

        if not duplicate:
            id = "New Set"
        else:
            id = "Duplicate of %s" % baseSet.getId()

        newSet = ParameterSet(id, baseSet=baseSet, duplicate=duplicate)

        self.activeSet = newSet
        self._list.append(newSet)

        self.changed.emit() # emit signal to let the world know something's changed :)

    def removeParameterSet(self):
        if self.selectedSet == self.defaultSet:
            logging.info("Can't remove the original data set.")
            return

        if not self.selectedSet:
            logging.info("No Set selected. Can't remove anything.")
            return

        if self.selectedSet == self.activeSet:  # revert to default Set if active set is removed
            self.activeSet = self.defaultSet

        try:
            self._list.remove(self.selectedSet)
        except Exception, e:
            logging.debug("ListOfParameterSets.removeParameterSet(): Can't remove selected set: %s\nError:%s" % (self.selectedSet, e))
            return 

        self.selectedSet = None

        self.changed.emit() # emit signal to let the world know something's changed :)

    def numParameters(self):
        if len(self) > 0:
            return self[0].numParameters()

    def getParamIds(self):
        if len(self) == 0:
            return []

        return self[0].getParamIds()

    def getSet(self, id):
        for set in self._list:
            if set.getId() == id:
                return set

    def getActiveSet(self):
        return self.activeSet

    def setDefaultSet(self, set):
        self.defaultSet = set

    def getDefaultSet(self):
        return self.defaultSet

    def __getitem__(self, item):
        return self._list[item]

    def __setitem__(self, key, value):
        self._list[key] = value

    def __len__(self):
        return len(self._list)

    def append(self, item):
        self._list.append(item)
        self.changed.emit()


class ParameterSet(object):
    """
    Simple subclass of SBase (so that it inherits IDs, possibilities for Annotations, etc.)
    with a ListOfParameters.

    @since: 2011-03-21
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    _id = None

    def __init__(self, id, baseSet=None, duplicate=False, name=None):
        #super(ParameterSet, self).__init__() #SBase is abstract
        self.setId(str(id))
        self._listOfParameters = ListOfParameters() # instance of ListOfParameterSets
        self.setName(str(name))

        if baseSet:
            for paramId in baseSet.getParamIds():
                baseParam = baseSet.getParam(paramId)
                id = baseParam.getId()
                value = baseParam.getValue() if duplicate else 0
                reactionId = baseParam.getReactionId()

                newParam = ParameterProxy(paramId, id, value, reactionId)
                self._listOfParameters[paramId] = newParam

    def getParam(self, id):
        try:
            return self[id]
        except:
            return

    def add(self, combinedId, id, value, reactionId=None):
        newParam = ParameterProxy(combinedId, id, value, reactionId)
        self._listOfParameters[combinedId] = newParam

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def numParameters(self):
        return len(self._listOfParameters)

    def getParamIds(self):
        if len(self._listOfParameters) == 0:
            return []

        return self._listOfParameters.keys()

    def __getitem__(self, item):
        return self._listOfParameters[item]

    def __setitem__(self, key, value):
        self._listOfParameters[key] = value

    def __len__(self):
        return len(self._listOfParameters)

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def keys(self):
        return self._listOfParameters.keys()

    def values(self):
        return self._listOfParameters.values()

    def items(self):
        return self._listOfParameters.items()



class ListOfParameters(OrderedDict):
    """
    This is just kind of a "renamed" OrderedDict object
    to make the naming of things more coherent, to adhere to the standard
    set by the SBML Multiple Parameter Sets annotation and to have a place
    for functionality for which a need might arise.

    A Parameter's "combined Id" (using Reaction ID and Param ID) is used
    as a key for every Parameter object.

    @since: 2011-03-21
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    def __init__(self):
        super(ListOfParameters, self).__init__()


class ParameterProxy(object):
    """
    Simple Parameter "proxy" object with references to the original libSBML Parameter
    (by Parameter and Reaction IDs) and the value of that Parameter within this Set.

    @since: 2011-03-21
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    sbmlId = None   # str: associated ID
    value = None # float
    reactionId = None #str: associated Reaction ID for local Parameters

    def __init__(self, combinedId, id, value, reactionId=None):
        self.sbmlId = id
        self.value = value
        self.reactionId = reactionId
        self.combinedId = combinedId

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def getId(self):
        return self.sbmlId

    def getReactionId(self):
        return self.reactionId

    def getCombinedId(self):
        return self.combinedId
