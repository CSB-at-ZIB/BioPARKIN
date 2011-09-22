'''
Created on Mar 29, 2010

@author: bzfwadem
'''

from PySide.QtCore import QObject, SIGNAL
import PySide.QtGui

class HyperEdgeNode(QObject):
    '''
    A very simple class that is used to enable hyper edges
    in NetworkX graphs. 
    A hyper edge is an edge that connects more than two nodes.
    E.g. to display A+B => C visually, one needs a hyper edge.
    
    NetworkX does not support hyper edges. Thus, hyper edges are reprsented
    by introducing an actual node between the end points of the hyper edge.
    
    @param reaction: A wrapped SBML reaction
    @type reaction: SBMLEntity
    
    @param label: A label that can be drawn onto this special node
    @type label: str
    
    @since: 2010-03-29
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, reaction=None, label = None):
        '''
        Simple constructor.
        '''
        super(HyperEdgeNode, self).__init__()
        self.Reaction = reaction # might be helpful for some look ups
        self.Label = label
        self.GraphicItem = None # reference to graphic representation
        self.Position = (0.0, 0.0)
        
    def getId(self):
        return "Hypernode: %s" % self.Label
    
    def selectionChange(self, value):
        '''
        Emitting a signal when this method is invoked from the outside.
        '''
        self.emit(SIGNAL("selectionChange()"), self, value)

#    def itemChange(self, change, value):
#        '''
#        Overriding itemChange to handle the selection state change by
#        calling .selectionChange on the wrapped SBMLEntity.
#
#        @param change: A QGraphicsItem change object
#
#        @param value: The new value after the change
#        @type value: QObject
#
#        @return: The value is passed through.
#        '''
#        #super(Node, self).itemChange(change,value)
##        if change == QtGui.QGraphicsItem.ItemSelectedChange and type(self.wrappedObject) is not str:
##            self.wrappedObject.selectionChange(value)
#        #el
#        if change == QtGui.QGraphicsItem.ItemPositionChange and type(self.wrappedObject) is not str:
#            self.Position = (self.pos().x(), self.pos().y())
#            #todo: add edge management
##            for edge in self.edges:
##                edge.update()

        #print change
        return value