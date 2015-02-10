# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Feb 10 11:06:33 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(680, 364)
        mainwindow.setDockNestingEnabled(True)
        self.centralwidget = QtGui.QWidget(mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainwindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.openOntology = QtGui.QMenu(self.menuFile)
        self.openOntology.setToolTip("")
        self.openOntology.setStatusTip("")
        self.openOntology.setWhatsThis("")
        self.openOntology.setAccessibleName("")
        self.openOntology.setAccessibleDescription("")
        self.openOntology.setTitle("Open")
        self.openOntology.setObjectName("openOntology")
        self.menuRecent_Ontologies = QtGui.QMenu(self.menuFile)
        self.menuRecent_Ontologies.setObjectName("menuRecent_Ontologies")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuToolbar = QtGui.QMenu(self.menuView)
        self.menuToolbar.setObjectName("menuToolbar")
        self.menuAdd = QtGui.QMenu(self.menuView)
        self.menuAdd.setObjectName("menuAdd")
        self.menuTextEditorWidgets = QtGui.QMenu(self.menuView)
        self.menuTextEditorWidgets.setObjectName("menuTextEditorWidgets")
        self.menuDocumentationWidgets = QtGui.QMenu(self.menuView)
        self.menuDocumentationWidgets.setObjectName("menuDocumentationWidgets")
        self.menuHierarchyWidgets = QtGui.QMenu(self.menuView)
        self.menuHierarchyWidgets.setObjectName("menuHierarchyWidgets")
        self.menuDelete = QtGui.QMenu(self.menuView)
        self.menuDelete.setEnabled(False)
        self.menuDelete.setObjectName("menuDelete")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuOntology = QtGui.QMenu(self.menubar)
        self.menuOntology.setObjectName("menuOntology")
        mainwindow.setMenuBar(self.menubar)
        self.toolBarFile = QtGui.QToolBar(mainwindow)
        self.toolBarFile.setObjectName("toolBarFile")
        mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarFile)
        self.toolBarEdit = QtGui.QToolBar(mainwindow)
        self.toolBarEdit.setObjectName("toolBarEdit")
        mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarEdit)
        self.toolBarOntology = QtGui.QToolBar(mainwindow)
        self.toolBarOntology.setObjectName("toolBarOntology")
        mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarOntology)
        self.toolBarTools = QtGui.QToolBar(mainwindow)
        self.toolBarTools.setObjectName("toolBarTools")
        mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarTools)
        self.toolBarHelp = QtGui.QToolBar(mainwindow)
        self.toolBarHelp.setObjectName("toolBarHelp")
        mainwindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarHelp)
        self.statusBar = QtGui.QStatusBar(mainwindow)
        self.statusBar.setObjectName("statusBar")
        mainwindow.setStatusBar(self.statusBar)
        self.newOntologyAction = QtGui.QAction(mainwindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newOntologyAction.setIcon(icon)
        self.newOntologyAction.setText("New Ontology")
        self.newOntologyAction.setIconText("New Ontology")
        self.newOntologyAction.setToolTip("New Ontology")
        self.newOntologyAction.setStatusTip("")
        self.newOntologyAction.setWhatsThis("")
        self.newOntologyAction.setShortcut("Ctrl+N")
        self.newOntologyAction.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.newOntologyAction.setIconVisibleInMenu(True)
        self.newOntologyAction.setObjectName("newOntologyAction")
        self.openLocalOntologyAction = QtGui.QAction(mainwindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openLocalOntologyAction.setIcon(icon1)
        self.openLocalOntologyAction.setIconVisibleInMenu(True)
        self.openLocalOntologyAction.setObjectName("openLocalOntologyAction")
        self.openRemoteOntologyAction = QtGui.QAction(mainwindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-open-remote.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openRemoteOntologyAction.setIcon(icon2)
        self.openRemoteOntologyAction.setText("Remote Ontology")
        self.openRemoteOntologyAction.setIconText("Remote Ontology")
        self.openRemoteOntologyAction.setToolTip("Remote Ontology")
        self.openRemoteOntologyAction.setStatusTip("")
        self.openRemoteOntologyAction.setWhatsThis("")
        self.openRemoteOntologyAction.setShortcut("Ctrl+R")
        self.openRemoteOntologyAction.setMenuRole(QtGui.QAction.ApplicationSpecificRole)
        self.openRemoteOntologyAction.setIconVisibleInMenu(True)
        self.openRemoteOntologyAction.setObjectName("openRemoteOntologyAction")
        self.action1_Table_kif = QtGui.QAction(mainwindow)
        self.action1_Table_kif.setObjectName("action1_Table_kif")
        self.action2_Distance_kif = QtGui.QAction(mainwindow)
        self.action2_Distance_kif.setObjectName("action2_Distance_kif")
        self.clearHistoryAction = QtGui.QAction(mainwindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-clear-history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearHistoryAction.setIcon(icon3)
        self.clearHistoryAction.setIconVisibleInMenu(True)
        self.clearHistoryAction.setObjectName("clearHistoryAction")
        self.actionSave = QtGui.QAction(mainwindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon4)
        self.actionSave.setIconVisibleInMenu(True)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtGui.QAction(mainwindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-save-as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSaveAs.setIcon(icon5)
        self.actionSaveAs.setIconVisibleInMenu(True)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionRevert = QtGui.QAction(mainwindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-revert.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRevert.setIcon(icon6)
        self.actionRevert.setIconVisibleInMenu(True)
        self.actionRevert.setObjectName("actionRevert")
        self.actionPrint = QtGui.QAction(mainwindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPrint.setIcon(icon7)
        self.actionPrint.setIconVisibleInMenu(True)
        self.actionPrint.setObjectName("actionPrint")
        self.actionClose = QtGui.QAction(mainwindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClose.setIcon(icon8)
        self.actionClose.setIconVisibleInMenu(True)
        self.actionClose.setObjectName("actionClose")
        self.actionExit = QtGui.QAction(mainwindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/application-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon9)
        self.actionExit.setMenuRole(QtGui.QAction.QuitRole)
        self.actionExit.setIconVisibleInMenu(True)
        self.actionExit.setObjectName("actionExit")
        self.actionProperties = QtGui.QAction(mainwindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-properties.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProperties.setIcon(icon10)
        self.actionProperties.setIconVisibleInMenu(True)
        self.actionProperties.setObjectName("actionProperties")
        self.actionQuickPrint = QtGui.QAction(mainwindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/document-quickprint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuickPrint.setIcon(icon11)
        self.actionQuickPrint.setIconVisibleInMenu(True)
        self.actionQuickPrint.setObjectName("actionQuickPrint")
        self.actionUndo = QtGui.QAction(mainwindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-undo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUndo.setIcon(icon12)
        self.actionUndo.setIconVisibleInMenu(True)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtGui.QAction(mainwindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-redo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRedo.setIcon(icon13)
        self.actionRedo.setIconVisibleInMenu(True)
        self.actionRedo.setObjectName("actionRedo")
        self.actionCut = QtGui.QAction(mainwindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-cut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCut.setIcon(icon14)
        self.actionCut.setIconVisibleInMenu(True)
        self.actionCut.setObjectName("actionCut")
        self.actionCopy = QtGui.QAction(mainwindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon15)
        self.actionCopy.setIconVisibleInMenu(True)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtGui.QAction(mainwindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-paste.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPaste.setIcon(icon16)
        self.actionPaste.setIconVisibleInMenu(True)
        self.actionPaste.setObjectName("actionPaste")
        self.actionDelete = QtGui.QAction(mainwindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon17)
        self.actionDelete.setIconVisibleInMenu(True)
        self.actionDelete.setObjectName("actionDelete")
        self.actionSelectAll = QtGui.QAction(mainwindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-select-all.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelectAll.setIcon(icon18)
        self.actionSelectAll.setIconVisibleInMenu(True)
        self.actionSelectAll.setObjectName("actionSelectAll")
        self.actionPySUMOHelp = QtGui.QAction(mainwindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/help-contents.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPySUMOHelp.setIcon(icon19)
        self.actionPySUMOHelp.setIconVisibleInMenu(True)
        self.actionPySUMOHelp.setObjectName("actionPySUMOHelp")
        self.actionPySUMOTutorials = QtGui.QAction(mainwindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/help-hint.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPySUMOTutorials.setIcon(icon20)
        self.actionPySUMOTutorials.setIconVisibleInMenu(True)
        self.actionPySUMOTutorials.setObjectName("actionPySUMOTutorials")
        self.actionFAQ = QtGui.QAction(mainwindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/help-faq.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFAQ.setIcon(icon21)
        self.actionFAQ.setIconVisibleInMenu(True)
        self.actionFAQ.setObjectName("actionFAQ")
        self.actionAboutSUMO = QtGui.QAction(mainwindow)
        self.actionAboutSUMO.setObjectName("actionAboutSUMO")
        self.actionAboutSUOKIF = QtGui.QAction(mainwindow)
        self.actionAboutSUOKIF.setObjectName("actionAboutSUOKIF")
        self.actionAboutpySUMO = QtGui.QAction(mainwindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/help-about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAboutpySUMO.setIcon(icon22)
        self.actionAboutpySUMO.setIconVisibleInMenu(True)
        self.actionAboutpySUMO.setObjectName("actionAboutpySUMO")
        self.actionSettings = QtGui.QAction(mainwindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon23)
        self.actionSettings.setIconVisibleInMenu(True)
        self.actionSettings.setObjectName("actionSettings")
        self.actionHierarchyWidget = QtGui.QAction(mainwindow)
        self.actionHierarchyWidget.setCheckable(False)
        self.actionHierarchyWidget.setChecked(False)
        self.actionHierarchyWidget.setEnabled(True)
        self.actionHierarchyWidget.setObjectName("actionHierarchyWidget")
        self.actionDocumentationWidget = QtGui.QAction(mainwindow)
        self.actionDocumentationWidget.setCheckable(False)
        self.actionDocumentationWidget.setChecked(False)
        self.actionDocumentationWidget.setObjectName("actionDocumentationWidget")
        self.actionGraphWidget = QtGui.QAction(mainwindow)
        self.actionGraphWidget.setCheckable(False)
        self.actionGraphWidget.setChecked(False)
        self.actionGraphWidget.setObjectName("actionGraphWidget")
        self.actionTextEditorWidget = QtGui.QAction(mainwindow)
        self.actionTextEditorWidget.setCheckable(False)
        self.actionTextEditorWidget.setEnabled(True)
        self.actionTextEditorWidget.setVisible(True)
        self.actionTextEditorWidget.setObjectName("actionTextEditorWidget")
        self.actionZoomIn = QtGui.QAction(mainwindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomIn.setIcon(icon24)
        self.actionZoomIn.setIconVisibleInMenu(True)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QtGui.QAction(mainwindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOut.setIcon(icon25)
        self.actionZoomOut.setIconVisibleInMenu(True)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionFile = QtGui.QAction(mainwindow)
        self.actionFile.setCheckable(True)
        self.actionFile.setChecked(True)
        self.actionFile.setObjectName("actionFile")
        self.actionEdit = QtGui.QAction(mainwindow)
        self.actionEdit.setCheckable(True)
        self.actionEdit.setChecked(True)
        self.actionEdit.setObjectName("actionEdit")
        self.actionTools = QtGui.QAction(mainwindow)
        self.actionTools.setCheckable(True)
        self.actionTools.setChecked(True)
        self.actionTools.setObjectName("actionTools")
        self.actionHelp = QtGui.QAction(mainwindow)
        self.actionHelp.setCheckable(True)
        self.actionHelp.setChecked(True)
        self.actionHelp.setObjectName("actionHelp")
        self.actionConfigureToollbars = QtGui.QAction(mainwindow)
        self.actionConfigureToollbars.setObjectName("actionConfigureToollbars")
        self.actionAddTerms = QtGui.QAction(mainwindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/list-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAddTerms.setIcon(icon26)
        self.actionAddTerms.setIconVisibleInMenu(True)
        self.actionAddTerms.setObjectName("actionAddTerms")
        self.actionRemoveTerms = QtGui.QAction(mainwindow)
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRemoveTerms.setIcon(icon27)
        self.actionRemoveTerms.setIconVisibleInMenu(True)
        self.actionRemoveTerms.setObjectName("actionRemoveTerms")
        self.actionUpdate = QtGui.QAction(mainwindow)
        icon28 = QtGui.QIcon()
        icon28.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/update-product.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUpdate.setIcon(icon28)
        self.actionUpdate.setIconVisibleInMenu(True)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionFind = QtGui.QAction(mainwindow)
        icon29 = QtGui.QIcon()
        icon29.addPixmap(QtGui.QPixmap(":/actions/gfx/actions/edit-find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFind.setIcon(icon29)
        self.actionFind.setIconVisibleInMenu(True)
        self.actionFind.setObjectName("actionFind")
        self.actionOntology = QtGui.QAction(mainwindow)
        self.actionOntology.setCheckable(True)
        self.actionOntology.setChecked(True)
        self.actionOntology.setObjectName("actionOntology")
        self.actionStatusbar = QtGui.QAction(mainwindow)
        self.actionStatusbar.setCheckable(True)
        self.actionStatusbar.setChecked(True)
        self.actionStatusbar.setObjectName("actionStatusbar")
        self.actionExpand = QtGui.QAction(mainwindow)
        self.actionExpand.setObjectName("actionExpand")
        self.actionCollapse = QtGui.QAction(mainwindow)
        self.actionCollapse.setObjectName("actionCollapse")
        self.openOntology.addAction(self.openLocalOntologyAction)
        self.openOntology.addSeparator()
        self.openOntology.addAction(self.openRemoteOntologyAction)
        self.menuRecent_Ontologies.addAction(self.action1_Table_kif)
        self.menuRecent_Ontologies.addAction(self.action2_Distance_kif)
        self.menuRecent_Ontologies.addSeparator()
        self.menuRecent_Ontologies.addAction(self.clearHistoryAction)
        self.menuFile.addAction(self.newOntologyAction)
        self.menuFile.addAction(self.openOntology.menuAction())
        self.menuFile.addAction(self.menuRecent_Ontologies.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addAction(self.actionQuickPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionProperties)
        self.menuFile.addAction(self.actionRevert)
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete)
        self.menuEdit.addAction(self.actionSelectAll)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionFind)
        self.menuToolbar.addAction(self.actionFile)
        self.menuToolbar.addAction(self.actionEdit)
        self.menuToolbar.addAction(self.actionOntology)
        self.menuToolbar.addAction(self.actionTools)
        self.menuToolbar.addAction(self.actionHelp)
        self.menuToolbar.addSeparator()
        self.menuToolbar.addAction(self.actionConfigureToollbars)
        self.menuAdd.addAction(self.actionTextEditorWidget)
        self.menuAdd.addAction(self.actionHierarchyWidget)
        self.menuAdd.addAction(self.actionGraphWidget)
        self.menuAdd.addAction(self.actionDocumentationWidget)
        self.menuView.addAction(self.menuAdd.menuAction())
        self.menuView.addAction(self.menuTextEditorWidgets.menuAction())
        self.menuView.addAction(self.menuDocumentationWidgets.menuAction())
        self.menuView.addAction(self.menuHierarchyWidgets.menuAction())
        self.menuView.addAction(self.menuDelete.menuAction())
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionExpand)
        self.menuView.addAction(self.actionCollapse)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addSeparator()
        self.menuView.addAction(self.menuToolbar.menuAction())
        self.menuView.addAction(self.actionStatusbar)
        self.menuTools.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionPySUMOHelp)
        self.menuHelp.addAction(self.actionPySUMOTutorials)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionFAQ)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAboutSUMO)
        self.menuHelp.addAction(self.actionAboutSUOKIF)
        self.menuHelp.addAction(self.actionAboutpySUMO)
        self.menuOntology.addAction(self.actionAddTerms)
        self.menuOntology.addAction(self.actionRemoveTerms)
        self.menuOntology.addSeparator()
        self.menuOntology.addAction(self.actionUpdate)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuOntology.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBarFile.addAction(self.newOntologyAction)
        self.toolBarFile.addAction(self.openLocalOntologyAction)
        self.toolBarFile.addAction(self.openRemoteOntologyAction)
        self.toolBarFile.addSeparator()
        self.toolBarFile.addAction(self.actionSave)
        self.toolBarFile.addAction(self.actionPrint)
        self.toolBarEdit.addAction(self.actionUndo)
        self.toolBarEdit.addAction(self.actionRedo)
        self.toolBarEdit.addSeparator()
        self.toolBarEdit.addAction(self.actionCut)
        self.toolBarEdit.addAction(self.actionCopy)
        self.toolBarEdit.addAction(self.actionPaste)
        self.toolBarOntology.addAction(self.actionAddTerms)
        self.toolBarOntology.addAction(self.actionRemoveTerms)
        self.toolBarOntology.addSeparator()
        self.toolBarOntology.addAction(self.actionUpdate)
        self.toolBarTools.addAction(self.actionSettings)
        self.toolBarHelp.addAction(self.actionPySUMOHelp)
        self.toolBarHelp.addAction(self.actionPySUMOTutorials)

        self.retranslateUi(mainwindow)
        QtCore.QObject.connect(self.actionFile, QtCore.SIGNAL("triggered(bool)"), self.toolBarFile.setVisible)
        QtCore.QObject.connect(self.actionEdit, QtCore.SIGNAL("triggered(bool)"), self.toolBarEdit.setVisible)
        QtCore.QObject.connect(self.actionOntology, QtCore.SIGNAL("triggered(bool)"), self.toolBarOntology.setVisible)
        QtCore.QObject.connect(self.actionTools, QtCore.SIGNAL("triggered(bool)"), self.toolBarTools.setVisible)
        QtCore.QObject.connect(self.actionHelp, QtCore.SIGNAL("triggered(bool)"), self.toolBarHelp.setVisible)
        QtCore.QObject.connect(self.actionStatusbar, QtCore.SIGNAL("triggered(bool)"), self.statusBar.setVisible)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL("triggered()"), mainwindow.close)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(QtGui.QApplication.translate("mainwindow", "pySUMO", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("mainwindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuRecent_Ontologies.setTitle(QtGui.QApplication.translate("mainwindow", "Recent Ontologies", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("mainwindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("mainwindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuToolbar.setTitle(QtGui.QApplication.translate("mainwindow", "Toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAdd.setTitle(QtGui.QApplication.translate("mainwindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTextEditorWidgets.setTitle(QtGui.QApplication.translate("mainwindow", "Text Editor Widgets", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDocumentationWidgets.setTitle(QtGui.QApplication.translate("mainwindow", "Documentation Widgets", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHierarchyWidgets.setTitle(QtGui.QApplication.translate("mainwindow", "Hierarchy Widgets", None, QtGui.QApplication.UnicodeUTF8))
        self.menuDelete.setTitle(QtGui.QApplication.translate("mainwindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTools.setTitle(QtGui.QApplication.translate("mainwindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("mainwindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuOntology.setTitle(QtGui.QApplication.translate("mainwindow", "Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarFile.setWindowTitle(QtGui.QApplication.translate("mainwindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarEdit.setWindowTitle(QtGui.QApplication.translate("mainwindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarOntology.setWindowTitle(QtGui.QApplication.translate("mainwindow", "toolBar_3", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarTools.setWindowTitle(QtGui.QApplication.translate("mainwindow", "toolBar_4", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarHelp.setWindowTitle(QtGui.QApplication.translate("mainwindow", "toolBar_5", None, QtGui.QApplication.UnicodeUTF8))
        self.openLocalOntologyAction.setText(QtGui.QApplication.translate("mainwindow", "Local Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.openLocalOntologyAction.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action1_Table_kif.setText(QtGui.QApplication.translate("mainwindow", "1 Table.kif", None, QtGui.QApplication.UnicodeUTF8))
        self.action2_Distance_kif.setText(QtGui.QApplication.translate("mainwindow", "2 Distance.kif", None, QtGui.QApplication.UnicodeUTF8))
        self.clearHistoryAction.setText(QtGui.QApplication.translate("mainwindow", "Clear History", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("mainwindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setText(QtGui.QApplication.translate("mainwindow", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveAs.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRevert.setText(QtGui.QApplication.translate("mainwindow", "Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setText(QtGui.QApplication.translate("mainwindow", "Print...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrint.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("mainwindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("mainwindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProperties.setText(QtGui.QApplication.translate("mainwindow", "Properties...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuickPrint.setText(QtGui.QApplication.translate("mainwindow", "Quick Print", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuickPrint.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+Shift+P", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setText(QtGui.QApplication.translate("mainwindow", "Undo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUndo.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setText(QtGui.QApplication.translate("mainwindow", "Redo", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRedo.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+Shift+Z", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setText(QtGui.QApplication.translate("mainwindow", "Cut", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCut.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+X", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setText(QtGui.QApplication.translate("mainwindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCopy.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setText(QtGui.QApplication.translate("mainwindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPaste.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("mainwindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setShortcut(QtGui.QApplication.translate("mainwindow", "Del", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectAll.setText(QtGui.QApplication.translate("mainwindow", "Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSelectAll.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPySUMOHelp.setText(QtGui.QApplication.translate("mainwindow", "pySUMO Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPySUMOHelp.setShortcut(QtGui.QApplication.translate("mainwindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPySUMOTutorials.setText(QtGui.QApplication.translate("mainwindow", "pySUMO Tutorials", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFAQ.setText(QtGui.QApplication.translate("mainwindow", "F.A.Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutSUMO.setText(QtGui.QApplication.translate("mainwindow", "About SUMO", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutSUOKIF.setText(QtGui.QApplication.translate("mainwindow", "About SUO-KIF", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutpySUMO.setText(QtGui.QApplication.translate("mainwindow", "About pySUMO", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("mainwindow", "Settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHierarchyWidget.setText(QtGui.QApplication.translate("mainwindow", "Hierarchy Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDocumentationWidget.setText(QtGui.QApplication.translate("mainwindow", "Documentation Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGraphWidget.setText(QtGui.QApplication.translate("mainwindow", "Graph Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTextEditorWidget.setText(QtGui.QApplication.translate("mainwindow", "Text Editor Widget", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setText(QtGui.QApplication.translate("mainwindow", "Zoom In ", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomIn.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomOut.setText(QtGui.QApplication.translate("mainwindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.actionZoomOut.setShortcut(QtGui.QApplication.translate("mainwindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFile.setText(QtGui.QApplication.translate("mainwindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit.setText(QtGui.QApplication.translate("mainwindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTools.setText(QtGui.QApplication.translate("mainwindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("mainwindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigureToollbars.setText(QtGui.QApplication.translate("mainwindow", "Configure Toolbars...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAddTerms.setText(QtGui.QApplication.translate("mainwindow", "Add Terms", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemoveTerms.setText(QtGui.QApplication.translate("mainwindow", "Remove Terms", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate.setText(QtGui.QApplication.translate("mainwindow", "Update ", None, QtGui.QApplication.UnicodeUTF8))
        self.actionFind.setText(QtGui.QApplication.translate("mainwindow", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOntology.setText(QtGui.QApplication.translate("mainwindow", "Ontology", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStatusbar.setText(QtGui.QApplication.translate("mainwindow", "Statusbar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExpand.setText(QtGui.QApplication.translate("mainwindow", "Expand", None, QtGui.QApplication.UnicodeUTF8))
        self.actionCollapse.setText(QtGui.QApplication.translate("mainwindow", "Collapse", None, QtGui.QApplication.UnicodeUTF8))

import pySUMOQt.Designer.css_rc
import pySUMOQt.Designer.gfx_rc
