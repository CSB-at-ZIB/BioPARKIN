'''
Created on Jul 2, 2010

@author: bzfwadem
'''
import logging
from PySide.QtCore import Signal, QObject
from datamanagement.entitydata import EntityData
import services.dataservice
import datahandling
from stabledict import StableDict
from time import time


FORMAT_SIM_DOP = "format_sim_dop"
FORMAT_EXP_PARKIN = "format_exp_parkin"
FORMAT_EXP_SIMPLE_CSV = "format_exp_simple_csv"


class DataSet(QObject):
    '''
    This class encapsulates all the data that is in an individual data file,
    either simulation or experimental data.
    
    It contains a stable dictionary of EntityData objects. Each such object
    holds the data for one entity (usually a SBML Species).
    
    @since: 2010-07-02
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"
    

    dataChanged = Signal(object, EntityData)

    def __init__(self, filename, format=None, listOfEntities = None, type = None, parkinController=None):
        '''
        Setting up needed instance variables.
        '''
        super(DataSet, self).__init__(None)
#        self._entityDataDict = StableDict()
        self.filename = filename

        # keys should be SBMLEntity objects!
        self.data = StableDict()
        self.type = type

        self.dataDescriptors = None # global dataDescriptors for the normal use case when all EntityData objects have the same descriptors
        self.dataDescriptorUnit = None
        self.descriptorHeader = None
        
        self.selected = False
        
        self.id = None
        self.timestamp = time()
        self.format = format

        if filename:
            self.loadFile(filename, format, listOfEntities, parkinController=parkinController)


    def connectEntityDataSignals(self, entityData):
        entityData.dataChanged.connect(self.on_entityDataChanged)

    def loadFile(self, filename, format=None, listOfEntities = None, parkinController = None):
        '''
        Loads a file of the optionally given format.
        '''
        self.filename = filename
        
        # for now, we only support the proprietary PARKIN format
        if format == FORMAT_EXP_PARKIN:
            self.data = datahandling.read_raw_data(filename, dataSet = self, parkinController=parkinController)
            self.type = services.dataservice.EXPERIMENTAL
        elif format == FORMAT_EXP_SIMPLE_CSV:
            self.data = datahandling.read_csv_data(filename, dataSet = self, parkinController=parkinController)
            self.type = services.dataservice.EXPERIMENTAL
        elif format == FORMAT_SIM_DOP:
            if not listOfEntities:
                logging.error("Can't load PARKIN simulation data without being provided a list of entities.")
                return
            self.data = datahandling.read_integrated_data(filename, listOfEntities, dataSet = self)
            #self.data.setAssociatedDataSet(self)
            self.type = services.dataservice.SIMULATION

        self.selected = False
        self.timestamp = time() #renew timestamp
            
    
    def setId(self, id):
        self.id = id
        
    def getId(self):
        if self.id:
            return self.id
        elif self.filename: # fallback
            return self.filename 
        else:
            return "no ID"

    def getDataIds(self):
        return self.data.keys()
        
    def getData(self, keyEntity=None):
        '''
        Get a dataset of given (Species) ID.
        '''
        if not keyEntity:
            return self.data

#        for species in self.data.keys():
#            if species.getId() == id:
#                return self.data[species]
        if self.data.has_key(keyEntity):
            return self.data[keyEntity]
        else:
            return None

    def setData(self, data, keyEntity=None):
        '''
        Set a dataset of given (Species/Parameter/...) ID. Reset the complete internal
        data dict if no keyEntity is given.
        '''
        if not keyEntity:
            self.data = data
        else:
            self.data[keyEntity] = data

    def getFormat(self):
        return self.format

    def getNumDataPoints(self):
        return len(self.data)

    def getNumOfRealData(self):
        """
        Walks through all EntityData objects this DataSet holds
        and counts the number where isMetaData = False *and* isWeightData = false.
        Those are the EntityData objects with "usable" data (i.e.
        that belong to a Species).
        """
        count = 0
        for entityData in self.data.values():
            if not (entityData.isMetaData or entityData.isWeightData):
                count += 1
        return count

    def setType(self, type):
        self.type = type
        
    def isSelected(self):
        return self.selected == True
        
    def setSelected(self, bvalue):
        if not type(bvalue) is bool:
            self.selected = False
        else:
            self.selected = bvalue

    def setDescriptorHeader(self, header):
        self.descriptorHeader = str(header)
        self.dataChanged.emit(self, None)

    def setDescriptor(self, index, value):
        self.dataDescriptors[index] = value
        self.dataChanged.emit(self, None)

    ########## SLOTS #############
    def on_entityDataChanged(self, entityData, type, index):
        self.dataChanged.emit(self, entityData)   # need to pass through all info?