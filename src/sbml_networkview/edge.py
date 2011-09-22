'''
Created on Feb 26, 2010

@author: moritz
'''

import math
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
#import libsbml


class Edge(QtGui.QGraphicsPathItem):
    '''
    Represents an edge in a graph. In networkx edges do not have actually to
    be objects. They are just connections between nodes (themselves possibly
    any python object). In order to attach information to the edges, instances
    of Edge are used and attached as kind of property to the networkx edge.
    
    Because networkx does not support hyper-edges (connecting more than two 
    nodes), each Edge has exactly one source and one target Node. (Hyper-Edges 
    within the SBML data are represented using "dummy" nodes with the 
    HyperEdgeNode class.
    
    @param sourceNode: The source node
    @type sourceNode: Node
    @param targetNode: The target node
    @type targetNode: Node
    
    @param scene: The associated scene
    @type scene: QGraphicsScene
    
    @param style: A style for drawing the Edge
    @type style: QBrush
    
    @param matrix: A transformation matrix
    @type matrix: QMatrix
    
    @param wrappedObject: The actual Reaction that is represente by this Edge
    @type wrappedObject: SBMLEntity
    
    
    @since: 2010-02-26
    '''


    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"
    
    # TODO: wrap the sbmlEntity with the reaction inside the Edge object
    def __init__(self, sourceNode, targetNode, scene, style = QtCore.Qt.SolidLine, matrix = QtGui.QMatrix(), wrappedObject=None):
        '''
        Sets a lot of instance variables. Defines a standard Pen for drawing.
        '''
        super(Edge, self).__init__(scene = scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable |
                      #QtGui.QGraphicsItem.ItemIsMovable|
                      QtGui.QGraphicsItem.ItemIsFocusable)

        self.style = style
        self.setMatrix(matrix)
        self.sourceNode = sourceNode
        self.targetNode = targetNode
        self.wrappedObject=wrappedObject

        self.setZValue(150)
        self.setBrush(QtGui.QColor(80,80,80))
        pen = QtGui.QPen(QtGui.QColor(80,80,80))
        self.setPen(pen)

        self.update_path()


    def update_path(self):
        '''
        Updates self.line to correspond to correct source/target node
        coordinates.
        
        It also incorporates the arrows of the edges into self.line.
        '''
        self.set_line()
        l = self.line
        path = QtGui.QPainterPath(QtCore.QPointF(l.x1(), l.y1()))
        path.lineTo(l.x2(), l.y2())
        #path.cubicTo(l.x2(), l.y2()) # cubic when dummy nodes are involved?
        
        #draw arrow
        size = 25
        
        diffX = l.x1() - l.x2()
        diffY = l.y1() - l.y2()
        tangent = math.atan2(diffY, diffX)
        
        firstArrowPointX = size * math.cos(tangent + math.pi / 11) + l.x2()
        firstArrowPointY = size * math.sin(tangent + math.pi / 11) + l.y2()
        path.lineTo(firstArrowPointX, firstArrowPointY)
        
        secondArrowPointX = size * math.cos(tangent - math.pi / 11) + l.x2()
        secondArrowPointY = size * math.sin(tangent - math.pi / 11) + l.y2()
        path.lineTo(secondArrowPointX, secondArrowPointY)
        path.lineTo(l.x2(), l.y2())
        
        #path.setFillRule(QtCore.Qt.WindingFill)
        
        self.setPath(path)



    def get_parent_widget(self):
        '''
        A hack to get to the first View that is associated with self.scene
        '''
        return self.Scene().views()[0]


    def set_line(self):
        '''
        Very simple method to set self.line. It's used within the more
        complex self.update_path().
        '''
        self.line = QtCore.QLineF(self.sourceNode.pos(), self.targetNode.pos())

    def paint(self, painter, option, widget):
        '''
        Override the paint method to draw the line and change the appearance
        when selected (no ugly selection box which also slows everything down).
        '''
        
        #painter.setClipRect(option.exposedRect) #speeding up the painting
        
        self.update_path()
        
        pen = QtGui.QPen(self.style) 
        pen.setColor(QtCore.Qt.black)
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.red)
            painter.setBrush(QtCore.Qt.darkRed);
        else:
            painter.setBrush(QtCore.Qt.darkGray);
        #self.setPen(pen)
        painter.setPen(pen)
        #painter.drawLine(self.line)
        painter.drawPath(self.path())
        
        
#        super(Edge, self).paint(painter, option, widget)


    def redraw(self):
        '''
        Redraw the Edge (e.g. when the ID of the underlying reaction has
        changed). This is not necessary now, because the Edge does not 
        display any additional information (like the Reaction's ID).
        '''
        pass # for now

#class EdgeSpline(QtGui.QGraph):
#    
#    def __init__(self, sourceNode, targetNode, scene, style = QtCore.Qt.SolidLine, matrix = QtGui.QMatrix()):
        