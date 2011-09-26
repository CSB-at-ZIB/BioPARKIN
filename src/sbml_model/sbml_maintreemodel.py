'''
Created on Apr 1, 2010

@author: bzfwadem
'''

#from PySide.QtCore import *
from PySide.QtCore import QAbstractItemModel, SIGNAL, Qt, QModelIndex, Signal, QObject

import libsbml
##
#import logging
##
from basics.helpers import enum
from sbml_model import sbml_entities
from sbml_model.definitions import CHANGETYPE
from sbml_model.sbml_entities import SBMLEntity


COLUMN = enum.enum('ROW', 'ID, NAME') # this effectively orders the columns

class SBMLMainTreeModel(QAbstractItemModel):
    '''
    This model wraps a libsbml model completely. The information about the type
    of individual entities (Species, Reaction, ...) is encoded in 
    the Type property of any SBMLEntity. 
    
    This model only provides two columns: ID and Name.
    Any detailed information (that differs for different types of entities
    is provided by the EntityTableModel that is bound to a table view 
    (EntityTableView).
    
    Idea: Views (e.g. TableViews) that should show only part of the model
    (e.g. only Species) use an intermediate QAbstractProxyModel.
    
    @param mainModel: The main model which wraps a SBML file
    @type mainModel: MainModel
    
    @since: 2010-04-01
    
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    structuralChange = Signal(SBMLEntity,int)

    def __init__(self, mainModel=None):
        '''
        Just sets instance variables, obtained from the main model.
        '''
        super(SBMLMainTreeModel, self).__init__(mainModel)
        self.MainModel = mainModel
        self.root = self.MainModel.SbmlModel
        self.CompartmentWrapper = self.MainModel.CompartmentWrapper
        self.SpeciesWrapper = self.MainModel.SpeciesWrapper
        self.ReactionWrapper = self.MainModel.ReactionWrapper
        self.ParameterWrapper = self.MainModel.ParameterWrapper
        self.RateRuleWrapper = self.MainModel.RateRuleWrapper
#        self.AlgebraicRuleWrapper = self.MainModel.AlgebraicRuleWrapper
        self.AssignmentRuleWrapper = self.MainModel.AssignmentRuleWrapper
        self.EventWrapper = self.MainModel.EventsWrapper
        #self.rootChildren= [self.CompartmentWrapper, self.SpeciesWrapper, self.ReactionWrapper]
        #self.reset()
#        self.modelIndexToEntityMap = {}

        self._connectToSignals(self.CompartmentWrapper)
        self._connectToSignals(self.SpeciesWrapper)
        self._connectToSignals(self.ReactionWrapper)
        self._connectToSignals(self.ParameterWrapper)
        self._connectToSignals(self.RateRuleWrapper)
#        self._connectToSignals(self.AlgebraicRuleWrapper)
        self._connectToSignals(self.AssignmentRuleWrapper)
        self._connectToSignals(self.EventWrapper)

        
        if self.MainModel:
            self.MainModel.structuralChange.connect(self.mainModelChanged)
        
    
    #@Slot("structuralChange(SBMLEntity)")
    def mainModelChanged(self, entity, changeType):
        '''
        We disregard the information about what has changed in which way.
        '''
        #self.modelIndexToEntityMap = {}
        #super(SBMLMainTreeModel, self).reset()  #reset may be a bit over-the-top

        # if something has been removed, we need to update references
        if changeType == CHANGETYPE.REMOVE: 
#            if self.modelIndexToEntityMap.has_key(entity):
#                index = self.modelIndexToEntityMap[entity]
#                self.modelIndexToEntityMap.pop(entity)
#                self.modelIndexToEntityMap.pop(index)
#            self.modelIndexToEntityMap = {}
            super(SBMLMainTreeModel, self).reset()

        self.layoutChanged.emit()

    def getMainModel(self):
        return self.MainModel

    def rowCount(self, parentIndex):
        '''
        Returns the number of rows.
        
        @requires: number of rows
        @rtype: int
        '''
        parent = self.nodeFromIndex(parentIndex)
        
        if parent is None:
            return 0
        return parent.getChildrenCount()


    def columnCount(self, nodeIndex):
        '''
        Returns the number of columns.
        
        @return: number of columns
        @rtype: int
        
        @todo: Make this non-hardcoded
        '''
        return 2


    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return int(Qt.AlignTop|Qt.AlignLeft)
        if role != Qt.DisplayRole and role != Qt.UserRole:
            return None
        node = self.nodeFromIndex(index)
        if node is None:
            return 
        
#        # save references
#        if not node in self.modelIndexToEntityMap:
#            self.modelIndexToEntityMap[node] = index
#        if not index.internalPointer() in self.modelIndexToEntityMap:
#            self.modelIndexToEntityMap[index.internalPointer()] = node


        # A word about the Qt.UserRole: It's used for "sorting".
        # Whenever this role is queries (by the QSortFilterProxyModel)
        # we return "None". This way, the proxy has no sort info and
        # does not sort these items whatsoever... which is exactly
        # what we want.

        
        assert node is not None
        if node is self.root:
            return "ModelTest"
        elif node == self.SpeciesWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Species"
        elif node == self.CompartmentWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Compartments"
        elif node == self.ReactionWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Reactions"
        elif node == self.ParameterWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Parameters"
        elif node == self.RateRuleWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Rate Rules"
#        elif node == self.AlgebraicRuleWrapper:
#            if role == Qt.UserRole: # used for sorting; set fixed sorting
#                return
#            if index.column() == COLUMN.ID:
#                return "Algebraic Rules"
        elif node == self.AssignmentRuleWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return "Assignment Rules"
        elif node == self.EventWrapper:
            if role == Qt.UserRole: # used for sorting; set fixed sorting
                return
            if index.column() == COLUMN.ID:
                return node.getLabel()
        
        elif node.Item is not None and isinstance(node.Item, libsbml.Compartment):
#            if index.column() == COLUMN.TYPE:
#                return "Compartment"
            if index.column() == COLUMN.ID:
                return node.Item.getId()
            if index.column() == COLUMN.NAME:
                return node.Item.getName()
        elif node.Item is not None and isinstance(node.Item, libsbml.Species):
#            if index.column() == COLUMN.TYPE:
#                return "Species"
            if index.column() == COLUMN.ID:
                return node.Item.getId()
            if index.column() == COLUMN.NAME:
                return node.Item.getName()
        elif node.Item is not None and isinstance(node.Item, libsbml.Reaction):
#            if index.column() == COLUMN.TYPE:
#                return "Reaction"
            if index.column() == COLUMN.ID:
                return node.Item.getId()
            if index.column() == COLUMN.NAME:
                return node.Item.getName()
            
        elif node.Item is not None and isinstance(node.Item, libsbml.Parameter):
            if index.column() == COLUMN.ID:
                return node.Item.getId()
            if index.column() == COLUMN.NAME:
                return node.Item.getName()
            
        elif node.Item is not None and isinstance(node.Item, libsbml.Rule):
            if index.column() == COLUMN.ID:
                return node.Item.getId()
            if index.column() == COLUMN.NAME:
                return node.Item.getName()
        else:
#            if index.column() == COLUMN.TYPE:
#                return "TypeTest"
            if index.column() == COLUMN.ID:
                if node.Item:
                    return node.Item.getId()
                else:
                    return None
            if index.column() == COLUMN.NAME:
                if node.Item:
                    return node.Item.getName()
                else:
                    return None


    def headerData(self, section, orientation, role):
        if (orientation == Qt.Horizontal and
            role == Qt.DisplayRole):
#            if section == COLUMN.TYPE:
#                return "Type"
            if section == COLUMN.ID:
                return "ID"
            if section == COLUMN.NAME:
                return "Name"
        return None

    def index(self, row, column, parentIndex):
        if row < 0 or column < 0:
            return QModelIndex()

        # we are only interested in the first (0th) column
        if parentIndex.isValid() and parentIndex.column() != 0:
            return QModelIndex()
        
        parent = self.nodeFromIndex(parentIndex)
        child = parent.getChild(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QModelIndex()
        
        

    def parent(self, childIndex):
        if not childIndex.isValid():
            return QModelIndex()
        
        child = self.nodeFromIndex(childIndex)        
        parent = child.Parent
        
        if parent is self.root:
            return QModelIndex()

        row = parent.getRowOfChild(child)
#        if row:
        return self.createIndex(row, 0, parent)
#        else:
#            return QModelIndex()


    def nodeFromIndex(self, index):
        return (index.internalPointer() if index.isValid() else self.root)
#        return (index.internalPointer() if index.isValid() else None)
        
    def entityHasChanged(self, entity=None):
        '''
        Is called, when an entity has changed.
        Creates the correct "QModelIndex"es and emits
        a Signal containing them.
        
        @param entity: The entity that has changed.
        @type entity: SBMLEntity
        '''
        if not entity:
            self.dataChanged.emit(QModelIndex(), QModelIndex())
        else:
            row = entity.Parent.getRowOfChild(entity)
            index1 = self.createIndex(row, 0, entity)
            index2 = self.createIndex(row, 1, entity)
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index1, index2)
        
    
      # methods necessary for editable models
      # flags()
      # setData()
    
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        try:
            node = self.nodeFromIndex(index)
            if node.Type is not sbml_entities.TYPE.NONE:
                return Qt.ItemFlags(QAbstractItemModel.flags(self, index) | Qt.ItemIsEditable)  # editable item
        except:
            pass
        
        return Qt.ItemFlags(QAbstractItemModel.flags(self, index))  # non-editable item
        
    
    def setData(self, index, value, role = Qt.EditRole):
        if not index.isValid():
            return False
        
        node = self.nodeFromIndex(index)
        if node is None:
            return False
        
        sbmlEntity = node.Item
        if sbmlEntity is None:
            return False
        
        column = index.column()
        if column == COLUMN.ID:
            sbmlEntity.setId(str(value))
        elif column == COLUMN.NAME:
            sbmlEntity.setName(str(value))
        
        self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
        return True


    def structuralEntityChange(self, entity, type):
        '''
        This is called by the EntityTableView whenever an individual EntityModel makes
        a structural change (e.g. changes Reactants/Products of a Reaction).
        '''
        self.structuralChange.emit(entity,type)
    
    def _connectToSignals(self, sbmlEntity):
        sbmlEntity.hasChanged.connect(self.entityHasChanged)
        numChildren = sbmlEntity.getChildrenCount()
        if numChildren > 0:
           for i in xrange(numChildren):
               self._connectToSignals(sbmlEntity.getChild(i))
