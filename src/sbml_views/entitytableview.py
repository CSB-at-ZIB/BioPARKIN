import logging
from PySide.QtGui import QWidget
from sbml_model.sbml_entities import SBMLEntity
from sbml_views.ui_entitytableview import Ui_EntityTableView
from sbml_model.sbml_entitytablemodel import SBMLEntityTableModel

class EntityTableView(QWidget, Ui_EntityTableView):
    """
    This View uses a TableView internally (which is defined in the UI
    part "Ui_EntityTableView" which is generated from a Qt Creator file)
    to display a given SBMLEntityTableModel. The model is kept in sync with
    the entity that is selected in the TreeView, so that this table view
    always displays the correct information.

    This class more or less adheres to the MVC principle by splitting the UI
    (Ui_EntityTabelView) and the logic (this class) into parts (the model is
    its own class anyway).

    @param parent: Standard Qt parent
    @type parent: QWidget

    @since: 2010-04-08
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent):
        """
        Intialize UI and set up some instance variables.
        """
        super(EntityTableView, self).__init__(parent)
        
        self.setupUi(self)
        
        self.model = None
        self.selectionModel = None
        self.entityModel = None
        self.sbmlEntity = None
        self.mainModel = None


    def setModel(self, model, mainModel=None):
        """
        Set the internal model and connect to model's Signals.
        This is not a specific entity model, it is the "large" MainTreeModel.
        The specific entity models are created internally, whenever selection
        on the large model (delivered via a specific QSelectionModel) changes.

        @param model: Main Model as a reference
        @type model: QAbstractItemModel (more specific: SBMLMainTreeModel)
        """
        if self.model:
            self.model.dataChanged.disconnect(self.dataChanged)
            self.model.modelReset.disconnect(self.dataChanged)

        self.model = model

        if mainModel:
            self.mainModel = mainModel

        if model:
            self.model.dataChanged.connect(self.dataChanged)
            self.model.modelReset.connect(self.dataChanged)
            self.tableView.setModel(None) #clear the internal model from the table view
        else:
            self._clearTableView()

        
    def setSelectionModel(self, selectionModel):
        """
        Sets the internal selection model. This must be called, otherwise
        keeping the TreeView's selected item in sync with what's displayed
        here, won't work.

        @param selectionModel: A selection model
        @type selectionModel: QSelectionModel
        """
        self.selectionModel = selectionModel
        self.selectionModel.currentChanged.connect(self.selectionChanged)


    def _clearTableView(self):

        if self.entityModel:
            self.entityModel.dataChanged.disconnect(self.currentEntityModelChanged)
            self.entityModel.structuralChange.disconnect(self.currentEntityModelChangedStructurally)
            self.entityModel = None
            
        self.tableView.setModel(None)

    def selectionChanged(self, currentIndex, previousIndex):
        """
        This is a Slot. It's called, when the selection on the internally
        referenced main model changes. The currentIndex is saved and later used
        to create the correct Entity model.

        @param currentIndex: Index of the (newly) selected item
        @type currentIndex: QModelIndex

        @param previousIndex: Index of previously selected item; not used
        @type previousIndex: QModelIndex
        """
        self.currentIndex = self.model.mapToSource(currentIndex)
        self.updateTableView()

    def dataChanged(self, topLeft, bottomRight):
        """
        This is a Slot. It's called when some data has changed in the main model.
        If the changed item is also the currently selected item (thus
        displayed in the table view), the view is updated.

        @param topLeft: Start index of change
        @type topLeft: QModelIndex

        @param bottomRight: End index of change; not used
        @type bottomRight: QModelIndex
        """
        if self.currentIndex == topLeft:
            self.updateTableView()
        
    def updateTableView(self):
        """
        Gets the SBMLEntity out of the currently selected QModelIndex
        and creates a SBMLEntityTableModel with it. This model is then bound to
        the internal table view. The entity model's Signals are connected to
        Slots.
        """
        self.sbmlEntity = self.currentIndex.internalPointer()
        if self.sbmlEntity is None or not isinstance(self.sbmlEntity, SBMLEntity):
            return
        
        if self.entityModel:
            self.entityModel.dataChanged.disconnect(self.currentEntityModelChanged)
            self.entityModel.structuralChange.disconnect(self.currentEntityModelChangedStructurally)

        self.entityModel = SBMLEntityTableModel(self.sbmlEntity, self.mainModel)
        self.entityModel.dataChanged.connect(self.currentEntityModelChanged)
        self.entityModel.structuralChange.connect(self.currentEntityModelChangedStructurally)
        self.tableView.setModel(self.entityModel)
        self.tableView.resizeColumnsToContents()
        #self.tableView.setItemDelegate(SBMLEntityTableDelegate()) # not in use right now

    def currentEntityModelChanged(self, topLeftIndex, bottomRightIndex):
        """
        C++: void QAbstractItemModel::dataChanged ( const QModelIndex & topLeft, const QModelIndex & bottomRight )

        This is a slot. It is called, when something inside an entity model
        changes (e.g. the Name). It calls a model.entityHasChangedMethod
        which will lead to a chain reaction, ultimately notifying the
        graphical representation of the entity to update itself (e.g. the
        displayed name).

        The supplied Indexes are not used. We have an internal reference to
        the currently displayed entity and use this reference instead.
        (The indexes would have to be used if some changes (e.g. ID or Name)
        should be handled separately.)

        @param topLeftIndex: Start index of change; not used
        @type topLeftIndex: QModelIndex

        @param bottomRightIndex: End index of change; not used
        @type bottomRightIndex: QModelIndex
        """
        # for now, we ignore that there is a range of indexes
        logging.debug("EntityTableView.currentEntityModelChanged(): Entered.")
        if self.sbmlEntity:
            self.sbmlEntity.hasChanged.emit()

    def currentEntityModelChangedStructurally(self, entity, type):
        logging.debug("EntityTableView.currentEntityModelChangedStructurally(): Entered.")
        if self.sbmlEntity:
            self.sbmlEntity.hasChanged.emit()
        
        