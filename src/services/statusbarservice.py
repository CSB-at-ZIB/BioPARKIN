from PySide.QtCore import  QMutex, QMutexLocker
from PySide.QtGui import QWidget

class StatusBarService(QWidget):
    """
    This class provides a "service" (realized as a Singleton) that should be used whenever
    any method anywhere inside BioPARKIN wants to write something to the status bar.
    That way, this class can (or, rather, tries to) ensure thread safety (by locking) and so on.

    @since: 2011-05-18
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    _instance = None

    def __new__(cls, *args, **kwargs): # making this a Singleton, always returns the same instance
        if not cls._instance:
            cls._instance = super(StatusBarService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, statusbar=None):
        """
        The constructor takes the QStatusBar that this service will wrap.
        """
        if statusbar:
            self.statusbar = statusbar  # needs to be provided when first (!) instantiated
        self.mutex = QMutex()

    def setStatusBar(self, statusBar):
        self.statusbar = statusBar


    ######### "Interface" methods to give the needed API compatibility with QStatusBar #######

    def showMessage(self, msg, time=5000):
        """
        Pass the given message on to the wrapped QStatusBar.
        Use a QMutex lock so that only one client of this service can write to the status bar
        at the same time.
        """
        with QMutexLocker(self.mutex):
            if self.statusbar:
                self.statusbar.showMessage(msg, time)

    def addPermanentWidget(self, widget):
        """
        Places the given widget on the wrapped QStatusBar.
        """
        with QMutexLocker(self.mutex):
            if self.statusbar:
                self.statusbar.addPermanentWidget(widget)

    #############################################################################################


    