""" This module involves all about the settings in the pySUMO GUI.

This module contains:

- WSettings: The settings of pySUMO's widgets.
- PluginManager: The manager for the plugin system in pySUMO.
- OptionDialog: The dialog that displays options of pySUMO.

"""

import pysumo
from PySide.QtCore import QSettings, Qt
from PySide.QtGui import QApplication, QColor
from pysumo.syntaxcontroller import Ontology

class LayoutManager(QSettings):
    """
    The layout manager handles the save and restore state of the main window and it's components.
    """
    def __init__(self, MainWindow):
        """
        Initializes the layout manager.
        
        Parameter :
        
        - MainWindow : The main window which owns the manager.
        """
        super(LayoutManager, self).__init__(pysumo.CONFIG_PATH + "/user-layout.ini", QSettings.IniFormat)
        self.mainwindow = MainWindow
    
    def saveLayout(self):
        """ 
        Save layout of the main window and persist it in a setting file.
        """
        self.clear()
        self.savePositionState(self.mainwindow)
        self.saveSizeState(self.mainwindow)
        self.setValue("mainWindow/state", self.mainwindow.saveState())
        self.saveStatusBarState()
        actions = self.mainwindow.menuTextEditorWidgets.actions()
        count = len(actions)
        self.setValue("TextEditorWidgets/count", count)
        actions = self.mainwindow.menuDocumentationWidgets.actions()
        count = len(actions)
        self.setValue("DocumentationWidgets/count", count)
        actions = self.mainwindow.menuHierarchyWidgets.actions()
        count = len(actions)
        self.setValue("HierarchyWidgets/count", count)
        actions = self.mainwindow.menuGraphWidgets.actions()
        count = len(actions)
        self.setValue("GraphWidgets/count", count)
        self.saveRecentOntologyHistory()
    
    def restoreLayout(self):
        """
        Restore the layout of the main window from the persitent setting file.
        """
        self.mainwindow.restoreState(self.value("mainWindow/state"))
        self.restoreSizeState(self.mainwindow)
        self.restorePositionState(self.mainwindow)
        self.restoreStatusBarState()
        # restore Text Editor Widgets
        self.restoreTextEditorWidgets()
        # restore Documentation Widgets
        self.restoreDocumentationWidgets()
        # restore Hierarchy Widgets
        self.restoreHierarchyWidgets()
        # restore graph widgets
        self.restoreGraphWidgets()
        self.restoreRecentOntologyHistory()
        
    def saveRecentOntologyHistory(self):
        """
        Save the list recently opened ontologies.
        """
        actions = self.mainwindow.menuRecent_Ontologies.actions()
        self.beginWriteArray("RecentOntologies")
        idx = 0
        for action in actions :
            data = action.data()
            if not data is None and type(data) == Ontology :
                self.setArrayIndex(idx)
                self.setValue("name", data.name)
                self.setValue("path", data.path)
                self.setValue("url", data.url)
                action_log = data.action_log
                log_io = action_log.log_io
                lpath = log_io.path
                self.setValue("lpath", lpath)
                idx = idx + 1
        self.endArray()

    def restoreRecentOntologyHistory(self):
        """
        Restore the recent opened ontologies and add them to index.
        """
        size = self.beginReadArray("RecentOntologies")
        for i in range(size) :
            self.setArrayIndex(i)
            name = self.value("name")
            path = self.value("path")
            url = self.value("url")
            lpath = self.value("lpath")
            ontology = Ontology(path=path, name=name, url=url, lpath=lpath)
            self.mainwindow.addRecentOntology(ontology)
        self.endArray()

    def restoreGraphWidgets(self):
        """
        Restore the graph widgets in the main window layout.
        """
        graphWidgetsCount = self.value("GraphWidgets/count")
        if graphWidgetsCount is None :
            graphWidgetsCount = 0
        graphWidgetsCount = int(graphWidgetsCount)
        count = 0
        while count < graphWidgetsCount :
            widget = self.mainwindow.createPySumoWidget("GraphWidget", self.mainwindow.menuGraphWidgets)
            self.mainwindow.addOrRestoreWidget(widget, self.mainwindow.menuGraphWidgets)
            count = count + 1
        
    def restoreTextEditorWidgets(self):
        """ 
        Restore the text editor widgets in the main window layout.
        """
        textEditorWidgetsCount = self.value("TextEditorWidgets/count")
        if textEditorWidgetsCount == None:
            textEditorWidgetsCount = 0
        textEditorWidgetsCount = int(textEditorWidgetsCount)
        count = 0
        while count < textEditorWidgetsCount:
            widget = self.mainwindow.createPySumoWidget("TextEditorWidget", self.mainwindow.menuTextEditorWidgets)
            self.mainwindow.addOrRestoreWidget(widget, self.mainwindow.menuTextEditorWidgets)
            count = count + 1
            
    def restoreDocumentationWidgets(self):
        """
        Restore the documentation widgets in the main window layout.
        """
        documentationWidgetsCount = self.value("DocumentationWidgets/count")
        if documentationWidgetsCount == None:
            documentationWidgetsCount = 0
        documentationWidgetsCount = int(documentationWidgetsCount)
        count = 0 
        while count < documentationWidgetsCount:
            widget = self.mainwindow.createPySumoWidget("DocumentationWidget", self.mainwindow.menuDocumentationWidgets)
            self.mainwindow.addOrRestoreWidget(widget, self.mainwindow.menuDocumentationWidgets)
            count = count + 1

    def restoreHierarchyWidgets(self):
        """
        Restore the hierarchy widgets in the main window layout.
        """
        hierarchyWidgetsCount = self.value("HierarchyWidgets/count")
        if hierarchyWidgetsCount == None:
            hierarchyWidgetsCount = 0
        hierarchyWidgetsCount = int(hierarchyWidgetsCount)
        count = 0 
        while count < hierarchyWidgetsCount:
            widget = self.mainwindow.createPySumoWidget("HierarchyWidget", self.mainwindow.menuHierarchyWidgets)
            self.mainwindow.addOrRestoreWidget(widget, self.mainwindow.menuHierarchyWidgets)
            count = count + 1

    def saveVisibilityState(self, qItem):
        """
        Saves the visibility state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which visibility has to be saved.
        """
        objName = qItem.objectName()
        self.setValue(objName + "/visible", qItem.isVisible())

    def restoreVisibilityState(self, qItem, qAction=None):
        """
        Restores the visibility state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which visibility has to be saved.
        - qAction : The action which toggles the visibility state of the qItem.
        """
        objName = qItem.objectName()
        visible = self.value(objName + "/visible")
        visible = str(visible).lower()
        if visible == "false":
            visible = False
        elif visible == "true":
            visible = True
        else:
            visible = None
        # if not visible :
        #   qAction.triggered.emit()
        #  qAction.setChecked(False)
        if visible != None:
            if qAction != None:
                qAction.setChecked(visible)
            qItem.setVisible(visible)

    def savePositionState(self, qItem):
        """
        Saves the position state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which position state has to be saved.
        """
        objName = qItem.objectName()
        pos = qItem.pos()
        xPos = pos.x()
        yPos = pos.y()
        self.setValue(objName + "/x", xPos)
        self.setValue(objName + "/y", yPos)

    def restorePositionState(self, qItem):
        """
        Restores the position state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which position state should be restored.
        """
        objName = qItem.objectName()
        xPos = self.value(objName + "/x")
        yPos = self.value(objName + "/y")
        if xPos == None or yPos == None:
            return
        xPos = int(xPos)
        yPos = int(yPos)
        qItem.move(xPos, yPos)

    def saveSizeState(self, qItem):
        """
        Saves the size state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which size state has to be saved.
        """
        objName = qItem.objectName()
        size = qItem.size()
        width = size.width()
        height = size.height()
        self.setValue(objName + "/width", width)
        self.setValue(objName + "/height", height)

    def restoreSizeState(self, qItem):
        """
        Restore the size state of a QWidget.
        
        Parameter :
        
        - qItem : The QWidget which size state has to be restored.
        """
        objName = qItem.objectName()
        width = self.value(objName + "/width")
        height = self.value(objName + "/height")
        if width == None or height == None:
            return
        width = int(width)
        height = int(height)
        qItem.resize(width, height)

    def saveStatusBarState(self):
        """ Save the status bar state. """
        self.saveVisibilityState(self.mainwindow.statusBar)

    def restoreStatusBarState(self):
        """ Restore the status bar state. """
        self.restoreVisibilityState(self.mainwindow.statusBar, self.mainwindow.actionStatusbar)

