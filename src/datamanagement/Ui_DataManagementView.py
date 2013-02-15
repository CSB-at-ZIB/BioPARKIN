# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/datamanagement/DataManagementView.ui'
#
# Created: Fri Feb 15 10:25:19 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DataManagementView(object):
    def setupUi(self, DataManagementView):
        DataManagementView.setObjectName("DataManagementView")
        DataManagementView.resize(656, 577)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/tango-actions-32px/images/tango-icon-theme/32x32/actions/document-properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DataManagementView.setWindowIcon(icon)
        DataManagementView.setModal(True)
        self.verticalLayout_4 = QtGui.QVBoxLayout(DataManagementView)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox_Experimental = QtGui.QGroupBox(DataManagementView)
        self.groupBox_Experimental.setObjectName("groupBox_Experimental")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_Experimental)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidget_Experimental = QtGui.QListWidget(self.groupBox_Experimental)
        self.listWidget_Experimental.setObjectName("listWidget_Experimental")
        self.horizontalLayout.addWidget(self.listWidget_Experimental)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 58, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_BrowseExperimental = QtGui.QPushButton(self.groupBox_Experimental)
        self.pushButton_BrowseExperimental.setObjectName("pushButton_BrowseExperimental")
        self.verticalLayout.addWidget(self.pushButton_BrowseExperimental)
        self.pushButton_RemoveExperimental = QtGui.QPushButton(self.groupBox_Experimental)
        self.pushButton_RemoveExperimental.setObjectName("pushButton_RemoveExperimental")
        self.verticalLayout.addWidget(self.pushButton_RemoveExperimental)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.groupBox_Experimental)
        self.groupBox_Simulation = QtGui.QGroupBox(DataManagementView)
        self.groupBox_Simulation.setObjectName("groupBox_Simulation")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_Simulation)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.listWidget_Simulation = QtGui.QListWidget(self.groupBox_Simulation)
        self.listWidget_Simulation.setObjectName("listWidget_Simulation")
        self.horizontalLayout_5.addWidget(self.listWidget_Simulation)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtGui.QSpacerItem(20, 58, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.pushButton_BrowseSimulation = QtGui.QPushButton(self.groupBox_Simulation)
        self.pushButton_BrowseSimulation.setObjectName("pushButton_BrowseSimulation")
        self.verticalLayout_2.addWidget(self.pushButton_BrowseSimulation)
        self.pushButton_RemoveSimulation = QtGui.QPushButton(self.groupBox_Simulation)
        self.pushButton_RemoveSimulation.setObjectName("pushButton_RemoveSimulation")
        self.verticalLayout_2.addWidget(self.pushButton_RemoveSimulation)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_5)
        self.verticalLayout_3.addWidget(self.groupBox_Simulation)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtGui.QSpacerItem(428, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.buttonBox_OkCancelResetApply = QtGui.QDialogButtonBox(DataManagementView)
        self.buttonBox_OkCancelResetApply.setStandardButtons(QtGui.QDialogButtonBox.Apply|QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Reset)
        self.buttonBox_OkCancelResetApply.setObjectName("buttonBox_OkCancelResetApply")
        self.horizontalLayout_3.addWidget(self.buttonBox_OkCancelResetApply)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.retranslateUi(DataManagementView)
        QtCore.QObject.connect(self.buttonBox_OkCancelResetApply, QtCore.SIGNAL("accepted()"), DataManagementView.accept)
        QtCore.QObject.connect(self.buttonBox_OkCancelResetApply, QtCore.SIGNAL("rejected()"), DataManagementView.reject)
        QtCore.QMetaObject.connectSlotsByName(DataManagementView)
        DataManagementView.setTabOrder(self.pushButton_BrowseExperimental, self.listWidget_Experimental)
        DataManagementView.setTabOrder(self.listWidget_Experimental, self.pushButton_RemoveExperimental)
        DataManagementView.setTabOrder(self.pushButton_RemoveExperimental, self.pushButton_BrowseSimulation)
        DataManagementView.setTabOrder(self.pushButton_BrowseSimulation, self.listWidget_Simulation)
        DataManagementView.setTabOrder(self.listWidget_Simulation, self.pushButton_RemoveSimulation)
        DataManagementView.setTabOrder(self.pushButton_RemoveSimulation, self.buttonBox_OkCancelResetApply)

    def retranslateUi(self, DataManagementView):
        DataManagementView.setWindowTitle(QtGui.QApplication.translate("DataManagementView", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Experimental.setTitle(QtGui.QApplication.translate("DataManagementView", "Files Containing &Experimental Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_BrowseExperimental.setText(QtGui.QApplication.translate("DataManagementView", "&Browse to Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_RemoveExperimental.setText(QtGui.QApplication.translate("DataManagementView", "&Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_Simulation.setTitle(QtGui.QApplication.translate("DataManagementView", "Files Containing &Simulation Data", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_BrowseSimulation.setText(QtGui.QApplication.translate("DataManagementView", "&Browse to Add...", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_RemoveSimulation.setText(QtGui.QApplication.translate("DataManagementView", "&Remove", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DataManagementView = QtGui.QDialog()
    ui = Ui_DataManagementView()
    ui.setupUi(DataManagementView)
    DataManagementView.show()
    sys.exit(app.exec_())

