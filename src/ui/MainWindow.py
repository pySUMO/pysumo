""" This module contains the Main Window for pySUMO.

This module contains:

- MainWindow: pySUMO's main window.
- HelpDialog: The dialog that displays help in pySUMO GUI.

"""
from PySide import QtGui
from PySide.QtGui import QMainWindow
from PySide.QtGui import QApplication
from PySide.QtGui import QMenu
from PySide.QtGui import QAction
from PySide.QtGui import QIcon
from PySide.QtCore import Qt
from PySide.QtGui import QToolBar
from ui import gfx
import sys

class MainWindow(QMainWindow):
    """ This class is the entry point of the application. It creates the main
    window, initiates all the subsystems and then displays the GUI.  It
    consists of: a main frame with a menu bar, toolbar, status bar and numerous
    widgets. It inherits from QMainWindow

    Variables:

    - widgets: A list of the main window's currently active widgets.

    """

    def __init__(self):
        """ Constructs the main window.  """
        super(MainWindow, self).__init__()
        self.resize(680, 364)
        self.setDockNestingEnabled(True)
        self.createActions()
        self.createMenuBar()
        self.createToolBars()
        
    def createMenuBar(self):
        menubar = self.menuBar()
        
        # build the file menu
        menuFile = QMenu(menubar)
        menuFile.setTitle("&File")
        menuFile.addAction(self.newOntologyAction)
        openOntologyMenu = QMenu(menuFile)
        openOntologyMenu.setTitle("&Open")
        openOntologyMenu.addAction(self.openLocalOntologyAction)
        openOntologyMenu.addAction(self.openRemoteOntologyAction)
        menuFile.addAction(openOntologyMenu.menuAction())
        recentOntologiesMenu = QMenu(menuFile)
        recentOntologiesMenu.setTitle("Recent Ontologies")
        self.addRecentlyOpenedOntologies(recentOntologiesMenu)
        recentOntologiesMenu.addSeparator()
        recentOntologiesMenu.addAction(self.clearHistoryAction)
        menuFile.addAction(recentOntologiesMenu.menuAction())
        menuFile.addSeparator()
        menuFile.addAction(self.saveAction)
        menuFile.addAction(self.saveAsAction)
        menuFile.addSeparator()
        menuFile.addAction(self.printAction)
        menuFile.addAction(self.quickPrintAction)
        menuFile.addSeparator()
        menuFile.addAction(self.propertiesAction)
        menuFile.addAction(self.revertAction)
        menuFile.addAction(self.closeAction)
        menuFile.addSeparator()
        menuFile.addAction(self.quitAction)
        
        # build the edit menu
        menuEdit = QtGui.QMenu(menubar)
        menuEdit.setTitle("&Edit")
        
        #self.menuOntology = QtGui.QMenu(self.menubar)
        #self.menuView = QtGui.QMenu(self.menubar)
        #self.menuTools = QtGui.QMenu(self.menubar)
        #self.menuHelp = QtGui.QMenu(self.menubar)
        
        menubar.addAction(menuFile.menuAction())
        menubar.addAction(menuEdit.menuAction())
     
    def addRecentlyOpenedOntologies(self, parent):
        """ """
        
    def createToolBars(self):
        fileToolbar = QToolBar(self)
        fileToolbar.addAction(self.newOntologyAction)
        fileToolbar.addAction(self.openLocalOntologyAction)
        fileToolbar.addAction(self.openRemoteOntologyAction)
        fileToolbar.addSeparator()
        fileToolbar.addAction(self.saveAction)
        fileToolbar.addAction(self.printAction)
        self.addToolBar(fileToolbar)
        
    def createActions(self):
        # New Ontology
        self.newOntologyAction = QAction(self)
        self.createAction(self.newOntologyAction, "document-new", "New Ontology", "Ctrl+N", True)
        
        # Open Local Ontology
        self.openLocalOntologyAction = QAction(self)
        self.createAction(self.openLocalOntologyAction, "document-open", "Local Ontology", "Ctrl+O", True)
        
        # Open Remote Ontology
        self.openRemoteOntologyAction = QAction(self)
        self.createAction(self.openRemoteOntologyAction, "document-open-remote", "Remote Ontology", "Ctrl+R", True)
        
        # Clear History
        self.clearHistoryAction = QAction(self)
        self.createAction(self.clearHistoryAction, "edit-clear-history", "Clear History", None, True)
        
        # Save 
        self.saveAction = QAction(self)
        self.createAction(self.saveAction, "document-save", "Save", "Ctrl+S", True)
        
        # Save As
        self.saveAsAction = QAction(self)
        self.createAction(self.saveAsAction, "document-save-as", "Save As...", "Ctrl+Shift+S", True)
        
        # Print
        self.printAction = QAction(self)
        self.createAction(self.printAction, "document-print", "Print...", "Ctrl+P", True)
        
        # Quick Print
        self.quickPrintAction = QAction(self)
        self.createAction(self.quickPrintAction, "document-quickprint", "Quick Print", "Ctrl+Shift+P", True)
        
        # Properties
        self.propertiesAction = QAction(self)
        self.createAction(self.propertiesAction, "document-propertiesAction", "Properties...", None, True)
        
        # Revert
        self.revertAction = QAction(self)
        self.createAction(self.revertAction, "document-revert", "Revert", None, True)
        
        # Close
        self.closeAction = QAction(self)
        self.createAction(self.closeAction, "document-close", "Close", None, True)
        
        # Quit
        self.quitAction = QAction(self)
        self.createAction(self.quitAction, "application-exit", "Quit", "Ctrl+Q", True)
        
        # Undo
        self.undoAction = QAction(self)
        self.createAction(self.undoAction, "edit-undo", "Undo", "Ctrl+Z", True)
        
        # Redo
        self.redoAction = QAction(self)
        self.createAction(self.redoAction, "edit-redo", "Redo", "Ctrl+Shift+Z", True)
        
        # Cut
        self.cutAction = QAction(self)
        self.createAction(self.cutAction, "edit-cut", "Cut", "Ctrl+X", True)
        
        # Copy
        self.copyAction = QAction(self)
        self.createAction(self.copyAction, "edit-copy", "Copy", "Ctrl+C", True)
        
        # Paste
        self.pasteAction = QAction(self)
        self.createAction(self.pasteAction, "edit-paste", "Paste", "Ctrl+V", True)
        
        # Delete
        self.deleteAction = QAction(self)
        self.createAction(self.deleteAction, "edit-delete", "Delete", "Delete", True)
        
        # Select All
        self.selectAllAction = QAction(self)
        self.createAction(self.selectAllAction, "edit-select-all", "Select All", "Ctrl+A", True)
        
        # Find 
        
    def createAction(self, action, iconName, text, shortcut, visibleInMenu):
        if iconName != None :
            icon = QIcon(":/actions/gfx/" + iconName + ".png")
            action.setIcon(icon)
        action.setText(text)
        action.setIconText(text)
        if shortcut != None :
            action.setShortcut(shortcut)
            action.setShortcutContext(Qt.ApplicationShortcut)
        action.setIconVisibleInMenu(visibleInMenu)

    def loadOptions(self):
        """ Loads the options of the main window and all its widgets. """

    def synchronize(self):
        """ Performs synchronization of the main window by reporting changes in
        all the others widgets. """

    def addWidget(self, widget):
        """ Adds widget to the main window. """

    def deleteWidget(self, widget):
        """ Deletes widget from the main window. """
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    sys.exit()
    
