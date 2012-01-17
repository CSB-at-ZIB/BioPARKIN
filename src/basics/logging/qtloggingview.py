from PySide.QtCore import QMutex, QMutexLocker
from PySide.QtGui import QPlainTextEdit, QTextCursor

class QtLoggingView(QPlainTextEdit):
    """
    This simply subclasses QPlainTextEdit so that it can easily be used
    from within the QtLoggingHandler.

    It provides the .append() method needed by QtLoggingHandler.

    @param parent: The standard Qt UI parent
    @type parent: QWidget

    @since: 2010-03-01
    """
    
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2010"


    def __init__(self, parent):
        super(QtLoggingView, self).__init__(parent)
        #self.setEnabled(False)
        self.setReadOnly(True)
        self.mutex = QMutex()
    
    def append(self, text):
        """
        Adding the text to the PlainTextEdit widget
        and setting the cursor, so that the text is visible.
        """
        with QMutexLocker(self.mutex):
            self.appendPlainText(str(text))
            self.moveCursor(QTextCursor.EndOfBlock)
            self.ensureCursorVisible()


