# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\sbml_views\entitytableview.ui'
#
# Created: Tue Sep 20 10:15:23 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_EntityTableView(object):
    def setupUi(self, EntityTableView):
        EntityTableView.setObjectName("EntityTableView")
        EntityTableView.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(EntityTableView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelEntityDetails = QtGui.QLabel(EntityTableView)
        self.labelEntityDetails.setObjectName("labelEntityDetails")
        self.verticalLayout.addWidget(self.labelEntityDetails)
        self.tableView = QtGui.QTableView(EntityTableView)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(EntityTableView)
        QtCore.QMetaObject.connectSlotsByName(EntityTableView)

    def retranslateUi(self, EntityTableView):
        EntityTableView.setWindowTitle(QtGui.QApplication.translate("EntityTableView", "EntityTableView", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEntityDetails.setText(QtGui.QApplication.translate("EntityTableView", "Entity Details", None, QtGui.QApplication.UnicodeUTF8))