if __name__ == '__main__':
    main()

class Toolbar():
    """ The toolbar displayed in the main window of pySUMO. The Toolbar
    contains useful menu options. Each menu has an associated toolbar, these
    Toolbars are floatable and can be moved around in the main window or out of
    the main window to create a new window for that Toolbar.

    Attributes:

    - mainWindow: The QMainWindow to which tho Toolbar belongs

    Methods:

    - initFileToolBar: Initializes the 'File' toolbar.
    - initEditToolBar: Initializes the 'Edit' toolbar.
    - initOntologyToolBar: Initializes the 'Ontology' toolbar.
    - initViewToolBar: Initializes the 'View' toolbar.
    - initToolsToolBar: Initializes the 'Tools' toolbar.
    - initHelpToolBar: Initializes the 'Help' toolbar.
    """

    def __init__(self, mainWindow):
        """ Initializes the Toolbar.

        Argument:

        - mainWindow: The QMainWindow whose toolbar has to be initialized.

        """

    def initFileToolBar(self):
        """ Initializes the 'File' toolbar which includes the most frequently
        used actions of the 'File' menu. These actions are, for example: 'New
        Ontology', 'Open Ontology', 'Close Ontology', 'Save Ontology', 'Print
        Ontology' and 'Quit'. """

    def initEditToolBar(self):
        """ Initializes the 'Edit' toolbar which includes the most frequently
        used actions of the 'Edit' menu. These actions include undo, redo, cut,
        copy, paste, search, search and replace."""

    def initOntologyToolBar(self):
        """ Initializes the 'Ontology' toolbar which includes the most
        frequently used actions of the ontology menu. These actions are: 'Merge
        Ontology', 'Update Ontology', and 'Add Term'. """

    def initViewToolBar(self):
        """ Initializes the 'View' toolbar which includes the most frequently
        used actions of the 'View' menu. These actions include: 'Toggle to
        Fullscreen, 'Hide/Show Statusbar' and 'Hide/Show Toolbar'. """

    def initToolsToolBar(self):
        """ Initializes the 'Tools' toolbar which includes the most frequently
        used actions of the 'Tools' menu such as displaying the pySUMO settings
        and downloading/updating an Ontology. """

    def initHelpToolBar(self):
        """ Initializes the 'Help' toolbar, which includes the action to open
        the 'Help' dialag. """

