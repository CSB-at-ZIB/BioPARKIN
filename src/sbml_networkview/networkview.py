'''
Created on Apr 12, 2010

@author: bzfwadem
'''

import logging

#from PySide.QtCore import *
#from PySide.QtGui import *
from PySide.QtCore import QReadWriteLock, SIGNAL, Slot, QModelIndex, QRect
from PySide.QtGui import QAbstractItemView, QGraphicsScene, QHBoxLayout, QItemSelectionModel, QItemSelection, QRegion

from sbml_networkview.node import Node
from sbml_networkview.edge import Edge
#import networkx
from sbml_networkview.graphicsview import GraphicsView
from layoutthread import LayoutThread
from sbml_networkview.hyperedgenode import HyperEdgeNode

class NetworkView(QAbstractItemView):
    '''
    The NetworkView is sort of a wrapper around the Qt Canvas concept
    with QGraphicsView and QGraphicsScene.
    It inherits from QAbstractItemView to live in the world of Qt Model
    View Controller (MVC). Basically, it is there to bring these two worlds 
    together. (Why the hell Qt does not provide something like this, I
    don't know.)
    
    NetworkView handles the usual model update methods (e.g. dataChanged)
    and handles selection changes between the model-based views and the 
    internal GraphicsView. (Which itself is not a QGraphicsView directly but
    a simple wrapper to support mousewheel zooming, etc.)
    
    @param parent: The standard Qt parent
    @type parent: QWidget (probably ;))
    
    @param controller: The network controller that belongs to this view.
    @type controller: ModelController
    
    @since: 2010-04-12
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, parent=None, controller=None):
        '''
        The initialization instanciates the GraphicsView/GraphicsScene
        combo. It sets up reference variables for handling nodes
        and edges of the graph. It register various signals.
        '''
        super(NetworkView, self).__init__(parent)
        
        self.parent = parent    # maybe needed later?
        self.controller = controller
        
        self.graphicsView = GraphicsView(self) 
        self.graphicsScene = QGraphicsScene(self)
        self.graphicsView.setScene(self.graphicsScene)
        
        self.modelSelectionInProgress = False
        
        self.registerSignals()
        
        self.statusBar = None   # can be set from the outside
        
        
        self.species = None
        self.reactions = None
        
        # TODO: check these
        self.nodes = []
        self.edges = []
        self.speciesNodesMapper = {}
        self.reactionEdgesMapper = {}        
        
        self.lock = QReadWriteLock()
        
        
        layout = QHBoxLayout()
        layout.addWidget(self.graphicsView, 1)
        self.setLayout(layout)


    def draw_graph(self, graph):
        '''
        Invokes a layout algorithm of the networkx package in another
        Thread and calls self.redraw.

        @param graph: A network graph
        @type graph: Graph

        @todo: See, that threading works correctly.
        '''
        logging.info("Drawing network...")

        self.graph = graph
        self.speciesNodesMapper = {}
        self.draw() # draws the current positions (may be None), creates Nodes/Edges

        # just testing a progress dialog
        #        progressDialog = QProgressDialog()
        #        progressDialog.setMinimum(0)
        #        progressDialog.setMaximum(100)
        #        progressDialog.show()
        #
        #        for i in range(100):
        #          time.sleep(0.2)
        #          progressDialog.setValue(i)
        self.positions = {}

        #        time.sleep(0.5)
        #
        #        dummyThread = DummyProgressThread()
        #        #dummyThread = DummyThrobberThread()
        #        progressService = ProgressBarService()
        #        progressService.connectToThread(dummyThread)
        #        dummyThread.start()

        # doing the layout
        threadedLayouter = LayoutThread(self.lock, self)

        self.connect(threadedLayouter, SIGNAL("finished(bool)"), self.layout_finished)
        #threadedLayouter.finished.connect(self.layout_finished)
        threadedLayouter.initialize(self.graph, "spring", self.positions)
        threadedLayouter.start()
#        threadedLayouter.run() # for debugging purposes


    def createEdge(self, graphEdge):
        '''
        Creates a graphical Edge given a networkX edge (which is basically
        a 3-tuple with ([reactants],[products],{"reaction": wrappedReaction}).
        '''
        species1 = graphEdge[0]
        species2 = graphEdge[1]
        try:
            reactionWrapper = graphEdge[2]["reaction"]
        except:
            pass
        sourceNode = self.speciesNodesMapper[species1]
        targetNode = self.speciesNodesMapper[species2]
        edge = Edge(sourceNode, targetNode, self.graphicsScene, wrappedObject=reactionWrapper)
        sourceNode.edges.append(edge)
        if reactionWrapper is not None:
            self.reactionEdgesMapper[edge] = reactionWrapper # 1 Edge corresponds to exactly 1 Reaction
            if reactionWrapper in self.reactionEdgesMapper:  # 1 Reaction can correspond to n Edges
                self.reactionEdgesMapper[reactionWrapper].append(edge)
            else:
                self.reactionEdgesMapper[reactionWrapper] = [edge]
        return edge

    def draw(self):
        self.isRedrawing = True

        self.graphicsScene.clear()
        #
        self.nodes = []
        self.speciesNodesMapper = {}
        self.reactionEdgesMapper = {}

        for speciesOrHyperNode in self.graph.nodes():
            (x, y) = speciesOrHyperNode.Position
            node = self.createNode(speciesOrHyperNode, x, y)


        for edge in self.graph.edges(data=True):
            edge = self.createEdge(edge)

        logging.info("Finished drawing network...")

        self.isRedrawing = False


    def layout_finished(self, finished):
        '''
        This is a slot. It calls self.redraw if finished = true.

        @param finished: Tells if the layout is finished.
        @type finished: bool
        '''
        if finished:
            for speciesOrHyperNode in self.graph.nodes(): # setting the updated coordinates
                (xRel, yRel) = self.positions[speciesOrHyperNode]
                x = xRel * self.width() / 2
                y = yRel * self.height() / 2
                speciesOrHyperNode.Position = (x, y)
            self.redraw()

    def redraw(self):
        '''
        Rewrite of the previous redraw approach. It is based on the node positions
        as stored in the SBMLEntitys' Position property.
        Nodes and Edges are only created once (on drawGraph). They are not
        recreated here, only repositioned.

        @since: 2010-09-20
        '''
        self.isRedrawing = True
        for speciesOrHyperNode in self.graph.nodes():
            (x, y) = speciesOrHyperNode.Position
            if speciesOrHyperNode not in self.speciesNodesMapper:
                logging.debug("Encountered unknown node while redrawing. %s" % speciesOrHyperNode)
                continue
                #self.addNode(speciesOrHyperNode)
            node = self.speciesNodesMapper[speciesOrHyperNode]
            node.isRedrawing = True
            node.setPos(x, y)
            node.isRedrawing = False


        self.isRedrawing = False

    def addNode(self, node):
        if type(node) is not HyperEdgeNode:
            x = self.width()/2
            y = self.height()/2
        else:
            x, y = self.calculateHyperNodePosition(node)

        self.createNode(node, x, y)


    def calculateHyperNodePosition(self, hyperNode):
        '''
        Gets the positions of node adjacent to the given hyper node
        and calculates an average position between them.
        '''
        #edges = self.graph.edges([hyperNode], data=True)
        neighbors = self.graph.neighbors(hyperNode)
        x = 0
        y = 0
        for neighbor in neighbors:
            currX,currY = neighbor.Position
            x += currX
            y += currY
        x /= len(neighbors)
        y /= len(neighbors)

        return x,y

    def registerSignals(self):
        '''
        Connects all the necessary signals.
        '''
        self.connect(self.graphicsScene, SIGNAL("selectionChanged()"), self.sceneSelectionChanged)

        
        
    def findItemInModel(self, item):
        '''
        Finds the QModelIndex corresponding to the given
        item. The given item is a Node or Edge.
        
        @param item: The item to find
        @type item: SBMLEntity
        
        @return: The model index of the given item
        @rtype: QModelIndex
        '''
        
        sbmlEntity = item.wrappedObject
        map = self.model().modelIndexToEntityMap
        
        if map is None:
            return
        
        if sbmlEntity in map:
            index = map[sbmlEntity]
            return index
        
        #print sbmlEntity
        
        
        
    def changeViewSelection(self, modelSelection, state):
        '''
        Gets a Qt selection object and works through it to
        set the given selection state on all the affected items.
        This syncs the selection (Model)View -> NetworkView
        
        @param modelSelection: A Qt selection consisting of indexes
        @todo: Include type of modelSelection in doc
        '''
        #self.setSelectedAll(False)
        for selectionRange in modelSelection:
            #logging.debug("Creating View selection for %s items" % len(selectionRange.indexes()))
            for itemIndex in selectionRange.indexes():
                item = itemIndex.internalPointer()
                #if item in self.speciesNodesMapper:
                try:    # fast then "if item in"
                    self.speciesNodesMapper[item].setSelected(state)
                except:
                    try:
                        
                #elif item in self.reactionEdgesMapper:
                # item will be a list for all the Edges that this Reaction
                # potentially has (in case of hyper-edge)
                        for edge in self.reactionEdgesMapper[item]:
                            edge.setSelected(state)
                    except:
                        pass
                                
        
        #return itemIndex, edge, selectionRange, item
        
        
    def setSelectedAll(self, state):
        self.setSelectedNodes(state)
        self.setSelectedEdges(state)
        
    def setSelectedNodes(self, state):
        for node in self.nodes:
            node.setSelected(state)
            
    def setSelectedEdges(self, state):
        for edge in self.edges:
            edge.setSelected(state)
        
    
    def createNode(self, speciesOrHyperNode, x, y):
        speciesOrHyperNode.Position = (x,y)
        node = Node(position=(x, y), scene=self.graphicsScene, wrappedObject=speciesOrHyperNode)
        self.speciesNodesMapper[speciesOrHyperNode] = node
        self.speciesNodesMapper[node] = speciesOrHyperNode

        if type(speciesOrHyperNode) == HyperEdgeNode:
            self.speciesNodesMapper[speciesOrHyperNode.Reaction] = node # to get from the wrapped reaction to the node
#        self.connect(speciesOrDummyNode, SIGNAL("PositionChanged"), lambda who = speciesOrDummyNode: self.nodeMoved(who))
        return node

    def removeSpeciesNode(self, sbmlEntity):
#        logging.debug("Remove Entity from NetworkView: %s\n\ID: %s" % (sbmlEntity.Item, sbmlEntity.getId()))
        if sbmlEntity in self.speciesNodesMapper:
            node = self.speciesNodesMapper[sbmlEntity]
            self.graphicsScene.removeItem(node)
            self.speciesNodesMapper.pop(sbmlEntity)
#        else:
#            print "Remove Entity from NetworkView: %s\n\ID: %s" % (sbmlEntity.Item, sbmlEntity.getId())
#            print


    def removeReaction(self, reaction):
        #for reaction in reactions:
        if not self.reactionEdgesMapper.has_key(reaction):
            return
        
        edges = self.reactionEdgesMapper[reaction]
        for edge in edges:
            # handle nodes that are connected to this Edge
            nodes = [edge.sourceNode, edge.targetNode]
            for node in nodes:
                if edge in node.edges:
                    node.edges.remove(edge)

            # handle the Edge itself
            self.graphicsScene.removeItem(edge)
            self.reactionEdgesMapper.pop(edge) # just remove it from the dict

        self.reactionEdgesMapper.pop(reaction)

        # reactions are also linked to hypernodes; clear this, too
        if reaction in self.speciesNodesMapper.keys():
            hyperNode = self.speciesNodesMapper[reaction]
            self.speciesNodesMapper.pop(reaction)
            self.graphicsScene.removeItem((hyperNode))
            self.speciesNodesMapper.pop(hyperNode)


    def addReaction(self, edge):
        self.createEdge(edge)

    def updateNodesAndEdges(self):
        '''
        Works through the graph and adds missing Nodes and Edges.

        @since: 2010-10-04
        '''
        # handling Nodes
        for node in self.graph.nodes():
            if node not in self.speciesNodesMapper.keys():
                self.addNode(node)

        # handling Edges
        for edge in self.graph.edges(data=True):
            reaction = edge[2]["reaction"]
            if not reaction:
                continue
            if reaction not in self.reactionEdgesMapper.keys():
                # reaction is totally new, just create this edge
                self.createEdge(edge)
            else:
                # have to check if the reaction is already there, but maybe
                # with a different edge (happens in the case of hyper-edges)

                reactionEdges = self.reactionEdgesMapper[reaction]
                edgeIsThere = False
                for existingEdge in reactionEdges:    # we have to compare based on source and target nodes
                    source = existingEdge.sourceNode.wrappedObject
                    target = existingEdge.targetNode.wrappedObject
                    reactionSource = edge[0]
                    reactionTarget = edge[1]
#                    if reactionSource == source:
#                        logging.debug("Source is identical")
#                    if reactionTarget == target:
#                        logging.debug("Target is identical")
#                    if reactionSource == source and reactionTarget == target:
#                        logging.debug("Edge is there")
                    if reactionSource == source and reactionTarget == target:
                        edgeIsThere = True

                if not edgeIsThere:
                    self.createEdge(edge)
                    # some debugging info
#                    logging.debug("About to add an edge between...")
#                    logging.debug("Source: %s" % edge[0].getId())
#                    logging.debug("Target: %s" % edge[1].getId())
#                if edge not in reactionEdges:
#                    edge = self.createEdge(edge)


        
    #==========================================================================
    # Slots
    #==========================================================================
    
    @Slot()
    def sceneSelectionChanged(self):
        '''
        C++: void sceneSelectionChanged()
        
        This syncs the selection 
        NetworkView -> (Model)View
        To do this it uses the QSelectionModel that the ModelController
        has as a reference.
        '''
        if self.modelSelectionInProgress:   # don't create an selection update loop
            return
        
        itemSelection = QItemSelection()
        selectionModel = self.controller.getGlobalSelectionModel()

        if not self.graphicsScene:
            return

        selectedItems = self.graphicsScene.selectedItems()
        #logging.debug("Creating model selection for %s items" % len(selectedItems))
        for item in selectedItems:
            index = self.findItemInModel(item)
            if index is not None:
                itemSelection.select(index, index)
            
        selectionModel.select(itemSelection, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        
        
        
    @Slot(QModelIndex)
    def update(self, index):
        '''
        C++: void update(const QModelIndex&)
        '''
        pass
        
    @Slot(QModelIndex, QModelIndex)
    def dataChanged(self, topLeftIndex, bottomRightIndex):
        '''
        C++: void dataChanged(const QModelIndex&,const QModelIndex&)
        
        Gets the range of changed indexes and updates all the nodes
        therein.
        
        Currently, only the topLeftIndex is used. The possible span
        of indexes is ignored.
        
        @todo: Use whole span of indexes.
        
        @param topLeftIndex: Starting index
        @type topLeftIndex: QModelIndex
        @param bottomRightIndex: Ending index
        @type bottomRightIndex: QModelIndex
        '''
        
        item = topLeftIndex.internalPointer()
        if item is None:
            return
        
        if item not in self.speciesNodesMapper:
            return
        
        node = self.speciesNodesMapper[item]
        if node is None:
            return
        
        node.redraw()
        

    #==========================================================================
    # base class methods that we override to enable the binding of the model 
    # (selection, etc.) to the GraphicsView
    #==========================================================================
        


    def selectionChanged(self, currentSelection, previousSelection):
        self.modelSelectionInProgress = True
        self.changeViewSelection(previousSelection, False)
        self.changeViewSelection(currentSelection, True)
        self.modelSelectionInProgress = False
            
        
        
    #==========================================================================
    # abstract base classes that need to be implemented but that we don't 
    # really use (maybe some of them later?)
    #==========================================================================
    
    def indexAt(self, point):
        return QModelIndex()
    
    def moveCursor(self, cursorAction, modifiers):
        return QModelIndex()
        
    def verticalOffset(self):
        return 0
    
    def horizontalOffset(self):
        return 0
    
    def visualRegionForSelection(self, selection):
        return QRegion()
    
    def visualRect(self, index):
        return QRect()
    
    def scrollTo(self, index, hint):
        pass



        