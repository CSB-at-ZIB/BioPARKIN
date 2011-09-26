
import logging
from PySide.QtCore import QAbstractTableModel, Signal, Qt, QModelIndex
from basics.helpers.enum import enum
from sbml_model.sbml_entities import SBMLEntity
from sbml_model import sbml_entities
import libsbml
from basics.helpers import typehelpers
import sbml_mainmodel


COLUMN = enum("COLUMN", "PROPERTY, VALUE")
COLUMN_COUNT = 2

#COMPARTMENT_ROW = enum('ROW', 'ID, NAME, COMPARTMENTTYPE, SPATIALDIMENSIONS, SIZE, UNITS, OUTSIDE, CONSTANT')
COMPARTMENT_ROW = enum('ROW', 'ID, NAME, SIZE')
COMPARTMENT_ROW_COUNT = 3

#SPECIES_ROW = enum("ROW", "ID, NAME, SPECIESTYPE, COMPARTMENT, INITIALQUANTITY, SUBSTANCEUNITS, QUANTITYTYPE, CONSTANT, BC")
SPECIES_ROW = enum("ROW", "ID, NAME, COMPARTMENT, INITIALQUANTITY, SUBSTANCEUNITS, QUANTITYTYPE, CONSTANT, BC")
SPECIES_ROW_COUNT = 8

REACTION_ROW = enum('ROW', 'ID, NAME, REVERSIBLE, REACTANTS, PRODUCTS, MODIFIERS, MATH')
REACTION_ROW_COUNT = 7
PARAMETER_ROW = enum('ROW', 'ID, NAME, VALUE, UNITS, CONSTANT, SCOPE')
PARAMETER_ROW_COUNT = 6
RULE_ROW = enum('ROW', 'ID, NAME, TYPE, MATH, VARIABLE, VARIABLETYPE')
RULE_ROW_COUNT = 6
EVENT_ROW = enum('ROW', 'ID, NAME, TARGET, EXPRESSION, TRIGGEREXPRESSION, DELAYED, DELAYEXPRESSION')
EVENT_ROW_COUNT = 7

QUANTITY_CONCENTRATION = "concentration"
QUANTITY_AMOUNT = "amount"

