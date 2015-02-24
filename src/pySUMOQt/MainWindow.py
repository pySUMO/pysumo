""" This module contains the Main Window for pySUMO.

This module contains:

- MainWindow: pySUMO's main window.
- HelpDialog: The dialog that displays help in pySUMO GUI.

"""

from functools import partial
from signal import signal, SIGINT
from pickle import loads
from struct import unpack
import logging
import os
import sys

from PySide.QtCore import QCoreApplication, Qt, Slot, QObject, SIGNAL
from PySide.QtCore import QEvent, Signal
from PySide.QtGui import QMainWindow, QApplication, QLabel, QPixmap
from PySide.QtGui import QIcon, QDockWidget, QFileDialog, QPrintDialog
from PySide.QtGui import QAction, QMenu
from PySide.QtNetwork import QLocalServer, QAbstractSocket

from pySUMOQt.Designer.MainWindow import Ui_mainwindow
from pySUMOQt.Widget.DocumentationWidget import DocumentationWidget
from pySUMOQt.Widget.HierarchyWidget import HierarchyWidget
from pySUMOQt.Widget.TextEditor import TextEditor
from pySUMOQt.Widget.Widget import RWWidget

from pySUMOQt.Settings import LayoutManager, PySumoSettings
from pySUMOQt.Dialog import NewOntologyDialog, OpenRemoteOntologyDialog, OptionDialog
from pySUMOQt.Widget.GraphWidget import GraphWidget
from pysumo.syntaxcontroller import Ontology
from pysumo import logger
from pysumo.logger.infolog import InfoLog

QCoreApplication.setApplicationName("pySUMO")
QCoreApplication.setApplicationVersion("1.0")
QCoreApplication.setOrganizationName("PSE Team")

class PySUMOWidget(QDockWidget):
    """This wrapper widget holds a pysumo widget."""

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
        if event.type() == QEvent.FocusIn:
            self.callback = self.mainWindow.connectWidget(self.wrappedWidget)
        elif event.type() == QEvent.FocusOut:
            self.mainWindow.disconnectWidget(self.wrappedWidget, self.callback)
        return super(PySUMOWidget, self).eventFilter(source, event)

