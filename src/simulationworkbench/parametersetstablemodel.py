'''
Created on Mar 25, 2011

@author: Moritz Wade
'''
import logging
#from PySide.QtCore import *
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL
from PySide.QtGui import QFont
from basics.helpers import enum
import libsbml

ROW = enum.enum("ROW", "ID, ACTIVE, SELECTED") # this effectively orders the rows; Param ID rows will be appended
numAdditionalRows = 3
# Columns will be defined by the available ParameterSets

class ParameterSetsTableModel(QAbstractTableModel):
    '''
    Fills the Parameter Set tab of the Simulation Workbench with data.
    
    @param listOfParameterSets: List-like object with parameter sets (see parameter_sets.py)
    @type listOfParams: ListOfParameterSets
    
    @since: 2011-03-25
    '''
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    def __init__(self, listOfParameterSets):
        '''
        Simple Constructor, just setting up some instance variables.
        '''
        super(ParameterSetsTableModel, self).__init__()
        self.paramSets = listOfParameterSets

        self.paramIds = self.paramSets.getParamIds()

        self.paramSets.changed.connect(self.paramSetsChanged)

        self.Dirty = False # True if something has been changed

    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.column() < self.columnCount()) or not (
        0 <= index.row() < self.rowCount()):
            return None

        paramSet = self.paramSets[index.column()]
        row = index.row()
        offsetRow = row - numAdditionalRows

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role == Qt.DisplayRole:
            if row == ROW.ID:
                return paramSet.getId()
            elif row == ROW.ACTIVE:
                return "Active"  if self.paramSets.activeSet == paramSet else ""
            elif row == ROW.SELECTED:
                return "Selected" if self.paramSets.selectedSet == paramSet else ""
            else: # get the param value of that Set
                try:
                    value = paramSet[self.paramIds[offsetRow]].getValue()
                    return value
                except:
                    logging.debug("ParameterSetsTableModel.data(): Could not get value for row %s" % offsetRow)
                    return None

        if role == Qt.CheckStateRole:
            if row == ROW.ACTIVE:
                return Qt.Checked if self.paramSets.activeSet == paramSet else Qt.Unchecked
            elif row == ROW.SELECTED:
                return Qt.Checked if self.paramSets.selectedSet == paramSet else Qt.Unchecked
            else:
                return None

        if role == Qt.EditRole:
            if row == ROW.ID:
                return paramSet.getId()
            elif row == ROW.ACTIVE:
                return None
            elif row == ROW.SELECTED:
                return None
            else: # get the param value of that Set
                try:
                    value = paramSet[self.paramIds[offsetRow]].getValue()
                    return str(value)
                except:
                    logging.debug("ParameterSetsTableModel.data(): Could not get value for row %s" % offsetRow)
                    return None

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.FontRole:
            if orientation == Qt.Vertical:
                return QFont("Courier", pointSize=-1, weight=QFont.Black)
            return None
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            #return "Set: %s" % self.paramSets[section].getId()
            return "Set #%s" % (section + 1)    #only output number; ID is shown in an editable field
        if orientation == Qt.Vertical:
            maxWidth = len(str(self.paramSets.numParameters()))+1
            if section == ROW.ID:
                return " %s |  Name" % ("#".rjust(maxWidth))
            elif section == ROW.ACTIVE:
                return " %s |  Active" % (" ".rjust(maxWidth))
            elif section == ROW.SELECTED:
                return " %s |  Selected" % (" ".rjust(maxWidth))
            else:
                rowOffset = section - numAdditionalRows
                return " %s |  %s" % (str(rowOffset+1).rjust(maxWidth), self.paramIds[rowOffset])
        return None

    def rowCount(self, index=QModelIndex()):
        return self.paramSets.numParameters() + numAdditionalRows

    def columnCount(self, index=QModelIndex()):
        return len(self.paramSets)


    # methods necessary for editable models
    # flags()
    # setData()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.row() in (ROW.ACTIVE, ROW.SELECTED):
            return (Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
                    #| Qt.ItemIsSelectable
            )

        #        elif index.row() == ROW.ID:
        #            return (Qt.ItemIsEnabled | Qt.ItemIsEditable )
        #elif index.row() == (COLUMN.INITIALVALUE):
        else:
            return (Qt.ItemIsEnabled
                    | Qt.ItemIsEditable
            )

        return Qt.NoItemFlags

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.column() < self.columnCount()) or not (
        0 <= index.row() < self.rowCount()):
            return False

        paramSet = self.paramSets[index.column()]
        row = index.row()
        offsetRow = row - numAdditionalRows

        if role == Qt.EditRole:
            if row == ROW.ID:
                try:
                    paramSet.setId(str(value))
                except:
                    logging.debug("ParameterSetsTableModel.setData(): Can't set ID: %s" % value)
                    return 

            elif row == ROW.ACTIVE or row == ROW.SELECTED:
                return  # these rows can only be checked/unchecked 

            else: # set the param value of that Set
                try:
                    value = float(value)
                    paramSet[self.paramIds[offsetRow]].setValue(value)
                except:
                    logging.debug(
                        "ParameterSetsTableModel.setData(): Could not set value (%s) for row %s" % (value, offsetRow))
                    return False

        if role == Qt.CheckStateRole:
            isChecked = value == Qt.Checked
            if row == ROW.ACTIVE:
                if isChecked:
                    self.paramSets.activeSet = paramSet
                else:
                    self.paramSets.activeSet = self.paramSets.defaultSet
                self.paramSetsChanged()
            elif row == ROW.SELECTED:
                if isChecked:
                    self.paramSets.selectedSet = paramSet
                else:
                    self.paramSets.selectedSet = None
                self.paramSetsChanged()
            else:
                return None

        self.Dirty = True
        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

        return True # if this is reached, setting data somewhere above was successful :)


    def paramSetsChanged(self):
        self.emit(SIGNAL("layoutChanged()"))

    def getActiveSet(self):
        if not self.paramSets:
            logging.debug("ParameterTableModel.getActiveSet(): No list of Parameter Sets! Aborting.")
            return
        if not self.paramSets.activeSet:
            logging.debug("ParameterTableModel.getActiveSet(): No active Parameter Set! Aborting.")
            return

        return self.paramSets.activeSet