class SBMLEntityTableModel(QAbstractTableModel):
    """
    A table model wrapping a single SBMLEntity, allowing
    easy access to its properties.

    @param entity: The SBMLEntity to which to provide access to
    @type entity: SBMLEntity

    @since: 2010-04-09
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    structuralChange = Signal(SBMLEntity,int)

    def __init__(self, entity, mainModel):
        """
        Justs sets some instance variables.
        """
        if entity is None or not isinstance(entity, SBMLEntity):
            return
        super(SBMLEntityTableModel, self).__init__()

        self.entity = entity
        self.dataMode = entity.Type
        self.mainModel = mainModel

    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)


    def data(self, index, role=Qt.DisplayRole):
        if self.dataMode == sbml_entities.TYPE.COMPARTMENT:
            return self.dataCompartment(index, role)
        elif self.dataMode == sbml_entities.TYPE.SPECIES:
            return self.dataSpecies(index, role)
        elif self.dataMode == sbml_entities.TYPE.REACTION:
            return self.dataReaction(index, role)
        elif self.dataMode == sbml_entities.TYPE.PARAMETER:
            return self.dataParameter(index, role)
        elif self.dataMode == sbml_entities.TYPE.RULE:
            return self.dataRule(index, role)
        elif self.dataMode == sbml_entities.TYPE.EVENT:
            return self.dataEvent(index, role)


    def dataCompartment(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < COMPARTMENT_ROW_COUNT):
            return

        compartment = self.entity.Item
        if compartment is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == COMPARTMENT_ROW.ID:
                    return "ID"
                elif row == COMPARTMENT_ROW.NAME:
                    return "Name"
#                elif row == COMPARTMENT_ROW.COMPARTMENTTYPE:
#                    return "Compartment Type"
#                elif row == COMPARTMENT_ROW.SPATIALDIMENSIONS:
#                    return "Spatial Dimensions"
                elif row == COMPARTMENT_ROW.SIZE:
                    return "Size"
#                elif row == COMPARTMENT_ROW.UNITS:
#                    return "Units"
#                elif row == COMPARTMENT_ROW.OUTSIDE:
#                    return "Outside"
            elif column == COLUMN.VALUE:
                if row == COMPARTMENT_ROW.ID:
                    return compartment.getId()
                elif row == COMPARTMENT_ROW.NAME:
                    return compartment.getName()
#                elif row == COMPARTMENT_ROW.COMPARTMENTTYPE:
#                    return compartment.getCompartmentType()
#                elif row == COMPARTMENT_ROW.SPATIALDIMENSIONS:
#                    return compartment.getSpatialDimensions()
                elif row == COMPARTMENT_ROW.SIZE:
                    return compartment.getSize()
#                elif row == COMPARTMENT_ROW.UNITS:
#                    return compartment.getUnits()
#                elif row == COMPARTMENT_ROW.OUTSIDE:
#                    return compartment.getOutside()
        elif role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == COMPARTMENT_ROW.ID:
                    return compartment.getId()
                elif row == COMPARTMENT_ROW.NAME:
                    return compartment.getName()
#                elif row == COMPARTMENT_ROW.COMPARTMENTTYPE:
#                    return compartment.getCompartmentType()
#                elif row == COMPARTMENT_ROW.SPATIALDIMENSIONS:
#                    return compartment.getSpatialDimensions()
                elif row == COMPARTMENT_ROW.SIZE:
                    return compartment.getSize()
#                elif row == COMPARTMENT_ROW.UNITS:
#                    return compartment.getUnits()
#                elif row == COMPARTMENT_ROW.OUTSIDE:
#                    return compartment.getOutside()


    def dataSpecies(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < SPECIES_ROW_COUNT):
            return

        species = self.entity.Item
        if species is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == SPECIES_ROW.ID:
                    return "ID"
                elif row == SPECIES_ROW.NAME:
                    return "Name"
#                elif row == SPECIES_ROW.SPECIESTYPE:
#                    return "Species Type"
                elif row == SPECIES_ROW.COMPARTMENT:
                    return "Compartment"
                elif row == SPECIES_ROW.INITIALQUANTITY:
                    return "Initial Quantity"
                elif row == SPECIES_ROW.SUBSTANCEUNITS:
                    return "Unit"
                elif row == SPECIES_ROW.QUANTITYTYPE:
                    return "Quantity Type"
                elif row == SPECIES_ROW.CONSTANT:
                    return "Constant"
                elif row == SPECIES_ROW.BC:
                    return "Boundary Condition"
            elif column == COLUMN.VALUE:
                if row == SPECIES_ROW.NAME:
                    return species.getName()
                elif row == SPECIES_ROW.ID:
                    return species.getId()
#                elif row == SPECIES_ROW.SPECIESTYPE:
#                    return species.getSpeciesType()
                elif row == SPECIES_ROW.COMPARTMENT:
                    return species.getCompartment()
                elif row == SPECIES_ROW.INITIALQUANTITY:
                    return self.getInitialValue(species)
                elif row == SPECIES_ROW.SUBSTANCEUNITS:
                    return species.getSubstanceUnits()
                elif row == SPECIES_ROW.QUANTITYTYPE:
                    return self.getQuantityType(species)
                elif row == SPECIES_ROW.CONSTANT:
                    return species.getConstant()
                elif row == SPECIES_ROW.BC:
                    return species.getBoundaryCondition()

        elif role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == SPECIES_ROW.NAME:
                    return species.getName()
                elif row == SPECIES_ROW.ID:
                    return species.getId()
#                elif row == SPECIES_ROW.SPECIESTYPE:
#                    return species.getSpeciesType()
                elif row == SPECIES_ROW.COMPARTMENT:
                    return species.getCompartment()
                elif row == SPECIES_ROW.INITIALQUANTITY:
                    return self.getInitialValue(species)
                elif row == SPECIES_ROW.SUBSTANCEUNITS:
                    return species.getSubstanceUnits()
                elif row == SPECIES_ROW.QUANTITYTYPE:
                    return self.getQuantityType(species)
                elif row == SPECIES_ROW.CONSTANT:
                    return species.getConstant()
                elif row == SPECIES_ROW.BC:
                    return species.getBoundaryCondition()

        elif role == Qt.StatusTipRole or role == Qt.ToolTipRole:
                if row == SPECIES_ROW.QUANTITYTYPE:
                    return "Write either 'Amount' or 'Concentration' to change the quantity type. (Typing 'a' and 'c' also works.)"


    def getReactionMath(self, reaction):
        try:
            kineticLaw = reaction.getKineticLaw()
            mathNode = kineticLaw.getMath()
            mathString = libsbml.formulaToString(mathNode)
            return mathString
        except: # most often happens when creating a new reaction that does not have a kinetic law
            return

    def dataReaction(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < REACTION_ROW_COUNT):
            return

        reaction = self.entity.Item
        if reaction is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == REACTION_ROW.ID:
                    return "ID"
                elif row == REACTION_ROW.NAME:
                    return "Name"
                elif row == REACTION_ROW.REVERSIBLE:
                    return "Reversible"
                elif row == REACTION_ROW.REACTANTS:
                    return "Reactants"
                elif row == REACTION_ROW.PRODUCTS:
                    return "Products"
                elif row == REACTION_ROW.MODIFIERS:
                    return "Modifiers"
                elif row == REACTION_ROW.MATH:
                    return "Math"
            elif column == COLUMN.VALUE:
                if row == REACTION_ROW.NAME:
                    return reaction.getName()
                elif row == REACTION_ROW.ID:
                    return reaction.getId()
                elif row == REACTION_ROW.REVERSIBLE:
                    return reaction.getReversible()
                elif row == REACTION_ROW.REACTANTS:
                    return self.getReactants(reaction)
                    #return "test"
                elif row == REACTION_ROW.PRODUCTS:
                    return self.getProducts(reaction)
                elif row == REACTION_ROW.MODIFIERS:
                    return self.getModifiers(reaction)
                elif row == REACTION_ROW.MATH:
                    return self.getReactionMath(reaction)
        if role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == REACTION_ROW.NAME:
                    return reaction.getName()
                elif row == REACTION_ROW.ID:
                    return reaction.getId()
                elif row == REACTION_ROW.REVERSIBLE:
                    return reaction.getReversible()
                elif row == REACTION_ROW.REACTANTS:
                    return self.getReactants(reaction)
                    #return "test"
                elif row == REACTION_ROW.PRODUCTS:
                    return self.getProducts(reaction)
                elif row == REACTION_ROW.MODIFIERS:
                    return self.getModifiers(reaction)
                elif row == REACTION_ROW.MATH:
                    return self.getReactionMath(reaction)


    def dataParameter(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < PARAMETER_ROW_COUNT):
            return

        parameter = self.entity.Item
        if parameter is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == PARAMETER_ROW.ID:
                    return "ID"
                elif row == PARAMETER_ROW.NAME:
                    return "Name"
                elif row == PARAMETER_ROW.VALUE:
                    return "Value"
                elif row == PARAMETER_ROW.UNITS:
                    return "Units"
                elif row == PARAMETER_ROW.CONSTANT:
                    return "Constant"
                elif row == PARAMETER_ROW.SCOPE:
                    return "Scope"
            elif column == COLUMN.VALUE:
                if row == PARAMETER_ROW.NAME:
                    return parameter.getName()
                elif row == PARAMETER_ROW.ID:
                    return parameter.getId()
                elif row == PARAMETER_ROW.VALUE:
                    return parameter.getValue()
                elif row == PARAMETER_ROW.UNITS:
                    return parameter.getUnits()
                elif row == PARAMETER_ROW.CONSTANT:
                    return parameter.getConstant()
                elif row == PARAMETER_ROW.SCOPE:
                    parent = parameter.getParentSBMLObject()
                    if parent:
                        grandpa = parent.getParentSBMLObject()
                        if type(grandpa) == libsbml.Model:
                            return "Global"
                        elif type(grandpa) == libsbml.KineticLaw:
                            reaction = grandpa.getParentSBMLObject()
                            return "%s" % reaction.getId()

                    return "N/A"
        if role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == PARAMETER_ROW.NAME:
                    return parameter.getName()
                elif row == PARAMETER_ROW.ID:
                    return parameter.getId()
                elif row == PARAMETER_ROW.VALUE:
                    return parameter.getValue()
                elif row == PARAMETER_ROW.UNITS:
                    return parameter.getUnits()
                elif row == PARAMETER_ROW.CONSTANT:
                    return parameter.getConstant()
                elif row == PARAMETER_ROW.SCOPE:
                    parent = parameter.getParentSBMLObject()
                    if parent:
                        grandpa = parent.getParentSBMLObject()
                        if type(grandpa) == libsbml.Model:
                            return "Global"
                        elif type(grandpa) == libsbml.KineticLaw:
                            reaction = grandpa.getParentSBMLObject()
                            return "%s" % reaction.getId()

                    return "N/A"


    def dataRule(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < RULE_ROW_COUNT):
            return

        rule = self.entity.Item
        if rule is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == RULE_ROW.ID:
                    return "ID"
                elif row == RULE_ROW.NAME:
                    return "Name"
                elif row == RULE_ROW.TYPE:
                    return "Type"
                elif row == RULE_ROW.MATH:
                    return "Formula"
                elif row == RULE_ROW.VARIABLE:
                    return "Variable"
                elif row == RULE_ROW.VARIABLETYPE:
                    return "Variable type"
            elif column == COLUMN.VALUE:
                if row == RULE_ROW.NAME:
                    return rule.getName()
                elif row == RULE_ROW.ID:
                    return rule.getId()
                elif row == RULE_ROW.TYPE:
                    return rule.getType()
                elif row == RULE_ROW.MATH:
                    return rule.getFormula()
                elif row == RULE_ROW.VARIABLE:
                    return rule.getVariable()
                elif row == RULE_ROW.VARIABLETYPE:
                    return "todo" #rule.getConstant()
        if role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == RULE_ROW.NAME:
                    return rule.getName()
                elif row == RULE_ROW.ID:
                    return rule.getId()
                elif row == RULE_ROW.TYPE:
                    return rule.getType()
                elif row == RULE_ROW.MATH:
                    return rule.getFormula()
                elif row == RULE_ROW.VARIABLE:
                    return rule.getVariable()
                elif row == RULE_ROW.VARIABLETYPE:
                    return "todo" #rule.getConstant()


    def dataEvent(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < EVENT_ROW_COUNT):
            return

        event = self.entity.Item
        if event is None:
            return

        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if column == COLUMN.PROPERTY:
                if row == EVENT_ROW.ID:
                    return "ID"
                elif row == EVENT_ROW.NAME:
                    return "Name"
                elif row == EVENT_ROW.TARGET:
                    return "Target"
                elif row == EVENT_ROW.EXPRESSION:
                    return "Expression"
                elif row == EVENT_ROW.TRIGGEREXPRESSION:
                    return "Trigger"
                elif row == EVENT_ROW.DELAYED:
                    return "Delayed"
                elif row == EVENT_ROW.DELAYEXPRESSION:
                    return "Delay Expression"
            elif column == COLUMN.VALUE:
                if row == EVENT_ROW.NAME:
                    return event.getName()
                elif row == EVENT_ROW.ID:
                    return event.getId()
                elif row == EVENT_ROW.TARGET:
                    # quick fix for now: shows the targets for all eventAssignments in one concatenated string
                    eventAssignments = event.getListOfEventAssignments()
                    targets = ""
                    for i, eventAssignment in enumerate(eventAssignments):
                        targetString = str(eventAssignment.getVariable())
                        targets += "Assignment %s: %s; " % (i + 1, targetString)
                    return targets
                elif row == EVENT_ROW.EXPRESSION:
                    # quick fix for now: shows the expressions for all eventAssignments in one concatenated string
                    eventAssignments = event.getListOfEventAssignments()
                    expressions = ""
                    for i, eventAssignment in enumerate(eventAssignments):
                        mathString = libsbml.formulaToString(eventAssignment.getMath())
                        expressions += "Assignment %s: %s; " % (i + 1, mathString)
                    return expressions
                elif row == EVENT_ROW.TRIGGEREXPRESSION:
                    trigger = event.getTrigger()
                    expression = libsbml.formulaToString(trigger.getMath())
                    return expression
                elif row == EVENT_ROW.DELAYED:
                    return "True" if event.isSetDelay() else "False"
                elif row == EVENT_ROW.DELAYEXPRESSION:
                    if event.isSetDelay():
                        delayObject = event.getDelay()
                        delay = libsbml.formulaToString(delayObject.getMath())
                        return delay
                    else:
                        return "No Delay"
        if role == Qt.EditRole:
            if column == COLUMN.VALUE:
                if row == EVENT_ROW.NAME:
                    return event.getName()
                elif row == EVENT_ROW.ID:
                    return event.getId()
                elif row == EVENT_ROW.TARGET:
                    # quick fix for now: shows the targets for all eventAssignments in one concatenated string
                    eventAssignments = event.getListOfEventAssignments()
                    targets = ""
                    for i, eventAssignment in enumerate(eventAssignments):
                        targetString = str(eventAssignment.getVariable())
                        targets += "Assignment %s: %s; " % (i + 1, targetString)
                    return targets
                elif row == EVENT_ROW.EXPRESSION:
                    # quick fix for now: shows the expressions for all eventAssignments in one concatenated string
                    eventAssignments = event.getListOfEventAssignments()
                    expressions = ""
                    for i, eventAssignment in enumerate(eventAssignments):
                        mathString = libsbml.formulaToString(eventAssignment.getMath())
                        expressions += "Assignment %s: %s; " % (i + 1, mathString)
                    return expressions
                elif row == EVENT_ROW.TRIGGEREXPRESSION:
                    trigger = event.getTrigger()
                    expression = libsbml.formulaToString(trigger.getMath())
                    return expression
                elif row == EVENT_ROW.DELAYED:
                    return "True" if event.isSetDelay() else "False"
                elif row == EVENT_ROW.DELAYEXPRESSION:
                    if event.isSetDelay():
                        delayObject = event.getDelay()
                        delay = libsbml.formulaToString(delayObject.getMath())
                        return delay
                    else:
                        return "No Delay"


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section == COLUMN.PROPERTY:
                return "Property"
            elif section == COLUMN.VALUE:
                return "Value"
        return None

    def rowCount(self, index=QModelIndex()):
        if self.dataMode == sbml_entities.TYPE.COMPARTMENT:
            return COMPARTMENT_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.SPECIES:
            return SPECIES_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.REACTION:
            return REACTION_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.PARAMETER:
            return PARAMETER_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.RULE:
            return RULE_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.EVENT:
            return EVENT_ROW_COUNT
        elif self.dataMode == sbml_entities.TYPE.NONE:
            return 0

    def columnCount(self, index=QModelIndex()):
        return COLUMN_COUNT


        # methods necessary for editable models
        # flags()
        # setData()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if self.dataMode == sbml_entities.TYPE.COMPARTMENT:
            return self.flagsGeneral(index)
        elif self.dataMode == sbml_entities.TYPE.SPECIES:
            return self.flagsGeneral(index)
        elif self.dataMode == sbml_entities.TYPE.REACTION:
            return self.flagsGeneral(index)    # not any more: only Reactions get a special flags method
        elif self.dataMode == sbml_entities.TYPE.PARAMETER:
            return self.flagsGeneral(index)
        elif self.dataMode == sbml_entities.TYPE.RULE:
            return self.flagsGeneral(index)
        elif self.dataMode == sbml_entities.TYPE.EVENT:
            return self.flagsGeneral(index)
        elif self.dataMode == sbml_entities.TYPE.NONE:
            return


    def flagsGeneral(self, index):
        row = index.row()
        if index.column() == COLUMN.VALUE and row == 1: # 1 is hardcoded; "Name" always has to be at 2nd position
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        else:
            #return Qt.ItemFlags(QAbstractTableModel.flags(self, index))
            return None


    def flagsReaction(self, index):
        row = index.row()
        if index.column() == COLUMN.VALUE and not (
        row == REACTION_ROW.REACTANTS    # previously: some rows are not editable
        or row == REACTION_ROW.PRODUCTS  # now: they can be edited (handled in setData)
        or row == REACTION_ROW.MODIFIERS):
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

        else:
            #return Qt.ItemFlags(QAbstractTableModel.flags(self, index))
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if self.dataMode == sbml_entities.TYPE.COMPARTMENT:
            return self.setDataCompartment(index, value, role)
        elif self.dataMode == sbml_entities.TYPE.SPECIES:
            return self.setDataSpecies(index, value, role)
        elif self.dataMode == sbml_entities.TYPE.REACTION:
            return self.setDataReaction(index, value, role)
        elif self.dataMode == sbml_entities.TYPE.PARAMETER:
            return self.setDataParameter(index, value, role)
        elif self.dataMode == sbml_entities.TYPE.RULE:
            return self.setDataRule(index, value, role)
        elif self.dataMode == sbml_entities.TYPE.EVENT:
            return self.setDataEvent(index, value, role)

    def setDataCompartment(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < COMPARTMENT_ROW_COUNT):
            return False

        compartment = self.entity.Item
        if compartment is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False    # should not happen; this column should not be editable
            elif column == COLUMN.VALUE:
                if row == COMPARTMENT_ROW.ID:
                    compartment.setId(str(value))
                elif row == COMPARTMENT_ROW.NAME:
                    compartment.setName(str(value))
                elif row == COMPARTMENT_ROW.COMPARTMENTTYPE:
                    compartment.setCompartmentType(str(value))
                elif row == COMPARTMENT_ROW.SPATIALDIMENSIONS:
                    compartment.setSpatialDimensions(int(value)) # should be a uint
                elif row == COMPARTMENT_ROW.SIZE:
                    compartment.setSize(float(value))
                elif row == COMPARTMENT_ROW.UNITS:
                    compartment.setUnits(str(value))
                elif row == COMPARTMENT_ROW.OUTSIDE:
                    compartment.setOutside(str(value))
#                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                self.dataChanged.emit(index, index)
                return True
        return False

    def setDataSpecies(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < SPECIES_ROW_COUNT):
            return False

        species = self.entity.Item
        if species is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False
            elif column == COLUMN.VALUE:
                if row == SPECIES_ROW.ID:
                    self.entity.setId(str(value))
                elif row == SPECIES_ROW.NAME:
                    species.setName(str(value))
                elif row == SPECIES_ROW.SPECIESTYPE:
                    species.setSpeciesType(str(value))
                elif row == SPECIES_ROW.COMPARTMENT:
                    species.setCompartment(str(value))
                elif row == SPECIES_ROW.INITIALQUANTITY:
                    self.setSpeciesInitialQuantity(species, value)
                elif row == SPECIES_ROW.SUBSTANCEUNITS:
                    species.setSubstanceUnits(str(value))
                elif row == SPECIES_ROW.QUANTITYTYPE:
                    self.setQuantityType(species, value)
                elif row == SPECIES_ROW.CONSTANT:
                    species.setConstant(typehelpers.stringToBool(value))
#                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                self.dataChanged.emit(index, index)
                return True
        return False


    def setDataReaction(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < REACTION_ROW_COUNT):
            return False

        reaction = self.entity.Item
        if reaction is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False
            elif column == COLUMN.VALUE:
                if row == REACTION_ROW.ID:
                    reaction.setId(str(value))
                elif row == REACTION_ROW.NAME:
                    reaction.setName(str(value))
                elif row == REACTION_ROW.REVERSIBLE:
                    reaction.setReversible(typehelpers.stringToBool(value))
                elif row == REACTION_ROW.REACTANTS:
                    success = self.entity.setReactants(str(value))
                    if success:
                        self.structuralChange.emit(self.entity, sbml_mainmodel.CHANGETYPE.CHANGE_REACTANTS)
                elif row == REACTION_ROW.PRODUCTS:
                    success = self.entity.setProducts(str(value))
                    if success:
                        self.structuralChange.emit(self.entity, sbml_mainmodel.CHANGETYPE.CHANGE_PRODUCTS)
                elif row == REACTION_ROW.MODIFIERS:
                    success = self.entity.setModifiers(str(value))
                    if success:
                        self.structuralChange.emit(self.entity, sbml_mainmodel.CHANGETYPE.CHANGE_MODIFIERS)
                elif row == REACTION_ROW.MATH:
                    try:
                        kineticLaw = reaction.getKineticLaw()
                        mathNode = libsbml.parseFormula(str(value))
                        if mathNode: # is None if expression is invalid (handy way of checking syntax)
                            kineticLaw.setMath(mathNode)
                    except:
                        logging.debug("Could not set math: %s (should be a valid SBML math string)" % value)

#                self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)

                self.dataChanged.emit(index, index)
                return True
        return False


    def setDataParameter(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < PARAMETER_ROW_COUNT):
            return False

        parameter = self.entity.Item
        if parameter is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False    # should not happen; this column should not be editable
            elif column == COLUMN.VALUE:
                if row == PARAMETER_ROW.ID:
                    parameter.setId(str(value))
                elif row == PARAMETER_ROW.NAME:
                    parameter.setName(str(value))
                elif row == PARAMETER_ROW.VALUE:
                    parameter.setValue(float(value))
                elif row == PARAMETER_ROW.UNITS:
                    parameter.setUnits(str(value))
                elif row == PARAMETER_ROW.CONSTANT:
                    parameter.setConstant(typehelpers.stringToBool(value))

#                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                self.dataChanged.emit(index, index)
                return True
        return False


    def setDataRule(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < RULE_ROW_COUNT):
            return False

        rule = self.entity.Item
        if rule is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False    # should not happen; this column should not be editable
            elif column == COLUMN.VALUE:
                if row == RULE_ROW.ID:
                    rule.setId(str(value))
                elif row == RULE_ROW.NAME:
                    rule.setName(str(value))
                elif row == RULE_ROW.TYPE:
                    #rule.setValue(float(value))
                    pass # TODO 
                elif row == RULE_ROW.MATH:
                    rule.setFormula(str(value))
                elif row == RULE_ROW.VARIABLE:
                    rule.setVariable(str(value))
                elif row == RULE_ROW.VARIABLETYPE:
                    #rule.setConstant(typehelpers.stringToBool(value))
                    pass # TODO

#                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                self.dataChanged.emit(index, index)
                return True
        return False


    def setDataEvent(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not (0 <= index.row() < EVENT_ROW_COUNT):
            return False

        event = self.entity.Item
        if event is None:
            return False

        row = index.row()
        column = index.column()
        if role == Qt.EditRole:
            if column == COLUMN.PROPERTY:
                return False    # should not happen; this column should not be editable
            elif column == COLUMN.VALUE:
                if row == EVENT_ROW.ID:
                    event.setId(str(value))
                elif row == EVENT_ROW.NAME:
                    event.setName(str(value))
                elif row == EVENT_ROW.TARGET:
                    # for now, only single targets (=simple string) are supported
                    try:
                        eventAssignment = event.getEventAssignment(0)
                        eventAssignment.setVariable(str(value))
                    except Exception, e:
                        logging.debug(
                            "SbmlEntityTableModel.setDataEvent(): Can't set the event target %s for event %s. Error: %s" % (
                            value, event.getId(), e))
                elif row == EVENT_ROW.EXPRESSION:
                    # for now, only single targets (=simple string) are supported
                    try:
                        eventAssignment = event.getEventAssignment(0)
                        expression = libsbml.parseFormula(str(value))
                        eventAssignment.setMath(expression)
                    except Exception, e:
                        logging.debug(
                            "SbmlEntityTableModel.setDataEvent(): Can't set the event expression %s for event %s. Error: %s" % (
                            value, event.getId(), e))
                elif row == EVENT_ROW.TRIGGEREXPRESSION:
                    try:
                        trigger = event.getTrigger()
                        expression = libsbml.parseFormula(str(value))
                        trigger.setMath(expression)
                    except Exception, e:
                        logging.debug(
                            "SbmlEntityTableModel.setDataEvent(): Can't set the trigger expression %s for event %s. Error: %s" % (
                            value, event.getId(), e))
                elif row == EVENT_ROW.DELAYED:
                    try:
                        event.setDelay(bool(value))
                    except Exception, e:
                        logging.debug(
                            "SbmlEntityTableModel.setDataEvent(): Can't set the delay status %s for event %s. Error: %s" % (
                            value, event.getId(), e))
                elif row == EVENT_ROW.DELAYEXPRESSION:
                    if event.isSetDelay():
                        delayObject = event.getDelay()
                    else: # create new delay object
                        delayObject = libsbml.Delay(2, 4)    # level 2 version 4 SBML object
                        #TODO: has to be created with all needed attributes; ID, name, etc.

                    delayMath = libsbml.parseFormula(str(value))
                    delayObject.setMath(delayMath)

#                self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                self.dataChanged.emit(index, index)
                return True
        return False


    # helper methods

    def getReactants(self, reaction):
        '''
        Returns a string of the reactants of the given Reaction.
        
        @param reaction: a libSBML Reaction
        @type reaction: Reaction
        
        @return: a string of the reactants of the given Reaction.
        @rtype: str
        '''
        if reaction is None:
            return
        reactantReferences = reaction.getListOfReactants()

        reactantIDs = []

        for ref in reactantReferences:
            reactantID = ref.getSpecies()
            #reactantIDs.append(reactant.getId())
            reactantIDs.append(reactantID)

        return ", ".join(reactantIDs)

    def getProducts(self, reaction):
        '''
        Returns a string of the products of the given Reaction.
        
        @param reaction: a libSBML Reaction
        @type reaction: Reaction
        
        @return: a string of the products of the given Reaction.
        @rtype: str
        '''
        if reaction is None:
            return
        productReferences = reaction.getListOfProducts()

        productIDs = []

        for ref in productReferences:
            productID = ref.getSpecies()
            #productIDs.append(reactant.getId())
            productIDs.append(productID)

        return ", ".join(productIDs)

    def getModifiers(self, reaction):
        '''
        Returns a string of the modifiers of the given Reaction.
        
        @param reaction: a libSBML Reaction
        @type reaction: Reaction
        
        @return: a string of the modifiers of the given Reaction.
        @rtype: str
        '''
        numModifiers = reaction.getNumModifiers()
        modifiers = []
        for i in range(numModifiers):
            modifiers.append(reaction.getModifier(i).getSpecies())
        return ", ".join(modifiers)

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
            #return "%f (concentration)" % initialConcentration
            return initialConcentration

        elif species.isSetInitialAmount():
            initialAmount = species.getInitialAmount()
            #return "%f (amount)" % initialAmount
            return initialAmount

    def getQuantityType(self, species):
        if species.isSetInitialConcentration():
            return "Concentration"
        elif species.isSetInitialAmount():
            return "Amount"

    def setQuantityType(self, species, type):
        #if type == QUANTITY_AMOUNT and species.isSetInitialConcentration():
        if QUANTITY_AMOUNT.startswith(str(type).lower()) and species.isSetInitialConcentration():
            value = species.getInitialConcentration()
            species.unsetInitialConcentration()
            species.setInitialAmount(value)
        #elif type == QUANTITY_CONCENTRATION and species.isSetInitialAmount():
        elif QUANTITY_CONCENTRATION.startswith(str(type).lower()) and species.isSetInitialAmount():
            value = species.getInitialAmount()
            species.unsetInitialAmount()
            species.setInitialConcentration(value)

    def setSpeciesInitialQuantity(self, species, quantity):
        if species.isSetInitialConcentration():
            species.setInitialConcentration(float(quantity))
        elif species.isSetInitialAmount():
            species.setInitialAmount(float(quantity))
