
#from PySide.QtCore import *
#from services.progressbarservice import ProgressBarService
from PySide.QtCore import QThread, Signal, QMutexLocker, QMutex

class BioParkinThreadBase(QThread):
    """
    This class is based on QThread and is thought to act as an intermediate
    layer to make it easy to write custom thread-based classes that report
    their progress to the UI.

    @since: 2010-03-04
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    finishedSignal = Signal(str)
    startWithoutProgressSignal = Signal(str)
    startWithProgressSignal = Signal(str)
    progressMinimumSignal = Signal(int)
    progressMaximumSignal = Signal(int)
    progressValueSignal = Signal(int)
    progressTextSignal = Signal(str)
    
    
    def __init__(self):
        """
        Remember to call this initializer in inheriting classes.

        You should connect this thread to the ProgressBarService via
        its connect_to_thread() method.
        """
        super(BioParkinThreadBase, self).__init__()

        #debugging
#        self.finishedSignal.connect(self.onSignalTest)

        # Connect to BioParkin's ProgressBarService
#        progressService = ProgressBarService()
#        if progressService is not None:
#          progressService.connect_to_thread(self)
          
        # setting up some instance variables that might
        # help to get the current progress status when needed
        self._progressMin = None
        self._progressMax = None
        self._lastProgressValue = None
        self._lastProgressInfo = None
        self._canGiveProgressValues = False
        self._progressMutex = QMutex()

#    def onSignalTest(self, msg):
#        ''' For Debugging purposes only. '''
#        print("BioParkinThreadBase: Signal received: %s" % msg)

    
    def run(self):
        """
        Override this method to use the QThread features.
        """
        raise NotImplementedError, "Do the main stuff here..."


#    def connectFinishedSignal(self, callable):
#        ''' Helper method to connect the finished Signal to some callable.
#        Sometimes this doesn't work correctly when trying to use signal.connect()
#        in some distant daughter class of this one. '''
#        self.finishedSignal.connect(callable)
      
    #=============================================================================
    # Use the following methods for reporting progress
    # (or reporting that the thread is running without
    # actual % progress information)!
    #=============================================================================
        
    def start_progress_report(self, canGiveProgressValues, text = None):
        """
        Start the progress report. Receives information about the type
        of this progress report (with % progress values or without).

        @param canGiveProgressValues: True, if the caller will give progress percentage updates.
        @type canGiveProgressValues: bool

        @param text: Optional message for the progress UI (e.g. status bar)
        @type text: str
        """
        with QMutexLocker(self._progressMutex):
            self._canGiveProgressValues = canGiveProgressValues
            #print "in start_progress_report()"
        if canGiveProgressValues:
#            self.emit(SIGNAL("startWithProgress(QString)"), text)
            self.startWithProgressSignal.emit(text)
        else:
            #print "emitting startWithoutProgress(QString)"
            #print "text: %s" % text
#            self.emit(SIGNAL("startWithoutProgress(QString)"), text)
            self.startWithoutProgressSignal.emit(text)
    
    def set_progress_range(self, min, max):
        """
        If the caller wants to give continuous progress information,
        the progress range (min and max values) should be provided.

        @param min: Minimum progress value (= 0%)
        @type min: float

        @param max: Maximum progress value (= 100%)
        @type max: float
        """
        with QMutexLocker(self._progressMutex):
            self._progressMin = min
            self._progressMax = max
#        self.emit(SIGNAL("progressMinimum(int)"), min)
        self.progressMinimumSignal.emit(min)
#        self.emit(SIGNAL("progressMaximum(int)"), max)
        self.progressMaximumSignal.emit(max)


    def report_progress(self, value=None, text=None):
        """
        Used to set one status update from the caller. It gives the status
        value (in the range previously defined by self.set_progress_range())
        and an optional status text.

        @param value: Status value (in the min/max frame)
        @type value: float

        @param text: Status text for the progress UI (e.g. status bar)
        @type text: str
        """
        with QMutexLocker(self._progressMutex):
            self._lastProgressValue = value
            self._lastProgressInfo = text
        if value is not None:
#            self.emit(SIGNAL("progressValue(int)"), value)
            self.progressValueSignal.emit(value)
        if text is not None:
#            self.emit(SIGNAL("progressText(QString)"), text)
            self.progressTextSignal.emit(text)

    def report_status(self, msg):
        """
        Simply report a status without altering the progress ("% done").
        """
        if msg is not None:
            self.progressTextSignal.emit(msg)
      
    def stop_progress_report(self, text = None):
        """
        Stops the progress reporting (used to disable/hide the UI, etc.).
        Optionally, a last status text can be given.

        @param text: Status text for the progress UI (e.g. status bar)
        @type text: str
        """
        with QMutexLocker(self._progressMutex):
            self._lastProgressInfo = text
#        self.emit(SIGNAL("finished(QString)"), text)
            self.finishedSignal.emit(text)



    