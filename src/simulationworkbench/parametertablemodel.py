import logging
#from PySide.QtCore import *
from PySide.QtCore import QAbstractTableModel, Qt, QModelIndex, SIGNAL
from basics.helpers import enum
import libsbml

#COLUMN = enum.enum("ROW", "NUMBER, SCOPE, ID, NAME, INITIALVALUE, UNIT, SCALE, ISCONSTANT, COMPUTESENSITIVITY, ESTIMATE") # this effectively orders the columns
COLUMN = enum.enum("ROW", "NUMBER, SCOPE, ID, NAME, INITIALVALUE, SCALE, COMPUTESENSITIVITY, ESTIMATE") # this effectively orders the columns
NUM_COLUMNS = 8 # keep in sync with COLUMN!

class ParameterTableModel(QAbstractTableModel):
    """
    Fills the Parameter tab of the Simulation Workbench with data.

    @param listOfParams: List of sbmlEntities wrapping libSBML Parameter objects
    @type listOfParams: []

    @since: 2010-06-25
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, listOfParams, mainModel):
        """
        Simple Constructor, just setting up some instance variables.
        """
        super(ParameterTableModel, self).__init__()
        self.paramList = listOfParams
        #self.paramSets = listOfParameterSets
        self.mainModel = mainModel

        # per default, all parameters are checked so that sensitivities are computed
        self.paramsToSensitivityMap = {}
        self.paramToEstimateMap = {}

        if self.paramList:
            for param in self.paramList:
                #self.paramsToSensitivityMap[param.Item] = True
                self.paramsToSensitivityMap[param] = True
                self.paramToEstimateMap[param] = False
        else:
            self.paramList = []

        #self.paramSets.changed.connect(self.paramSetsChanged)
        #self.getListOfParameterSets
        self.mainModel.ListOfParameterSets.changed.connect(self.paramSetsChanged)

        self.Dirty = False # True if something has been changed

    # methods necessary for read-only models
    # experimentalData()
    # rowCount()
    # columnCount()
    # headerData() (almost always)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.paramList)):
            return None

        sbmlEntity = self.paramList[index.row()]
        param = sbmlEntity.Item
        column = index.column()
        
        if role == Qt.TextAlignmentRole:
            if column == COLUMN.NUMBER:
                return Qt.AlignRight | Qt.AlignVCenter
            else:
                return Qt.AlignCenter

        if role == Qt.DisplayRole:
            if column == COLUMN.NUMBER:
                maxWidth = len(str(len(self.paramList))) + 1
                return "%s " % (str(index.row() + 1).rjust(maxWidth))
            elif column == COLUMN.ID:
                return param.getId()
            elif column == COLUMN.NAME:
                return param.getName()
            elif column == COLUMN.INITIALVALUE:
                #return param.getValue()
                if not param.getConstant():
                    return "Assignment Rule"
                
                combinedId = sbmlEntity.getCombinedId()
                #                if self.getActiveSet():
                #                    return self.getActiveSet()[combinedId].getValue()
                #                else:
                #                    return "N/A"
                try:
                    return self.getActiveSet()[combinedId].getValue()
                except:
                    return "N/A"
            elif column == COLUMN.SCALE:
                value = sbmlEntity.getThreshold()
                if value:
                    return value
                else:
                    return "N/A"

#            elif column == COLUMN.UNIT:
#                unit = param.getUnits()
#                if unit is None or unit == "":
#                    return "N/A"
#                else:
#                    return unit
#            elif column == COLUMN.ISCONSTANT:
#                return param.getConstant()
            elif column == COLUMN.SCOPE:
                parent = param.getParentSBMLObject()
                if parent:
                    grandpa = parent.getParentSBMLObject()
                    if type(grandpa) == libsbml.Model:
                        return "Global"
                    elif type(grandpa) == libsbml.KineticLaw:
                        reaction = grandpa.getParentSBMLObject()
                        return "%s" % reaction.getId()

                return "N/A"

        if role == Qt.CheckStateRole:
            if column == COLUMN.ID:
                return None
            elif column == COLUMN.NAME:
                return None
            elif column == COLUMN.INITIALVALUE:
                return None
#            elif column == COLUMN.UNIT:
#                return None
#            elif column == COLUMN.ISCONSTANT:
#                return Qt.Checked if param.getConstant() else Qt.Unchecked
            elif column == COLUMN.SCOPE:
                return None
            elif column == COLUMN.COMPUTESENSITIVITY:
                #return Qt.Checked if self.paramsToSensitivityMap[param] else Qt.Unchecked
                return Qt.Checked if self.paramsToSensitivityMap[sbmlEntity] else Qt.Unchecked
            elif column == COLUMN.ESTIMATE:
                return Qt.Checked if self.paramToEstimateMap[sbmlEntity] else Qt.Unchecked

        if role == Qt.EditRole:
            if column == COLUMN.INITIALVALUE:
                #return param.getValue()
                combinedId = sbmlEntity.getCombinedId()
                #                if self.getActiveSet():
                #                    return self.getActiveSet()[combinedId].getValue()
                #                else:
                #                    return "N/A"
                try:
                    return str(self.getActiveSet()[combinedId].getValue())
                except:
                    return None
            elif column == COLUMN.SCALE:
                return str(sbmlEntity.getThreshold())
            elif column == COLUMN.NAME:
                return param.getName()
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
            elif section == COLUMN.INITIALVALUE:
                if self.getActiveSet():
                    return "Value (from Set %s)" % self.getActiveSet().getId()
                else:
                    return "No active Set!"
#            elif section == COLUMN.UNIT:
#                return "Unit"
            elif section == COLUMN.SCALE:
                return "Threshold"
#            elif section == COLUMN.ISCONSTANT:
#                return "Constant"
            elif section == COLUMN.SCOPE:
                return "Scope"
            elif section == COLUMN.COMPUTESENSITIVITY:
                return "Compute Sensitivity"
            elif section == COLUMN.ESTIMATE:
                return "Estimate Value"
        return None

    def rowCount(self, index=QModelIndex()):
        return len(self.paramList)

    def columnCount(self, index=QModelIndex()):
        return NUM_COLUMNS


    # methods necessary for editable models
    # flags()
    # setData()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        #if index.column() == COLUMN.ISCONSTANT or index.column() in (COLUMN.COMPUTESENSITIVITY, COLUMN.ESTIMATE):
        if index.column() in (COLUMN.COMPUTESENSITIVITY, COLUMN.ESTIMATE):
            return (Qt.ItemIsUserCheckable
                    | Qt.ItemIsEnabled
                    #| Qt.ItemIsSelectable
            )

        elif index.column() == (COLUMN.INITIALVALUE) or index.column() == (COLUMN.SCALE) or index.column() == (COLUMN.NAME):
            return (Qt.ItemIsEnabled
                    | Qt.ItemIsEditable
            )

        return Qt.NoItemFlags

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and 0 <= index.row() < len(self.paramList):
            sbmlEntity = self.paramList[index.row()]
            param = sbmlEntity.Item
            column = index.column()

            if role == Qt.EditRole:
                if column == COLUMN.INITIALVALUE:
                    #param.setValue(float(value))
                    combinedId = sbmlEntity.getCombinedId()
                    try:
                        floatValue = float(value)
                        self.getActiveSet()[combinedId].setValue(floatValue)
                    except:
                        pass    # don't touch the old value
                elif column == COLUMN.SCALE:
                    try:
                        sbmlEntity.setThreshold(float(value))
                    except:
                        return False
                elif column == COLUMN.NAME:
                    try:
                        sbmlEntity.setName(str(value))
                    except:
                        return False

            if role == Qt.CheckStateRole:
                isChecked = value == Qt.Checked
#                if column == COLUMN.ISCONSTANT:
#                    param.setConstant(isChecked)
                if column == COLUMN.COMPUTESENSITIVITY:
                    #self.paramsToSensitivityMap[param] = isChecked
                    self.paramsToSensitivityMap[sbmlEntity] = isChecked
                if column == COLUMN.ESTIMATE:
                    self.paramToEstimateMap[sbmlEntity] = isChecked

            self.Dirty = True
            #self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            self.dataChanged.emit(index, index)
            return True

        return False


    def selectAllSensitivity(self, doSelect):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for key in self.paramsToSensitivityMap.keys():
            self.paramsToSensitivityMap[key] = doSelect

        self.emit(SIGNAL("layoutChanged()"))

    def invertSelectionSensitivity(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for key, value in self.paramsToSensitivityMap.items():
            self.paramsToSensitivityMap[key] = not value

        self.emit(SIGNAL("layoutChanged()"))


    def selectAllEstimation(self, doSelect):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for key in self.paramToEstimateMap.keys():
            self.paramToEstimateMap[key] = doSelect

        self.emit(SIGNAL("layoutChanged()"))

    def invertSelectionEstimation(self):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))

        for key, value in self.paramToEstimateMap.items():
            self.paramToEstimateMap[key] = not value

        self.emit(SIGNAL("layoutChanged()"))


    def paramSetsChanged(self):
        self.emit(SIGNAL("layoutChanged()"))

    def getActiveSet(self):
    #        if not self.paramSets:
    #            logging.debug("ParameterTableModel.getActiveSet(): No list of Parameter Sets! Aborting.")
    #            return
    #        if not self.paramSets.activeSet:
    #            logging.debug("ParameterTableModel.getActiveSet(): No active Parameter Set! Aborting.")
    #            return
    #
    #        return self.paramSets.activeSet
        if not self.mainModel:
            logging.debug("ParameterTableModel.getActiveSet(): Reference to MainModel is missing. Aborting.")
            return
        if not self.mainModel.ListOfParameterSets:
            logging.debug("ParameterTableModel.getActiveSet(): No list of Parameter Sets! Aborting.")
            return
        if not self.mainModel.ListOfParameterSets.activeSet:
            logging.debug("ParameterTableModel.getActiveSet(): No active Parameter Set! Aborting.")
            return

        return self.mainModel.ListOfParameterSets.activeSet
