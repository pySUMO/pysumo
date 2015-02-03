# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DocumentationWidget.ui'
#
# Created: Tue Feb  3 14:47:08 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(557, 300)
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 531, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.WordNet = QtGui.QWidget()
        self.WordNet.setObjectName("WordNet")
        self.plainTextEdit = QtGui.QPlainTextEdit(self.WordNet)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 5, 521, 201))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.tabWidget.addTab(self.WordNet, "")
        self.Ontology = QtGui.QWidget()
        self.Ontology.setObjectName("Ontology")
        self.plainTextEdit_2 = QtGui.QPlainTextEdit(self.Ontology)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(0, 5, 521, 201))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.tabWidget.addTab(self.Ontology, "")
        self.lineEdit = QtGui.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 10, 321, 23))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.WordNet), QtGui.QApplication.translate("Form", "Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ontology), QtGui.QApplication.translate("Form", "WordNet", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setPlaceholderText(QtGui.QApplication.translate("Form", "Search", None, QtGui.QApplication.UnicodeUTF8))

