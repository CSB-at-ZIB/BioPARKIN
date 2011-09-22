# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\dataviewing\DataView2.ui'
#
# Created: Tue Sep 20 10:15:23 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DataViewWidget(object):
    def setupUi(self, DataViewWidget):
        DataViewWidget.setObjectName("DataViewWidget")
        DataViewWidget.resize(716, 450)
        self.horizontalLayout = QtGui.QHBoxLayout(DataViewWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(DataViewWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayoutLeft = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayoutLeft.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutLeft.setObjectName("verticalLayoutLeft")
        self.groupBoxSources = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxSources.setObjectName("groupBoxSources")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBoxSources)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.tableSources = QtGui.QTableView(self.groupBoxSources)
        self.tableSources.setObjectName("tableSources")
        self.verticalLayout_5.addWidget(self.tableSources)
        self.verticalLayoutLeft.addWidget(self.groupBoxSources)
        spacerItem = QtGui.QSpacerItem(20, 98, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayoutLeft.addItem(spacerItem)
        self.groupBoxOptions = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxOptions.setObjectName("groupBoxOptions")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBoxOptions)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayoutCheckboxes = QtGui.QVBoxLayout()
        self.verticalLayoutCheckboxes.setObjectName("verticalLayoutCheckboxes")
        self.checkBoxShowLegend = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxShowLegend.setChecked(True)
        self.checkBoxShowLegend.setObjectName("checkBoxShowLegend")
        self.verticalLayoutCheckboxes.addWidget(self.checkBoxShowLegend)
        self.checkBoxLogYAxis = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxLogYAxis.setObjectName("checkBoxLogYAxis")
        self.verticalLayoutCheckboxes.addWidget(self.checkBoxLogYAxis)
        self.checkBoxSeparatePlots = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxSeparatePlots.setObjectName("checkBoxSeparatePlots")
        self.verticalLayoutCheckboxes.addWidget(self.checkBoxSeparatePlots)
        self.verticalLayout_6.addLayout(self.verticalLayoutCheckboxes)
        self.verticalLayoutLeft.addWidget(self.groupBoxOptions)
        self.pushButtonReplot = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonReplot.setObjectName("pushButtonReplot")
        self.verticalLayoutLeft.addWidget(self.pushButtonReplot)
        self.plotWindowsArea = QtGui.QMdiArea(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotWindowsArea.sizePolicy().hasHeightForWidth())
        self.plotWindowsArea.setSizePolicy(sizePolicy)
        self.plotWindowsArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plotWindowsArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plotWindowsArea.setViewMode(QtGui.QMdiArea.SubWindowView)
        self.plotWindowsArea.setObjectName("plotWindowsArea")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(DataViewWidget)
        QtCore.QMetaObject.connectSlotsByName(DataViewWidget)

    def retranslateUi(self, DataViewWidget):
        DataViewWidget.setWindowTitle(QtGui.QApplication.translate("DataViewWidget", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxSources.setTitle(QtGui.QApplication.translate("DataViewWidget", "Sources", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxOptions.setTitle(QtGui.QApplication.translate("DataViewWidget", "Options for New Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowLegend.setText(QtGui.QApplication.translate("DataViewWidget", "Show &Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogYAxis.setText(QtGui.QApplication.translate("DataViewWidget", "&Logarithmic Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSeparatePlots.setText(QtGui.QApplication.translate("DataViewWidget", "&Separate Plots for Exp. and Sim. Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonReplot.setText(QtGui.QApplication.translate("DataViewWidget", "&Replot", None, QtGui.QApplication.UnicodeUTF8))

