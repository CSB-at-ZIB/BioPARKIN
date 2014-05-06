# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/tom/Work/Eric4/BioPARKIN/src/sbml_views/modelview.ui'
#
# Created: Mon Sep  9 14:28:37 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ModelView(object):
    def setupUi(self, ModelView):
        ModelView.setObjectName("ModelView")
        ModelView.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(ModelView)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelModelList = QtGui.QLabel(ModelView)
        self.labelModelList.setObjectName("labelModelList")
        self.verticalLayout.addWidget(self.labelModelList)
        self._modelListWidget = QtGui.QListWidget(ModelView)
        self._modelListWidget.setObjectName("_modelListWidget")
        self.verticalLayout.addWidget(self._modelListWidget)

        self.retranslateUi(ModelView)
        QtCore.QMetaObject.connectSlotsByName(ModelView)

    def retranslateUi(self, ModelView):
        ModelView.setWindowTitle(QtGui.QApplication.translate("ModelView", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.labelModelList.setText(QtGui.QApplication.translate("ModelView", "Model List", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ModelView = QtGui.QWidget()
    ui = Ui_ModelView()
    ui.setupUi(ModelView)
    ModelView.show()
    sys.exit(app.exec_())

