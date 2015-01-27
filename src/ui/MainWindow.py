""" This module contains the Main Window for pySUMO.

This module contains:

- MainWindow: pySUMO's main window.
- HelpDialog: The dialog that displays help in pySUMO GUI.

"""
from PySide import QtGui
from PySide.QtGui import QMainWindow, QApplication, QStatusBar, QLabel, QWidget, QPixmap
import ui.Widget.TextEditor
from ui.Designer import MainWindow, ZoomWidget
import sys
from PySide.QtCore import QFile, QSettings, QCoreApplication, QFileInfo


QCoreApplication.setApplicationName("pySUMO")
QCoreApplication.setApplicationVersion("1.0")
QCoreApplication.setOrganizationName("PSE Team")

class ZoomWidget(QWidget, ZoomWidget.Ui_zoomWidget):
    def __init__(self, parent):
        super(ZoomWidget, self).__init__(parent)
        self.setupUi(self)

def loadStyleSheet(widget, styleName):
    print(styleName)
    cssfile = QFile("./ui/Designer/css/" + styleName + ".css")
    cssfile.open(QFile.ReadOnly)
    print(cssfile.exists())
    print(QFileInfo(cssfile).absoluteFilePath())
    stylesheet = cssfile.readAll()
    print(stylesheet.data())
    widget.setStyleSheet(str(stylesheet))
    cssfile.close()

class MainWindow(MainWindow.Ui_mainwindow, QMainWindow):
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
        self.setupUi(self)
        texteditor = ui.Widget.TextEditor.TextEditor(self)
        self.setCentralWidget(texteditor.getWidget())
        self.createStatusBar()
        self.show()
        
    def closeEvent(self, event):
        settings = QSettings("conf", QSettings.IniFormat)
        settings.setValue("geometry", self.saveGeometry())
        super(MainWindow, self).closeEvent(event)
        
    def showEvent(self, *args, **kwargs):
        settings = QSettings("conf", QSettings.IniFormat)
        self.restoreGeometry(settings.value("geometry"))
        
    def createStatusBar(self):
        statusbar = self.statusBar
        statusbar.setMaximumHeight(35)
        loadStyleSheet(statusbar, "Statusbar")
        # encoding of the current editing file.
        encodingLbl = QLabel(statusbar)
        encodingLbl.setMaximumHeight(24)
        encodingLbl.setText("UTF-8")
        statusbar.addPermanentWidget(encodingLbl)
        
        # writing state of the current editing file.
        writableLbl = QLabel(statusbar)
        writableLbl.setText("Writable")
        writableLbl.setMaximumHeight(24)
        statusbar.addPermanentWidget(writableLbl)
        
        # keyword writing mode.
        editModeLbl = QLabel(statusbar)
        editModeLbl.setText("Insert")
        editModeLbl.setMaximumHeight(24)
        statusbar.addPermanentWidget(editModeLbl)
        
        # ligne and column number
        ligneColNumber = QLabel(statusbar)
        ligneColNumber.setText("58 : 35")
        ligneColNumber.setMaximumHeight(24)
        statusbar.addPermanentWidget(ligneColNumber)
        
        # zoom widget
        # zoomWidget = ZoomWidget(statusbar)
        # statusbar.addPermanentWidget(zoomWidget)
        
        # internet state icon
        internetState = QLabel(statusbar)
        internetState.setPixmap(QPixmap(":/status/gfx/status/network-connect.png").scaled(24, 24))
        internetState.setMaximumSize(24, 24)
        statusbar.addPermanentWidget(internetState)
#         self.setStatusBar(statusbar)
        
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
    MainWindow()
    
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
