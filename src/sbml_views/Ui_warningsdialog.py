# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/sbml_views/warningsdialog.ui'
#
# Created: Mon Sep  9 14:28:36 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_WarningsDialog(object):
    def setupUi(self, WarningsDialog):
        WarningsDialog.setObjectName("WarningsDialog")
        WarningsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        WarningsDialog.resize(520, 435)
        self.horizontalLayout = QtGui.QHBoxLayout(WarningsDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.errorMsgTextEdit = QtGui.QPlainTextEdit(WarningsDialog)
        self.errorMsgTextEdit.setObjectName("errorMsgTextEdit")
        self.horizontalLayout.addWidget(self.errorMsgTextEdit)

        self.retranslateUi(WarningsDialog)
        QtCore.QMetaObject.connectSlotsByName(WarningsDialog)

    def retranslateUi(self, WarningsDialog):
        WarningsDialog.setWindowTitle(QtGui.QApplication.translate("WarningsDialog", "Recent Warnings and Errors", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    WarningsDialog = QtGui.QDialog()
    ui = Ui_WarningsDialog()
    ui.setupUi(WarningsDialog)
    WarningsDialog.show()
    sys.exit(app.exec_())

