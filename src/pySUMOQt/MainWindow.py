""" This module contains the Main Window for pySUMO.

This module contains:

- MainWindow: pySUMO's main window.
- HelpDialog: The dialog that displays help in pySUMO GUI.

"""
from PySide import QtGui, QtCore
from PySide.QtCore import QSettings, QCoreApplication, Qt, Slot, QObject, SIGNAL
from PySide.QtGui import QMainWindow, QApplication, QLabel, QWidget, QPixmap
import sys

from pySUMOQt.Designer.MainWindow import Ui_mainwindow
from pySUMOQt.Widget.DocumentationWidget import DocumentationWidget
from pySUMOQt.Widget.HierarchyWidget import HierarchyWidget
from pySUMOQt.Widget.TextEditor import TextEditor
from functools import partial
from pysumo.syntaxcontroller import Ontology
from pySUMOQt.Designer.NewOntologyDialog import Ui_NewOntologyDialog
import os
from pySUMOQt.Designer.OpenRemoteOntologyDialog import Ui_OpenRemoteOntologyDialog
import urllib
from pySUMOQt.Widget.Widget import Widget, RWWidget
from pysumo import updater
from signal import signal, SIGINT

QCoreApplication.setApplicationName("pySUMO")
QCoreApplication.setApplicationVersion("1.0")
QCoreApplication.setOrganizationName("PSE Team")

