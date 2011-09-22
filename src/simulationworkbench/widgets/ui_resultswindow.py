# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\simulationworkbench\widgets\resultswindow.ui'
#
# Created: Tue Sep 20 10:15:25 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ResultsWindow(object):
    def setupUi(self, ResultsWindow):
        ResultsWindow.setObjectName("ResultsWindow")
        ResultsWindow.resize(896, 680)
        self.centralwidget = QtGui.QWidget(ResultsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(False)
        self.mdiArea.setTabPosition(QtGui.QTabWidget.West)
        self.mdiArea.setObjectName("mdiArea")
        self.verticalLayout.addWidget(self.mdiArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.buttonCloseAll = QtGui.QPushButton(self.centralwidget)
        self.buttonCloseAll.setObjectName("buttonCloseAll")
        self.horizontalLayout.addWidget(self.buttonCloseAll)
        self.ButtonClose = QtGui.QPushButton(self.centralwidget)
        self.ButtonClose.setObjectName("ButtonClose")
        self.horizontalLayout.addWidget(self.ButtonClose)
        self.checkBoxTabMode = QtGui.QCheckBox(self.centralwidget)
        self.checkBoxTabMode.setChecked(True)
        self.checkBoxTabMode.setObjectName("checkBoxTabMode")
        self.horizontalLayout.addWidget(self.checkBoxTabMode)
        self.buttonTileWindows = QtGui.QPushButton(self.centralwidget)
        self.buttonTileWindows.setEnabled(True)
        self.buttonTileWindows.setCheckable(False)
        self.buttonTileWindows.setChecked(False)
        self.buttonTileWindows.setAutoRepeat(False)
        self.buttonTileWindows.setFlat(False)
        self.buttonTileWindows.setObjectName("buttonTileWindows")
        self.horizontalLayout.addWidget(self.buttonTileWindows)
        self.buttonCascadeWindows = QtGui.QPushButton(self.centralwidget)
        self.buttonCascadeWindows.setObjectName("buttonCascadeWindows")
        self.horizontalLayout.addWidget(self.buttonCascadeWindows)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        ResultsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ResultsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 896, 21))
        self.menubar.setObjectName("menubar")
        ResultsWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ResultsWindow)
        self.statusbar.setObjectName("statusbar")
        ResultsWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ResultsWindow)
        QtCore.QObject.connect(self.checkBoxTabMode, QtCore.SIGNAL("toggled(bool)"), self.buttonTileWindows.setHidden)
        QtCore.QObject.connect(self.checkBoxTabMode, QtCore.SIGNAL("toggled(bool)"), self.buttonCascadeWindows.setHidden)
        QtCore.QObject.connect(self.buttonCloseAll, QtCore.SIGNAL("clicked()"), self.mdiArea.closeAllSubWindows)
        QtCore.QObject.connect(self.ButtonClose, QtCore.SIGNAL("clicked()"), self.mdiArea.closeActiveSubWindow)
        QtCore.QObject.connect(self.buttonTileWindows, QtCore.SIGNAL("clicked()"), self.mdiArea.tileSubWindows)
        QtCore.QObject.connect(self.buttonCascadeWindows, QtCore.SIGNAL("clicked()"), self.mdiArea.cascadeSubWindows)
        QtCore.QMetaObject.connectSlotsByName(ResultsWindow)
        ResultsWindow.setTabOrder(self.buttonCloseAll, self.ButtonClose)
        ResultsWindow.setTabOrder(self.ButtonClose, self.checkBoxTabMode)
        ResultsWindow.setTabOrder(self.checkBoxTabMode, self.buttonTileWindows)
        ResultsWindow.setTabOrder(self.buttonTileWindows, self.buttonCascadeWindows)

    def retranslateUi(self, ResultsWindow):
        ResultsWindow.setWindowTitle(QtGui.QApplication.translate("ResultsWindow", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCloseAll.setText(QtGui.QApplication.translate("ResultsWindow", "Close &All", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonClose.setText(QtGui.QApplication.translate("ResultsWindow", "&Close", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxTabMode.setText(QtGui.QApplication.translate("ResultsWindow", "&Tab Mode", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonTileWindows.setText(QtGui.QApplication.translate("ResultsWindow", "T&ile Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonCascadeWindows.setText(QtGui.QApplication.translate("ResultsWindow", "Casca&de &Windows", None, QtGui.QApplication.UnicodeUTF8))

