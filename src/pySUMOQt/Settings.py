""" This module involves all about the settings in the pySUMO GUI.

This module contains:

- WSettings: The settings of pySUMO's widgets.
- PluginManager: The manager for the plugin system in pySUMO.
- OptionDialog: The dialog that displays options of pySUMO.

"""

from PySide.QtCore import QSettings, Qt
from PySide.QtGui import QApplication, QColor
from pysumo import logger
from os import environ

class WSettings(QSettings):
    """ This class represents the settings of the widgets in pySUMO's GUI.  The
    settings are stored in a local file for persistence and are loaded from
    there at init. """

    def __init__(self, widget):
        """ Initializes the widget's settings.

        Argument:

        - widget: The widget which owns the settings.

        """
        pass
    
class LayoutManager(QSettings):
    
    def __init__(self, MainWindow):
        super(LayoutManager, self).__init__(logger.CONFIG_PATH + "/user-layout.ini", QSettings.IniFormat)
        self.mainwindow = MainWindow
    
    def saveLayout(self):
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
        pass

    def restoreRecentOntologyHistory(self):
        pass
    
    def restoreGraphWidgets(self):
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
        objName = qItem.objectName()
        self.setValue(objName + "/visible", qItem.isVisible())

    def restoreVisibilityState(self, qItem, qAction=None):
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
        objName = qItem.objectName()
        pos = qItem.pos()
        xPos = pos.x()
        yPos = pos.y()
        self.setValue(objName + "/x", xPos)
        self.setValue(objName + "/y", yPos)

    def restorePositionState(self, qItem):
        objName = qItem.objectName()
        xPos = self.value(objName + "/x")
        yPos = self.value(objName + "/y")
        if xPos == None or yPos == None:
            return
        xPos = int(xPos)
        yPos = int(yPos)
        qItem.move(xPos, yPos)

    def saveSizeState(self, qItem):
        objName = qItem.objectName()
        size = qItem.size()
        width = size.width()
        height = size.height()
        self.setValue(objName + "/width", width)
        self.setValue(objName + "/height", height)

    def restoreSizeState(self, qItem):
        objName = qItem.objectName()
        width = self.value(objName + "/width")
        height = self.value(objName + "/height")
        if width == None or height == None:
            return
        width = int(width)
        height = int(height)
        qItem.resize(width, height)

    def saveStatusBarState(self):
        self.saveVisibilityState(self.mainwindow.statusBar)

    def restoreStatusBarState(self):
        self.restoreVisibilityState(self.mainwindow.statusBar, self.mainwindow.actionStatusbar)

class PySumoSettings(QSettings):
    
    def __init__(self, MainWindow, filepath):
        super(PySumoSettings, self).__init__(filepath, QSettings.IniFormat)
        
    def loadDefaults(self):
        self.setValue("configPath", environ['HOME'] + "/pySUMO")
        self.setValue("maxQueueSize", 10)
        self.setValue("maxUndoRedoQueueSize", 10)
        self.setValue("flushWriteQueuesTimeout", 10)
        self.setValue("logOutputPath", logger.CONFIG_PATH)
        self.setValue("socketOutputPath", logger.CONFIG_PATH)
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
    
class PluginManager():
    """ The PluginManager handles all loadabel plugins. At startup it loads all
    plugins and restores their settings from the persistence file.  It also
    manages unloading of plugins from the current application instance. The
    PluginManager also maintains the list of active plugins which is used on
    initialization of pySUMO to check which plugins should be loaded.
    """

    def __init__(self):
        """ Initializes the PluginManager. """
        self.plugins = []

    def get_plugins(self):
        """ Returns a list of the currently active plugins.

        Returns:

        - Widget[]

        """
        pass

    def add_plugin(self, path):
        """ Adds a plugin to the list of managed plugins.

        Argument:

        - path: The path where the plugin is located.

        Returns:

        - Boolean

        """
        pass

    def remove_plugin(self, name):
        """ Removes a plugin from the list of managed plugins.

        Argument:

        - name: The name of the plugin to remove.

        Returns:

        - Boolean

        """
        pass

