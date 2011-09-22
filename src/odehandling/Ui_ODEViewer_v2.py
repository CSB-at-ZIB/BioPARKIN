# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/odehandling/ODEViewer_v2.ui'
#
# Created: Tue Aug  2 16:49:39 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ODEViewer(object):
    def setupUi(self, ODEViewer):
        ODEViewer.setObjectName(_fromUtf8("ODEViewer"))
        ODEViewer.resize(920, 553)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bitstream Vera Sans Mono"))
        ODEViewer.setFont(font)
        self.horizontalLayout = QtGui.QHBoxLayout(ODEViewer)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.plainTextEdit = QtGui.QPlainTextEdit(ODEViewer)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Bitstream Vera Sans Mono"))
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.buttonBox = QtGui.QDialogButtonBox(ODEViewer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.actionGenerateODEs = QtGui.QAction(ODEViewer)
        self.actionGenerateODEs.setObjectName(_fromUtf8("actionGenerateODEs"))

        self.retranslateUi(ODEViewer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ODEViewer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ODEViewer.reject)
        QtCore.QMetaObject.connectSlotsByName(ODEViewer)

    def retranslateUi(self, ODEViewer):
        ODEViewer.setWindowTitle(QtGui.QApplication.translate("ODEViewer", "ODE Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerateODEs.setText(QtGui.QApplication.translate("ODEViewer", "Generate ODEs", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ODEViewer = QtGui.QDialog()
    ui = Ui_ODEViewer()
    ui.setupUi(ODEViewer)
    ODEViewer.show()
    sys.exit(app.exec_())

