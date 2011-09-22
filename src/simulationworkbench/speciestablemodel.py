"""
Created on Jun 25, 2010

@author: bzfwadem
"""
#from PySide.QtCore import *
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL
from basics.helpers import enum

COLUMN = enum.enum("ROW",
                   "NUMBER, ID, NAME, COMPARTMENT, INITIALQUANTITY, UNIT, SCALE, QUANTITYTYPE, ISCONSTANT, ISBC, COMPUTESENSITIVITY") # this effectively orders the columns
NUM_COLUMNS = 11 # keep in sync with COLUMN!

class SpeciesTableModel(QAbstractTableModel):
    """
    Model for filling the Species table of the Simulation
    Workbench with data.

    @param speciesList: List of SBML entities that wrap libSBML Species objects
    @type speciesList: []

    @since: 2010-06-25

    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, speciesList):
        """
        Simple constructor, setting some instance variables.
        """
        super(SpeciesTableModel, self).__init__()
        self.speciesList = speciesList

        self.Dirty = False # True if something has been changed

    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.speciesList)):
            return None

        sbmlEntity = self.speciesList[index.row()]
        species = sbmlEntity.Item
        column = index.column()

        if role == Qt.TextAlignmentRole:
            if column == COLUMN.NUMBER:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignCenter

        if role == Qt.DisplayRole:
            if column == COLUMN.NUMBER:
                maxWidth = len(str(len(self.speciesList))) + 1
                return "%s " % (str(index.row() + 1).rjust(maxWidth))
            elif column == COLUMN.ID:
                return species.getId()
            elif column == COLUMN.NAME:
                return species.getName()
            elif column == COLUMN.COMPARTMENT:
                return species.getCompartment()
            elif column == COLUMN.INITIALQUANTITY:
                return self.getInitialValue(species)
            elif column == COLUMN.SCALE:
                scale = sbmlEntity.getThreshold()
                if scale:
                    return scale
                else:
                    return "N/A"
            elif column == COLUMN.UNIT:
                unit = species.getSubstanceUnits()
                if unit is None or unit == "":
                    return "N/A"
                else:
                    return unit
            elif column == COLUMN.QUANTITYTYPE:
                return self.getQuantityType(species)
            elif column == COLUMN.ISCONSTANT:
#                return species.getConstant()
                return  # don't display true/false strings
            elif column == COLUMN.ISBC:
#                return species.getBoundaryCondition()
                return # don't display true/false strings

        if role == Qt.CheckStateRole:
            if column == COLUMN.ISCONSTANT:
                return Qt.Checked if species.getConstant() else Qt.Unchecked
            elif column == COLUMN.ISBC:
                return Qt.Checked if species.getBoundaryCondition() else Qt.Unchecked
            elif column == COLUMN.COMPUTESENSITIVITY:
                return Qt.Checked if sbmlEntity.getComputeSensitivity() else Qt.Unchecked
            else:
                return None

        if role == Qt.EditRole:
            if column == COLUMN.INITIALQUANTITY:
                return str(self.getInitialValue(species))
            elif column == COLUMN.SCALE:
                return str(sbmlEntity.getThreshold())
            else:
                return None

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == COLUMN.NUMBER:
                return "#"
            elif section == COLUMN.ID:
                return "ID"
            elif section == COLUMN.NAME:
                return "Name"
            elif section == COLUMN.COMPARTMENT:
                return "Compartment"
            elif section == COLUMN.INITIALQUANTITY:
                return "Initial Quantity"
            elif section == COLUMN.UNIT:
                return "Unit"
            elif section == COLUMN.SCALE:
                return "Threshold"
            elif section == COLUMN.QUANTITYTYPE:
                return "Quantity Type"
            elif section == COLUMN.ISCONSTANT:
                return "Constant"
            elif section == COLUMN.ISBC:
                return "Boundary Condition"
            elif section == COLUMN.COMPUTESENSITIVITY:
                return "Compute Sensitivity"
        return None

    def rowCount(self, index=QModelIndex()):
        count = 0
        if not self.speciesList:
            return 0
        for speciesEntity in self.speciesList:
            if not speciesEntity.Item.getId().startswith("helper"):
                count = count + 1
        return count
        #return len(self.speciesList)

    def columnCount(self, index=QModelIndex()):
        return NUM_COLUMNS


    # methods necessary for editable models
    # flags()
    # setData()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == COLUMN.ISCONSTANT:
            return (Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
                    #| Qt.ItemIsSelectable
            )
            
        elif index.column() == COLUMN.ISBC or index.column() == COLUMN.COMPUTESENSITIVITY:
            return (Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
            )

        elif index.column() == (COLUMN.INITIALQUANTITY) or index.column() == (COLUMN.SCALE):
            return (Qt.ItemIsEnabled
                    | Qt.ItemIsEditable
            )

        return Qt.NoItemFlags

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.speciesList):
            sbmlEntity = self.speciesList[index.row()]
            species = sbmlEntity.Item
            column = index.column()

            if role == Qt.EditRole:
                if column == COLUMN.INITIALQUANTITY:
                    try:
                        self.setInitialValue(species, float(value))
                    except:
                        return False
                elif column == COLUMN.SCALE:
                    try:
                        sbmlEntity.setThreshold(float(value))
                    except:
                        return False

            if role == Qt.CheckStateRole:
                isChecked = value == Qt.Checked
                if column == COLUMN.ISCONSTANT:
                    species.setConstant(isChecked)
                elif column == COLUMN.ISBC:
                    species.setBoundaryCondition(isChecked)
                elif column == COLUMN.COMPUTESENSITIVITY:
                    sbmlEntity.setComputeSensitivity(isChecked)

            self.Dirty = True
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True

        return False


    ### HELPER METHODS ####

    def getInitialValue(self, species):
        '''
        Returns the initial value of a Species which can be either defined
        as a concentration or as an amount.
        
        @param species: A libSBML Species
        @type species: Species
        
        @return: The initial value
        @rtype: str
        '''
        if species.isSetInitialConcentration():
            initialConcentration = species.getInitialConcentration()
            return initialConcentration

        elif species.isSetInitialAmount():
            initialAmount = species.getInitialAmount()
            return initialAmount


    def setInitialValue(self, species, value):
        if species.isSetInitialConcentration():
            species.setInitialConcentration(value)
        elif species.isSetInitialAmount():
            species.setInitialAmount(value)

    def getQuantityType(self, species):
        if species.isSetInitialConcentration():
            return "Concentration"
        elif species.isSetInitialAmount():
            return "Amount"


    def selectAllSensitivity(self, doSelect):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for speciesEntity in self.speciesList:
            speciesEntity.setComputeSensitivity(doSelect)

        self.emit(SIGNAL("layoutChanged()"))

    def invertSelectionSensitivity(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for speciesEntity in self.speciesList:
            speciesEntity.setComputeSensitivity(not speciesEntity.getComputeSensitivity())

        self.emit(SIGNAL("layoutChanged()"))