
import logging
from PySide.QtCore import QMutex, QObject, Signal

MESSAGE_DURATION = 1500

class StatusBarLoggingHandler(logging.Handler):
    """
    This is a handler for the built-in python logging
    facilities that enables logging to a status bar:
      - either directly to a QStatusBar (using an internal QMutexLocker)
      - or via  the StatusBarService (which should ensure thread safety)

    @param statusBar: The status bar to which to log to.
    @type statusBar: StatusBarService or QStatusBar

    @since: 2010-06-29
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"

    
    def __init__(self, statusBar=None):
        """
        Constructor sets up a QMutex (for logging directly to
        a QStatusBar) and a logging.Formatter.

        If no statusBar is given, it *has to be* set later via
        .setStatusBar()!
        """
        logging.Handler.__init__(self)

        self.signaller = StatusBarLoggingSignaller()
        
        self.statusBar = statusBar
        self.mutex = QMutex()

        self.formatter = logging.Formatter("%(message)s")

        if self.statusBar:
            self.signaller.messageSignal.connect(self.statusBar.showMessage)

        
    def setStatusBar(self, statusBar):
        """
        Sets the internal status bar reference.
        """
        self.statusBar = statusBar
        if statusBar:
            self.signaller.messageSignal.connect(self.statusBar.showMessage)
    
    def emit(self, record):
        """
        Log the record.
        """
        if not self.statusBar:
            return

        msg = str(self.formatter.format(record))
        self.signaller.messageSignal.emit(msg)



class StatusBarLoggingSignaller(QObject):
    """
    Use to inherit from QObject to access SIGNALs and SLOTs.
    """

    messageSignal = Signal(str)

    def __init__(self):
        QObject.__init__(self)