class PySumoSettings(QSettings):
    """ 
    Settings of PySumo.
    """
    
    def __init__(self, MainWindow, filepath):
        """
        Initializes the settings of pysumo.
        
        Parameter :
        
        - MainWindow : The main window of pysumo.
        - filepath : The path where to save settings.
        """
        super(PySumoSettings, self).__init__(filepath, QSettings.IniFormat)
        
    def loadDefaults(self):
        """ 
        Loads defaults settings of pysumo.
        """
        self.setValue("configPath", pysumo.CONFIG_PATH)
        self.setValue("maxQueueSize", 10)
        self.setValue("maxUndoRedoQueueSize", 10)
        self.setValue("flushWriteQueuesTimeout", 10)
        self.setValue("logOutputPath", pysumo.CONFIG_PATH)
        self.setValue("socketOutputPath", pysumo.CONFIG_PATH)
        self.setValue("logLevel", 10)
        defFont = QApplication.font().family()
        defSize = QApplication.font().pointSize()
        self.setValue("keywordsFontFamily", defFont)
        self.setValue("keywordsFontSize", defSize)
        self.setValue("keywordsFontColor", QColor(Qt.darkGreen).name())
        self.setValue("keywordsBoldStyle", True)
        self.setValue("keywordsItalicStyle", False)
        self.setValue("keywordsUnderlinedStyle", False)
        self.setValue("logicExprFontFamily", defFont)
        self.setValue("logicExprFontSize", defSize)
        self.setValue("logicExprFontColor", QColor(Qt.black).name())
        self.setValue("logicExprBoldStyle", True)
        self.setValue("logicExprItalicStyle", False)
        self.setValue("logicExprUnderlinedStyle", False)
        self.setValue("commentFontFamily", defFont)
        self.setValue("commentFontSize", defSize)
        self.setValue("commentFontColor", QColor(Qt.darkMagenta).name())
        self.setValue("commentBoldStyle", False)
        self.setValue("commentItalicStyle", True)
        self.setValue("commentUnderlinedStyle", False)
        self.setValue("stringsFontFamily", defFont)
        self.setValue("stringsFontSize", defSize)
        self.setValue("stringsFontColor", QColor(Qt.red).name())
        self.setValue("stringsBoldStyle", False)
        self.setValue("stringsItalicStyle", False)
        self.setValue("stringsUnderlinedStyle", False)
        self.setValue("maxTextEditorWidgets", 10)
        self.setValue("maxDocumentationWidgets", 10)
        self.setValue("maxHierarchyWidgets", 10)
        self.setValue("maxGraphWidgets", 10)
        self.setValue("defaultFontSize", defSize)
        self.setValue("defaultFontFamily", defFont)
        self.setValue("defaultFontColor", QApplication.palette().text().color().name())
        self.setValue("useHighlightingFontSize", False)
    