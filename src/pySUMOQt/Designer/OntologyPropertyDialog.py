# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OntologyPropertyDialog.ui'
#
# Created: Thu Mar  5 15:30:08 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 233)
        Dialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 10, -1, 10)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtGui.QLabel(self.widget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.ontologyName = QtGui.QLineEdit(self.widget)
        self.ontologyName.setObjectName("ontologyName")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.ontologyName)
        self.pathLabel = QtGui.QLabel(self.widget)
        self.pathLabel.setObjectName("pathLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.pathLabel)
        self.ontologyPathWidget = QtGui.QWidget(self.widget)
        self.ontologyPathWidget.setObjectName("ontologyPathWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.ontologyPathWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ontologyPath = QtGui.QLineEdit(self.ontologyPathWidget)
        self.ontologyPath.setEnabled(False)
        self.ontologyPath.setReadOnly(True)
        self.ontologyPath.setObjectName("ontologyPath")
        self.horizontalLayout.addWidget(self.ontologyPath)
        self.ontologyPathChooser = QtGui.QToolButton(self.ontologyPathWidget)
        self.ontologyPathChooser.setObjectName("ontologyPathChooser")
        self.horizontalLayout.addWidget(self.ontologyPathChooser)
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.ontologyPathWidget)
        self.urlLabel = QtGui.QLabel(self.widget)
        self.urlLabel.setObjectName("urlLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.urlLabel)
        self.ontologyUrl = QtGui.QLineEdit(self.widget)
        self.ontologyUrl.setObjectName("ontologyUrl")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.ontologyUrl)
        self.logPathLabel = QtGui.QLabel(self.widget)
        self.logPathLabel.setObjectName("logPathLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.logPathLabel)
        self.ontologyLogPathWidget = QtGui.QWidget(self.widget)
        self.ontologyLogPathWidget.setObjectName("ontologyLogPathWidget")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.ontologyLogPathWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ontologyLogPath = QtGui.QLineEdit(self.ontologyLogPathWidget)
        self.ontologyLogPath.setEnabled(False)
        self.ontologyLogPath.setReadOnly(True)
        self.ontologyLogPath.setObjectName("ontologyLogPath")
        self.horizontalLayout_3.addWidget(self.ontologyLogPath)
        self.ontologyLogPathChooser = QtGui.QToolButton(self.ontologyLogPathWidget)
        self.ontologyLogPathChooser.setObjectName("ontologyLogPathChooser")
        self.horizontalLayout_3.addWidget(self.ontologyLogPathChooser)
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ontologyLogPathWidget)
        self.gridLayout_2.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Ontology Properties", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.pathLabel.setText(QtGui.QApplication.translate("Dialog", "Path", None, QtGui.QApplication.UnicodeUTF8))
        self.ontologyPathChooser.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.urlLabel.setText(QtGui.QApplication.translate("Dialog", "Url", None, QtGui.QApplication.UnicodeUTF8))
        self.logPathLabel.setText(QtGui.QApplication.translate("Dialog", "Log Path", None, QtGui.QApplication.UnicodeUTF8))
        self.ontologyLogPathChooser.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))

