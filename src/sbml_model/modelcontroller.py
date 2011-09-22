import logging
#from PySide.QtCore import *
#from PySide.QtGui import *
from PySide.QtCore import Signal, QObject, Qt
from PySide.QtGui import  QItemSelectionModel, QMessageBox, QSortFilterProxyModel
from sbml_model.sbml_mainmodel import SBMLMainModel

class ModelController(QObject):
    """
    The network controller which basically manages all aspects
    revolving around a single SBML model (i.e. SBML file).
    It has references to outside Views (e.g. TreeView). Internally,
    it has a reference to the custom NetworkView.
    A Dirty state is used to handle the need for saving/rejecting changes, etc.

    It inherits from QObject for the use of Signals/Slots.

    @param filename: Filename of the SBML model that should be opened. If None, an empty model is created.
    @type filename: str

    @param views: The views of the main window that are to be associated with the model.
    @type views: L{QAbstractItemView}

    @since: 2010-04-12
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    dirtyChanged = Signal(bool)

    def GetDirty(self):
        return self.__Dirty


    def SetDirty(self, value): 
        self.__Dirty = value
#        self.emit(SIGNAL("DirtyChanged(bool)"), value)
        self.dirtyChanged.emit(value)


    def DelDirty(self):
        del self.__Dirty

    Dirty = property(GetDirty, SetDirty, DelDirty, "Defines whether this model has any unsaved changes. This is passed through to SbmlMainModel's Dirty.")


    def __init__(self, filename=None, views=[], networkViewController=None):
        """
        Sets up some instance variables. Most importantly,
        it executes the loading of a SBML file, if a filename is given.
        """
        super(ModelController, self).__init__()
        
        self.filename = None    # will be set by self._loadFile
        self.sbmlModel = None
        self.treeModel = None
        self.selectionModel = None
        self.proxyModel = None # we have the proxy model here, so that all Views can use it and the same SelectionModel still works (!)
        
        self.views = views
        self.networkViewController = networkViewController # a special place for the NetworkViewController
        
#        self.connect(self, SIGNAL("DirtyChanged(bool)"), self.updateUI)
#        self.dirtyChanged.connect(self.updateUI)
        
        if filename is not None:
            self._loadFile(filename)

    def setViews(self, views=None, networkViewController=None):
        """
        Can be used to re-reference the ModelController with Views (either if they
        haven't been given to the Constructor or if they have changed somehow).
        This internally calls self._connectViews to set the correct models and a
        single QSelectionModel on the views.
        """
        if views:
            self.views = views
        if networkViewController:
            self.networkViewController = networkViewController

        self._connectViews()
        if self.networkViewController:
            self.networkViewController._createGraph()
        
    def _loadFile(self, filename=None):
        '''
        Loads a SBML file. It invokes the creation of a data model and 
        a networkx graph based on the SBML data.
        
        @param filename: Name of the SBML file
        @type filename: str
        '''
        if filename is None:
            return
        
        self.filename = filename
        
        
        self.sbmlModel = SBMLMainModel(filename)
        self.treeModel = self.sbmlModel.MainTreeModel
#        self.connect(self.sbmlModel, SIGNAL("DirtyChanged(bool)"), self.on_dirtyChanged)
        self.sbmlModel.dirtyChanged.connect(self.on_dirtyChanged)

#        self.proxyModel = self.treeModel   # DEBUGGING: "disabling" the proxy approach
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSortRole(Qt.UserRole)
        self.proxyModel.setSourceModel(self.treeModel)

        
        self.selectionModel = QItemSelectionModel(self.proxyModel)
#        self.selectionModel = self.proxyModel.selectionModel()
        
        self._connectViews()    # probably not needed here, there is no View after __init__
        if self.networkViewController:
            self.networkViewController._createGraph()
        
        self.Dirty = False
        
    def _connectViews(self):
        ''' 
        Calls .setModel() on the NetworkView
        and on "outside" Views that have been passed to .__init__().
        '''
        # connecting internal NetworkView
        if self.networkViewController is not None:
            self.networkViewController.setModel(self.proxyModel)
            self.networkViewController.setSelectionModel(self.selectionModel)
        
        
        # connecting outside Views
        for view in self.views:
            if hasattr(view, "setModel"):
                view.setModel(self.proxyModel, mainModel = self.sbmlModel)
            if hasattr(view, "setSelectionModel"):
                view.setSelectionModel(self.selectionModel)


    
    
    
    def on_dirtyChanged(self, value):
        '''
        Sets self.Dirty to value.
        This is hooked up to the "DirtyChanged" event of the SbmlMainModel.

        self.Dirty is a property (which emits a Signal itself if it is changed)
        
        @param value: Is self now "Dirty"?
        @type value: bool
        '''
        self.Dirty = value  


        
            
    def save(self, filename=None):   
        '''
        Saves the current model with the given filename.
        
        @param filename: Filename to save the model to
        @type filename: str
        ''' 
        try:
            self.sbmlModel.save(filename)
            self.Dirty = False
        except Exception, e:
            QMessageBox.warning(self.networkView, "Filename is not valid.", 
                                "Please, try to select another filename.")
            logging.warning("Selected an invalid filename: %s\nException: %s" % (filename,e))

    def getNetworkView(self):
        return self.networkViewController.networkView