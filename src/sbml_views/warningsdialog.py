import logging
from PySide.QtCore import Slot
from PySide.QtGui import QDialog, QIcon, QPixmap
from services.statusbarservice import StatusBarService
from sbml_views.ui_warningsdialog import Ui_WarningsDialog

class WarningsDialog(QDialog, Ui_WarningsDialog):
    """
    This is the Controller (more in the line of a code-behind file)
    for the small Warnings Dialog.

    The UI is handled separately by QT Designer 4 with the
    *.ui file.

    @since: 2011-05-20
    """
    __author__ = "Moritz Wade"
    __contact__ = "wade@zib.de"
    __copyright__ = "Zuse Institute Berlin 2011"


    def __init__(self, parent=None, warningAction=None, warningService=None):
        """
        Constructor

        @param parent: Qt widget parent of this dialog window
        @type parent: QWidget

        @param warningAction: The action to connect to.
        @type warningAction: QAction
        """
        super(WarningsDialog, self).__init__(parent)
        self.setupUi(self)

        self.setWarningAction(warningAction)
        self.setWarningService(warningService)

        self.statusBarService = StatusBarService()

        self.errorString = ""
        self.errorMsgTextEdit.setPlainText(self.errorString)


        self.iconWarning = QIcon()
        self.iconWarning.addPixmap(QPixmap(":/tango-status-32px/images/tango-icon-theme/32x32/status/weather-severe-alert.png"), QIcon.Normal, QIcon.Off)

        self.iconNoWarning = QIcon()
        self.iconNoWarning.addPixmap(QPixmap(":/tango-status-32px/images/tango-icon-theme/32x32/status/weather-clear.png"), QIcon.Normal, QIcon.Off)

    def setWarningAction(self, warningAction):
        """
        Sets the warning QAction (for setting icons and to connect to
        its triggered SIGNAL to show self).
        """
        self.warningAction = warningAction
        self._connectToWarningAction()

    def setWarningService(self, warningService):
        """
        Sets the WarningService (to whose SIGNALs to listen to).
        """
        self.warningService = warningService
        self._connectToWarningService()

    def updateWarnings(self, errorString, desc):
        """
        Having updated the errorString elsewhere,
        this method updates the error string in the UI and
        sets the correct warning icon.
        """
        self.errorString = errorString
        self.errorMsgTextEdit.setPlainText(self.errorString)
        if self.warningAction:
        # todo: figure out how to use the tooltip to show desc
        #            self.warningAction.setToolTip(desc)

            self.warningAction.setIcon(self.iconWarning)

        if not desc:
            desc = "There are new warnings. Open the Warnings Window to see them."
        logging.info(desc)

    @Slot(str, str)
    def appendWarning(self, msg, desc):
        """
        Public slot to append a warning to the list of warnings.
        Usually, this is called by the WarningsService.
        """
        errorString = "%s\n%s" % (self.errorString,msg)
        self.updateWarnings(errorString, desc)
    
    @Slot(str, str)
    def setWarning(self, msg, desc):
        """
        Public slot to clear all warnings and send this one as the only one.
        Usually, this is called by the WarningsService.
        """
        errorString = msg
        self.updateWarnings(errorString, desc)

    def _connectToWarningAction(self):
        if self.warningAction:
            self.warningAction.triggered.connect(self._showDialog)
            
    def _showDialog(self):
        self.show()
        scrollBar = self.errorMsgTextEdit.verticalScrollBar()
        scrollBar.setValue(scrollBar.maximum())
        if self.warningAction:
            # set no warning icon
            self.warningAction.setIcon(self.iconNoWarning)

    def _connectToWarningService(self):
        if self.warningService:
            self.warningService.appendWarningSignal.connect(self.appendWarning)
            self.warningService.setWarningSignal.connect(self.setWarning)

