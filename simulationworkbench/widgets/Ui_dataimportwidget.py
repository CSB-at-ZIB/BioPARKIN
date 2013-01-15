# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/simulationworkbench/widgets/dataimportwidget.ui'
#
# Created: Tue Jul 17 14:30:01 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DataImportWidget(object):
    def setupUi(self, DataImportWidget):
        DataImportWidget.setObjectName("DataImportWidget")
        DataImportWidget.resize(628, 405)
        self.horizontalLayout_4 = QtGui.QHBoxLayout(DataImportWidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtGui.QSpacerItem(58, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(20, 68, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(DataImportWidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem2 = QtGui.QSpacerItem(198, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lineEdit = QtGui.QLineEdit(DataImportWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.buttonBrowse = QtGui.QPushButton(DataImportWidget)
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.horizontalLayout_2.addWidget(self.buttonBrowse)
        self.buttonImport = QtGui.QPushButton(DataImportWidget)
        self.buttonImport.setObjectName("buttonImport")
        self.horizontalLayout_2.addWidget(self.buttonImport)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 178, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem5 = QtGui.QSpacerItem(78, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.retranslateUi(DataImportWidget)
        QtCore.QMetaObject.connectSlotsByName(DataImportWidget)

    def retranslateUi(self, DataImportWidget):
        DataImportWidget.setWindowTitle(QtGui.QApplication.translate("DataImportWidget", "Data Import", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DataImportWidget", "Import a Data File", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonBrowse.setText(QtGui.QApplication.translate("DataImportWidget", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonImport.setText(QtGui.QApplication.translate("DataImportWidget", "Import", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DataImportWidget = QtGui.QWidget()
    ui = Ui_DataImportWidget()
    ui.setupUi(DataImportWidget)
    DataImportWidget.show()
    sys.exit(app.exec_())

