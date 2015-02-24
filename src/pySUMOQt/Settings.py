""" This module involves all about the settings in the pySUMO GUI.

This module contains:

- WSettings: The settings of pySUMO's widgets.
- PluginManager: The manager for the plugin system in pySUMO.
- OptionDialog: The dialog that displays options of pySUMO.

"""

from PySide.QtCore import QSettings
from PySide.QtGui import QDialog

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
        super(LayoutManager, self).__init__("user-layout.ini", QSettings.IniFormat)
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
        self.restoreRecentOntologyHistory()
        
    def saveRecentOntologyHistory(self):
        pass

    def restoreRecentOntologyHistory(self):
        pass
    
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

class OptionDialog(QDialog):
    """ The option dialog is the displays and allows modification of settings
    for pySUMO. It displays options for the GUI, Widgets and library. The
    settings are organized by type and owner for ease of use. It also
    contains a plugin manager which enables loading and unloading of
    plugins.  The class also provides settings persistence by writing
    storing them in a file and reading from it on init.

    Attributes:

    - options: The options dictionary to manage in the option's dialog.

    Methods:

    - createView: Creates the view of the options dialog.
    - save: Saves the options.
    - load: Loads the options.

    """

    def __init__(self):
        """ Initializes the OptionDialog. """
        pass

    def createView(self):
        """ Initializes the view of the OptionDialog. """
        pass

    def save(self, path):
        """ Saves the settings to the given path.

        Arguments:

        - path: The path to which the settings will be written.

        Raises:

        - IOError

        """
        pass

    def load(self, path):
        """ Reads the settingns from the given path.

        Arguments:

        - path: The path from which the settings will be read.

        Raises:

        - IOError

        """
        pass
