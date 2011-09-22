'''
Created on Apr 12, 2010

@author: bzfwadem
'''
from PySide.QtCore import QObject
from sbml_model.sbml_mainmodel import SBMLMainModel
from sbml_networkview.networkview import NetworkView
import networkx
import logging
from sbml_networkview.hyperedgenode import HyperEdgeNode
from sbml_networkview import networkview
from sbml_model import sbml_mainmodel, sbml_entities

class NetworkController(QObject):
    '''
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
    '''
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

#    def GetDirty(self):
#        return self.__Dirty
#
#
#    def SetDirty(self, value):
#        self.__Dirty = value
#        self.emit(SIGNAL("DirtyChanged(bool)"), value)
#
#
#    def DelDirty(self):
#        del self.__Dirty
#
#    Dirty = property(GetDirty, SetDirty, DelDirty, "Defines whether this network has any unsaved changes.")
#
#    def __init__(self, filename=None, views=[]):
#        '''
#        Sets up some instance variables. Most importantly,
#        it executes the loading of a SBML file, if a filename is given.
#        '''
#        super(NetworkController, self).__init__()
#
#        self.filename = None    # will be set by self._loadFile
#        self.sbmlModel = None
#        self.treeModel = None
#        self.selectionModel = None
#
#        self.views = views
#        self.networkView = None # a special place for the NetworkView
#        self.reactionsToHyperNodes = None
#
#        self.connect(self, SIGNAL("DirtyChanged(bool)"), self.updateUI)
#
#        if filename is not None:
#            self._loadFile(filename)
#
#
#    def _loadFile(self, filename=None):
#        '''
#        Loads a SBML file. It invokes the creation of a data model and
#        a networkx graph based on the SBML data.
#
#        @param filename: Name of the SBML file
#        @type filename: str
#        '''
#        if filename is None:
#            return
#
#        self.filename = filename
#
#
#        self.sbmlModel = SBMLMainModel(filename)
#        self.treeModel = self.sbmlModel.MainTreeModel
#        self.connect(self.sbmlModel, SIGNAL("DirtyChanged(bool)"), self.dirtyChanged)
#        self.sbmlModel.structuralChange.connect(self._updateGraph)
#
#        self.selectionModel = QItemSelectionModel(self.treeModel)
#
#        self._connectViews()    # probably not needed here, there is no View after __init__
#        self._createGraph()
#
#        self.Dirty = False
#
#    def _connectViews(self):
#        '''
#        Calls .setModel() on the internal NetworkView
#        and on "outside" Views that have been passed to .__init__().
#        '''
#        # connecting internal NetworkView
#        if self.networkView is not None:
#            self.networkView.setModel(self.treeModel)
#            self.networkView.setSelectionModel(self.selectionModel)
#
#
#        # connecting outside Views
#        for view in self.views:
#            if hasattr(view, "setModel"):
#                view.setModel(self.treeModel)
#            if hasattr(view, "setSelectionModel"):
#                view.setSelectionModel(self.selectionModel)
#
#    def createNetworkView(self, parent=None):
#        '''
#        Creates the internal NetworkView. Returns the network view.
#
#        @return: The internal NetworkView.
#        @param parent: QWidget parent that is passed to the NetworkView
#        @type parent: QWidget
#        '''
#        self.networkView = NetworkView(parent, controller=self)
#        #self.networkView.setViewport(QGLWidget)    # would improve performance
#        #for debugging:
#        #self.networkView.setWindowTitle("Test")    # works
#        self._connectViews()
#        if self.graph is not None:
#            self.networkView.draw_graph(self.graph)
#
#        self.networkView.species = self.sbmlModel.SbmlSpecies
#        self.networkView.reactions = self.sbmlModel.SbmlReactions
#
#        self.updateUI()
#        return self.networkView
#
#    def updateUI(self):
#        '''
#        Updates dynamic aspects of the UI, e.g. depending
#        on whether the current model needs saving, etc.
#        '''
#        if self.Dirty:
#            windowTitle = self.filename + " (*)"
#        else:
#            windowTitle = self.filename
#        if self.networkView is not None:
#            self.networkView.setWindowTitle(windowTitle)
#
#
#
#    def dirtyChanged(self, value):
#        '''
#        Sets self.Dirty to value.
#
#        @param value: Is self now "Dirty"?
#        @type value: bool
#        '''
#        self.Dirty = value
#
#
#    def addReactionToGraph(self, products, reactants, wrappedReaction, networkView=None):
#        reaction = wrappedReaction.Item
#        if len(reactants) == 1 and len(products) == 1:  # normal case for non-hyperedge
#            self.graph.add_edge(reactants[0], products[0], reaction=wrappedReaction)
#        else:   # build an hyperedge
#            if reaction.getName() == None or reaction.getName() == "":
#                node = HyperEdgeNode(reaction=reaction)
#            else:
#                node = HyperEdgeNode(reaction=reaction, label=reaction.getName())
#
#            # for hyperedge management
#            if wrappedReaction not in self.reactionsToHyperNodes:
#                self.reactionsToHyperNodes[wrappedReaction] = set([node])
#            else:
#                self.reactionsToHyperNodes[wrappedReaction].add(node)
#
#            self.graph.add_node(node)
#            for reactant in reactants:
#                self.graph.add_edge(reactant, node, reaction=wrappedReaction)
#            for product in products:
#                self.graph.add_edge(node, product, reaction=wrappedReaction)
#
#    def _createGraph(self):
#        '''
#        Basically builds a networkx graph out
#        of the SBML model which is ready to be painted.
#
#        Hyperedges (edges connecting more than one node)
#        are built using dummy nodes of type HyperEdgeNode.
#        '''
#
#        self.graph = networkx.DiGraph()
#        reactions = self.sbmlModel.SbmlReactions
#
#        self.SpeciesRowIndexToSpeciesMapper = {}    # important for syncing index-based table views to network view
#        if self.sbmlModel.SbmlSpecies is not None:
#            for (i, species) in enumerate(self.sbmlModel.SbmlSpecies):
#                self.SpeciesRowIndexToSpeciesMapper[i] = species
#                self.SpeciesRowIndexToSpeciesMapper[species] = i
#
#        if reactions is None:
#            logging.info("Empty model.")
#            return
#
#
#        # building the graph from the reactions
#        self.reactionsToHyperNodes = {}
#        if reactions is not None and len(reactions) > 1:
#            for (wrappedReaction, reactants, products) in reactions:
#                self.addReactionToGraph(products, reactants, wrappedReaction)
#        else:
#            for species in self.sbmlModel.SbmlSpecies:
#                self.graph.add_node(species)
#
#        #self.register_model_signals(self.sbmlModel)
#
#        if self.networkView is not None:
#            self.networkView.draw_graph(self.graph)
#
#
#    #@Slot("structuralChange(SBMLEntity)")
#    def _updateGraph(self, sbmlEntity, changeType):
#        '''
#        Updates the graph, when the MainModel signals a structural change,
#        e.g. a Species has been added/removed, ...
#        '''
#        #print sbmlEntity
#        if changeType == sbml_mainmodel.CHANGETYPE.ADD:
#            #print "add"
#            if sbmlEntity.Type == sbml_entities.TYPE.SPECIES:
#                i = len(self.SpeciesRowIndexToSpeciesMapper)
#                self.SpeciesRowIndexToSpeciesMapper[i] = sbmlEntity
#                self.SpeciesRowIndexToSpeciesMapper[sbmlEntity] = i
#                self.graph.add_node(sbmlEntity) # for Node that is not in a Reaction
#                self.networkView.addNode(sbmlEntity)
#
#        elif changeType == sbml_mainmodel.CHANGETYPE.REMOVE:
#            print "remove: to be done"
#
#        elif changeType == sbml_mainmodel.CHANGETYPE.CHANGE_REACTANTS:
#            #print "Draw changed Reactants: to be done"
#            self.updateReaction(sbmlEntity)
#
#        elif changeType == sbml_mainmodel.CHANGETYPE.CHANGE_PRODUCTS:
#            #print "Draw changed Products: to be done"
#            self.updateReaction(sbmlEntity)
#        else:
#            logging.error("NetworkController: Unsupported type of change in the main model.")
#
#        self.networkView.redraw()
#
#
#    def save(self, filename=None):
#        '''
#        Saves the current model with the given filename.
#
#        @param filename: Filename to save the model to
#        @type filename: str
#        '''
#        try:
#            self.sbmlModel.save(filename)
#            self.Dirty = False
#        except Exception, e:
#            QMessageBox.warning(self.networkView, "Filename is not valid.",
#                                "Please, try to select another filename.")
#            logging.warning("Selected an invalid filename: %s\nException: %s" % (filename,e))
#
#    def updateReaction(self, reactionWrapper):
#        '''
#        Searches the graph for the given Reaction, removes all Edges and then creates
#        new edges in and out of this Reaction node.
#        '''
#
#        # remove hyper node that represents the reaction (if there is one)
#        if reactionWrapper in self.reactionsToHyperNodes:
#            nodeSet = self.reactionsToHyperNodes[reactionWrapper]
#            for hyperEdgeNode in nodeSet:
#                edges = self.graph.edges([hyperEdgeNode], data=True)
#                self.graph.remove_edges_from(edges) #remove structural (!) edges
#            self.graph.remove_nodes_from([hyperEdgeNode]) # remove structural (!) node(s)
#            if self.networkView:
#                self.networkView.removeSpeciesNode(hyperEdgeNode)   # remove graphical(!) node(s)
#
#        #for (u,v,edata['reaction']) in [for u,v,edata in self.graph.edges(data=True) if 'reaction' in edata]:
#        for (sourceSpecies, targetSpecies, edata) in self.graph.edges(data=True):
#            if "reaction" not in edata:
#                logging.debug("Encountered a graph edge without associated Reaction.")
#                continue
#            currentReaction = edata["reaction"]
#            if reactionWrapper == currentReaction:
#                self.graph.remove_edge(sourceSpecies, targetSpecies)
#                break
#
#        # remove graphical (!) edges (1 or more)
#        if self.networkView:
#            self.networkView.removeReaction(reactionWrapper)
#
#        # create Reaction in graph
#        reactionTuples = self.sbmlModel.SbmlReactions
#        for (wrappedReaction, newReactants, newProducts) in reactionTuples:
#            if wrappedReaction == reactionWrapper:
#                self.addReactionToGraph(newProducts, newReactants, wrappedReaction, networkView = self.networkView)
#
#                #debugging
#                logging.debug("Adding Reaction between...")
#                for reactant in newReactants:
#                    logging.debug("Reactant: %s" % reactant.getId())
#                for product in newProducts:
#                    logging.debug("Product: %s" % product.getId())
#
#
#        self.networkView.updateNodesAndEdges()
#        self.networkView.redraw()
#
#
