# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\BioPARKIN.ui'
#
# Created: Mon Sep 12 14:55:20 2011
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 700)
        MainWindow.setMinimumSize(QtCore.QSize(800, 0))
        MainWindow.setAcceptDrops(True)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "BioPARKIN", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Active, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Disabled, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Selected, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/application/images/2010-12-22 - Poem Icon v1.png")), QtGui.QIcon.Active, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.mainTabWidget = QtGui.QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName(_fromUtf8("mainTabWidget"))
        self.tabModel = QtGui.QWidget()
        self.tabModel.setObjectName(_fromUtf8("tabModel"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tabModel)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.tabModel)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.masterDetailSplitter = QtGui.QSplitter(self.splitter_2)
        self.masterDetailSplitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.masterDetailSplitter.setFrameShadow(QtGui.QFrame.Plain)
        self.masterDetailSplitter.setLineWidth(5)
        self.masterDetailSplitter.setMidLineWidth(0)
        self.masterDetailSplitter.setOrientation(QtCore.Qt.Horizontal)
        self.masterDetailSplitter.setChildrenCollapsible(True)
        self.masterDetailSplitter.setObjectName(_fromUtf8("masterDetailSplitter"))
        self.layoutWidget = QtGui.QWidget(self.masterDetailSplitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.modelListLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.modelListLayout.setMargin(11)
        self.modelListLayout.setMargin(0)
        self.modelListLayout.setObjectName(_fromUtf8("modelListLayout"))
        self._mdiArea = QtGui.QMdiArea(self.splitter_2)
        self._mdiArea.setFrameShape(QtGui.QFrame.NoFrame)
        self._mdiArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self._mdiArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self._mdiArea.setBackground(brush)
        self._mdiArea.setDocumentMode(False)
        self._mdiArea.setObjectName(_fromUtf8("_mdiArea"))
        self.verticalLayout.addWidget(self.splitter_2)
        self.bottomLayout = QtGui.QHBoxLayout()
        self.bottomLayout.setObjectName(_fromUtf8("bottomLayout"))
        self.verticalLayout.addLayout(self.bottomLayout)
        self.mainTabWidget.addTab(self.tabModel, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.mainTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        self.menuSimulation = QtGui.QMenu(self.menubar)
        self.menuSimulation.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSimulation.setObjectName(_fromUtf8("menuSimulation"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.fileToolBar = QtGui.QToolBar(MainWindow)
        self.fileToolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.fileToolBar.setObjectName(_fromUtf8("fileToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.fileToolBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionNew = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon1)
        self.actionNew.setText(QtGui.QApplication.translate("MainWindow", "&New...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a new project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setStatusTip(QtGui.QApplication.translate("MainWindow", "Create a new project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Create a new project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNew.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "&Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setToolTip(QtGui.QApplication.translate("MainWindow", "Open SBML file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open SBML file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setToolTip(QtGui.QApplication.translate("MainWindow", "Save current project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setStatusTip(QtGui.QApplication.translate("MainWindow", "Save current project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_as = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-save-as.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_as.setIcon(icon4)
        self.actionSave_as.setText(QtGui.QApplication.translate("MainWindow", "Save &as...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setToolTip(QtGui.QApplication.translate("MainWindow", "Save current project with a new filename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setStatusTip(QtGui.QApplication.translate("MainWindow", "Save current project with a new filename", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.actionQuit = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/system-shutdown.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon5)
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setToolTip(QtGui.QApplication.translate("MainWindow", "Quit the Application", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Quit the Application", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionAbout = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-status-32px/images/tango-icon-theme/32x32/status/dialog-information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon6)
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionLogViewer = QtGui.QAction(MainWindow)
        self.actionLogViewer.setCheckable(True)
        self.actionLogViewer.setChecked(True)
        self.actionLogViewer.setText(QtGui.QApplication.translate("MainWindow", "Log Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogViewer.setToolTip(QtGui.QApplication.translate("MainWindow", "Show/Hide the Log Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLogViewer.setObjectName(_fromUtf8("actionLogViewer"))
        self.actionCopy = QtGui.QAction(MainWindow)
        self.actionCopy.setText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setObjectName(_fromUtf8("actionCopy"))
        self.actionCut = QtGui.QAction(MainWindow)
        self.actionCut.setText(QtGui.QApplication.translate("MainWindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setObjectName(_fromUtf8("actionCut"))
        self.actionPaste = QtGui.QAction(MainWindow)
        self.actionPaste.setText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setObjectName(_fromUtf8("actionPaste"))
        self.actionSettings = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-categories-32px/images/tango-icon-theme/32x32/categories/applications-system.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon7)
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setToolTip(QtGui.QApplication.translate("MainWindow", "Open the Settings window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setStatusTip(QtGui.QApplication.translate("MainWindow", "Open the Settings window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionSpecies = QtGui.QAction(MainWindow)
        self.actionSpecies.setText(QtGui.QApplication.translate("MainWindow", "Species", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSpecies.setObjectName(_fromUtf8("actionSpecies"))
        self.actionCompartments = QtGui.QAction(MainWindow)
        self.actionCompartments.setText(QtGui.QApplication.translate("MainWindow", "Compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCompartments.setObjectName(_fromUtf8("actionCompartments"))
        self.actionReactions = QtGui.QAction(MainWindow)
        self.actionReactions.setText(QtGui.QApplication.translate("MainWindow", "Reactions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReactions.setObjectName(_fromUtf8("actionReactions"))
        self.actionIntegrate = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-categories-32px/images/tango-icon-theme/32x32/categories/applications-other.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIntegrate.setIcon(icon8)
        self.actionIntegrate.setText(QtGui.QApplication.translate("MainWindow", "Integrate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setToolTip(QtGui.QApplication.translate("MainWindow", "Starts the selected integrator for the current problem", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setStatusTip(QtGui.QApplication.translate("MainWindow", "Start Integration", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIntegrate.setObjectName(_fromUtf8("actionIntegrate"))
        self.actionShowPlots = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-categories-32px/images/tango-icon-theme/32x32/categories/applications-accessories.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShowPlots.setIcon(icon9)
        self.actionShowPlots.setText(QtGui.QApplication.translate("MainWindow", "Show Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowPlots.setToolTip(QtGui.QApplication.translate("MainWindow", "Show Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShowPlots.setObjectName(_fromUtf8("actionShowPlots"))
        self.actionShow_Data_Manager = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-properties.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Data_Manager.setIcon(icon10)
        self.actionShow_Data_Manager.setText(QtGui.QApplication.translate("MainWindow", "Show Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Data_Manager.setToolTip(QtGui.QApplication.translate("MainWindow", "Allows to define data sources", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Data_Manager.setObjectName(_fromUtf8("actionShow_Data_Manager"))
        self.actionODEGenerator = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/format-justify-fill.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionODEGenerator.setIcon(icon11)
        self.actionODEGenerator.setText(QtGui.QApplication.translate("MainWindow", "Show generated ODEs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionODEGenerator.setToolTip(QtGui.QApplication.translate("MainWindow", "Show generated ODEs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionODEGenerator.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show generated ODEs", None, QtGui.QApplication.UnicodeUTF8))
        self.actionODEGenerator.setObjectName(_fromUtf8("actionODEGenerator"))
        self.actionSBMLEntities = QtGui.QAction(MainWindow)
        self.actionSBMLEntities.setCheckable(True)
        self.actionSBMLEntities.setChecked(True)
        self.actionSBMLEntities.setText(QtGui.QApplication.translate("MainWindow", "SBML Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSBMLEntities.setToolTip(QtGui.QApplication.translate("MainWindow", "Show/Hide the SBML Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSBMLEntities.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show/Hide the SBML Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSBMLEntities.setObjectName(_fromUtf8("actionSBMLEntities"))
        self.actionProperties = QtGui.QAction(MainWindow)
        self.actionProperties.setCheckable(True)
        self.actionProperties.setChecked(True)
        self.actionProperties.setText(QtGui.QApplication.translate("MainWindow", "Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setToolTip(QtGui.QApplication.translate("MainWindow", "Show/Hide the Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setStatusTip(QtGui.QApplication.translate("MainWindow", "Show/Hide the Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setObjectName(_fromUtf8("actionProperties"))
        self.actionSimulate = QtGui.QAction(MainWindow)
        self.actionSimulate.setText(QtGui.QApplication.translate("MainWindow", "&Simulate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setToolTip(QtGui.QApplication.translate("MainWindow", "Simulate with current settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSimulate.setObjectName(_fromUtf8("actionSimulate"))
        self.actionComputeSensitivities = QtGui.QAction(MainWindow)
        self.actionComputeSensitivities.setText(QtGui.QApplication.translate("MainWindow", "Compute Sensitivities", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputeSensitivities.setToolTip(QtGui.QApplication.translate("MainWindow", "Compute sensitivities of the currently selected Species", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputeSensitivities.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionComputeSensitivities.setObjectName(_fromUtf8("actionComputeSensitivities"))
        self.actionEstimateParameterValues = QtGui.QAction(MainWindow)
        self.actionEstimateParameterValues.setText(QtGui.QApplication.translate("MainWindow", "Estimate Parameter Values", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEstimateParameterValues.setToolTip(QtGui.QApplication.translate("MainWindow", "Starts the parameter value estimation process", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEstimateParameterValues.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEstimateParameterValues.setObjectName(_fromUtf8("actionEstimateParameterValues"))
        self.actionClose_Model = QtGui.QAction(MainWindow)
        self.actionClose_Model.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Model.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Model.setObjectName(_fromUtf8("actionClose_Model"))
        self.actionShow_Results_Window = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/window-new.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Results_Window.setIcon(icon12)
        self.actionShow_Results_Window.setText(QtGui.QApplication.translate("MainWindow", "Show Results Window", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Results_Window.setToolTip(QtGui.QApplication.translate("MainWindow", "Opens a Window with Results (Tables, Plots, Sensitivities, etc.) if they have already been calculated.", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Results_Window.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Results_Window.setObjectName(_fromUtf8("actionShow_Results_Window"))
        self.actionShow_Warnings = QtGui.QAction(MainWindow)
        self.actionShow_Warnings.setCheckable(False)
        self.actionShow_Warnings.setChecked(False)
        self.actionShow_Warnings.setEnabled(True)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(_fromUtf8(":/tango-status-32px/images/tango-icon-theme/32x32/status/weather-clear.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_Warnings.setIcon(icon13)
        self.actionShow_Warnings.setText(QtGui.QApplication.translate("MainWindow", "Show Warnings", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Warnings.setToolTip(QtGui.QApplication.translate("MainWindow", "Opens a Window showing recent Warnings and Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Warnings.setStatusTip(QtGui.QApplication.translate("MainWindow", "Opens a Window showing recent Warnings and Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Warnings.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Opens a Window showing recent Warnings and Errors", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Warnings.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Alt+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_Warnings.setVisible(True)
        self.actionShow_Warnings.setObjectName(_fromUtf8("actionShow_Warnings"))
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionClose_Model)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuTools.addAction(self.actionODEGenerator)
        self.menuSimulation.addAction(self.actionSimulate)
        self.menuSimulation.addAction(self.actionComputeSensitivities)
        self.menuSimulation.addAction(self.actionEstimateParameterValues)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimulation.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.fileToolBar.addAction(self.actionOpen)
        self.fileToolBar.addAction(self.actionSave)
        self.fileToolBar.addAction(self.actionSave_as)
        self.toolBar.addAction(self.actionODEGenerator)
        self.toolBar.addAction(self.actionShow_Results_Window)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionShow_Warnings)

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tabModel), QtGui.QApplication.translate("MainWindow", "Model", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
