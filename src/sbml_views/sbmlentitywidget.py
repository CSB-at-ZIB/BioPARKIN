import logging
from PySide.QtCore import Slot
from PySide.QtGui import QWidget
from sbml_views.ui_sbmlentitywidget import Ui_SBMLEntityWidget
from sbml_model.sbml_entities import SBMLEntity
from sbml_model import sbml_entities
import libsbml

class SBMLEntityWidget(QWidget, Ui_SBMLEntityWidget):
    """
    A simple widget that combines some buttons (for adding, deleting, ...
    SBML entities) with a TreeView to display the entity tree.

    @since: 2010-09-15
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent):
        """
        Simple constructor setting up the UI and some variables.
        """
        super(SBMLEntityWidget, self).__init__(parent)
        
        self.setupUi(self)
        
        self.model = None
        
    def setModel(self, model, mainModel=None):
        """
        Set the internal model and connect to model's Signals.
        This is not a specific entity model, it is the "large" MainTreeModel.

        @param model: Main Tree Model as a reference
        @type model: QAbstractItemModel (more specific: SBMLMainTreeModel)
        """
        self.model = model


        self.treeView.setModel(self.model)
        self.treeView.viewport().setMouseTracking(True)
        self.treeView.resizeColumnToContents(0)
        
        self.treeView.setSortingEnabled(True)

        
        
    def setSelectionModel(self, selectionModel):
        """
        Sets the internal selection model. This must be called, otherwise
        keeping the TreeView's selected item in sync with what's displayed
        here, won't work.

        @param selectionModel: A selection model
        @type selectionModel: QSelectionModel
        """
        self.selectionModel = selectionModel
        self.treeView.setSelectionModel(self.selectionModel)
        #self.connect(self.selectionModel, SIGNAL("currentChanged(QModelIndex,QModelIndex)"), self.selectionChanged)
        
    
#    @Slot("")
#    def on_buttonAdd_clicked(self):
#        self.addEntity()
#
#
#    def addEntity(self):
#        """
#        Adds a new entity (Species, Reaction, ...) based on the currently selected
#        entity (or category).
#        """
#        # getting currently selected entity (e.g. if it's a Species, we have to add another Species)
#        if not self.model:
#            logging.info("No network selected. Can't add anything.")
#            return
#
#        currentIndex = self.selectionModel.currentIndex()
#        sbmlEntity = currentIndex.internalPointer()
#
#        sbmlLevel = self.model.MainModel.SbmlDocument.Item.getLevel()
#        sbmlVersion = self.model.MainModel.SbmlDocument.Item.getVersion()
#
#        if sbmlEntity is None or not isinstance(sbmlEntity, SBMLEntity):
#            return
#
#        if sbmlEntity.Type == sbml_entities.TYPE.SPECIES or (sbml_entities.TYPE.NONE and sbmlEntity.Label == "Species"):
#            self.model.MainModel.addSpecies()   # without ID, etc. standard values are used
#        elif sbmlEntity.Type == sbml_entities.TYPE.COMPARTMENT or (sbml_entities.TYPE.NONE and sbmlEntity.Label == "Compartments"):
#            self.model.MainModel.addCompartment()   # without ID, etc. standard values are used
#        elif sbmlEntity.Type == sbml_entities.TYPE.REACTION or (sbml_entities.TYPE.NONE and sbmlEntity.Label == "Reactions"):
#            self.model.MainModel.addReaction()   # without ID, etc. standard values are used
#        elif sbmlEntity.Type == sbml_entities.TYPE.PARAMETER or (sbml_entities.TYPE.NONE and sbmlEntity.Label == "Parameters"):
#            self.model.MainModel.addParameter()   # without ID, etc. standard values are used
#        elif sbmlEntity.Type == sbml_entities.TYPE.RULE or (sbml_entities.TYPE.NONE and sbmlEntity.Label == "Rules"):
#            self.model.MainModel.addRateRule()   # without ID, etc. standard values are used
#
#
#
#
#    @Slot("")
#    def on_buttonRemove_clicked(self):
#        self.removeEntity()
#
#
#
#    def removeEntity(self):
#        """
#        Removes the currently selected entity.
#        """
#        if not self.model:
#            logging.info("No network selected. Can't remove anything.")
#            return
#
#        currentIndex = self.selectionModel.currentIndex()
#        sbmlEntity = currentIndex.internalPointer()
#
#        self.model.MainModel.removeEntity(sbmlEntity) # takes optional index argument