class StatusBar():
    """ The StatusBar displays information about the status of pySUMO.  It
    displays both permanent status information as well as status messages from
    the informational log.  It initializes a QLabel to display the encoding of
    the Ontology file, a QLabel to display the line/column number of the cursor
    in the TextEditor, a QSlider with 3 QPushButtons to represent text zoom in
    the TextEditor.  It also has a QProgressBar to display the status of
    background processes

    Attributes:

    - infoLog: The refence to the info log of pySUMO.
    - statusBar: The reference to the QStatusBar of the main window of pySUMO.

    Methods:

    - initialize: Initializes the statusbar's components.
    - update: Updates the status bar.
    - clear: Clears the status text'field.

    """

    def __init__(self, statusBar, infoLog):
        """ Initializes the StatusBar.

        Arguments:

        - statusBar: The statusbar which has to be initialized.
        - infoLog: The info log whose text hast to be displayed.

        """
        pass

    def initialize(self):
        """ Initializes the StatusBar's components. """
        pass

    def update(self):
        """ Updates the status text with the content of the info log and the
        other components which need to be updated. """
        pass

    def clear(self):
        """ Clears the status text. """
        pass

    def setProgressBarActivated(self, activated):
        """ Activates or Deactivates the progress bar in the status bar.

        Argument:

        - activated: The activation state (true or false) of the progress bar.

        """
        pass

    def setProgressBarText(self, msg):
        """ Sets the message to display in the progress bar.

        Argument:

        - msg: The message to display in the progress bar.

        """
    pass

    def clearProgressBarText(self):
        """ Clears the text of the progress bar. """
    pass

    def setProgressValue(self, val):
        """ Sets the progress value in the progress bar.

        Argument:

        - val: The value to set to the progress bar, it should be value between 0 and 100, with 0 meaning that the process is starting and 100 meaning that the process is finished.

        """

class Menubar():
    """ The builder for pySUMO's MenuBar. Receives references to a QMenuBar in
    a QMainWindow and initializes it's components.

    Attributes:

    - menuBar: The reference to the QMenuBar of the main window to build.

    Methods:

    - initFileMenu: Builds the menu file.
    - initEditMenu: Builds the menu edit.
    - initOntologyMenu: Builds the menu ontology.
    - initViewMenu: Builds the menu view.
    - initToolsMenu: Builds the menu tools.
    - initHelpMenu: Builds the menu help.
    """

    def __init__(self, menuBar):
        """ Initializes the MenuBar.

        Argument:

        - menuBar: The reference to the MenuBar to build.

        """
        pass

    def initFileMenu(self):
        """ Initializes the 'File' menu. """
        pass

    def initEditMenu(self):
        """ Initializes the 'Edit' menu. """
        pass

    def initOntologyMenu(self):
        """ Initializes the 'Ontology' menu. """
        pass

    def initViewMenu(self):
        """ Initializes the 'View' menu. """
        pass

    def initToolsMenu(self):
        """ Initializes the 'Tools' menu. """
        pass

    def initHelpMenu(self):
        """ Initializes the 'Help' menu. """
        pass

class HelpDialog(QtGui.QDialog):
    """ The help dialog for the pySUMO main window. It contains information
    about Ontologies, SUMO and pySUMO such as the pySUMO API reference and the
    homepage for SUMO.  It can display both locally stored documentation as
    well as documentation retrieved from the internet.  An about box displays
    general information about pySUMO's authors and the license. """

    def __init__(self):
        """ Initializes the help dialog. """
        pass

    def initView(self):
        """ Initializes the view of the help dialog. """
        pass
