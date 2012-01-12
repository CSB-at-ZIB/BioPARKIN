
import logging, time
from PySide.QtCore import QObject, QMutex, QSize, QMutexLocker
from PySide.QtGui import QProgressBar, QLabel, QMovie
from basics.threadbase import BioParkinThreadBase

class ProgressBarService(QObject):
    """
    This service is initialized with a status bar upon which it sets
    a progress bar. Consumers of the service can then show/hide
    the progress bar and set values.

    The __new__ method is overridden to make this class a singleton.
    Every time it is instantiated somewhere in code, the same instance will be
    returned. In this way, it can serve like a static class.

    @param statusbar: The status bar on which to display progress.
    @type statusbar: QStatusBar (I think)

    @since: 2010-03-02
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    _instance = None

    def __new__(cls, *args, **kwargs): # making this a Singleton, always returns the same instance
        if not cls._instance:
            cls._instance = super(ProgressBarService, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, parent=None, statusBarService = None):
        """
        Creates a QProgressBar and adds it to the given status bar (for
        threads that can provide accurate progress information).

        Note: The status bar can either be a QStatusBar or the StatusBarService. In the default
        BioPARKIN use, it is the StatusBarService instance.

        @todo: A throbber is created and also added to the status bar (for
        threads that can only provide start/stop information).
        """
#        super(ProgressBarService, self).__init__(parent)   # done in __new__

        if statusBarService is not None:
            self.statusBarService = statusBarService
            self.progressBar = QProgressBar(None) # used for showing progress
            self.progressBarMutex = QMutex()
            self.progressBar.hide()
            self.statusBarService.addPermanentWidget(self.progressBar)
            self.progressRunning = False
    
    
            self.throbber = QLabel()
            self.throbberRunning = False
            self.throbberMutex = QMutex()
            self.statusBarService.addPermanentWidget(self.throbber)
            self.throbber.show()
            self.throbber.hide()

            throbberImage = QMovie(":/images/Spinning_wheel_throbber.gif", parent=self.throbber)
            throbberImage.setScaledSize(QSize(24, 24))
            throbberImage.setCacheMode(QMovie.CacheAll)
            throbberImage.start()
            self.throbber.setMovie(throbberImage)
            self.throbber.setFixedSize(24,24)


    def getStatusBar(self):
        """
        Gets the internal status bar (or StatusBarService)
        """
        return self.statusBarService
    
    def connect_to_thread(self, thread):
        """
        Connects standard BioParkinThreadBase SIGNALs to update methods.

        @param thread: Thread whose Signals to handle
        @type thread: BioParkinThreadBase
        """
        if thread is not None:
            self.thread = thread
            self.thread.startWithoutProgressSignal.connect(self.start_throbber)
            self.thread.startWithProgressSignal.connect(self.start_progress)
            self.thread.finishedSignal.connect(self.finish)
            self.thread.progressMinimumSignal.connect(self.setProgressBarMinimum)
            self.thread.progressMaximumSignal.connect(self.setProgressBarMaximum)
            self.thread.progressValueSignal.connect(self.setProgressBarValue)
            self.thread.progressTextSignal.connect(self.showMessage)

    def setProgressBarMinimum(self, min):
        """
        Uses a QMutexLocker to set the minimum value for the progress bar.
        """
        with QMutexLocker(self.progressBarMutex):
            self.progressBar.setMinimum(min)

    def setProgressBarMaximum(self, max):
        """
        Uses a QMutexLocker to set the maximum value for the progress bar.
        """
        with QMutexLocker(self.progressBarMutex):
            self.progressBar.setMaximum(max)

    def setProgressBarValue(self, value):
        """
        Uses a QMutexLocker to set the minimum value for the progress bar.

        This also implicitely "starts" the progress, e.g. show the ProgressBar.
        """
        self.progressRunning = True
        with QMutexLocker(self.progressBarMutex):
            self.progressBar.setValue(value)
            self.progressBar.show()
    
    def update(self, value, min=None, max=None, text = None):
        """
        Updates the progress bar with the given information.

        @param value: current value
        @type value: int

        @param min: Value that represents 0%
        @type min: int

        @param max: Value that represents 100%
        @type max: int

        @param text: Text to display on status bar
        @type text: str
        """
        #
        self.progressRunning = True
        with QMutexLocker(self.progressBarMutex):
            if min and max:
                self.progressBar.setRange(min, max)
            self.progressBar.setValue(value)
            self.progressBar.show()

        if text is not None:
            self.statusBarService.showMessage(text)
    
    
#    @Slot("QString")
    def finish(self, text = None):
        """
        This is a slot. It's called when a thread emits its "finished" Signal.

        The given text is posted to the status bar.

        @param text: Text for status bar
        @type text: str
        """
        if self.progressRunning:
            with QMutexLocker(self.progressBarMutex):
                self.progressBar.hide()
        if self.throbberRunning:
            with QMutexLocker(self.throbberMutex):
                self.throbber.hide()

        if text is None:
            self.statusBarService.showMessage("Finished", 1000)
        else:
            self.statusBarService.showMessage(text, 3000) # show finish message for 3 seconds

        self.thread = None  # release reference to thread

    def start_throbber(self, text = None):
        """
        This is a slot. It starts (the progress-state-less) throbber
        animation.

        The given text is posted to the status bar.

        @param text: Text for status bar
        @type text: str
        """
        with QMutexLocker(self.throbberMutex):
            self.throbber.show()
            self.throbberRunning = True

        if text is None:
            self.statusBarService.showMessage("Computing...")
        else:
            self.statusBarService.showMessage(text)
    
    
#    @Slot("QString")
    def start_progress(self, text = None):
        """
        This is a slot. It starts the progress animation.

        The given text is posted to the status bar.

        @param text: Text for status bar
        @type text: str
        """
        self.progressRunning = True
        with QMutexLocker(self.progressBarMutex):
            self.progressBar.show()
        
        if text is None:
            self.statusBarService.showMessage("Computing...", 1000)
        else:
            self.statusBarService.showMessage(text)

    def showMessage(self, text):
        if self.statusBarService:
            self.statusBarService.showMessage(text)


class DummyProgressThread(BioParkinThreadBase): #Test class
    """
    Just a small class to demonstrate the use of the
    ProgressBarService.

    Usage::
        dummyThread = DummyProgressThread()
        progressService = ProgressBarService()
        progressService.connect_to_thread(dummyThread)
        dummyThread.start()
    """
    STEPS = 50

    def run(self):

        self.startWithProgressSignal.emit("Computing something complicated...")
        self.progressMinimumSignal.emit(0)
        self.progressMaximumSignal.emit(self.STEPS-1)
        for i in range(self.STEPS):
            self.progressValueSignal.emit(i)
            text = "Running..."
            self.progressTextSignal.emit(text)
            time.sleep(0.05)

        finishedText = "Dummy Thread finished..."
        self.finishedSignal.emit(finishedText)
        logging.info(finishedText)


class DummyThrobberThread(BioParkinThreadBase): # test class
    """
    Just a small class to demonstrate the use of the
    ProgressBarService.

    Usage::
        dummyThread = DummyThrobberThread()
        progressService = ProgressBarService()
        progressService.connect_to_thread(dummyThread)
        dummyThread.start()
    """
    STEPS = 50
    def run(self):
        self.startWithoutProgressSignal.emit("Computing something complicated...")
        for i in range(self.STEPS):
          time.sleep(0.05)

        finishedText = "Dummy Thread finished..."
        self.finishedSignal.emit(finishedText)
        logging.info(finishedText)
