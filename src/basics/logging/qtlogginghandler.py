import logging
from PySide.QtCore import QMutex, QMutexLocker

class QtLoggingHandler(logging.Handler):
    """
    This is a handler for the built-in python logging
    facilities that enables logging to a Qt class
    like QPlainTextEdit.

    @param widget: The widget to which to log to. Has to support .append()
    @type widget: A suitable QWidget (with .append())

    @since: 2010-03-01
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"
    
    
    def __init__(self, widget):
        logging.Handler.__init__(self)
        
        self.widget = widget
        self.mutex = QMutex()
        
        self.formatter = logging.Formatter("%(levelname)s | %(message)s")
        

    def emit(self, record):
        with QMutexLocker(self.mutex):
            self.widget.append(self.formatter.format(record))



