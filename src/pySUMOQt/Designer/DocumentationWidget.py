# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DocumentationWidget.ui'
#
# Created: Thu Feb 19 10:27:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(507, 290)
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(10, 10, 491, 271))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        self.Ontology = QtGui.QWidget()
        self.Ontology.setObjectName("Ontology")
        self.horizontalLayout = QtGui.QHBoxLayout(self.Ontology)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OntologyText = QtGui.QTextBrowser(self.Ontology)
        self.OntologyText.setReadOnly(True)
        self.OntologyText.setOpenLinks(False)
        self.OntologyText.setObjectName("OntologyText")
        self.horizontalLayout.addWidget(self.OntologyText)
        self.tabWidget.addTab(self.Ontology, "")
        self.WordNet = QtGui.QWidget()
        self.WordNet.setObjectName("WordNet")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.WordNet)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.WordNetText = QtGui.QPlainTextEdit(self.WordNet)
        self.WordNetText.setReadOnly(True)
        self.WordNetText.setObjectName("WordNetText")
        self.horizontalLayout_2.addWidget(self.WordNetText)
        self.tabWidget.addTab(self.WordNet, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 1, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setPlaceholderText(QtGui.QApplication.translate("Form", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ontology), QtGui.QApplication.translate("Form", "Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.WordNet), QtGui.QApplication.translate("Form", "WordNet", None, QtGui.QApplication.UnicodeUTF8))

