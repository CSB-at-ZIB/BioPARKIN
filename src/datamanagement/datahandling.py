'''
Created on Mar 9, 2010

@author: bzfwadem
'''
from collections import OrderedDict

import csv, logging
import math

import services.dataservice
from datamanagement import entitydata
from datamanagement.entitydata import EntityData
from basics.helpers.sbmlhelpers import  findSbmlEntity


__author__ = "Moritz Wade"
__contact__ = "wade@zib.de"
__copyright__ = "Zuse Institute Berlin 2010"

parkinController = None

STANDARD_DEVIATION = "sd"

def read_raw_data(filename, dataSet=None, parkinController=None):
    '''
    Parses files of the PARKIN raw format (see below)
    into a dictionary.
    
    The entityMap is put into objects of type EntityData.
    
    
    Raw format::
        0 4
          2 4.85286 1
          4 7.61857 1
          17 40.8571 1
          18 0.411429 1
        1 4
          2 4.811 1
          4 6.972 1
          17 42.7 1
          18 0.331 1
     
     Time points: 0 and 1 have 4 entityMap points.
     
    
    @since: 2010-06-07
    '''
    entityMap = OrderedDict()

    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(" ")
                if line[0] != " ":  # new time point
                    time = float(parts[0])
                else: # new entry for current time point
                    dataID = parts[0]
                    value = float(parts[1])
                    # we disregard parts[2], i.e. the "1"
                    if dataID in entityMap:  # fetch existing entity
                        entity = entityMap[dataID]
                    else: # create new entry
                        #entry = ([],[])
                        entity = entitydata.EntityData()
                        if dataSet:
                            entity.setAssociatedDataSet(dataSet)
                        entityMap[dataID] = entity
                    entity.dataDescriptors.append(time)
                    entity.datapoints.append(value)
    except Exception, e:
        logging.error("Could not read file %s. Error: %s" % (filename, e))
        return

    for (id, entity) in entityMap.items():
        entity.originalId = id
        entity.originalFilename = filename
        if parkinController and parkinController.ActiveModelController and parkinController.ActiveModelController.sbmlModel:
            #entity.sbmlEntity = helpers.sbmlhelpers.findSbmlEntity(id, parkinController.ActiveModelController.sbmlModel)
            entity.sbmlEntity = findSbmlEntity(id, parkinController.ActiveModelController.sbmlModel)

    return entityMap