class MainWindow(Ui_mainwindow, QMainWindow):
    """ This class is the entry point of the application. It creates the main
    window, initiates all the subsystems and then displays the GUI.  It
    consists of: a main frame with a menu bar, toolbar, status bar and numerous
    widgets. It inherits from QMainWindow

    Variables:

    - widgets: A list of the main window's currently active widgets.

    """
    
    ontologyAdded = Signal(Ontology)
    synchronizeRequested = Signal()
    def __init__(self):
        """ Constructs the main window.  """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.infolog = InfoLog()
        self.log = logging.getLogger('.' + __name__)
        self.setCentralWidget(None)
        callback = partial(self.addWidget, "TextEditorWidget", self.menuTextEditorWidgets)
        self.actionTextEditorWidget.triggered.connect(callback)
        callback = partial(self.addWidget, "DocumentationWidget", self.menuDocumentationWidgets)
        self.actionDocumentationWidget.triggered.connect(callback)
        callback = partial(self.addWidget, "HierarchyWidget", self.menuHierarchyWidgets)
        self.actionHierarchyWidget.triggered.connect(callback)
        callback = partial(self.addWidget, "GraphWidget", self.menuGraphWidgets)
        self.actionGraphWidget.triggered.connect(callback)
        self.newOntologyAction.triggered.connect(self.onNewOntology)
        self.openLocalOntologyAction.triggered.connect(self.onOpenLocalOntology)
        self.openRemoteOntologyAction.triggered.connect(self.onOpenRemoteOntology)
        self.createStatusBar()
        self.ontologyAdded.connect(self.notifyOntologyAdded)
        self.clearHistoryAction.triggered.connect(self.onClearRecentOntologiesHistory)
        self.widgets = list()
        # unique instances.
        self.fileChooser = QFileDialog(self)  
        self.dialog = QPrintDialog()
        self.userLayout = LayoutManager(self)
        filepath = logger.CONFIG_PATH + "/settings.ini"
        exist = False
        try :
            with open(filepath) as f :
                f.close()
                exist = True
        except IOError :
            pass
        settings = PySumoSettings(self, filepath)
        if not exist :
            settings.loadDefaults()
        optionDialog = OptionDialog(self, settings)
        self.actionSettings.triggered.connect(optionDialog.show)
        # restore and show the view.
        self.userLayout.restoreLayout()
        self.show()

    def addWidget(self, widgetType, widgetMenu):
        '''Add a widget into the layout with the given widget type as string.'''
        widget = self.createPySumoWidget(widgetType, widgetMenu)
        self.addOrRestoreWidget(widget, widgetMenu, True)
        
    def createPySumoWidget(self, widgetType, widgetMenu):
        '''Create a widget wrapper containing the given widget type.'''
        widget = PySUMOWidget(self)
        wrappedWidget = None
        if widgetType == "TextEditorWidget" :
            wrappedWidget = TextEditor(widget)
            wrappedWidget.plainTextEdit.installEventFilter(widget)
            wrappedWidget.ontologyChanged.connect(self.synchronize)
        elif widgetType == "DocumentationWidget" :
            wrappedWidget = DocumentationWidget(widget)
        elif widgetType == "HierarchyWidget" :
            wrappedWidget = HierarchyWidget(widget)
        elif widgetType == "GraphWidget":
            wrappedWidget = GraphWidget(widget)
            wrappedWidget.graphicsView.installEventFilter(widget)
            wrappedWidget.ontologyChanged.connect(self.synchronize)
        if wrappedWidget is None :
            print("can not create widget with type " + widgetType)
            return
        self.synchronizeRequested.connect(wrappedWidget.refresh)
        objName = widgetType
        objName += str(len(widgetMenu.actions()))
        widget.setObjectName(objName)
        widget.setWidget(wrappedWidget.widget)
        widget.wrappedWidget = wrappedWidget
        return widget

    def addDeleteWidgetAction(self, widget):
        '''Add the delete action for the given widget in the delete menu.'''
        action = QAction(widget)
        action.setText(widget.windowTitle())
        callback = partial(self.deleteWidget, widget)
        action.triggered.connect(callback)
        if not self.menuDelete.isEnabled():
            self.menuDelete.setEnabled(True)
        self.menuDelete.addAction(action)

    def addOrRestoreWidget(self, widget, menu, directAdd=False):
        '''Restore a widget on the layout or place it, if restore failed.'''
        restored = False
        if not directAdd:
            restored = self.restoreDockWidget(widget)
        if not restored:
            if type(widget.wrappedWidget) == TextEditor:
                self.addDockWidget(Qt.TopDockWidgetArea, widget)
            else:
                self.addDockWidget(Qt.BottomDockWidgetArea, widget)
        if not menu.isEnabled():
            menu.setEnabled(True)
        menu.addAction(widget.toggleViewAction())
        self.addDeleteWidgetAction(widget)
        self.widgets.append(widget.wrappedWidget)

    def closeEvent(self, event):
        self.userLayout.saveLayout()
        super(MainWindow, self).closeEvent(event)

    def createStatusBar(self):
        '''Create the status bar.'''
        statusbar = self.statusBar
        # line and column number
        self.lineColNumber = QLabel(statusbar)
        self.lineColNumber.setText("")
        statusbar.addPermanentWidget(self.lineColNumber)

        statusbar.socketServer = QLocalServer()
        statusbar.socketServer.removeServer(self.infolog.socket)
        statusbar.socketServer.listen(self.infolog.socket)
        statusbar.socketServer.newConnection.connect(self.setupStatusConnection)
        self.log.info('Ready')

    @Slot()
    def setupStatusConnection(self):
        socket = self.statusBar.socketServer.nextPendingConnection()
        socket.readyRead.connect(partial(self.displayLog, socket))

    @Slot()
    def displayLog(self, socket):
        data = socket.readAll().data()
        slen = unpack(">L", data[:4])[0]
        data = data[4:]
        assert len(data) == slen
        logrecord = logging.makeLogRecord(loads(data))
        self.statusBar.showMessage(logrecord.getMessage())

    def updateStatusbar(self, wrappedWidget = None):
        '''Update the status bar.'''
        # arg1 and arg2 are used to resolve an argument number error.
        plainTextEdit = None
        if wrappedWidget is None :
            self.lineColNumber.setVisible(False)
            return
        else : 
            self.lineColNumber.setVisible(True)
        if type(wrappedWidget) == TextEditor :
            plainTextEdit = wrappedWidget.plainTextEdit 
        else :
            return
        textCursor = plainTextEdit.textCursor()
        document = plainTextEdit.document()
        lineNbr = document.findBlock(textCursor.position()).blockNumber()
        cursorPos = str(lineNbr + 1) + " : " + str(textCursor.columnNumber())
        self.lineColNumber.setText(cursorPos)

    def synchronize(self):
        """ Performs synchronization of the main window by reporting changes in
        all the others widgets. """
        print("synchronizing ...")
        self.synchronizeRequested.emit()

    def deleteWidget(self, widget):
        '''Delete a widget from the layout.'''
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
        elif widgetType == GraphWidget:
            QMenu = self.menuGraphWidgets

        if QMenu != None and len(QMenu.actions()) == 1:
            QMenu.setEnabled(False)

        if len(self.menuDelete.actions()) == 1:
            self.menuDelete.setEnabled(False)

    def connectWidget(self, widget):
        widgetType = type(widget)
        self.actionPrint.triggered.connect(widget._print_)
        self.actionPrintPreview.triggered.connect(widget._printPreview_)
        self.actionQuickPrint.triggered.connect(widget._quickPrint_)
        self.actionSave.triggered.connect(widget._save_)
        self.actionZoomIn.triggered.connect(widget._zoomIn_)
        self.actionZoomOut.triggered.connect(widget._zoomOut_)
        if widgetType == TextEditor :
            callback = partial(self.updateStatusbar, widget)
            widget.getWidget().cursorPositionChanged.connect(callback)
            self.actionExpand.triggered.connect(widget.expandAll)
            self.actionCollapse.triggered.connect(widget.hideAll)
            self.actionUndo.triggered.connect(widget.plainTextEdit.undo)
            self.actionRedo.triggered.connect(widget.plainTextEdit.redo)
            self.actionCut.triggered.connect(widget.plainTextEdit.cut)
            self.actionCopy.triggered.connect(widget.plainTextEdit.copy)
            self.actionPaste.triggered.connect(widget.plainTextEdit.paste)
            self.actionDelete.triggered.connect(widget.plainTextEdit.clear)
            self.actionSelectAll.triggered.connect(widget.plainTextEdit.selectAll)
            return callback

    def disconnectWidget(self, widget, callback=None):
        widgetType = type(widget)
        self.actionPrint.triggered.disconnect(widget._print_)
        self.actionQuickPrint.triggered.disconnect(widget._quickPrint_)
        self.actionPrintPreview.triggered.disconnect(widget._printPreview_)
        self.actionSave.triggered.disconnect(widget._save_)
        self.actionZoomIn.triggered.disconnect(widget._zoomIn_)
        self.actionZoomOut.triggered.disconnect(widget._zoomOut_)
        if widgetType == TextEditor :
            self.updateStatusbar()
            widget.getWidget().cursorPositionChanged.disconnect(callback)
            self.actionExpand.triggered.disconnect(widget.expandAll)
            self.actionCollapse.triggered.disconnect(widget.hideAll)
            self.actionUndo.triggered.disconnect(widget.plainTextEdit.undo)
            self.actionRedo.triggered.disconnect(widget.plainTextEdit.redo)
            self.actionCut.triggered.disconnect(widget.plainTextEdit.cut)
            self.actionCopy.triggered.disconnect(widget.plainTextEdit.copy)
            self.actionPaste.triggered.disconnect(widget.plainTextEdit.paste)
            self.actionDelete.triggered.disconnect(widget.plainTextEdit.clear)
            self.actionSelectAll.triggered.disconnect(widget.plainTextEdit.selectAll)

    def onNewOntology(self):
        '''Handles the new ontology action when it is triggered.'''
        dialog = NewOntologyDialog(self)
        dialog.show()

    def onOpenLocalOntology(self):
        '''Handles the open local ontology action when it is triggered.'''
        x, y = QFileDialog.getOpenFileName(self, "Open Ontology File",
                                                 os.environ['HOME'] + "/.pysumo", "SUO KIF Files (*.kif)")
        if x == '' and y == '':
            return
        filepath = x
        filename = os.path.split(filepath)[1]
        filename = os.path.splitext(filename)[0]
        ontology = Ontology(filepath, filename)
        self.addOntology(ontology)

    def onOpenRemoteOntology(self):
        '''Handles the open remote ontology action when it is triggered.'''
        dialog = OpenRemoteOntologyDialog(self)
        dialog.show()

    def addOntology(self, ontology):
        '''Adds an ontology to index and notify all components required.'''
        RWWidget.SyntaxController.add_ontology(ontology)
        self.ontologyAdded.emit(ontology)

    def notifyOntologyAdded(self, ontology):
        '''Notify that an ontology was added to index.'''
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
            action = QAction(self.menuRecent_Ontologies)
            action.setText(name)
            action.setData(ontology)
            callback = partial(self.addOntology, ontology)
            action.triggered.connect(callback)
            self.menuRecent_Ontologies.insertAction(befAction, action)
        ontologyMenu = QMenu(self)
        ontologyMenu.setTitle(ontology.name)
        
        # Update action
        actionUpdate = ontologyMenu.addAction("Update")
        actionUpdate.setData(ontology)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/update-product.png"), QIcon.Normal, QIcon.Off)
        actionUpdate.setIcon(icon)
        actionUpdate.setIconVisibleInMenu(True)
        actionRevert = ontologyMenu.addAction("Revert")
        actionRevert.setData(ontology)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-revert.png"), QIcon.Normal, QIcon.Off)
        actionRevert.setIcon(icon)
        actionRevert.setIconVisibleInMenu(True)
        actionProperties = ontologyMenu.addAction("Properties")
        actionProperties.setData(ontology)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-properties.png"), QIcon.Normal, QIcon.Off)
        actionProperties.setIconVisibleInMenu(True)
        actionProperties.setIcon(icon)
        ontologyMenu.addSeparator()
        # Close action
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-close.png"), QIcon.Normal, QIcon.Off)
        actionClose = ontologyMenu.addAction("Close")
        actionClose.setIcon(icon)
        actionClose.setIconVisibleInMenu(True)
        actionClose.setData(ontology)
        ontologyMenu.addSeparator()
        
        self.menuOntology.addMenu(ontologyMenu)
        for widget in self.widgets:
            if type(widget) == TextEditor:
                widget._updateOntologySelector()
                
        # update graph widget
            if type(widget) == GraphWidget :
                widget.newVariant()
                widget._updateActiveOntology()
#                 x.initRelationBox()
                
        # print(gv)

    def onClearRecentOntologiesHistory(self):
        '''Handles the clear recent ontologies action when it is triggered.'''
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
