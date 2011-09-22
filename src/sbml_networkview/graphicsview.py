'''
Created on Apr 13, 2010

@author: bzfwadem
'''
#from PySide.QtGui import *
from PySide.QtGui import QGraphicsView, QPainter

class GraphicsView(QGraphicsView):
    '''
    A small wrapper around QGraphicsView for intercepting
    events like the scroll wheel.
    
    @param parent: The standard Qt parent
    @type parent: QObject
    
    @since: 2010-04-13
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, parent):
        '''
        Sets some flags.
        '''
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        
        
    def wheelEvent(self, event):
        '''
        Override the wheel event to support
        zooming.
        
        @param event: The wheel event
        @type event: QEvent 
        '''
        factor = 1.41 ** (event.delta() / 240.0)
        self.scale(factor, factor)