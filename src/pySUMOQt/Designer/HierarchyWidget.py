# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HierarchyWidget.ui'
#
# Created: Sun Mar  1 00:17:56 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(539, 300)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 469, 263))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget1 = QtGui.QWidget(self.widget)
        self.widget1.setObjectName("widget1")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtGui.QWidget(self.widget1)
        self.widget_2.setObjectName("widget_2")
        self.formLayout = QtGui.QFormLayout(self.widget_2)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.relationSelector = QtGui.QComboBox(self.widget_2)
        self.relationSelector.setEditable(True)
        self.relationSelector.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        self.relationSelector.setObjectName("relationSelector")
        self.relationSelector.addItem("")
        self.relationSelector.setItemText(0, "")
        self.relationSelector.addItem("")
        self.relationSelector.addItem("")
        self.relationSelector.addItem("")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.relationSelector)
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget_3 = QtGui.QWidget(self.widget1)
        self.widget_3.setObjectName("widget_3")
        self.formLayout_2 = QtGui.QFormLayout(self.widget_3)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtGui.QLabel(self.widget_3)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.rootSelector = QtGui.QComboBox(self.widget_3)
        self.rootSelector.setEditable(True)
        self.rootSelector.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.rootSelector.setObjectName("rootSelector")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.rootSelector)
        self.horizontalLayout.addWidget(self.widget_3)
        self.gridLayout.addWidget(self.widget1, 0, 0, 1, 1)
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Nodes")
        self.treeWidget.header().setVisible(True)
        self.treeWidget.header().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.treeWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Relation: ", None, QtGui.QApplication.UnicodeUTF8))
        self.relationSelector.setItemText(1, QtGui.QApplication.translate("Form", "instance", None, QtGui.QApplication.UnicodeUTF8))
        self.relationSelector.setItemText(2, QtGui.QApplication.translate("Form", "subclass", None, QtGui.QApplication.UnicodeUTF8))
        self.relationSelector.setItemText(3, QtGui.QApplication.translate("Form", "domain", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Node: ", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.setSortingEnabled(True)