def read_csv_data(filename, dataSet=None, parkinController=None):
    '''
    Parses a CSV (comma separated values) file with experimental data.

    The CSV has to have a header line. Fields may be encapsulated by " (but they
    don't have to be). The value format is e.g. "3.14".

    Headers have the following convention:
        - First column called C{"Timepoint [%UNIT%]"}, e.g. C{"Timepoint [s]"}
        - Second column called C{"Unit"} for the time unit.
        - One column per Species ID, given the unit in square brackets. E.g: C{"LH [mg/ml]"}
        - Optionally: One column per Species Weight called "Weight" *immediately* after the ID column.
        - All other columns are handled as kind of "meta data". So, there can be e.g. a "patient id" column.
          The data of this column will be put in its own EntityData object with isMetaData = True.
    '''
    try:
        logging.info("Reading file %s" % filename)
        csv.register_dialect("ExperimentalDataCSV", delimiter='\t', quotechar='"', skipinitialspace=True)
        reader = csv.reader(open(filename), dialect="ExperimentalDataCSV")

        descriptors = []
        descriptorUnit = ""

        columnIDs = []
        columnIDToUnit = {}
        columnIDHasWeightColumn = {}
        columnIDsToValues = {}  
        columnIndexToColumnID = {}

        idToName = {}

        originalHeaders = {}

        columnIndexesWithWeightData = []

        columnIndexesWithMetaData = [] # for columns with "non-critical" information
        columnIDsWithMetaData = []

        previousId = None

        # getting data from file and preparing it for a DataSet
        for (i, row) in enumerate(reader):
            if i == 0: # in header row
                for (j, header) in enumerate(row):
                    if j == 0:  # timepoint header
                        originalDescriptorHeader = header
                        if not "[" in header:
                            descriptorUnit = "N/A"
                        else:
                            descriptorUnit = header.split("[")[1].rsplit("]")[0].strip()
                    else: # all non-timepoint headers
                        if "[" in header:   # the current cell is a Species definition
                            splitID = header.split("[")
                            id = splitID[0].strip()
                            unit = splitID[1].strip()[:-1]
                            columnIDs.append(id)
                            columnIDToUnit[id] = unit
                            columnIDsToValues[id] = []
                            columnIndexToColumnID[j] = id
                            originalHeaders[id] = header
                            previousId = id
                        elif previousId and STANDARD_DEVIATION in header.lower():    # if in weight-defining cell
                            # radical change: handle weight columns as "normal" data, save them in separate EntityData
                            columnIDHasWeightColumn[previousId] = True # will be used later on
                            columnIndexesWithWeightData.append(j)

                            id = "weight_%s" % previousId
                            columnIDs.append(id)
                            columnIDsToValues[id] = []
                            columnIndexToColumnID[j] = id
                            idToName[id] = "SD"
                            originalHeaders[id] = header

                            previousId = None
                        else:   # in non-defined arbitrary cell, e.g. "Patient ID"
                            columnIndexesWithMetaData.append(j)
                            columnIDsWithMetaData.append(header)
                            columnIDs.append(header)
                            columnIDsToValues[header] = []
                            columnIndexToColumnID[j] = header
                            originalHeaders[header] = header
                            previousId = None
                            logging.debug("DataHandling.read_csv_data(): Reading 'meta data' of column %s" % header)


            else:   # for all non-header rows
                for (j, value) in enumerate(row):
                    if j == 0:    # data descriptor column (e.g. timepoints)
                        descriptors.append(value)
                    elif j in columnIndexesWithMetaData:    # handling "non-species" columns
                        id = columnIndexToColumnID[j]
                        columnIDsToValues[id].append(value)
                        previousId = None
                    elif columnIDHasWeightColumn.get(previousId, False):    # this is a weight-defining cell
                        columnIDsToValues[previousId].append(value)
                        previousId = None
                    else:
                        id = columnIndexToColumnID[j]
                        columnIDsToValues[id].append(value)

        # loop through the collected data and feed it into a OrderedDict with EntityData objects
        # as values. This is the internal data structure of a DataSet object.

        dataSet.dataDescriptors = descriptors   # e.g. global timepoint list
        dataSet.dataDescriptorUnit = descriptorUnit
        dataSet.descriptorHeader = originalDescriptorHeader

        lastEntityData = None
        entityMap = OrderedDict()    # keep Species order
        for j, columnID in enumerate(columnIDs):
            logging.debug("About to save data for column %s" % columnID)

            entityData = EntityData()

            entityData.dataDescriptorUnit = descriptorUnit
            entityData.datapointUnit = columnIDToUnit.get(columnID, None)
            entityData.setType(entitydata.TYPE_EXPERIMENTAL)
            entityData.setAssociatedDataSet(dataSet)    # always use this method, so SIGNALs are correctly connected!
            entityData.originalId = columnID  # can be used as an ID fallback (e.g. for plotting) later
            entityData.originalHeader = originalHeaders[columnID]

            if idToName.has_key(columnID):
                entityData.setName(idToName[columnID])

            if columnID in columnIDsWithMetaData:
                entityData.isMetaData = True
            if j in columnIndexesWithWeightData:
                entityData.isWeightData = True
                entityData.setWeightData(lastEntityData)

            values = columnIDsToValues[columnID]
            if not values:
                logging.error("datahandling.load_csv_data(): No values for column %s" % columnID)
                continue


            for i, value in enumerate(values):
                try:
                    value = float(value)
                except :
                    value = None
                    
                timepoint = descriptors[i]
                entityData.dataDescriptors.append(timepoint)

                entityData.datapoints.append(value)

            # try to associate a Species in the currently loaded model (if any) with the current Species ID
            if not columnID in columnIDsWithMetaData and parkinController and parkinController.ActiveModelController and parkinController.ActiveModelController.sbmlModel:
                entityData.sbmlEntity = findSbmlEntity(columnID, parkinController.ActiveModelController.sbmlModel)

            if entityData.sbmlEntity:
                entityMap[entityData.sbmlEntity] = entityData
            else:
                entityMap[columnID] = entityData

            lastEntityData = entityData

        return entityMap


    except Exception, e:
        logging.error("DataHandling.read_csv_data(): Error while reading file %s:\n%s" % (filename, e))

#def read_raw_data_old(filename):
#    '''
#    OLD VERSION, DON'T USE!
#    Only for looking up old code!
#
#    Parses files of the PARKIN raw format (see below)
#    into a dictionary.
#
#    The dictionary will have the following structure:
#    data = { key : ([xvalues], [yvalues] ) }
#
#
#    Raw format:
#  0 4
#     2 4.85286 1
#     4 7.61857 1
#     17 40.8571 1
#     18 0.411429 1
#  1 4
#     2 4.811 1
#     4 6.972 1
#     17 42.7 1
#     18 0.331 1
#
#     Time points: 0 and 1 have 4 data points.
#
#     Resulting dict (for Species "2") should be:
#
#     data = { "2" : {DataManager.TIME: [0, 1],
#                     DataManager.VALUE: [4.85286, 4.811]},
#              "4" : ...
#              "17": ...
#              "18": ...
#            }
#    '''
#    data = {}
#    try:
#        with open(filename, 'r') as f:
#            for line in f:
#                parts = line.strip().split(" ")
#                if line[0] != " ":  # new time point
#                    time = float(parts[0])
#                else: # new entry for current time point
#                    dataID = parts[0]
#                    value = float(parts[1])
#                    # we disregard parts[2], i.e. the "1"
#                    if dataID in data:  # fetch existing entry
#                        entry = data[dataID]
#                    else: # create new entry
#                        #entry = ([],[])
#                        entry = {services.dataservice.TIME: [],
#                                 services.dataservice.VALUE: []}
#                        data[dataID] = entry
#                        #        entry[0].append(time)
#                        #        entry[1].append(value)
#                    entry[services.dataservice.TIME].append(time)
#                    entry[services.dataservice.VALUE].append(value)
#    except Exception, e:
#        logging.error("Could not read file %s. Error: %s" % (filename, e))
#
#    return data


