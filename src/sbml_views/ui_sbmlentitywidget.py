# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\sbml_views\sbmlentitywidget.ui'
#
# Created: Tue Sep 20 10:15:24 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
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
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonAdd = QtGui.QToolButton(SBMLEntityWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/editadd"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAdd.setIcon(icon)
        self.buttonAdd.setObjectName("buttonAdd")
        self.horizontalLayout.addWidget(self.buttonAdd)
        self.buttonRemove = QtGui.QToolButton(SBMLEntityWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/editdelete"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonRemove.setIcon(icon1)
        self.buttonRemove.setObjectName("buttonRemove")
        self.horizontalLayout.addWidget(self.buttonRemove)
        self.buttonCopy = QtGui.QToolButton(SBMLEntityWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/editcopy"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonCopy.setIcon(icon2)
        self.buttonCopy.setObjectName("buttonCopy")
        self.horizontalLayout.addWidget(self.buttonCopy)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(SBMLEntityWidget)
        QtCore.QMetaObject.connectSlotsByName(SBMLEntityWidget)

    def retranslateUi(self, SBMLEntityWidget):
        SBMLEntityWidget.setWindowTitle(QtGui.QApplication.translate("SBMLEntityWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEntityTree.setText(QtGui.QApplication.translate("SBMLEntityWidget", "Entity Tree", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAdd.setText(QtGui.QApplication.translate("SBMLEntityWidget", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRemove.setText(QtGui.QApplication.translate("SBMLEntityWidget", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCopy.setText(QtGui.QApplication.translate("SBMLEntityWidget", "Duplicate", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
