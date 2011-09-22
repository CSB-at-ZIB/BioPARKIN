'''
Created on Feb 26, 2010

@author: moritz
'''
import libsbml
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui

from sbml_model.sbml_entities import SBMLEntity
from sbml_networkview.hyperedgenode import HyperEdgeNode
import logging

class Node(QtGui.QGraphicsEllipseItem):
    '''
    Represents a node in the GraphicsView. When drawing the (networkx) graph
    every wrapped Species is put into a Node to facilitate drawing.
    
    @param position: Position of the Node
    @type position: Tuple of x,y floats
    
    @param scene: The corresponding Scene
    @type scene: QGraphicsScene
    
    @param style: Drawing style/brush for the node
    @type style: QBrush
    
    @param rect: Defines the size of the Node
    @type rect: QRect
    
    @param matrix: A transformation matrix
    @type matrix: QMatrix
    
    @param wrappedObject: Object represented by this node
    @type wrappedObject: SBMLEntity
    
    @since: 2010-02-26
    '''


    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, position = None, scene = None, style = QtCore.Qt.SolidLine,
                 rect = None,
                 matrix = QtGui.QMatrix(),
                 wrappedObject = None):
        '''
        Setting flags. Setting the label. Setting the size of the Node.
        '''
        super(Node, self).__init__(scene = scene)
        

        self.isRedrawing = False
        self.edges = []

        if wrappedObject is None:
            return
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | 
                      QtGui.QGraphicsItem.ItemIsMovable | 
                      QtGui.QGraphicsItem.ItemIsFocusable |
                      QtGui.QGraphicsItem.ItemSendsGeometryChanges)


        self.wrappedObject = wrappedObject #if wrappedObject is not None else None
        
        #if wrappedObject is not None and type(wrappedObject) is not str:
        wrappedObject.GraphicItem = self


        #if wrappedObject is not None and type(wrappedObject) is str:
        if type(wrappedObject) is HyperEdgeNode:
            self.isDummyNode = True
        else:
            self.isDummyNode = False

        if rect == None:
            self.size = 30 if not self.isDummyNode else 2
            self.setRect(QtCore.QRectF(0 - self.size / 2, 0 - self.size / 2, self.size, self.size))
        else:
            self.setRect(rect)

        # TODO: Make the following if statement less awkward
        if wrappedObject is not None and type(wrappedObject) is SBMLEntity and type(wrappedObject.Item) is libsbml.Species:
            self.species = wrappedObject.Item
            self.nodeTextItem = QtGui.QGraphicsTextItem(self.species.getName(), parent = self)
            #self.nodeTextItem.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations)
            self.nodeTextItem.setPos(-self.size / 2, self.size / 2)

        self.setBrush(QtGui.QColor(120,120,200))
        self.setZValue(100)

        self.style = style  
        self.setPos(position[0], position[1])
        self.setMatrix(matrix)

        
        #self.connect(wrappedObject, QtCore.SIGNAL("changed()"), self.redraw)

    def redraw(self):
        '''
        Redrawing primarily revolves around updating the label to correspond
        to the Name of the wrapped SBMLEntity
        '''
        if self.wrappedObject is not None and type(self.wrappedObject) is SBMLEntity and type(self.wrappedObject.Item) is libsbml.Species:
            if self.nodeTextItem is None:
#            self.nodeTextItem.setParentItem(None)
#            del self.nodeTextItem
                self.species = self.wrappedObject.Item
                self.nodeTextItem = QtGui.QGraphicsTextItem(self.species.getName(), parent = self)
                self.nodeTextItem.setPos(-self.size / 2, self.size / 2)
            else:
                self.nodeTextItem.setPlainText(self.species.getName())

    def get_parent_widget(self):
        '''
        Hack to get to the parent widget by taking the corresponding
        Scene's first View.
        '''
        return self.Scene().views()[0]


# This is now done in self.itemChange (where it should be)
#    def mouseMoveEvent(self, event):
#        '''
#        Overriding the mouse move event so that not only the Node moves
#        but also the adjacent Edges.
#        
#        @param event: The mouse move event
#        @type event: QEvent
#        '''
#        super(Node, self).mouseMoveEvent(event)   # provides basic movement
#        for edge in self.edges:
#            edge.update()

    def itemChange(self, change, value):
        '''
        Overriding itemChange to handle the selection state change by
        calling .selectionChange on the wrapped SBMLEntity.
        
        @param change: A QGraphicsItem change object
        
        @param value: The new value after the change
        @type value: QObject
        
        @return: The value is passed through.
        '''
        #super(Node, self).itemChange(change,value)
        if change == QtGui.QGraphicsItem.ItemSelectedChange and type(self.wrappedObject) is not str:
            self.wrappedObject.on_selectionChange(value)
        elif change == QtGui.QGraphicsItem.ItemPositionChange and type(self.wrappedObject) is not str:
            if not self.isRedrawing:
                #logging.debug("Setting node position to x: %s \ty: %s" % (value.x(), value.y()))
                self.wrappedObject.Position = (value.x(), value.y())
            for edge in self.edges:
                edge.update()
            
        #print change
        return value
    
    def paint(self, painter, option, widget):
        '''
        Overriding the paint method to paint the Node with custom Pens
        and Brushes (especially for the selected state).
        '''
        #painter.setClipRect(option.exposedRect) #speeding up the painting
        
        #self.update_path()
        pen = QtGui.QPen(self.style) 
        pen.setColor(QtCore.Qt.black)
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.red)
        painter.setPen(pen)
        painter.setBrush(self.brush())  # brush is set in __init
        painter.drawEllipse(self.rect())
        
        
    #def setText(self, text):
        