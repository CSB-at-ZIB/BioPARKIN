from PySide.QtCore import QObject, Signal, SIGNAL
from contrib.singletonmixin import Singleton

class Mediator(QObject):
    appendWarningSignal = Signal(str, str)
    setWarningSignal = Signal(str, str)
    def __init__(self):
        super(Mediator, self).__init__()
    

class WarningService(Singleton):
    """
    Whenever some part of the program wants to display (extensive) warnings
    to the user, it can do so with this service.

    @since: 2011-05-20
    """

    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"

    def __init__(self):
        super(WarningService, self).__init__()
        self._mediator = Mediator()

    def appendWarning(self, warning, description=None):
        """
        Append a warning to the existing warnings without
        clearing previous warnings. This is the normal way to use this
        service.

        If a description is given, it will displayed to the user instead
        of a generic "there are warnings" message.
        """
        self.appendWarningSignal.emit(warning, description)
        

    def setWarning(self, warning, description=None):
        """
        Clears previous warnings and set this warning as the only one.

        If a description is given, it will displayed to the user instead
        of a generic "there are warnings" message.
        """
        self.setWarningSignal.emit(warning, description)


    # This way of defining properties looks crazy, but it works!
    # taken from: http://kedeligdata.blogspot.com/2010/01/pyqt-emitting-events-from-non-qobject.html
    # This effectively hides the fact that the SIGNALS are not defined within this class
    # but within the Mediator. This circumvents problems with multiple-inheritance
    # and inheriting from QObject.

    def appendWarningSignal():
        def fget(self):
            return self._mediator.appendWarningSignal
        return locals()

    appendWarningSignal = property(**appendWarningSignal())

    def setWarningSignal():
        def fget(self):
            return self._mediator.setWarningSignal
        return locals()

    setWarningSignal = property(**setWarningSignal())
            

  