class NewOntologyDialog(QtGui.QDialog, Ui_NewOntologyDialog):

    def __init__(self, parent):
        super(NewOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = '/'.join([os.environ['HOME'], '.pysumo'])
        self.ontologyPath.setText(self.defPath)
        self.browseFolderBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QtGui.QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        path = self.ontologyPath.text()
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.ontologyPath.setText(path)

    def restoreDefaults(self):
        self.ontologyPath.setText(self.defPath)

    def accept(self):
        path = self.ontologyPath.text()
        if not os.path.exists(path):
            os.makedirs(path)
        path = ''.join([path, '/', self.ontologyName.text(), '.kif'])
        path = os.path.normpath(path)

        # create the ontology file.
        try:
            with open(path, 'x') as f:
                pass
        except FileExistsError:
            pass

        ontology = Ontology(path, self.ontologyName.text())
        self.parent().addOntology(ontology)
        super(NewOntologyDialog, self).accept()

class OpenRemoteOntologyDialog(QtGui.QDialog, Ui_OpenRemoteOntologyDialog):

    def __init__(self, parent):
        super(OpenRemoteOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = '/'.join([os.environ['HOME'], '.pysumo'])
        self.path.setText(self.defPath)
        self.browseBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QtGui.QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        path = self.path.text()
        path = QtGui.QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.path.setText(path)

    def restoreDefaults(self):
        self.path.setText(self.defPath)

    def accept(self):
        path = self.path.text()
        if not os.path.exists(path) :
            os.makedirs(path)
        path += "/"
        path += self.name.text()
        path += ".kif"
        path = os.path.normpath(path)

        # create the ontology file.
        ontology = Ontology(path, self.name.text(), self.url.text())
        with open(path, 'wb+') as f:
            # download the ontology and fill the file,
            updater.update(ontology)

        self.parent().addOntology(ontology)
        super(OpenRemoteOntologyDialog, self).accept()

class PySUMOWidget(QtGui.QDockWidget):
    def __init__(self, parent):
        super(PySUMOWidget, self).__init__(parent)
        self.mainWindow = parent
        self.isPopedOut = False
        QObject.connect(self, SIGNAL("topLevelChanged(bool)"), self.setPopedOut)
        self.wrappedWidget = None
        self.callback = None

    @Slot()
    def setPopedOut(self):
        if not self.isPopedOut :
            self.setWindowFlags(Qt.Window)
            self.show()
            self.isPopedOut = True
        else :
            self.isPopedOut = False

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.FocusIn:
            if type(self.wrappedWidget) == TextEditor:
                self.callback = self.mainWindow.connectTextEditor(self.wrappedWidget)
        elif event.type() == QtCore.QEvent.FocusOut:
            if type(self.wrappedWidget) == TextEditor:
                self.mainWindow.disconnectTextEditor(self.wrappedWidget, self.callback)
        return super(PySUMOWidget, self).eventFilter(source, event)

class MainWindow(Ui_mainwindow, QMainWindow):
    """ This class is the entry point of the application. It creates the main
    window, initiates all the subsystems and then displays the GUI.  It
    consists of: a main frame with a menu bar, toolbar, status bar and numerous
    widgets. It inherits from QMainWindow

    Variables:

    - widgets: A list of the main window's currently active widgets.

    """
    ontologyAdded = QtCore.Signal(Ontology)

    def __init__(self):
        """ Constructs the main window.  """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.menuTextEditorWidgets.setEnabled(False)
        self.menuDocumentationWidgets.setEnabled(False)
        self.menuHierarchyWidgets.setEnabled(False)
        self.setWindowTitle("pySUMO")
        self.setCentralWidget(None)
        self.actionTextEditorWidget.triggered.connect(self.addTextEditorWidget)
        self.actionDocumentationWidget.triggered.connect(
            self.addDocumentationWidget)
        self.actionHierarchyWidget.triggered.connect(self.addHierarchyWidget)
        self.newOntologyAction.triggered.connect(self.createNewOntology)
        self.openLocalOntologyAction.triggered.connect(self.openLocalOntology)
        self.openRemoteOntologyAction.triggered.connect(self.openRemoteOntology)
        self.createStatusBar()
        self.fileChooser = QtGui.QFileDialog(self)  # unique instance.

        self.ontologyAdded.connect(self.notifyOntologyAdded)
        self.clearHistoryAction.triggered.connect(self.clearRecentOntologiesHistory)
        self.widgets = list()
        # restore and show the view.
        self.show()

    @Slot()
    def addTextEditorWidget(self):
        widget = self.createTextEditorWidget()
        self.addOrRestoreWidget(widget, self.menuTextEditorWidgets, True)

    def createTextEditorWidget(self):
        widget = PySUMOWidget(self)
        textEditorWidget = TextEditor(widget)
        objName = "TextEditorWidget"
        objName += str(len(self.menuTextEditorWidgets.actions()))
        widget.setObjectName(objName)
        widget.setWindowTitle("Text Editor Widget")
        widget.setWidget(textEditorWidget.getLayoutWidget())
        # gives the reference of the wrapped widget.
        widget.wrappedWidget = textEditorWidget
        # install event filter.
        textEditorWidget.plainTextEdit.installEventFilter(widget)
        return widget

    @Slot()
    def addDocumentationWidget(self):
        widget = self.createDocumentationWidget()
        self.addOrRestoreWidget(widget, self.menuDocumentationWidgets, True)

    def createDocumentationWidget(self):
        widget = PySUMOWidget(self)
        wWidget = QWidget(self)
        documentationWidget = DocumentationWidget(wWidget)
        objName = "DocumentationWidget"
        objName += str(len(self.menuDocumentationWidgets.actions()))
        widget.wrappedWidget = documentationWidget
        widget.setObjectName(objName)
        widget.setWindowTitle("Documentation Widget")
        widget.setWidget(wWidget)
        return widget

    @Slot()
    def addHierarchyWidget(self):
        widget = self.createHierarchyWidget()
        self.addOrRestoreWidget(widget, self.menuHierarchyWidgets, True)

    def createHierarchyWidget(self):
        widget = PySUMOWidget(self)
        hierarchyWidget = HierarchyWidget(widget)
        objName = "HierarchyWidget"
        objName += str(len(self.menuHierarchyWidgets.actions()))
        widget.wrappedWidget = hierarchyWidget
        widget.setObjectName(objName)
        widget.setWindowTitle("Hierarchy Widget")
        widget.setWidget(hierarchyWidget.widget)
        return widget

    def addDeleteWidgetAction(self, widget):
        action = QtGui.QAction(widget)
        action.setText(widget.windowTitle())
        callback = partial(self.deleteWidget, widget)
        action.triggered.connect(callback)
        if not self.menuDelete.isEnabled():
            self.menuDelete.setEnabled(True)
        self.menuDelete.addAction(action)

    def addOrRestoreWidget(self, widget, menu, directAdd=False):
        restored = False
        if not directAdd:
            restored = self.restoreDockWidget(widget)
        if not restored:
            # print("could not restore the widget " + widget.objectName())
            if type(widget.wrappedWidget) == TextEditor:
                self.addDockWidget(Qt.TopDockWidgetArea, widget)
            else:
                self.addDockWidget(Qt.BottomDockWidgetArea, widget)
        if not menu.isEnabled():
            menu.setEnabled(True)
        menu.addAction(widget.toggleViewAction())
        self.addDeleteWidgetAction(widget)
        self.widgets.append(widget.wrappedWidget)

    def updateStatusbar(self, plainTextEdit, arg1, arg2):
        if (plainTextEdit == None):
            return
        textCursor = plainTextEdit.textCursor()
        document = plainTextEdit.document()
        lineNbr = document.findBlock(textCursor.position()).blockNumber()
        cursorPos = str(lineNbr + 1) + " : " + str(textCursor.columnNumber())
        self.ligneColNumber.setText(cursorPos)

    def closeEvent(self, event):
        self.settings = QSettings("user-layout.ini", QSettings.IniFormat)
        self.savePositionState(self)
        self.saveSizeState(self)
        self.settings.setValue("mainWindow/state", self.saveState())
        self.saveStatusBarState()
        actions = self.menuTextEditorWidgets.actions()
        count = len(actions)
        self.settings.setValue("TextEditorWidgets/count", count)
        actions = self.menuDocumentationWidgets.actions()
        count = len(actions)
        self.settings.setValue("DocumentationWidgets/count", count)
        actions = self.menuHierarchyWidgets.actions()
        count = len(actions)
        self.settings.setValue("HierarchyWidgets/count", count)
        self.saveRecentOntologyHistory()
        super(MainWindow, self).closeEvent(event)

    def showEvent(self, event):
        self.settings = QSettings("user-layout.ini", QSettings.IniFormat)
        self.restoreState(self.settings.value("mainWindow/state"))
        self.restoreSizeState(self)
        self.restorePositionState(self)
        self.restoreStatusBarState()
        # restore Text Editor Widgets
        self.restoreTextEditorWidgets()
        # restore Documentation Widgets
        self.restoreDocumentationWidgets()
        # restore Hierarchy Widgets
        self.restoreHierarchyWidgets()
        self.restoreRecentOntologyHistory()
        super(MainWindow, self).showEvent(event)

    def saveRecentOntologyHistory(self):
        pass

    def restoreRecentOntologyHistory(self):
        pass

    def restoreTextEditorWidgets(self):
        textEditorWidgetsCount = self.settings.value("TextEditorWidgets/count")
        if textEditorWidgetsCount == None:
            textEditorWidgetsCount = 0
        textEditorWidgetsCount = int(textEditorWidgetsCount)
        count = 0
        while count < textEditorWidgetsCount:
            widget = self.createTextEditorWidget()
            self.addOrRestoreWidget(widget, self.menuTextEditorWidgets)
            count = count + 1
            
    def restoreDocumentationWidgets(self):
        documentationWidgetsCount = self.settings.value("DocumentationWidgets/count")
        if documentationWidgetsCount == None:
            documentationWidgetsCount = 0
        documentationWidgetsCount = int(documentationWidgetsCount)
        count = 0 
        while count < documentationWidgetsCount:
            widget = self.createDocumentationWidget()
            self.addOrRestoreWidget(widget, self.menuDocumentationWidgets)
            count = count + 1

    def restoreHierarchyWidgets(self):
        hierarchyWidgetsCount = self.settings.value("HierarchyWidgets/count")
        if hierarchyWidgetsCount == None:
            hierarchyWidgetsCount = 0
        hierarchyWidgetsCount = int(hierarchyWidgetsCount)
        count = 0 
        while count < hierarchyWidgetsCount:
            widget = self.createHierarchyWidget()
            self.addOrRestoreWidget(widget, self.menuHierarchyWidgets)
            count = count + 1

    def saveVisibilityState(self, qItem):
        objName = qItem.objectName()
        self.settings.setValue(objName + "/visible", qItem.isVisible())

    def restoreVisibilityState(self, qItem, qAction=None):
        objName = qItem.objectName()
        visible = self.settings.value(objName + "/visible")
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
        self.settings.setValue(objName + "/x", xPos)
        self.settings.setValue(objName + "/y", yPos)

    def restorePositionState(self, qItem):
        objName = qItem.objectName()
        xPos = self.settings.value(objName + "/x")
        yPos = self.settings.value(objName + "/y")
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
        self.settings.setValue(objName + "/width", width)
        self.settings.setValue(objName + "/height", height)

    def restoreSizeState(self, qItem):
        objName = qItem.objectName()
        width = self.settings.value(objName + "/width")
        height = self.settings.value(objName + "/height")
        if width == None or height == None:
            return
        width = int(width)
        height = int(height)
        qItem.resize(width, height)

    def saveStatusBarState(self):
        self.saveVisibilityState(self.statusBar)

    def restoreStatusBarState(self):
        self.restoreVisibilityState(self.statusBar, self.actionStatusbar)

    def createStatusBar(self):
        statusbar = self.statusBar
        # statusbar.setMaximumHeight(35)
        statusbarWrapperWidget = QWidget(statusbar)
        statusBarLayout = QtGui.QHBoxLayout(statusbarWrapperWidget)
        # statusBarLayout.setContentsMargins(10, 10, 10, 10)
        statusBarLayout.setSpacing(30)
        # loadStyleSheet(statusbar, "Statusbar")

        # writing state of the current editing file.
        writableLbl = QLabel(statusbar)
        writableLbl.setText("Writable")
        statusBarLayout.addWidget(writableLbl)

        # keyword writing mode.
        self.editModeLbl = QLabel(statusbar)
        self.editModeLbl.setText("Insert")
        statusBarLayout.addWidget(self.editModeLbl)

        # ligne and column number
        self.ligneColNumber = QLabel(statusbar)
        self.ligneColNumber.setText("")
        statusBarLayout.addWidget(self.ligneColNumber)

        # zoom widget
        # zoomWidget = ZoomWidget(statusbar)
        # statusbar.addPermanentWidget(zoomWidget)

        # internet state icon
        internetState = QLabel(statusbar)
        internetState.setPixmap(
            QPixmap(":/status/gfx/status/network-connect.png").scaled(24, 24))
        statusBarLayout.addWidget(internetState)
#         self.setStatusBar(statusbar)
        statusbar.addPermanentWidget(statusbarWrapperWidget)

    def loadOptions(self):
        """ Loads the options of the main window and all its widgets. """

    def synchronize(self):
        """ Performs synchronization of the main window by reporting changes in
        all the others widgets. """

    def addWidget(self, widget):
        """ Adds widget to the main window. """

    def deleteWidget(self, widget):
        self.widgets.remove(widget.wrappedWidget)
        widget.deleteLater()
        QMenu = None
        widgetType = type(widget.wrappedWidget)
        if widgetType == TextEditor:
            QMenu = self.menuTextEditorWidgets
        elif widgetType == DocumentationWidget:
            QMenu = self.menuDocumentationWidgets
        elif widgetType == HierarchyWidget:
            QMenu = self.menuHierarchyWidgets

        if QMenu != None and len(QMenu.actions()) == 1:
            QMenu.setEnabled(False)

        if len(self.menuDelete.actions()) == 1:
            self.menuDelete.setEnabled(False)

    def connectTextEditor(self, widget):
        callback = partial(self.updateStatusbar, widget.plainTextEdit)
        widget.getWidget().updateRequest.connect(callback)
        self.actionExpand.triggered.connect(widget.expandAll)
        self.actionCollapse.triggered.connect(widget.hideAll)
        self.actionZoomIn.triggered.connect(widget.increaseSize)
        self.actionZoomOut.triggered.connect(widget.decreaseSize)
        return callback

    def disconnectTextEditor(self, widget, callback):
        widget.getWidget().updateRequest.disconnect(callback)
        self.actionExpand.triggered.disconnect(widget.expandAll)
        self.actionCollapse.triggered.disconnect(widget.hideAll)
        self.actionZoomIn.triggered.disconnect(widget.increaseSize)
        self.actionZoomOut.triggered.disconnect(widget.decreaseSize)

    @Slot()
    def createNewOntology(self):
        dialog = NewOntologyDialog(self)
        dialog.show()

    @Slot()
    def openLocalOntology(self):
        x, y = QtGui.QFileDialog.getOpenFileName(self, "Open Ontology File",
                                                 os.environ['HOME'] + "/.pysumo", "SUO KIF Files (*.kif)")
        if x == '' and y == '':
            return
        filepath = x
        filename = os.path.split(filepath)[1]
        filename = os.path.splitext(filename)[0]
        ontology = Ontology(filepath, filename)
        self.addOntology(ontology)

    @Slot()
    def openRemoteOntology(self):
        dialog = OpenRemoteOntologyDialog(self)
        dialog.show()

    def addOntology(self, ontology):
        RWWidget.SyntaxController.add_ontology(ontology)
        self.ontologyAdded.emit(ontology)

    @Slot(Ontology)
    def notifyOntologyAdded(self, ontology):
        if ontology is None:
            return
        count = len(self.menuRecent_Ontologies.actions())
        count = count - 2  # remove the separator action and the clear history action.
        name = str(count + 1)
        name += ". "
        name += ontology.name
        name += ".kif"
        found = False
        for a in self.menuRecent_Ontologies.actions():
            o = a.data()
            if o is None:
                continue
            if o.__eq__(ontology):
                found = True
                break
        if not found:
            befAction = self.menuRecent_Ontologies.actions()[count]
            action = QtGui.QAction(self.menuRecent_Ontologies)
            action.setText(name)
            action.setData(ontology)
            callback = partial(self.addOntology, ontology)
            action.triggered.connect(callback)
            self.menuRecent_Ontologies.insertAction(befAction, action)
        ontologyMenu = QtGui.QMenu(self)
        ontologyMenu.setTitle(ontology.name)
        ontologyMenu.addAction("Close")
        ontologyMenu.addAction("Delete")
        ontologyMenu.addAction("Update")
        self.menuOntology.addMenu(ontologyMenu)
        for widget in self.widgets:
            if type(widget) == TextEditor:
                widget._updateOntologySelector()

    def clearRecentOntologiesHistory(self):
        self.menuRecent_Ontologies.clear()
        self.menuRecent_Ontologies.addSeparator()
        self.menuRecent_Ontologies.addAction(self.clearHistoryAction)

def main():
    app = QApplication(sys.argv)
    signal(SIGINT, quit_handler)
    mainwindow = MainWindow()
    app.setActiveWindow(mainwindow)
    sys.exit(app.exec_())

def quit_handler(signum, frame):
    QApplication.closeAllWindows()
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
    the informational log. It initializes a QLabel to display the line/column
    number of the cursor in the TextEditor, a QSlider with 3 QPushButtons to
    represent text zoom in the TextEditor.  It also has a QProgressBar to
    display the status of background processes

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
