# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\simulationworkbench\simulationworkbench_v1.ui'
#
# Created: Tue Sep 20 10:15:24 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SimulationWindow(object):
    def setupUi(self, SimulationWindow):
        SimulationWindow.setObjectName("SimulationWindow")
        SimulationWindow.resize(1024, 740)
        self.centralwidget = QtGui.QWidget(SimulationWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.actionTabWidget = QtGui.QTabWidget(self.layoutWidget)
        self.actionTabWidget.setObjectName("actionTabWidget")
        self.tabSpecies = QtGui.QWidget()
        self.tabSpecies.setObjectName("tabSpecies")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.tabSpecies)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.speciesTableView = QtGui.QTableView(self.tabSpecies)
        self.speciesTableView.setObjectName("speciesTableView")
        self.verticalLayout_5.addWidget(self.speciesTableView)
        self.actionTabWidget.addTab(self.tabSpecies, "")
        self.tabParameters = QtGui.QWidget()
        self.tabParameters.setObjectName("tabParameters")
        self.verticalLayout = QtGui.QVBoxLayout(self.tabParameters)
        self.verticalLayout.setObjectName("verticalLayout")
        self.parametersTableView = QtGui.QTableView(self.tabParameters)
        self.parametersTableView.setObjectName("parametersTableView")
        self.verticalLayout.addWidget(self.parametersTableView)
        self.actionTabWidget.addTab(self.tabParameters, "")
        self.tabSensitivity = QtGui.QWidget()
        self.tabSensitivity.setObjectName("tabSensitivity")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.tabSensitivity)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sensitivityTableView = QtGui.QTableView(self.tabSensitivity)
        self.sensitivityTableView.setObjectName("sensitivityTableView")
        self.verticalLayout_2.addWidget(self.sensitivityTableView)
        self.computeSensitivitiesButton = QtGui.QPushButton(self.tabSensitivity)
        self.computeSensitivitiesButton.setObjectName("computeSensitivitiesButton")
        self.verticalLayout_2.addWidget(self.computeSensitivitiesButton)
        self.actionTabWidget.addTab(self.tabSensitivity, "")
        self.tabFit = QtGui.QWidget()
        self.tabFit.setObjectName("tabFit")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tabFit)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtGui.QLabel(self.tabFit)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.actionTabWidget.addTab(self.tabFit, "")
        self.tabSettings = QtGui.QWidget()
        self.tabSettings.setObjectName("tabSettings")
        self.verticalLayout_12 = QtGui.QVBoxLayout(self.tabSettings)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBoxTimes = QtGui.QGroupBox(self.tabSettings)
        self.groupBoxTimes.setObjectName("groupBoxTimes")
        self.gridLayout = QtGui.QGridLayout(self.groupBoxTimes)
        self.gridLayout.setObjectName("gridLayout")
        self.labelStartTime = QtGui.QLabel(self.groupBoxTimes)
        self.labelStartTime.setObjectName("labelStartTime")
        self.gridLayout.addWidget(self.labelStartTime, 0, 0, 1, 1)
        self.lineEditStartTime = QtGui.QLineEdit(self.groupBoxTimes)
        self.lineEditStartTime.setObjectName("lineEditStartTime")
        self.gridLayout.addWidget(self.lineEditStartTime, 0, 1, 1, 1)
        self.labelEndTime = QtGui.QLabel(self.groupBoxTimes)
        self.labelEndTime.setObjectName("labelEndTime")
        self.gridLayout.addWidget(self.labelEndTime, 1, 0, 1, 1)
        self.lineEditEndTime = QtGui.QLineEdit(self.groupBoxTimes)
        self.lineEditEndTime.setObjectName("lineEditEndTime")
        self.gridLayout.addWidget(self.lineEditEndTime, 1, 1, 1, 1)
        self.labelTimeUnit = QtGui.QLabel(self.groupBoxTimes)
        self.labelTimeUnit.setObjectName("labelTimeUnit")
        self.gridLayout.addWidget(self.labelTimeUnit, 2, 0, 1, 1)
        self.lineEditTimeUnit = QtGui.QLineEdit(self.groupBoxTimes)
        self.lineEditTimeUnit.setObjectName("lineEditTimeUnit")
        self.gridLayout.addWidget(self.lineEditTimeUnit, 2, 1, 1, 1)
        self.labelNumTimepoints = QtGui.QLabel(self.groupBoxTimes)
        self.labelNumTimepoints.setObjectName("labelNumTimepoints")
        self.gridLayout.addWidget(self.labelNumTimepoints, 3, 0, 1, 1)
        self.lineEditNumTimepoints = QtGui.QLineEdit(self.groupBoxTimes)
        self.lineEditNumTimepoints.setObjectName("lineEditNumTimepoints")
        self.gridLayout.addWidget(self.lineEditNumTimepoints, 3, 1, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBoxTimes)
        self.groupBoxTolerances = QtGui.QGroupBox(self.tabSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxTolerances.sizePolicy().hasHeightForWidth())
        self.groupBoxTolerances.setSizePolicy(sizePolicy)
        self.groupBoxTolerances.setFlat(False)
        self.groupBoxTolerances.setCheckable(False)
        self.groupBoxTolerances.setObjectName("groupBoxTolerances")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxTolerances)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelTolerance1 = QtGui.QLabel(self.groupBoxTolerances)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTolerance1.sizePolicy().hasHeightForWidth())
        self.labelTolerance1.setSizePolicy(sizePolicy)
        self.labelTolerance1.setObjectName("labelTolerance1")
        self.gridLayout_2.addWidget(self.labelTolerance1, 0, 0, 1, 1)
        self.lineEditTolerance1 = QtGui.QLineEdit(self.groupBoxTolerances)
        self.lineEditTolerance1.setObjectName("lineEditTolerance1")
        self.gridLayout_2.addWidget(self.lineEditTolerance1, 0, 1, 1, 1)
        self.labelTolerance2 = QtGui.QLabel(self.groupBoxTolerances)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTolerance2.sizePolicy().hasHeightForWidth())
        self.labelTolerance2.setSizePolicy(sizePolicy)
        self.labelTolerance2.setObjectName("labelTolerance2")
        self.gridLayout_2.addWidget(self.labelTolerance2, 1, 0, 1, 1)
        self.lineEditTolerance2 = QtGui.QLineEdit(self.groupBoxTolerances)
        self.lineEditTolerance2.setObjectName("lineEditTolerance2")
        self.gridLayout_2.addWidget(self.lineEditTolerance2, 1, 1, 1, 1)
        self.lineEditTolerance3 = QtGui.QLineEdit(self.groupBoxTolerances)
        self.lineEditTolerance3.setObjectName("lineEditTolerance3")
        self.gridLayout_2.addWidget(self.lineEditTolerance3, 2, 1, 1, 1)
        self.labelTolerance3 = QtGui.QLabel(self.groupBoxTolerances)
        self.labelTolerance3.setObjectName("labelTolerance3")
        self.gridLayout_2.addWidget(self.labelTolerance3, 2, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.groupBoxTolerances)
        spacerItem = QtGui.QSpacerItem(20, 238, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.verticalLayout_12.addLayout(self.verticalLayout_4)
        self.actionTabWidget.addTab(self.tabSettings, "")
        self.verticalLayout_6.addWidget(self.actionTabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.simulateButton = QtGui.QPushButton(self.layoutWidget)
        self.simulateButton.setObjectName("simulateButton")
        self.horizontalLayout.addWidget(self.simulateButton)
        self.resetButton = QtGui.QPushButton(self.layoutWidget)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout.addWidget(self.resetButton)
        self.autoRefreshCheckBox = QtGui.QCheckBox(self.layoutWidget)
        self.autoRefreshCheckBox.setObjectName("autoRefreshCheckBox")
        self.horizontalLayout.addWidget(self.autoRefreshCheckBox)
        spacerItem1 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.splitter = QtGui.QSplitter(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.dataTabWidget = QtGui.QTabWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTabWidget.sizePolicy().hasHeightForWidth())
        self.dataTabWidget.setSizePolicy(sizePolicy)
        self.dataTabWidget.setObjectName("dataTabWidget")
        self.tabPlot = QtGui.QWidget()
        self.tabPlot.setObjectName("tabPlot")
        self.dataTabWidget.addTab(self.tabPlot, "")
        self.tabTable = QtGui.QWidget()
        self.tabTable.setObjectName("tabTable")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tabTable)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.dataTableWidget = QtGui.QTableWidget(self.tabTable)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTableWidget.sizePolicy().hasHeightForWidth())
        self.dataTableWidget.setSizePolicy(sizePolicy)
        self.dataTableWidget.setObjectName("dataTableWidget")
        self.dataTableWidget.setColumnCount(0)
        self.dataTableWidget.setRowCount(0)
        self.verticalLayout_7.addWidget(self.dataTableWidget)
        self.dataTabWidget.addTab(self.tabTable, "")
        self.tabSensitivityTable = QtGui.QWidget()
        self.tabSensitivityTable.setObjectName("tabSensitivityTable")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tabSensitivityTable)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.sensitivitiesTableWidget = QtGui.QTableWidget(self.tabSensitivityTable)
        self.sensitivitiesTableWidget.setObjectName("sensitivitiesTableWidget")
        self.sensitivitiesTableWidget.setColumnCount(0)
        self.sensitivitiesTableWidget.setRowCount(0)
        self.horizontalLayout_4.addWidget(self.sensitivitiesTableWidget)
        self.dataTabWidget.addTab(self.tabSensitivityTable, "")
        self.tabSettings1 = QtGui.QWidget()
        self.tabSettings1.setObjectName("tabSettings1")
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.tabSettings1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.groupBox = QtGui.QGroupBox(self.tabSettings1)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.showLegendCheckBox = QtGui.QCheckBox(self.groupBox)
        self.showLegendCheckBox.setObjectName("showLegendCheckBox")
        self.verticalLayout_9.addWidget(self.showLegendCheckBox)
        self.logYAxisCheckBox = QtGui.QCheckBox(self.groupBox)
        self.logYAxisCheckBox.setObjectName("logYAxisCheckBox")
        self.verticalLayout_9.addWidget(self.logYAxisCheckBox)
        self.verticalLayout_10.addLayout(self.verticalLayout_9)
        self.verticalLayout_11.addWidget(self.groupBox)
        spacerItem2 = QtGui.QSpacerItem(20, 452, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem2)
        self.dataTabWidget.addTab(self.tabSettings1, "")
        self.dataSourceTableView = QtGui.QTableView(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataSourceTableView.sizePolicy().hasHeightForWidth())
        self.dataSourceTableView.setSizePolicy(sizePolicy)
        self.dataSourceTableView.setMinimumSize(QtCore.QSize(100, 0))
        self.dataSourceTableView.setMaximumSize(QtCore.QSize(300, 16777215))
        self.dataSourceTableView.setObjectName("dataSourceTableView")
        self.verticalLayout_8.addWidget(self.splitter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtGui.QSpacerItem(128, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.importButton = QtGui.QPushButton(self.layoutWidget1)
        self.importButton.setObjectName("importButton")
        self.horizontalLayout_2.addWidget(self.importButton)
        self.saveDataButton = QtGui.QPushButton(self.layoutWidget1)
        self.saveDataButton.setObjectName("saveDataButton")
        self.horizontalLayout_2.addWidget(self.saveDataButton)
        self.savePlotButton = QtGui.QPushButton(self.layoutWidget1)
        self.savePlotButton.setObjectName("savePlotButton")
        self.horizontalLayout_2.addWidget(self.savePlotButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.splitter_2)
        SimulationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SimulationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuActions = QtGui.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        self.menuData = QtGui.QMenu(self.menubar)
        self.menuData.setObjectName("menuData")
        self.menuPlot = QtGui.QMenu(self.menubar)
        self.menuPlot.setObjectName("menuPlot")
        SimulationWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SimulationWindow)
        self.statusbar.setObjectName("statusbar")
        SimulationWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(SimulationWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionAbout = QtGui.QAction(SimulationWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSimulate = QtGui.QAction(SimulationWindow)
        self.actionSimulate.setObjectName("actionSimulate")
        self.actionReset = QtGui.QAction(SimulationWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionImport = QtGui.QAction(SimulationWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionSaveData = QtGui.QAction(SimulationWindow)
        self.actionSaveData.setObjectName("actionSaveData")
        self.actionSavePlot = QtGui.QAction(SimulationWindow)
        self.actionSavePlot.setObjectName("actionSavePlot")
        self.actionAutoRefresh = QtGui.QAction(SimulationWindow)
        self.actionAutoRefresh.setCheckable(True)
        self.actionAutoRefresh.setObjectName("actionAutoRefresh")
        self.actionComputeSensitivities = QtGui.QAction(SimulationWindow)
        self.actionComputeSensitivities.setObjectName("actionComputeSensitivities")
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionAbout)
        self.menuActions.addAction(self.actionSimulate)
        self.menuActions.addAction(self.actionComputeSensitivities)
        self.menuActions.addAction(self.actionReset)
        self.menuData.addAction(self.actionImport)
        self.menuData.addAction(self.actionSaveData)
        self.menuPlot.addAction(self.actionSavePlot)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())
        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(SimulationWindow)
        self.actionTabWidget.setCurrentIndex(0)
        self.dataTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL("activated()"), SimulationWindow.close)
        QtCore.QObject.connect(self.simulateButton, QtCore.SIGNAL("clicked()"), self.actionSimulate.trigger)
        QtCore.QObject.connect(self.resetButton, QtCore.SIGNAL("clicked()"), self.actionReset.trigger)
        QtCore.QObject.connect(self.importButton, QtCore.SIGNAL("clicked()"), self.actionImport.trigger)
        QtCore.QObject.connect(self.saveDataButton, QtCore.SIGNAL("clicked()"), self.actionSaveData.trigger)
        QtCore.QObject.connect(self.savePlotButton, QtCore.SIGNAL("clicked()"), self.actionSavePlot.trigger)
        QtCore.QObject.connect(self.autoRefreshCheckBox, QtCore.SIGNAL("toggled(bool)"), self.actionAutoRefresh.setChecked)
        QtCore.QObject.connect(self.computeSensitivitiesButton, QtCore.SIGNAL("clicked()"), self.actionComputeSensitivities.trigger)
        QtCore.QMetaObject.connectSlotsByName(SimulationWindow)

    def retranslateUi(self, SimulationWindow):
        SimulationWindow.setWindowTitle(QtGui.QApplication.translate("SimulationWindow", "Simulation Workbench", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTabWidget.setTabText(self.actionTabWidget.indexOf(self.tabSpecies), QtGui.QApplication.translate("SimulationWindow", "&Species", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTabWidget.setTabText(self.actionTabWidget.indexOf(self.tabParameters), QtGui.QApplication.translate("SimulationWindow", "&Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.computeSensitivitiesButton.setText(QtGui.QApplication.translate("SimulationWindow", "Compute Sensitivities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTabWidget.setTabText(self.actionTabWidget.indexOf(self.tabSensitivity), QtGui.QApplication.translate("SimulationWindow", "&Sensitivity", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SimulationWindow", "This is an upcoming feature.", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTabWidget.setTabText(self.actionTabWidget.indexOf(self.tabFit), QtGui.QApplication.translate("SimulationWindow", "&Fit", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxTimes.setTitle(QtGui.QApplication.translate("SimulationWindow", "Time Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelStartTime.setText(QtGui.QApplication.translate("SimulationWindow", "Start Time", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditStartTime.setText(QtGui.QApplication.translate("SimulationWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEndTime.setText(QtGui.QApplication.translate("SimulationWindow", "End Time", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditEndTime.setText(QtGui.QApplication.translate("SimulationWindow", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTimeUnit.setText(QtGui.QApplication.translate("SimulationWindow", "Time Unit", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTimeUnit.setText(QtGui.QApplication.translate("SimulationWindow", "d", None, QtGui.QApplication.UnicodeUTF8))
        self.labelNumTimepoints.setText(QtGui.QApplication.translate("SimulationWindow", "# Points", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditNumTimepoints.setText(QtGui.QApplication.translate("SimulationWindow", "30", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxTolerances.setTitle(QtGui.QApplication.translate("SimulationWindow", "Tolerance Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTolerance1.setText(QtGui.QApplication.translate("SimulationWindow", "Rel. Tolerance", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTolerance1.setText(QtGui.QApplication.translate("SimulationWindow", "9.9999999999999995E-07", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTolerance2.setText(QtGui.QApplication.translate("SimulationWindow", "Tolerance 2", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTolerance2.setText(QtGui.QApplication.translate("SimulationWindow", "5.2499999999999995E-07", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEditTolerance3.setText(QtGui.QApplication.translate("SimulationWindow", "1.0000000000000000E+00", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTolerance3.setText(QtGui.QApplication.translate("SimulationWindow", "Tolerance 3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTabWidget.setTabText(self.actionTabWidget.indexOf(self.tabSettings), QtGui.QApplication.translate("SimulationWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.simulateButton.setText(QtGui.QApplication.translate("SimulationWindow", "&Simulate", None, QtGui.QApplication.UnicodeUTF8))
        self.resetButton.setText(QtGui.QApplication.translate("SimulationWindow", "&Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.autoRefreshCheckBox.setText(QtGui.QApplication.translate("SimulationWindow", "&Auto Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.tabPlot), QtGui.QApplication.translate("SimulationWindow", "Simulation: &Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.tabTable), QtGui.QApplication.translate("SimulationWindow", "Simulation: &Table", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.tabSensitivityTable), QtGui.QApplication.translate("SimulationWindow", "&Sensitivities: Table", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("SimulationWindow", "Plot Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.showLegendCheckBox.setText(QtGui.QApplication.translate("SimulationWindow", "Show Legend", None, QtGui.QApplication.UnicodeUTF8))
        self.logYAxisCheckBox.setText(QtGui.QApplication.translate("SimulationWindow", "Logarithmic Y Axis", None, QtGui.QApplication.UnicodeUTF8))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.tabSettings1), QtGui.QApplication.translate("SimulationWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.importButton.setText(QtGui.QApplication.translate("SimulationWindow", "&Import Data...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveDataButton.setText(QtGui.QApplication.translate("SimulationWindow", "Save &Data...", None, QtGui.QApplication.UnicodeUTF8))
        self.savePlotButton.setText(QtGui.QApplication.translate("SimulationWindow", "Save &Plot...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("SimulationWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("SimulationWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuActions.setTitle(QtGui.QApplication.translate("SimulationWindow", "&Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuData.setTitle(QtGui.QApplication.translate("SimulationWindow", "&Data", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlot.setTitle(QtGui.QApplication.translate("SimulationWindow", "&Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("SimulationWindow", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Close the Workbench", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("SimulationWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setShortcut(QtGui.QApplication.translate("SimulationWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setText(QtGui.QApplication.translate("SimulationWindow", "&Simulate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Simulate with current settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setText(QtGui.QApplication.translate("SimulationWindow", "&Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReset.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("SimulationWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveData.setText(QtGui.QApplication.translate("SimulationWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveData.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Save Data", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveData.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSavePlot.setText(QtGui.QApplication.translate("SimulationWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSavePlot.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Save Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSavePlot.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoRefresh.setText(QtGui.QApplication.translate("SimulationWindow", "Auto Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoRefresh.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Simulation will occur automatically if enabled", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAutoRefresh.setShortcut(QtGui.QApplication.translate("SimulationWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputeSensitivities.setText(QtGui.QApplication.translate("SimulationWindow", "Compute Sensitivities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputeSensitivities.setToolTip(QtGui.QApplication.translate("SimulationWindow", "Compute sensitivities of the currently selected Species", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
