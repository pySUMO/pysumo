# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OpenRemoteOntologyDialog.ui'
#
# Created: Wed Feb 11 09:55:15 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_OpenRemoteOntologyDialog(object):
    def setupUi(self, OpenRemoteOntologyDialog):
        OpenRemoteOntologyDialog.setObjectName("OpenRemoteOntologyDialog")
        OpenRemoteOntologyDialog.resize(535, 186)
        self.gridLayout = QtGui.QGridLayout(OpenRemoteOntologyDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(OpenRemoteOntologyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.RestoreDefaults)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(OpenRemoteOntologyDialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.url = QtGui.QLineEdit(self.widget)
        self.url.setObjectName("url")
        self.gridLayout_2.addWidget(self.url, 0, 1, 1, 2)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.browseBtn = QtGui.QToolButton(self.widget)
        self.browseBtn.setObjectName("browseBtn")
        self.gridLayout_2.addWidget(self.browseBtn, 2, 2, 1, 1)
        self.path = QtGui.QLineEdit(self.widget)
        self.path.setEnabled(False)
        self.path.setReadOnly(True)
        self.path.setObjectName("path")
        self.gridLayout_2.addWidget(self.path, 2, 1, 1, 1)
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 3, 1, 1, 2)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(OpenRemoteOntologyDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), OpenRemoteOntologyDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), OpenRemoteOntologyDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(OpenRemoteOntologyDialog)

    def retranslateUi(self, OpenRemoteOntologyDialog):
        OpenRemoteOntologyDialog.setWindowTitle(QtGui.QApplication.translate("OpenRemoteOntologyDialog", "Open Remote Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OpenRemoteOntologyDialog", "Url: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("OpenRemoteOntologyDialog", "Path: ", None, QtGui.QApplication.UnicodeUTF8))
        self.browseBtn.setText(QtGui.QApplication.translate("OpenRemoteOntologyDialog", "...", None, QtGui.QApplication.UnicodeUTF8))

