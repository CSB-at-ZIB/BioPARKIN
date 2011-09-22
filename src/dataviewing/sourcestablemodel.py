'''
Created on Mar 11, 2010

@author: bzfwadem
'''
#from PySide.QtCore import *
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL

from basics.helpers import enum

COLUMN = enum.enum('ROW', 'ID, SHOWEXPERIMENTALDATA, SHOWSIMULATIONDATA') # this effectively orders the columns


class SourcesTableModel(QAbstractTableModel):
    '''
    Wraps the experimental experimentalData (and later on simulationData) 
    and makes its data IDs accessible read-only to a table view.
    It also creates checkboxes to tell whether to draw plots of the data.
    
    This is just a helper data model.
    
    @param experimentalData: The dict with the experimental data
    @type experimentalData: dict with {dataID: [[time points],[values at time points]]}
    
    @since: 2010-03-11
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, combinedData = None, experimentalData=None, simulationData=None):
        '''
        Parses through the data and puts it into a list and into a dict
        for easier use throughout the class.
        '''
        super(SourcesTableModel, self).__init__()
#        self.experimentalData = experimentalData
#        self.simulationData = simulationData
        self.combinedData = combinedData
        
        self.dataList = []
        self.dataDict = {}
        self.idToEntityMap = {}
        if self.combinedData is not None:
            for sbmlEntity in self.combinedData.keys():
                entry = {COLUMN.ID : sbmlEntity.id,
                         COLUMN.SHOWEXPERIMENTALDATA : False,
                         COLUMN.SHOWSIMULATIONDATA : False}
                self.dataList.append(entry)
                self.dataDict[sbmlEntity.id] = entry
                self.idToEntityMap[sbmlEntity.id] = sbmlEntity
#            self.dataList = []  # we need this list to have access on a per-column-index basis
#            for sbmlEntity in self.combinedData.keys():
#                self.dataList.append(sbmlEntity)
        
        self.Dirty = False # True if something has been changed
        
##        # table access is index based, but we use a dict. map indices to dict sbmlEntity.
##        # warning: unorderedness of dict could create problems.
##        if self.experimentalData is not None:
##            self.indexToDataEntry = []
##            for sbmlEntity in self.experimentalData.keys():
##                self.indexToDataEntry.append(sbmlEntity)
#
#        # "convert" dict to list to use that internally, with the additional parameters like "show exp. experimentalData", etc. 
#        # (which themselves are not part of the experimentalData and should not be)
#        # C#/MVVM speak: this is something like a view model
#        
#        self.dataList = []
#        self.idToEntityMap = {}
#        if self.experimentalData is not None:
#            for sbmlEntity.id in self.experimentalData.keys():
#                entry = {COLUMN.ID : sbmlEntity.id,
#                         COLUMN.SHOWEXPERIMENTALDATA : False,
#                         COLUMN.SHOWSIMULATIONDATA : False}
#                self.dataList.append(entry)
#                self.idToEntityMap[sbmlEntity.id] = entry
#        if self.simulationData is not None:
#            for sbmlEntity in self.simulationData.keys():
#                if sbmlEntity.id in self.idToEntityMap: # list data entries only once    
#                    continue
#                entry = {COLUMN.ID : sbmlEntity.id,
#                         COLUMN.SHOWEXPERIMENTALDATA : False,
#                         COLUMN.SHOWSIMULATIONDATA : False}
#                self.dataList.append(entry)
#                self.idToEntityMap[sbmlEntity.id] = entry
                
    def does_show_experimental_data_of(self, id):
        '''
        Returns experimental data with given id.
        '''
        #return self.idToEntityMap[id][COLUMN.SHOWEXPERIMENTALDATA]
        return self.dataDict[id][COLUMN.SHOWEXPERIMENTALDATA]
    
    def does_show_simulation_data_of(self, id):
        '''
        Returns simulation data with given id.
        '''
        return self.dataDict[id][COLUMN.SHOWSIMULATIONDATA]

# methods necessary for read-only models
# experimentalData()
# rowCount()
# columnCount()
# headerData() (almost always)

    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.dataList)):
            return None
        
        dataEntry = self.dataList[index.row()]
        column = index.column()
        
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        
        if role == Qt.DisplayRole:
            if column == COLUMN.ID:
                return dataEntry[COLUMN.ID]
            if column == COLUMN.SHOWEXPERIMENTALDATA:
                #return dataEntry[COLUMN.SHOWEXPERIMENTALDATA]
                entity = self.idToEntityMap[dataEntry[COLUMN.ID]]
                dataTuple = self.combinedData[entity]
                if dataTuple[1] is None:
                    return "N/A"
                else:
                    return None
                
            if column == COLUMN.SHOWSIMULATIONDATA:
                #return dataEntry[COLUMN.SHOWSIMULATIONDATA]
                entity = self.idToEntityMap[dataEntry[COLUMN.ID]]
                dataTuple = self.combinedData[entity]
                if dataTuple[0] is None:
                    return "N/A"
                else:
                    return None
        
        if role == Qt.CheckStateRole:
            if column == COLUMN.ID:
                return None
            if column == COLUMN.SHOWEXPERIMENTALDATA:
                return Qt.Checked if dataEntry[COLUMN.SHOWEXPERIMENTALDATA] else Qt.Unchecked
            if column == COLUMN.SHOWSIMULATIONDATA:
                return Qt.Checked if dataEntry[COLUMN.SHOWSIMULATIONDATA] else Qt.Unchecked

        
        return None
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == COLUMN.ID:
                return "ID"
            if section == COLUMN.SHOWEXPERIMENTALDATA:
                return "Show exp. Data"
            if section == COLUMN.SHOWSIMULATIONDATA:
                return "Show sim. Data"
        return None
    
    def rowCount(self, index = QModelIndex()):
        return len(self.dataList)
    
    def columnCount(self, index = QModelIndex()):
        return 3
    
    
# methods necessary for editable models
# flags()
# setData()
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        
        if index.column() == COLUMN.SHOWEXPERIMENTALDATA or index.column() == COLUMN.SHOWSIMULATIONDATA:
            return (Qt.ItemIsUserCheckable                                 
                    | Qt.ItemIsEnabled                                
                    #| Qt.ItemIsSelectable
                    )
            
        elif index.column() == (COLUMN.ID):
            return (Qt.ItemIsEnabled 
                    #| Qt.ItemIsSelectable
                    )
            
        return Qt.ItemIsEnabled 
    
    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.dataList):
            dataEntry = self.dataList[index.row()]
            column = index.column()
            
            if role == Qt.CheckStateRole:
                
                isChecked = value == Qt.Checked
                
#            if column == COLUMN.ID: # not editable
#                # would have to update experimentalData dict and list
                if column == COLUMN.SHOWEXPERIMENTALDATA:
                    dataEntry[COLUMN.SHOWEXPERIMENTALDATA] = isChecked
                elif column == COLUMN.SHOWSIMULATIONDATA:
                    dataEntry[COLUMN.SHOWSIMULATIONDATA] = isChecked
            
            self.Dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        
        return False        