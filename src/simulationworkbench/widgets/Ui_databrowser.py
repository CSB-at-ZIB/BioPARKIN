# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/simulationworkbench/widgets/databrowser.ui'
#
# Created: Mon Sep  9 14:28:43 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DataBrowser(object):
    def setupUi(self, DataBrowser):
        DataBrowser.setObjectName("DataBrowser")
        DataBrowser.resize(871, 764)
        DataBrowser.setWindowOpacity(1.0)
        self.verticalLayout_8 = QtGui.QVBoxLayout(DataBrowser)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableView = QtGui.QTableView(DataBrowser)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.horizontalLayout.addWidget(self.tableView)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(DataBrowser)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidgetPage1 = QtGui.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditInfoSpecies = QtGui.QLineEdit(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditInfoSpecies.sizePolicy().hasHeightForWidth())
        self.lineEditInfoSpecies.setSizePolicy(sizePolicy)
        self.lineEditInfoSpecies.setFrame(True)
        self.lineEditInfoSpecies.setReadOnly(True)
        self.lineEditInfoSpecies.setObjectName("lineEditInfoSpecies")
        self.gridLayout.addWidget(self.lineEditInfoSpecies, 1, 1, 1, 1)
        self.line = QtGui.QFrame(self.tabWidgetPage1)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 5, 0, 1, 2)
        self.labelInfoPath = QtGui.QLabel(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfoPath.sizePolicy().hasHeightForWidth())
        self.labelInfoPath.setSizePolicy(sizePolicy)
        self.labelInfoPath.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelInfoPath.setObjectName("labelInfoPath")
        self.gridLayout.addWidget(self.labelInfoPath, 9, 0, 1, 1)
        self.lineEditInfoPath = QtGui.QLineEdit(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditInfoPath.sizePolicy().hasHeightForWidth())
        self.lineEditInfoPath.setSizePolicy(sizePolicy)
        self.lineEditInfoPath.setFrame(True)
        self.lineEditInfoPath.setReadOnly(True)
        self.lineEditInfoPath.setObjectName("lineEditInfoPath")
        self.gridLayout.addWidget(self.lineEditInfoPath, 9, 1, 1, 1)
        self.labelInfoFilesize = QtGui.QLabel(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfoFilesize.sizePolicy().hasHeightForWidth())
        self.labelInfoFilesize.setSizePolicy(sizePolicy)
        self.labelInfoFilesize.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelInfoFilesize.setObjectName("labelInfoFilesize")
        self.gridLayout.addWidget(self.labelInfoFilesize, 10, 0, 1, 1)
        self.lineEditInfoFilesize = QtGui.QLineEdit(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditInfoFilesize.sizePolicy().hasHeightForWidth())
        self.lineEditInfoFilesize.setSizePolicy(sizePolicy)
        self.lineEditInfoFilesize.setFrame(True)
        self.lineEditInfoFilesize.setReadOnly(True)
        self.lineEditInfoFilesize.setObjectName("lineEditInfoFilesize")
        self.gridLayout.addWidget(self.lineEditInfoFilesize, 10, 1, 1, 1)
        self.labelInfoLastModified = QtGui.QLabel(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfoLastModified.sizePolicy().hasHeightForWidth())
        self.labelInfoLastModified.setSizePolicy(sizePolicy)
        self.labelInfoLastModified.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelInfoLastModified.setObjectName("labelInfoLastModified")
        self.gridLayout.addWidget(self.labelInfoLastModified, 11, 0, 1, 1)
        self.lineEditInfoLastModified = QtGui.QLineEdit(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditInfoLastModified.sizePolicy().hasHeightForWidth())
        self.lineEditInfoLastModified.setSizePolicy(sizePolicy)
        self.lineEditInfoLastModified.setFrame(True)
        self.lineEditInfoLastModified.setReadOnly(True)
        self.lineEditInfoLastModified.setObjectName("lineEditInfoLastModified")
        self.gridLayout.addWidget(self.lineEditInfoLastModified, 11, 1, 1, 1)
        self.labelInfoSpecies = QtGui.QLabel(self.tabWidgetPage1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelInfoSpecies.sizePolicy().hasHeightForWidth())
        self.labelInfoSpecies.setSizePolicy(sizePolicy)
        self.labelInfoSpecies.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelInfoSpecies.setObjectName("labelInfoSpecies")
        self.gridLayout.addWidget(self.labelInfoSpecies, 1, 0, 1, 1)
        self.lineEditInfoDataType = QtGui.QLineEdit(self.tabWidgetPage1)
        self.lineEditInfoDataType.setReadOnly(True)
        self.lineEditInfoDataType.setObjectName("lineEditInfoDataType")
        self.gridLayout.addWidget(self.lineEditInfoDataType, 2, 1, 1, 1)
        self.labelInfoDataType = QtGui.QLabel(self.tabWidgetPage1)
        self.labelInfoDataType.setObjectName("labelInfoDataType")
        self.gridLayout.addWidget(self.labelInfoDataType, 2, 0, 1, 1)
        self.label = QtGui.QLabel(self.tabWidgetPage1)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tabWidgetPage1)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 458, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QtGui.QWidget()
        self.tabWidgetPage2.setObjectName("tabWidgetPage2")
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.tabWidgetPage2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(self.tabWidgetPage2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lineEditTimeshift = QtGui.QLineEdit(self.groupBox)
        self.lineEditTimeshift.setObjectName("lineEditTimeshift")
        self.verticalLayout_6.addWidget(self.lineEditTimeshift)
        self.buttonTimeshift = QtGui.QPushButton(self.groupBox)
        self.buttonTimeshift.setObjectName("buttonTimeshift")
        self.verticalLayout_6.addWidget(self.buttonTimeshift)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBoxPerturbation = QtGui.QGroupBox(self.tabWidgetPage2)
        self.groupBoxPerturbation.setObjectName("groupBoxPerturbation")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBoxPerturbation)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.spinBoxPerturb = QtGui.QDoubleSpinBox(self.groupBoxPerturbation)
        self.spinBoxPerturb.setDecimals(1)
        self.spinBoxPerturb.setSingleStep(0.5)
        self.spinBoxPerturb.setProperty("value", 5.0)
        self.spinBoxPerturb.setObjectName("spinBoxPerturb")
        self.verticalLayout_5.addWidget(self.spinBoxPerturb)
        self.labelPerturb = QtGui.QLabel(self.groupBoxPerturbation)
        self.labelPerturb.setObjectName("labelPerturb")
        self.verticalLayout_5.addWidget(self.labelPerturb)
        self.buttonPerturb = QtGui.QPushButton(self.groupBoxPerturbation)
        self.buttonPerturb.setObjectName("buttonPerturb")
        self.verticalLayout_5.addWidget(self.buttonPerturb)
        self.verticalLayout_2.addWidget(self.groupBoxPerturbation)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 498, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonPlot = QtGui.QPushButton(DataBrowser)
        self.buttonPlot.setObjectName("buttonPlot")
        self.verticalLayout.addWidget(self.buttonPlot)
        self.buttonSaveAs = QtGui.QPushButton(DataBrowser)
        self.buttonSaveAs.setObjectName("buttonSaveAs")
        self.verticalLayout.addWidget(self.buttonSaveAs)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.actionPlot = QtGui.QAction(DataBrowser)
        self.actionPlot.setObjectName("actionPlot")

        self.retranslateUi(DataBrowser)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonPlot, QtCore.SIGNAL("clicked()"), self.actionPlot.trigger)
        QtCore.QMetaObject.connectSlotsByName(DataBrowser)

    def retranslateUi(self, DataBrowser):
        DataBrowser.setWindowTitle(QtGui.QApplication.translate("DataBrowser", "DataBrowser", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfoPath.setText(QtGui.QApplication.translate("DataBrowser", "Path:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfoFilesize.setText(QtGui.QApplication.translate("DataBrowser", "Filesize:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfoLastModified.setText(QtGui.QApplication.translate("DataBrowser", "Last Modified:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfoSpecies.setText(QtGui.QApplication.translate("DataBrowser", "# Species:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelInfoDataType.setText(QtGui.QApplication.translate("DataBrowser", "Data Type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DataBrowser", "<b>Data</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("DataBrowser", "<b>File</b>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QtGui.QApplication.translate("DataBrowser", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("DataBrowser", "Timeshifting", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonTimeshift.setText(QtGui.QApplication.translate("DataBrowser", "Timeshift Data", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxPerturbation.setTitle(QtGui.QApplication.translate("DataBrowser", "Perturbation", None, QtGui.QApplication.UnicodeUTF8))
        self.spinBoxPerturb.setSuffix(QtGui.QApplication.translate("DataBrowser", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPerturb.setText(QtGui.QApplication.translate("DataBrowser", "Perturbation Factor:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonPerturb.setText(QtGui.QApplication.translate("DataBrowser", "Perturb Data", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QtGui.QApplication.translate("DataBrowser", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonPlot.setText(QtGui.QApplication.translate("DataBrowser", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonSaveAs.setText(QtGui.QApplication.translate("DataBrowser", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlot.setText(QtGui.QApplication.translate("DataBrowser", "Plot", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPlot.setToolTip(QtGui.QApplication.translate("DataBrowser", "Plot this data set.", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DataBrowser = QtGui.QWidget()
    ui = Ui_DataBrowser()
    ui.setupUi(DataBrowser)
    DataBrowser.show()
    sys.exit(app.exec_())

