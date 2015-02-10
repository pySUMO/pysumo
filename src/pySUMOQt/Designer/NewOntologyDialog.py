# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewOntologyDialog.ui'
#
# Created: Tue Feb 10 16:35:07 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_NewOntologyDialog(object):
    def setupUi(self, NewOntologyDialog):
        NewOntologyDialog.setObjectName("NewOntologyDialog")
        NewOntologyDialog.resize(520, 192)
        NewOntologyDialog.setSizeGripEnabled(True)
        NewOntologyDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(NewOntologyDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(NewOntologyDialog)
        self.buttonBox.setStyleSheet("")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(NewOntologyDialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.ontologyName = QtGui.QLineEdit(self.widget)
        self.ontologyName.setObjectName("ontologyName")
        self.gridLayout_2.addWidget(self.ontologyName, 0, 2, 1, 1)
        self.ontologyPath = QtGui.QLineEdit(self.widget)
        self.ontologyPath.setEnabled(False)
        self.ontologyPath.setReadOnly(True)
        self.ontologyPath.setObjectName("ontologyPath")
        self.gridLayout_2.addWidget(self.ontologyPath, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.browseFolderBtn = QtGui.QToolButton(self.widget)
        self.browseFolderBtn.setObjectName("browseFolderBtn")
        self.gridLayout_2.addWidget(self.browseFolderBtn, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(NewOntologyDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewOntologyDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewOntologyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewOntologyDialog)

    def retranslateUi(self, NewOntologyDialog):
        NewOntologyDialog.setWindowTitle(QtGui.QApplication.translate("NewOntologyDialog", "New Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewOntologyDialog", "Path: ", None, QtGui.QApplication.UnicodeUTF8))
        self.ontologyName.setToolTip(QtGui.QApplication.translate("NewOntologyDialog", "<html><head/><body><p align=\"justify\">Enter the name of the ontology in this field. The name should not be empty and respect the ASCII standard.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.ontologyName.setPlaceholderText(QtGui.QApplication.translate("NewOntologyDialog", "The name of the ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.ontologyPath.setToolTip(QtGui.QApplication.translate("NewOntologyDialog", "<html><head/><body><p>This field contains the path to the folder where the ontology file sould be save. By default this field contains the default user director. To choose another output directory for the ontology file, click on the &quot;...&quot; browse button.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewOntologyDialog", "Name: ", None, QtGui.QApplication.UnicodeUTF8))
        self.browseFolderBtn.setText(QtGui.QApplication.translate("NewOntologyDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

