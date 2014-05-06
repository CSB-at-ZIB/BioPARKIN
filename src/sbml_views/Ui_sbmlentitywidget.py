# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/sbml_views/sbmlentitywidget.ui'
#
# Created: Mon Sep  9 14:28:37 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SBMLEntityWidget(object):
    def setupUi(self, SBMLEntityWidget):
        SBMLEntityWidget.setObjectName("SBMLEntityWidget")
        SBMLEntityWidget.resize(421, 438)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SBMLEntityWidget.sizePolicy().hasHeightForWidth())
        SBMLEntityWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(SBMLEntityWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelEntityTree = QtGui.QLabel(SBMLEntityWidget)
        self.labelEntityTree.setObjectName("labelEntityTree")
        self.verticalLayout.addWidget(self.labelEntityTree)
        self.treeView = QtGui.QTreeView(SBMLEntityWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)

        self.retranslateUi(SBMLEntityWidget)
        QtCore.QMetaObject.connectSlotsByName(SBMLEntityWidget)

    def retranslateUi(self, SBMLEntityWidget):
        SBMLEntityWidget.setWindowTitle(QtGui.QApplication.translate("SBMLEntityWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEntityTree.setText(QtGui.QApplication.translate("SBMLEntityWidget", "Entity Tree", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SBMLEntityWidget = QtGui.QWidget()
    ui = Ui_SBMLEntityWidget()
    ui.setupUi(SBMLEntityWidget)
    SBMLEntityWidget.show()
    sys.exit(app.exec_())