def read_integrated_data(filename, listOfEntities, dataSet=None):
    '''
    Reads the results of a Fortran-BioParkin run.
    
    The list of SBML entities is used to associate columns in the entityData file
    with their corresponding entityData entities.
        
    format:
    C{[time [WHITESPACE] par 1 [WHITESPACE] par n}
    
    e.g.:
    C{0.0000000000000000E+00     1.4999999999999999E-02    0.0000000000000000E+00}
    
    '''

    try:
        csv.register_dialect("SimulationData", delimiter=' ', quotechar='"', skipinitialspace=True)
        reader = csv.reader(open(filename), dialect="SimulationData")
        time = []
        values = {}
        for (i, row) in enumerate(reader):  # we don't use the i... yet

            for (j, value) in enumerate(row):
                if j == 0:  # jump over the 0th row
                    time.append(value) # time value is always in the 0th row
                    continue

                columnID = j - 1 # possibility to compensate for column offset
                entity = listOfEntities[columnID]
                if values.has_key(entity):
                    values[entity].append(value) # append to existing list
                else:
                    values[entity] = [value] # create list for the first time

        # create final data structure
        dataMap = {}
        if len(values) > 0: # if we have dataMap
            for entity in values.keys():
                entityData = EntityData()
                if dataSet:
                    entityData.setAssociatedDataSet(dataSet)
                entityData.dataDescriptors = time
                entityData.datapoints = values[entity]
                entityData.type = entitydata.TYPE_SIMULATED
                entityData.sbmlEntity = entity.wrappedEntity
                entityData.originalFilename = filename
                dataMap[entity] = entityData
            return dataMap

    except Exception, e:
        logging.error("Error while trying to read simulation dataMap file: %s" % e)

#def read_integrated_data_old(filename):
#    '''
#    OLD VERSION, DON'T USE!
#    Only for looking up old code!
#
#    Reads the results of a Fortran-BioParkin run.
#
#    input format, e.g. see:
#    /home/bzfwadem/workspace/BioParkin/compute/temp/P_gnrh_rec4_Solution.dat
#
#    format:
#    time \t par 1 \t par n
#
#    '''
#    data = {}
#
#    #with csv.reader(open(filename), delimiter=' ', quotechar='"') as reader:
#    try:
#        csv.register_dialect("SimulationData", delimiter=' ', quotechar='"', skipinitialspace=True)
#        reader = csv.reader(open(filename), dialect="SimulationData")
#        time = []
#        values = {}
#        for (i, row) in enumerate(reader):  # we don't use the i... yet
#
#            for (j, value) in enumerate(row):
#                if j == 0:  # jump over the 0th row
#                    time.append(value) # time value is always in the 0th row
#                    continue
#
#                columnID = j # possibility to compensate for column offset
#                # we will use the column index as the key
#                # TODO: We need something better than the column index. Column indices should be matched to previously loaded experimental data (or parts of the SBML model?)
#                if values.has_key(columnID):
#                    values[columnID].append(value) # append to existing list
#                else:
#                    values[columnID] = [value] # create list for the first time
#
#        # create final data structure
#        if len(values) > 0: # if we have data
#            for dataID in values.keys():
#                #if not data.has_key(dataID):
#                entry = {services.dataservice.TIME: time,
#                         services.dataservice.VALUE: values[dataID]}
#                data[str(dataID)] = entry   #str: because the experimental data's keys are strings
#                #else:
#                #    entry = data[dataID]
#            #                entry[Services.DataService.TIME] = time
#            #                entry[Services.DataService.VALUE].append(value)
#
#    except Exception, e:
#        logging.error("Error while trying to read simulation data file: %s" % e)
#    #    finally:
#    #        reader.close() # does not exist and does not seem to be necessary
#
#
#    #
#    #    dictReader = csv.DictReader(open(filename), ["time", range(nrCols)-1])
#    #    unformattedData = dictReader.
#
#    # TODO
#    #    for row in reader:
#    #        #time = float(row[0])
#    #        for (i, value) in row.enumerate_stripped():
#    #            if i == 0:
#    #                time = float(row[0])
#    #            else:
#
#    return data