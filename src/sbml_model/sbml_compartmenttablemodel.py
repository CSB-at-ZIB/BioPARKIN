'''
Created on Feb 24, 2010

@author: moritz

'''


#import sip
from PySide.QtCore import QAbstractTableModel, Signal, Qt, QModelIndex, SIGNAL
from sbml_model.sbml_entities import SBMLEntity
#sip.setapi('QString', 2)  # practically disables QStrings
#sip.setapi('QVariant', 2) # practically disables QVariants

#from PySide.QtCore import *
#from PySide.QtGui import  *

import libsbml
from basics.helpers import enum

COLUMN = enum.enum('ROW', 'NAME, ID, COMPARTMENTTYPE, SPATIALDIMENSIONS, SIZE, UNITS, OUTSIDE, CONSTANT') # this effectively orders the columns


###############
#
# NOTE: Don't use, this is outdated. Still works but changes will not be reflected by
# Views working on the newer SBMLMainTreeModel.
#
###############

class SBMLCompartmentTableModel(QAbstractTableModel):
    '''
    Obsolete! This has been replaced by SBMLMainTreeModel (which wraps
    all the Species types at once) and only remains here for
    future reference.
    
    
    
    This class encapsulates the ListOfCompartments of an SBML file/model.
    '''
    
    def GetDirty(self):
        return self.__Dirty


    def SetDirty(self, value):
        self.__Dirty = value
#        self.emit(SIGNAL("DirtyChanged(bool)"), value)
        self.dirtyChanged.emit(value)


    def DelDirty(self):
        del self.__Dirty

    Dirty = property(GetDirty, SetDirty, DelDirty, "Defines whether this model has any unsaved changes.")

    dirtyChanged = Signal(bool)
    
    def __init__(self, mainModel):
        '''
        Standard Initializer
        '''
        super(SBMLCompartmentTableModel, self).__init__()
        self.mainModel = mainModel # necessary, handles saving, etc. 
        self.mainModel.CompartmentTableModel = self
        
        #self.setWindowTitle("Compartments of %s" % self.mainModel.SbmlModel.getName())
        
#        self.filename = None
        self.Dirty = False # True if something has been changed
        self.compartments = self.mainModel.SbmlCompartments
    
    
    # custom methods for this Model
    # save()
    
#    def save(self, filename = None):
#        '''
#        Uses the "meta model class" SBMLMainModel to save the model to a file.
#        
#        If a filename is given it will do: "Save as [filename]"
#        '''
#        if not self.mainModel:
#            return
#        self.mainModel.save_compartments(self.compartments, filename)
    
    
    
    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)
    
    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.compartments)):
            return None
        
        compartment = self.compartments[index.row()].Item
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.NAME:
                return compartment.getName()
            if column == COLUMN.ID:
                return compartment.getId()
            if column == COLUMN.COMPARTMENTTYPE:
                return compartment.getCompartmentType()
            if column == COLUMN.SPATIALDIMENSIONS:
                return compartment.getSpatialDimensions()
            if column == COLUMN.SIZE:
                return compartment.getSize()
            if column == COLUMN.UNITS:
                return compartment.getUnits()
            if column == COLUMN.OUTSIDE:
                return compartment.getOutside()
        
        return None
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == COLUMN.NAME:
                return "Name"
            if section == COLUMN.ID:
                return "ID"
            if section == COLUMN.COMPARTMENTTYPE:
                return "Compartment Type"
            if section == COLUMN.SPATIALDIMENSIONS:
                return "Spatial Dimensions"
            if section == COLUMN.SIZE:
                return "Size"
            if section == COLUMN.UNITS:
                return "Units"
            if section == COLUMN.OUTSIDE:
                return "Outside"
            if section == COLUMN.CONSTANT:
                return "Constant"
        return None
    
    def rowCount(self, index = QModelIndex()):
        return len(self.compartments)
    
    def columnCount(self, index = QModelIndex()):
        return 8  # TODO: hard-coded... how to make this better?
    
    
      # methods necessary for editable models
      # flags()
      # setData()
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
    
    def setData(self, index, value, role = Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.compartments):
            compartment = self.compartments[index.row()].Item
            column = index.column()
            if column == COLUMN.NAME:
                compartment.setName(str(value))
            elif column == COLUMN.ID:
                compartment.setId(str(value))
            elif column == COLUMN.COMPARTMENTTYPE:
                compartment.setCompartmentType(str(value))
            elif column == COLUMN.SPATIALDIMENSIONS:
                compartment.setSpatialDimensions(int(value))  # TODO: Does not work. Why?
            elif column == COLUMN.SIZE:
                compartment.setSize(float(value))
            elif column == COLUMN.UNITS:
                compartment.setUnits(str(value))
            elif column == COLUMN.OUTSIDE:
                compartment.setOutside(str(value))
            elif column == COLUMN.CONSTANT:
                compartment.setConstant(bool(value))
            
            self.Dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    
    
      # methods necessary for adding/removing
      # insertRows()
      # removeRows()
    
    def insertRows(self, position, rows = 1, index = QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1) # mandatory Qt call
        
        for row in range(rows): # we don't take the actual row into account as the libSBML always appends at the end
            newCompartment = libsbml.Compartment()
            self.mainModel.SbmlModel.addCompartment(SBMLEntity(newCompartment))
        
        self.endInsertRows() # mandatory Qt call
        self.Dirty = True
        return True
    
    def removeRows(self, position, rows = 1, index = QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        
        for row in range(position, rows):
            compartment = self.compartments[row]
            self.mainModel.SbmlModel.removeCompartment(compartment)
        
        self.endRemoveRows()
        self.Dirty = True
        return True

