'''
Created on Apr 30, 2010

@author: bzfwadem
'''
import logging
from PySide.QtCore import QThread, QMutex, QMutexLocker, SIGNAL, QWriteLocker
import networkx

#from PySide.QtCore import *
#from PySide.QtGui import *

class LayoutThread(QThread):   # internal class
    '''
    Provides layouting mechanisms (using networkx)
    that run in a separate thread as not to clog up the UI thread.
    
    @param lock: A shared lock to sync access to the class using self
    @type lock: QReadWriteLock
    
    @param parent: The usual Qt parent
    @type parent: QObject (I think)
    
    
    @since: 2010-04-30 
    '''

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    def __init__(self, lock, parent = None):
        super(LayoutThread, self).__init__(parent)
        self.lock = lock
        self.stopped = False
        self.mutex = QMutex()
        self.completed = False

    
    def initialize(self, graph, layoutType, positions):
        self.stopped = False
        self.graph = graph
        self.layoutType = layoutType
        self.positions = positions # only used to pass as a reference and to use the data outside this thread
        self.completed = False
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stopped = True
    
    
    def is_stopped(self):
        with QMutexLocker(self.mutex):
            return self.stopped
    
    
    def run(self):
        self.layout_graph(self.graph, self.layoutType)
        self.stop()
        self.emit(SIGNAL("finished(bool)"), self.completed)

    def layout_graph(self, graph, type):#, positions):
        if len(graph.nodes()) < 1:
            logging.warning("Graph is empty, could not be layouted.")
            return 
        
        if type == "spring":
            with QWriteLocker(self.lock):
                #logging.info()
                try:
                    newPositions = networkx.spring_layout(graph, iterations=100, scale=2.5)
                except Exception, e:
                    logging.warning("Spring layout could not be computed. Exception: %s" % e)
                    logging.info("Drawing a random layout instead.")
                    newPositions = networkx.random_layout(graph)
                #logging.info(newPositions)

                #newPositions = networkx.spectral_layout(graph,scale=2.5)
                self.completed = True
                for key, value in newPositions.items(): # dict is unordered but that's no problem because we set references using the keys
                    self.positions[key] = value # we need to fill the reference with data, because we can not just set a new reference



    
            