# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/odehandling/ODEViewer.ui'
#
# Created: Tue Jul 17 14:29:55 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ODEViewer(object):
    def setupUi(self, ODEViewer):
        ODEViewer.setObjectName("ODEViewer")
        ODEViewer.resize(920, 553)
        self.horizontalLayout = QtGui.QHBoxLayout(ODEViewer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtGui.QPlainTextEdit(ODEViewer)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans Mono")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.buttonBox = QtGui.QDialogButtonBox(ODEViewer)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.actionGenerateODEs = QtGui.QAction(ODEViewer)
        self.actionGenerateODEs.setObjectName("actionGenerateODEs")

        self.retranslateUi(ODEViewer)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), ODEViewer.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), ODEViewer.reject)
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

