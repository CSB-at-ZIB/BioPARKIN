# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\workspace\bioparkin\src\aboutdialog.ui'
#
# Created: Tue Sep 20 10:15:22 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(464, 483)
        AboutDialog.setMinimumSize(QtCore.QSize(464, 483))
        AboutDialog.setMaximumSize(QtCore.QSize(464, 483))
        self.verticalLayout_2 = QtGui.QVBoxLayout(AboutDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelTitle = QtGui.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")
        self.verticalLayout.addWidget(self.labelTitle)
        self.labelVersion = QtGui.QLabel(AboutDialog)
        self.labelVersion.setObjectName("labelVersion")
        self.verticalLayout.addWidget(self.labelVersion)
        self.labelUrl = QtGui.QLabel(AboutDialog)
        self.labelUrl.setText("<a href=\"http://www.zib.de/en/numerik/csb/software/bioparkin.html\">BioPARKIN Web Page</a>")
        self.labelUrl.setTextFormat(QtCore.Qt.AutoText)
        self.labelUrl.setScaledContents(False)
        self.labelUrl.setOpenExternalLinks(True)
        self.labelUrl.setObjectName("labelUrl")
        self.verticalLayout.addWidget(self.labelUrl)
        self.labelHeadline = QtGui.QLabel(AboutDialog)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.labelHeadline.setFont(font)
        self.labelHeadline.setObjectName("labelHeadline")
        self.verticalLayout.addWidget(self.labelHeadline)
        self.textLiteratureList = QtGui.QTextBrowser(AboutDialog)
        self.textLiteratureList.setObjectName("textLiteratureList")
        self.verticalLayout.addWidget(self.textLiteratureList)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(188, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelCopyright = QtGui.QLabel(AboutDialog)
        self.labelCopyright.setObjectName("labelCopyright")
        self.horizontalLayout.addWidget(self.labelCopyright)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QtGui.QApplication.translate("AboutDialog", "About BioPARKIN", None, QtGui.QApplication.UnicodeUTF8))
        self.labelTitle.setText(QtGui.QApplication.translate("AboutDialog", "BioPARKIN", None, QtGui.QApplication.UnicodeUTF8))
        self.labelVersion.setText(QtGui.QApplication.translate("AboutDialog", "Version x.y.z", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHeadline.setText(QtGui.QApplication.translate("AboutDialog", "\n"
"\n"
"See / Cite the following references when using this software:", None, QtGui.QApplication.UnicodeUTF8))
        self.textLiteratureList.setHtml(QtGui.QApplication.translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">P.Deuflhard:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Newton Methods for Nonlinear Problems - </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Affine Invariance and Adaptive Algorithms</span>, </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Springer, Berlin, 2004.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">U.Nowak, P.Deuflhard: </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Numerical Identification of Selected Rate Constants </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">in Large Chemical Reaction Systems, </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">Appl. Num. Math.</span> <span style=\" font-weight:600;\">1</span> (1985), 59 - 75.</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">T.Dierkes, M.Wade, U.Nowak, S.Röblitz:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">BioPARKIN - Biology-related Parameter Identification </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">in Large Kinetic Networks,</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">ZIB report</span> <span style=\" font-weight:600;\">11-15 </span>(2011), to appear.</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelCopyright.setText(QtGui.QApplication.translate("AboutDialog", "© Zuse Institute Berlin 2011", None, QtGui.QApplication.UnicodeUTF8))

