'''
Created on Jun 4, 2010

@author: bzfwadem
'''
import logging
from PySide.QtCore import Signal, QObject

TYPE_NONE, TYPE_EXPERIMENTAL, TYPE_SIMULATED, TYPE_SENSITIVITY_OVERVIEW, TYPE_PARAMETERS_ESTIMATED = range(5)

DATACHANGE_DESCRIPTOR = "datachange_descriptor"
DATACHANGE_POINT = "datachange_point"
DATACHANGE_HEADER = "datachange_header"

class EntityData(QObject):
    """
    This serves as a data container for experimental and
    simulation data.

    The data is in two lists one for time points (more
    generally called "Data Descriptors", one for data points.

    Some properties give more information about the encapsulated data (e.g.
    the referenced libSBML Species/Parameter).
    Some convenience methods are provided (like .getId() which works on the
    referenced SBML entity).
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    dataChanged = Signal(object, str, int)
    selectionStateChanged = Signal(bool)

    def GetTimepoints(self):
        return self.dataDescriptors


    def SetTimepoints(self, value):
        self.dataDescriptors = value


    def DelTimepoints(self):
        del self.dataDescriptors

    timepoints = property(GetTimepoints, SetTimepoints, DelTimepoints,
                          "Provides a wrapper for the now-renamed self.dataDescriptors")

    def __init__(self):
        '''
        Setting up some instance variables.
        
        '''
        super(EntityData, self).__init__(None)

        self.type = TYPE_NONE
        self.dataDescriptors = []
        self.datapoints = []
#        self.weights = []

        self.isMetaData = False # by default, self is a "real" data object with measured/computed relevant data
        self.isWeightData = False
        self._weightData = None # will hold reference to EntityData object with weight data

        self.dataDescriptorName = None
        self.dataDescriptorUnit = None
        self.datapointUnit = None

        self.sbmlEntity = None

        self.id = None
        self.name = None

        self.originalColumn = None
        self.originalFilename = None
        self.originalId = None
        self.originalHeader = None  # e.g.: "FSH [unit]"

        self.associatedDataSet = None

        self._isSelected = True

    def setId(self, id):
        self.id = id
        if not self.name:   # also set as name if there is no name yet
            self.setName(id)

    def getId(self):
        if self.id:
            return self.id
        elif self.getSbmlId(): # fallback
            return self.getSbmlId()
        elif self.originalId:   # 2nd fallback
            return self.originalId
        else:
            return "no ID"

    def setSelected(self, isSelected):
        if self._isSelected != isSelected:  # only update (and emit SIGNAL) when necessary
            self._isSelected = isSelected
            logging.info("Selection of %s is now: %s" % (self.getId(), isSelected))
            self.selectionStateChanged.emit(isSelected)


    def isSelected(self):
        return self._isSelected

    def setName(self, name):
        self.name = str(name)
        self.dataChanged.emit(self, -1, -1)

    def getName(self):
        name = self.name if self.name else self.getId()
        return name

    def getCombinedId(self):
        try:
            return self.sbmlEntity.getCombinedId()
        except:
            return self.getId()


    def getSbmlId(self):
        '''
        A wrapper for the internal SBML Entity's getId() method.
        '''
        try:
            return self.sbmlEntity.getId()
        except:
            return None

    def getUnit(self):
        '''
        Primarily a getter for the internal unit variable, if set.
        Else:
        A wrapper for the internal SBML Entity's getSubstanceUnits() method.
        '''

        try:
            if self.dataDescriptorUnit:
                return self.dataDescriptorUnit
            else:
                return self.sbmlEntity.Item.getSubstanceUnits()
        except:
            return None

    def getType(self):
        if not self.sbmlEntity or not self.sbmlEntity.Item:
            return "N/A"
        elif self.sbmlEntity.Item.isSetInitialAmount():
            return "Amount"
        elif self.sbmlEntity.Item.isSetInitialConcentration():
            return "Concentration"
        else:
            return "N/A"

    def getAxisLabel(self):
        return "%s [%s]" % (self.getType(), self.getUnit())

    def setAssociatedDataSet(self, dataSet):
        self.associatedDataSet = dataSet
        dataSet.connectEntityDataSignals(self)

    def getAssociatedDataSet(self):
        return self.associatedDataSet

    def setSbmlEntity(self, entity):
        self.sbmlEntity = entity

    def getSbmlEntity(self):
        return self.sbmlEntity

    def setType(self, type):
        self.type = type

    def copy(self):
        '''
        Makes a shallow (!) copy of self.
        '''
        # TODO Update this method to reflect all the structural changes of the class!

        clone = EntityData()
        clone.type = self.type  # real copy, as it's only an int
        clone.dataDescriptors = self.dataDescriptors[:] # use slice to make clone
        clone.datapoints = self.datapoints[:]   # use slice to make clone

        if self._weightData:    # copy associated EntityData object with weights, if there is one
            clone._weightData = self._weightData.copy()

        if self.dataDescriptorUnit:
            clone.dataDescriptorUnit = str(self.dataDescriptorUnit)[:] # clone string
        if self.datapointUnit:
            clone.datapointUnit = str(self.datapointUnit)[:] # clone string

        clone.sbmlEntity = self.sbmlEntity # retain identical reference

        if self.id:
            clone.id = str(self.id)[:] # clone string

        clone.originalColumn = self.originalColumn # int: copy
        if self.originalFilename:
            clone.originalFilename = str(self.originalFilename)[:] # str: slice
        if self.originalId:
            clone.originalId = str(self.originalId)[:]  # str: slice

        # Note: Don't clone dataSet!
        # Set new dataset from the outside!

        return clone

    def getDataWithDescriptor(self, descriptor):
        try:
            index = self.dataDescriptors.index(descriptor)
            return self.datapoints[index]
        except:
            return None

    def getDataPointAtIndex(self, index):
        try:
            return self.datapoints[index]
        except :
            return

    def hasWeights(self):
        if self.weights:
            return True
        else:
            return False

    def getWeights(self):
        if self._weightData:
            return self._weightData.datapoints
        else:
            return None

    def setWeightData(self, entityData):
        self._weightData = entityData

    def setDatapoint(self, index, value):
        self.datapoints[index] = value
        self.dataChanged.emit(self, DATACHANGE_POINT, index)


    def setDescriptor(self, index, value):
        self.dataDescriptors[index] = value
        self.dataChanged.emit(self, DATACHANGE_DESCRIPTOR, index)

    def setHeader(self, header):
        #we don't touch the original header; that's only done once when loading
        # So, we have to parse the header (according to BioPARKIN file specifications)
        header = str(header)
        if "[" in header:
            splitID = header.split("[")
            id = splitID[0].strip()
            unit = splitID[1].strip()[:-1]
            self.setId(id)
            self.setDatapointUnit(unit)
        else:
            id = header.strip()
            self.setId(id)

        self.dataChanged.emit(self, DATACHANGE_HEADER, None)

    def getHeader(self):
        if self.datapointUnit:
            return "%s [%s]" % (self.getName(),self.datapointUnit)  # header uses name and not id
        else:
            return self.getName()

    def setDatapointUnit(self, unit):
        self.datapointUnit = str(unit)