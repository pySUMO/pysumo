# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HierarchyWidget.ui'
#
# Created: Tue Feb 24 21:05:22 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(539, 300)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 491, 271))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget1 = QtGui.QWidget(self.widget)
        self.widget1.setObjectName("widget1")
        self.formLayout = QtGui.QFormLayout(self.widget1)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.widget1)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.relationSelector = QtGui.QComboBox(self.widget1)
        self.relationSelector.setObjectName("relationSelector")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.relationSelector)
        self.gridLayout.addWidget(self.widget1, 0, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Choose Relation: ", None, QtGui.QApplication.UnicodeUTF8))

