'''
Created on Mar 4, 2010

@author: bzfwadem
'''
from basics.threadbase import BioParkinThreadBase

class BaseBackend(BioParkinThreadBase):
    '''
    This serves as an Interface definition
    for classes that help to connect to
    with an Integrator.

    @since: 2010-03-04
    '''
  
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

#    statusUpdate = QtCore.Signal(str, int)

    def __init__(self):
        '''
        Do parameterless initialization here (in inheriting classes).
        '''
        super(BaseBackend, self).__init__()
        self.statusBar = None
      
        
    def initialize(self, model):
        '''
        Do data- and parameter-dependent initialization here.
        '''
        raise NotImplementedError, "Do data- and parameter-dependent initialization here." 

#    def setStatusBar(self, statusBar):
#        self.statusBar = statusBar
#
#    def setStatus(self, msg, time = None):
#        if time:
#            self.statusBar.showMessage(msg, time)
#        else:
#            self.statusBar.showMessage(msg)


#    def setStatus(self, msg, time = None):
#        '''
#        Emits the L{statusUpdate} Signal with status text and (optionally)
#        time (e.g. to display status bar update and/or progress bar).
#        '''
#        if time:
#            self.statusUpdate.emit(msg, time)
#        else:
#            self.statusUpdate.emit(msg, -1)

    
    def run(self):
        '''
        Calls the integrate method. This run() method is called internally when invoking
        this thread's start method. Don't call run() directly!
        '''
        self._compute()
        
    def _compute(self):
        '''
        This is an abstract method that has to be implemented in children classes.

        Please, remember to report progress via the inherited BioParkinThreadBase's methods.
        '''
        raise NotImplementedError, "Please implement this abstract method in inheriting classes."

#    def testCompute(self):
#        self.start(QThread.LowestPriority)
    