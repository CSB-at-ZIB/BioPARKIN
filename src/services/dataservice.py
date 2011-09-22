'''
Created on Mar 11, 2010

@author: bzfwadem
'''

#import backend_fortran.datahandling
import csv
import math
from stabledict import StableDict
import logging
from datamanagement.dataset import DataSet
import datamanagement.dataset


TIME, VALUE = range(2)
SIMULATION = "simulation"
EXPERIMENTAL = "experimental"
SENSITIVITY_DETAILS = "sensitivity_details"
SENSITIVITY_OVERVIEW = "sensitivity_overview"
ESTIMATED_PARAMS = "estimated_params"

class DataService(object):
    '''
    A data manager for accessing experimental data
    and simulation data results. The service can read data files
    and provide the data in a convenient data structure.
    
    The __new__ method is overridden to make this class a singleton.
    Every time it is instantiated somewhere in code, the same instance will be
    returned. In this way, it can serve like a static class.
    
    The data will have format:
    {DataID: [[time points/or other identifier],[value at time point/identifier]]}
    
    The DataID is given in the input files.
    
    This class can read the very special file formats used by PARKIN.
    
    @since: 2010-03-11
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    _instance = None

    def __new__(cls, *args, **kwargs): # making this a Singleton, always returns the same instance
        if not cls._instance:
            cls._instance = super(DataService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "data"):   # only create on first init
            self.data = None
            self.dataDict = None
            self.Dirty = True
            self.DataFiles = None


    def _read_experimental_data(self, listOfFilenames, format, parkinController=None):
        if listOfFilenames is None:
            logging.debug("DataService: listOfFilenames (experimental data): %s" % listOfFilenames)
            return

        if not self.data:
            self.data = []
        if not self.dataDict:
            self.dataDict = StableDict()

        for filename in listOfFilenames:
            fileData = DataSet(filename, format=format, type=EXPERIMENTAL, parkinController=parkinController)
            if not fileData.data:
                continue
            if fileData.getId() in self.dataDict.keys():
                continue
            fileData.setSelected(True)
            self.data.append(fileData)
            self.dataDict[fileData.getId()] = fileData



        #    def set_experimental_data_files(self, listOfFilenames = None):
        #        '''
        #        Only supports the special BioParkin file format, for now.
        #        '''
        #        if listOfFilenames is None:
        #            return
        #
        #        self.ExperimentalDataFiles = listOfFilenames
        #        self.DirtyExperimental = True
        #
        #    def get_experimental_data_files(self):
        #        return self.ExperimentalDataFiles

    def get_selected_experimental_data(self):
        '''
        Returns all experimental DataSet objects that are currently selected by the user.
        '''
        if not self.data:
            logging.error("DataService.get_data(): No data available.")
            return

        selectedData = StableDict()
        for dataSet in self.data:
            if dataSet.type == EXPERIMENTAL and dataSet.isSelected() == True:
                selectedData[dataSet.getId()] = dataSet
                
        return selectedData

    def get_experimental_data(self):
        '''
        @returns: StableDict with all experimental data.
        '''
        #print "self.DirtyExperimental: %s" % self.DirtyExperimental
        #        if self.DirtyExperimental:
        #            self._read_experimental_data(self.ExperimentalDataFiles)
        #            self.DirtyExperimental = False
        #        return self.experimentalData
        return self.get_data(type=EXPERIMENTAL)

    def getMaximumNumberOfObservedPoints(self):
    #        if self.DirtyExperimental:
    #            self._read_experimental_data(self.ExperimentalDataFiles)
    #            self.DirtyExperimental = False
        experimentalData = self.get_experimental_data()
        if not experimentalData:
            return

        maxCount = -1
        for key, items in experimentalData.items():
            count = max(len(items[0]), len(items[1]))
            if count > maxCount: maxCount = count
        return maxCount


    def _read_simulation_data(self, listOfFilenames, format=None, listOfEntities=None):
        if listOfFilenames is None:
            logging.debug("DataService: Can't load simulation data without being given a list of reference entities.")
            return
        if format is None:
            return

        if not self.data:
            self.data = []
        if not self.dataDict:
            self.dataDict = StableDict()

        for filename in listOfFilenames:
            fileData = DataSet(filename, format=format, listOfEntities=listOfEntities)
            if not fileData.data:
                continue
            if fileData.getId() in self.dataDict.keys():
                continue
            self.data.append(fileData)
            self.dataDict[fileData.getId()] = fileData


        #    def set_simulation_data_files(self, listOfFilenames = None, listOfEntities = None):
        #        '''
        #        Only supports the special BioParkin file format, for now.
        #        '''
        #        if listOfFilenames is None or listOfEntities is None:
        #            return
        #
        #        self.SimulationDataFiles = listOfFilenames
        #        self.SimulationEntityList = listOfEntities
        #        self.DirtySimulation = True
        #
        #    def get_simulation_data_files(self):
        #        return self.SimulationDataFiles

    def get_simulation_data(self):
        return self.get_data(type=SIMULATION)


    def get_sensitivity_details_data(self):
        return self.get_data(type=SENSITIVITY_DETAILS)

    def get_sensitivity_trajectory_data(self):
        return self.get_data(type=SENSITIVITY_OVERVIEW)

    def get_estimated_param_data(self):
        return self.get_data(type=ESTIMATED_PARAMS)


    #    def get_data_sources_with_dataIDs(self):
    ##        dataSources = StableDict()  # regenerate this every time
    ##
    ##        self.get_simulation_data() #read data (discard result reference, we don't need it here)
    ##
    ##        for (i, fileID) in enumerate(self.simulationData.keys()):
    ##            #sourceID = "Simulation %s" % i   # nice way of renaming cryptic and irrelevant file names
    ##            if self.simulationData[fileID].data:
    ##                dataIDs = map(lambda x: x.id, self.simulationData[fileID].data.keys())
    ##                dataSources[fileID] = dataIDs
    ##
    ##        self.get_experimental_data() # read data (discard result reference, we don't need it here)
    ##        if self.experimentalDataDict is not None:   # it is None if there's no experimental data
    ##            #expFiles = self.get_experimental_data_files()
    ##            if self.experimentalDataDict.data:
    ##                for (i, fileID) in enumerate(self.experimentalDataDict.data.keys()):    # self.experimentalDataDict is a StableDict
    ##                    #sourceID = expFiles[i]
    ##                    dataIDs = self.experimentalDataDict[fileID]
    ##                    dataSources[fileID] = dataIDs
    ##
    ##        return dataSources
    #        return self.dataDict

    #    def get_sensitivity_data_with_dataIDs(self):
    #        dataSource = StableDict()
    #
    #        sensData = self.get_sensitivity_data_per_species_parameter()
    #        if sensData.data:
    #            #dataIDs = map(lambda x: x, sensData.data.keys())
    #            dataIDs = sensData.data.keys()
    #            dataSource[sensData.getId()] = dataIDs
    #            #print(sensData.data.keys())
    #            #print("%s : %s" %(sensData.getId(), dataIDs))
    #            #logging.debug("%s : %s" %(sensData.getId(), dataIDs))  # crashes python
    #        return dataSource


    def get_all_data(self):
        '''
        Combines simulation and experimental data into one data structure.
        
        The data structure currently is just an StableDict which has a fixed
        key for the simulation data and filenames for keys for the experimental
        data.
        '''
        #        allData = StableDict()
        #
        #        #map(lambda (key, value): allData[key] = value, self.simulationData.items())
        #        if self.simulationData:
        #            for (key, value) in self.simulationData.items():
        #                allData[key] = value
        #
        #        #map(lambda (key, value): allData[key] = value, self.experimentalData.items())
        #        if self.experimentalData:
        #            for (key, value) in self.experimentalData.items():
        #                allData[key] = value


        #        return allData
        return self.dataDict

    #    def set_sensitivity_data(self, speciesParameter = None, speciesParameterTime = None):
    #        self.sensitivitiesParameterSpeciesTime = speciesParameterTime
    #        self.sensitivitiesSpeciesParameter = speciesParameter
    #
    #    def get_sensitivity_data_per_parameter_species_time(self):
    #        return self.sensitivitiesParameterSpeciesTime
    #
    #    def get_sensitivity_data_per_species_parameter(self):
    #        return self.sensitivitiesSpeciesParameter


    # new methods

    def load_data(self, filenames, type=None, format=None, listOfEntities=None, parkinController=None):
        ''' Loads one or more files with experimental data into memory.'''
        if not filenames:
            logging.error("DataService: No filename(s) given for loading data.")
            return
        if not type:
            logging.error("DataService: No data type given for loading data.")
            return
        if not format:
            logging.error(
                "DataService: No file format given for loading data. Assuming standard format based on data type.")

        if filenames is str:
            filenames = [filenames]

        if type == EXPERIMENTAL:
            if not format:
                format = datamanagement.dataset.FORMAT_EXP_PARKIN
            self._read_experimental_data(filenames, format, parkinController=parkinController)
        elif type == SIMULATION:
            if not listOfEntities:
                logging.error(
                    "DataService: Can't load simulation data without being given a list of reference entities.")
                return
            if not format:
                format = datamanagement.dataset.FORMAT_SIM_DOP
            self._read_simulation_data(filenames, format=format, listOfEntities=listOfEntities)


    def get_data(self, type=None):
        '''
        Returns all stored DataSet objects of given type.
        '''
        if not type:
            logging.error("DataService.get_data(): Can't access data without being given a data type.")
            return

        if not self.data:
            logging.error("DataService.get_data(): No data available.")
            return

        dataOfType = StableDict()
        for dataSet in self.data:
            if dataSet.type == type:
                #dataOfType.append(dataSet)
                dataOfType[dataSet.getId()] = dataSet
        return dataOfType

    def add_data(self, data):
        if not type(data) is DataSet:
            logging.error("DataService: Can't add a non DataSet object to the internal data.")
            logging.error("object: %s" % data)
            return

        if not self.data:
            self.data = []

        if not self.dataDict:
            self.dataDict = StableDict()

        self.data.append(data)
        self.dataDict[data.getId()] = data

    def remove_data(self, dataSet):
        if not dataSet:
            return
        
        try:
            self.data.remove(dataSet)
            self.dataDict.pop(dataSet.getId(), None)
        except:
            logging.error("DataService.remove_data(): Error while trying to remove DataSet %s" % dataSet.getId())

    def select_data(self, dataSet, isSelected):
        if not dataSet:
            return
            
        try:
            if dataSet in self.data:
                j = self.data.index(dataSet)
                self.data[j].setSelected(isSelected)
        except:
            logging.error("DataService.select_data(): Error while selecting DataSet %s" % dataSet.getId())

    def select_all(self):
        for dataSet in self.data:
            self.select_data(dataSet, True)

    def has_data(self, id):
        if self.dataDict:
            return id in self.dataDict.keys()
        return False


    def save_data_as_csv(self, id, path):
        '''
        Save data with given ID as CSV file at given path.
        '''

        try:

            dataSet = self.dataDict[id]
            if not dataSet:
                return

            csv.register_dialect("BioPARKIN_TabDelimited", delimiter='\t', quotechar='"', skipinitialspace=True)
            writer = csv.writer(open(path, "wb"), dialect="BioPARKIN_TabDelimited")

            dataTable = [] # 2D table

            # handle first column (e.g. global timepoints)
            if not dataSet.dataDescriptors:
                logging.error("Can't save data to file %s" % path)
                logging.debug("DataService.save_data_as_csv(): Can't save because there is no global list of data descriptors (e.g. timepoints).")
                return

            firstCol =  [dataSet.descriptorHeader] + dataSet.dataDescriptors  # list concatenation
            dataTable.append(firstCol)


            # handle the other columns
            for entityId, entityData in dataSet.getData().items():
                col = [entityData.getHeader()] +  entityData.datapoints
                dataTable.append(col)


            # switch rows and cols
            dataTable = zip(*dataTable) # * is for unpacking the list into individual arguments

            for row in dataTable:
                writer.writerow(row)


        except Exception, e:
            logging.error("Error while trying to write CSV file: %s\nError: %s" % (path, e))


