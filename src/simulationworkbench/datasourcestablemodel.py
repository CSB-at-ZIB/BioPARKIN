'''
Created on Jun 30, 2010

@author: bzfwadem
'''

import os

#from PySide.QtCore import *
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL
from stabledict import StableDict
from basics.helpers import enum
import logging
from sbml_model.sbml_entities import SBMLEntity
from odehandling.specieswrapper import SpeciesWrapper


COLUMN = enum.enum("ROW", "ID, NAME, INITIALVALUE, UNIT, ISCONSTANT") # this effectively orders the columns 
STATE = enum.enum("STATE", "CHECKED, UNCHECKED, NODATA")

class DataSourcesTableModel(QAbstractTableModel):
    '''
    A data model that wraps an dictionary providing the existing data IDs
    for several sets of data (obtained from several data files).
    
    @since: 2010-06-30
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, dataSources):
        '''
        Simple Constructor, just setting up some instance variables.
        '''
        super(DataSourcesTableModel, self).__init__()


        self.dataSources = dataSources

        #print(dataSources) # debugging
        
        self.Dirty = False # True if something has been changed
        
        #construct 2D array with all the data for easier access later-on
        self.dataIDs = []
        self.dataMatrix = [self.dataIDs] # outer list is for columns, 1st inner list for data IDs
        self.headers = ["ID"]


        if not dataSources:
            logging.error("DataSourcesTableModel.__init__(): Can't init without datasources.")
            return
        
        # collect all dataIDs
        for (fileID, dataSet) in self.dataSources.items():
            #print("fileID: %s\tdataSet:%s" % (fileID, dataSet))
            dataDict = dataSet.getData()
            if not dataDict:
                continue
            for dataWrapper in dataDict.keys():
                # we now regard strings as valid keys (necessary for sensitivities, etc.)
#                if type(dataWrapper) is str:
#                    logging.error("DataSourcesTableModel: Encountered DataSet with str as key! Should be an SBMLEntity object.")
#                    dataID = dataWrapper
                dataID = dataWrapper
#                else:
#                    dataID = dataWrapper.getId()
                if dataID not in self.dataIDs:
                    self.dataIDs.append(dataID)
        
        first = True
        for (fileID, dataSet) in self.dataSources.items():
            #dataIDs = map(lambda x: x.getId(),dataSet.getData().keys())
            #dataIDs = dataSet.getData().keys()  # keys should be strings
            data = dataSet.getData()
            if not data:
                logging.debug("DataSourcesTableModel.__init__(): No data for file %s" % fileID)
                continue
            dataIDs = data.keys()  # keys are SBMLEntity objects

            # fill column for this file
            columnForFile = []
            for existingDataID in self.dataIDs: # going through all IDs
                if existingDataID in dataIDs: # and comparing with file's subset of IDs
                    if first:
                        columnForFile.append(STATE.CHECKED)
                        first = False
                    else:
                        columnForFile.append(STATE.UNCHECKED)
                else:
                    columnForFile.append(STATE.NODATA)
            
            # add complete entry        
            self.headers.append(fileID)
            self.dataMatrix.append(columnForFile)
                    
        
# methods necessary for read-only models
# experimentalData()
# rowCount()
# columnCount()
# headerData() (almost always)

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.dataIDs)) or not (0 <= index.column() < len(self.headers)):
            return 
        
        row = index.row()
        column = index.column()
        
        if role == Qt.TextAlignmentRole:
            if column == 0:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignCenter
        
        if role == Qt.DisplayRole:

            data =  self.dataMatrix[column][row]
            if type(data) is str:
                return data
            #elif type(data) is SBMLEntity or type(data) is SpeciesWrapper or type(data):
            elif hasattr(data,  "getCombinedId"):
                return data.getCombinedId()
            elif hasattr(data, "getId"):
                return data.getId()
            elif data == STATE.NODATA:
                return "N/A"
            #return True if data == STATE.CHECKED else False
            return "Show" if data == STATE.CHECKED else "Hide"
            
        
        if role == Qt.CheckStateRole:
            data =  self.dataMatrix[column][row]
            if type(data) is str:
                return
            elif type(data) is SBMLEntity or type(data) is SpeciesWrapper:
                return 
            elif data == STATE.NODATA:
                return 
            return Qt.Checked if data == STATE.CHECKED else Qt.Unchecked

        
        return 
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
#            return self.headers[section].split(os.path.sep)[-1]
            return self.headers[section].split("/")[-1] # for now, use "/" because that's used throughout BioPARKIN
        return None
    
    def rowCount(self, index = QModelIndex()):
        return len(self.dataIDs)
    
    def columnCount(self, index = QModelIndex()):
        return len(self.headers)
    
    
# methods necessary for editable models
# flags()
# setData()
    
    def flags(self, index):
        if not index.isValid() or not (0 <= index.row() < len(self.dataIDs)) or not (0 <= index.column() < len(self.headers)):
            return Qt.NoItemFlags
        
        row = index.row()
        column = index.column()
        
        if index.column() == 0:
            return Qt.NoItemFlags
        else:
            data =  self.dataMatrix[column][row]
            return Qt.NoItemFlags if data == STATE.NODATA else (Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            
            
#        elif index.column() == (COLUMN.INITIALVALUE):
#            return (Qt.ItemIsEnabled 
#                    | Qt.ItemIsEditable
#                    )
            
        return Qt.NoItemFlags
    
    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.dataIDs) and 0 <= index.column() < len(self.headers):
#            sbmlEntity = self.paramList[index.row()]
#            param = sbmlEntity.Item

            row = index.row()
            column = index.column()
            if column == 0:
                return
            
#            if role == Qt.EditRole:
#                if column == COLUMN.INITIALVALUE:
#                    param.setValue(float(value))
                
            if role == Qt.CheckStateRole:
                if self.dataMatrix[column][row] != STATE.NODATA:
                    isChecked = value == Qt.Checked
                    if isChecked:
                        self.dataMatrix[column][row] = STATE.CHECKED
                    else:
                        self.dataMatrix[column][row] = STATE.UNCHECKED
            
            self.Dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        
        return False              
        
        
        
########## HELPER METHODS #############

    def getSelectedIDs(self):
        '''
        Returns all currently checked IDs in a stable dict.
        '''
        selectedIDs = StableDict()
        
        for col in xrange(len(self.dataMatrix)):
            if col == 0:
                continue
            for row in xrange(len(self.dataMatrix[col])):
                if self.dataMatrix[col][row] == STATE.CHECKED:
                    dataID = self.dataIDs[row]
                    fileID = self.headers[col]
                    if dataID in selectedIDs:
                        selectedIDs[dataID].append(fileID)
                    else:
                        selectedIDs[dataID] = [fileID]
                        
        return selectedIDs

    def selectAllSources(self, doSelect, column=None, row=None):

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
#        self.emit(SIGNAL("modelAboutToBeReset()"))
        
        for columnIter in xrange(1,self.columnCount()):
            if column is not None and column != columnIter: # inefficient but easiest way to do this without code duplication
                continue
            for rowIter in xrange(self.rowCount()):
                if row is not None and row != rowIter: # inefficient but easiest way to do this without code duplication
                    continue
                if self.dataMatrix[columnIter][rowIter] == STATE.NODATA:
                    continue
                    
                if doSelect:
                    isChecked = STATE.CHECKED
                else:
                    isChecked = STATE.UNCHECKED
                    
                self.dataMatrix[columnIter][rowIter] = isChecked


        self.emit(SIGNAL("layoutChanged()"))
        self.dataChanged.emit(QModelIndex(), QModelIndex())
#        self.emit(SIGNAL("modelReset()"))

    def invertSelection(self):

        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for column in xrange(1,self.columnCount()):
            for row in xrange(self.rowCount()):
                if self.dataMatrix[column][row] == STATE.NODATA:
                    continue
                    
                if self.dataMatrix[column][row] ==  STATE.CHECKED:
                    self.dataMatrix[column][row] = STATE.UNCHECKED
                else:
                    self.dataMatrix[column][row] = STATE.CHECKED


        self.emit(SIGNAL("layoutChanged()"))
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def getNumberOfDataItems(self):
        return self.rowCount(None) * self.columnCount(None)

    def getEntityIDs(self):
        return self.dataIDs