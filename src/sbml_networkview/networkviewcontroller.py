import logging
from PySide.QtCore import QObject, SIGNAL
import networkx
from sbml_model import sbml_mainmodel, sbml_entities
from sbml_networkview.hyperedgenode import HyperEdgeNode
from sbml_networkview.networkview import NetworkView

__author__ = 'bzfwadem'


class NetworkViewController(QObject):
    """
    This controller works as an adapter between main program logic (like
    in ModelController) and the NetworkView.
    The code in this class could have been included in NetworkView but
    was kept separate for historical and housekeeping reasons.

    @since: 2011-05-13
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    def __init__(self, modelController):
        super(NetworkViewController, self).__init__()

        if not modelController:
            logging.error("NetworkViewController: Can't initialize without reference to ModelController.")
            return

        self.modelController = modelController
        self.modelController.dirtyChanged.connect(self.updateUI)

        self.networkView = None
        self.reactionsToHyperNodes = None
        self.subWindow = None   # a place to hold the QSubWindow where self.networkView ic placed
        self.graph = None

        self.modelController.on_structuralChange.connect(self._updateGraph)


    def createNetworkView(self, parent=None):
        """
        Creates the internal NetworkView. Returns the network view.

        @return: The internal NetworkView.
        @param parent: QWidget parent that is passed to the NetworkView
        @type parent: QWidget
        """
        self.networkView = NetworkView(parent, controller=self)
        #self.networkView.setViewport(QGLWidget)    # would improve performance
        #for debugging:
        #self.networkView.setWindowTitle("Test")    # works
#        self._connectViews()
        if self.graph is not None:
            self.networkView.draw_graph(self.graph)

        self.networkView.species = self.modelController.sbmlModel.SbmlSpecies
        self.networkView.reactions = self.modelController.sbmlModel.SbmlReactions

        self.updateUI()
        return self.networkView


    def addReactionToGraph(self, products, reactants, wrappedReaction, networkView=None):
        reaction = wrappedReaction.Item
        if len(reactants) == 1 and len(products) == 1:  # normal case for non-hyperedge
            self.graph.add_edge(reactants[0], products[0], reaction=wrappedReaction)
        else:   # build an hyperedge
            if reaction.getName() == None or reaction.getName() == "":
                node = HyperEdgeNode(reaction=reaction)
            else:
                node = HyperEdgeNode(reaction=reaction, label=reaction.getName())

            # for hyperedge management
            if wrappedReaction not in self.reactionsToHyperNodes:
                self.reactionsToHyperNodes[wrappedReaction] = set([node])
            else:
                self.reactionsToHyperNodes[wrappedReaction].add(node)

            self.graph.add_node(node)
            for reactant in reactants:
                self.graph.add_edge(reactant, node, reaction=wrappedReaction)
            for product in products:
                self.graph.add_edge(node, product, reaction=wrappedReaction)

    def _createGraph(self):
        """
        Basically builds a networkx graph out
        of the SBML model which is ready to be painted.

        Hyperedges (edges connecting more than one node)
        are built using dummy nodes of type HyperEdgeNode.
        """

        self.graph = networkx.DiGraph()
        reactions = self.modelController.sbmlModel.SbmlReactions

        self.SpeciesRowIndexToSpeciesMapper = {}    # important for syncing index-based table views to network view
        if self.modelController.sbmlModel.SbmlSpecies is not None:
            for (i, species) in enumerate(self.modelController.sbmlModel.SbmlSpecies):
                self.SpeciesRowIndexToSpeciesMapper[i] = species
                self.SpeciesRowIndexToSpeciesMapper[species] = i

        if reactions is None:
            logging.info("Empty model.")
            return


        # building the graph from the reactions
        self.reactionsToHyperNodes = {}
        if reactions is not None and len(reactions) > 1:
            for (wrappedReaction, reactants, products) in reactions:
                self.addReactionToGraph(products, reactants, wrappedReaction)
        else:
            for species in self.modelController.sbmlModel.SbmlSpecies:
                self.graph.add_node(species)

        #self.register_model_signals(self.sbmlModel)

        if self.networkView is not None:
            self.networkView.draw_graph(self.graph)


    #@Slot("structuralChange(SBMLEntity)")
    def _updateGraph(self, sbmlEntity, changeType):
        """
        Updates the graph, when the MainModel signals a structural change,
        e.g. a Species has been added/removed, ...
        """
        #print sbmlEntity
        if changeType == sbml_mainmodel.CHANGETYPE.ADD:
            #print "add"
            if sbmlEntity.Type == sbml_entities.TYPE.SPECIES:
                i = len(self.SpeciesRowIndexToSpeciesMapper)
                self.SpeciesRowIndexToSpeciesMapper[i] = sbmlEntity
                self.SpeciesRowIndexToSpeciesMapper[sbmlEntity] = i
                self.graph.add_node(sbmlEntity) # for Node that is not in a Reaction
                self.networkView.addNode(sbmlEntity)

        elif changeType == sbml_mainmodel.CHANGETYPE.REMOVE:
            # TODO: Add support for this type of change
            logging.error("NetworkViewController: Removing a network entity is not yet supported.")

        elif changeType == sbml_mainmodel.CHANGETYPE.CHANGE_REACTANTS:
            self.updateReaction(sbmlEntity)

        elif changeType == sbml_mainmodel.CHANGETYPE.CHANGE_PRODUCTS:
            self.updateReaction(sbmlEntity)
        else:
            logging.error("NetworkViewController: Unsupported type of change in the main model.")

        self.networkView.redraw()


    def updateReaction(self, reactionWrapper):
        """
        Searches the graph for the given Reaction, removes all Edges and then creates
        new edges in and out of this Reaction node.
        """

        # remove hyper node that represents the reaction (if there is one)
        if reactionWrapper in self.reactionsToHyperNodes:
            nodeSet = self.reactionsToHyperNodes[reactionWrapper]
            for hyperEdgeNode in nodeSet:
                edges = self.graph.edges([hyperEdgeNode], data=True)
                self.graph.remove_edges_from(edges) #remove structural (!) edges
            self.graph.remove_nodes_from([hyperEdgeNode]) # remove structural (!) node(s)
            if self.networkView:
                self.networkView.removeSpeciesNode(hyperEdgeNode)   # remove graphical(!) node(s)

        #for (u,v,edata['reaction']) in [for u,v,edata in self.graph.edges(data=True) if 'reaction' in edata]:
        for (sourceSpecies, targetSpecies, edata) in self.graph.edges(data=True):
            if "reaction" not in edata:
                logging.debug("Encountered a graph edge without associated Reaction.")
                continue
            currentReaction = edata["reaction"]
            if reactionWrapper == currentReaction:
                self.graph.remove_edge(sourceSpecies, targetSpecies)
                break

        # remove graphical (!) edges (1 or more)
        if self.networkView:
            self.networkView.removeReaction(reactionWrapper)

        # create Reaction in graph
        if not self.modelController.sbmlModel:
            return
        reactionTuples = self.modelController.sbmlModel.SbmlReactions
        for (wrappedReaction, newReactants, newProducts) in reactionTuples:
            if wrappedReaction == reactionWrapper:
                self.addReactionToGraph(newProducts, newReactants, wrappedReaction, networkView = self.networkView)

                #debugging
                logging.debug("Adding Reaction between...")
                for reactant in newReactants:
                    logging.debug("Reactant: %s" % reactant.getId())
                for product in newProducts:
                    logging.debug("Product: %s" % product.getId())


        self.networkView.updateNodesAndEdges()
        self.networkView.redraw()



    def updateUI(self):
        """
        Updates dynamic aspects of the UI, e.g. depending
        on whether the current model needs saving, etc.
        """
        if self.modelController.Dirty:
            windowTitle = self.modelController.filename + " (*)"
        else:
            windowTitle = self.modelController.filename
        if self.networkView is not None:
            self.networkView.setWindowTitle(windowTitle)


    def setModel(self, model):
        self.networkView.setModel(model)

    def setSelectionModel(self, selectionModel):
        self.networkView.setSelectionModel(selectionModel)

    def getGlobalSelectionModel(self):
        return self.modelController.selectionModel