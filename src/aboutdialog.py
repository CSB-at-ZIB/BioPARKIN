from PySide.QtGui import QDialog
from Ui_aboutdialog_v2 import Ui_AboutDialog


class AboutDialog(QDialog, Ui_AboutDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setupUi(self)

        self.labelVersion.setText("Version %s" % parent.__version__)
