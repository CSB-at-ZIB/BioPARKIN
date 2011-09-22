# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\dataviewing\DataView.ui'
#
# Created: Tue Sep 20 10:15:23 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_dataViewWidget(object):
    def setupUi(self, dataViewWidget):
        dataViewWidget.setObjectName("dataViewWidget")
        dataViewWidget.resize(670, 648)
        dataViewWidget.setFloating(True)
        dataViewWidget.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        dataViewWidget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtGui.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(self.dockWidgetContents)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBoxSources = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxSources.setObjectName("groupBoxSources")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxSources)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableSources = QtGui.QTableView(self.groupBoxSources)
        self.tableSources.setObjectName("tableSources")
        self.verticalLayout.addWidget(self.tableSources)
        self.verticalLayout_4.addWidget(self.groupBoxSources)
        spacerItem = QtGui.QSpacerItem(20, 98, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.groupBoxOptions = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxOptions.setObjectName("groupBoxOptions")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBoxOptions)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxShowLegend = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxShowLegend.setChecked(True)
        self.checkBoxShowLegend.setObjectName("checkBoxShowLegend")
        self.verticalLayout_2.addWidget(self.checkBoxShowLegend)
        self.checkBoxLogYAxis = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxLogYAxis.setObjectName("checkBoxLogYAxis")
        self.verticalLayout_2.addWidget(self.checkBoxLogYAxis)
        self.checkBoxSeparatePlots = QtGui.QCheckBox(self.groupBoxOptions)
        self.checkBoxSeparatePlots.setObjectName("checkBoxSeparatePlots")
        self.verticalLayout_2.addWidget(self.checkBoxSeparatePlots)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addWidget(self.groupBoxOptions)
        self.pushButtonReplot = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonReplot.setObjectName("pushButtonReplot")
        self.verticalLayout_4.addWidget(self.pushButtonReplot)
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
        dataViewWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(dataViewWidget)
        QtCore.QMetaObject.connectSlotsByName(dataViewWidget)
        dataViewWidget.setTabOrder(self.tableSources, self.checkBoxSeparatePlots)
        dataViewWidget.setTabOrder(self.checkBoxSeparatePlots, self.pushButtonReplot)

    def retranslateUi(self, dataViewWidget):
        dataViewWidget.setWindowTitle(QtGui.QApplication.translate("dataViewWidget", "Data View", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxSources.setTitle(QtGui.QApplication.translate("dataViewWidget", "Sources", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxOptions.setTitle(QtGui.QApplication.translate("dataViewWidget", "Options for New Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxShowLegend.setText(QtGui.QApplication.translate("dataViewWidget", "Show &Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxLogYAxis.setText(QtGui.QApplication.translate("dataViewWidget", "&Logarithmic Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxSeparatePlots.setText(QtGui.QApplication.translate("dataViewWidget", "&Separate Plots for Exp. and Sim. Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonReplot.setText(QtGui.QApplication.translate("dataViewWidget", "&Replot", None, QtGui.QApplication.UnicodeUTF8))

