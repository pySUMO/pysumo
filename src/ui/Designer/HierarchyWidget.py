# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HierarchyWidget.ui'
#
# Created: Tue Feb  3 15:30:30 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(574, 300)
        self.treeView = QtGui.QTreeView(Form)
        self.treeView.setGeometry(QtCore.QRect(0, 11, 571, 271))
        self.treeView.setObjectName("treeView")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))

