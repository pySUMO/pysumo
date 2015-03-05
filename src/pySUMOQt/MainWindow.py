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
import pysumo
import os
import sys

from PySide.QtCore import QCoreApplication, Qt, Slot, QObject, SIGNAL
from PySide.QtCore import QEvent, Signal
from PySide.QtGui import QMainWindow, QApplication, QLabel, QPixmap
from PySide.QtGui import QIcon, QDockWidget, QFileDialog, QPrintDialog
from PySide.QtGui import QAction, QMenu
from PySide.QtNetwork import QLocalServer

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
from pysumo.updater import update

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
        self.prefixName = None
        self.suffixName = None

    def _setSuffixName_(self, s):
        if s is None :
            return
        s = s.strip()
        if "" == s :
            s = None
        self.suffixName = s
        self.updateTitle()

    def setPrefixName(self, s):
        if s is None :
            return
        s = s.strip()
        if "" == s :
            return
        self.prefixName = s
        self.updateTitle()

    def updateTitle(self):
        assert self.prefixName is not None
        title = self.prefixName
        if self.suffixName is not None :
            title = title + " | " + self.suffixName
        self.setWindowTitle(title)

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
    ontologyRemoved = Signal(Ontology)
    synchronizeRequested = Signal()
    def __init__(self):
        """ Constructs the main window.  """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.infolog = InfoLog()
        self.log = logging.getLogger('.' + __name__)
        self.setCentralWidget(None)
        callback = partial(self._addWidget_, "TextEditorWidget", self.menuTextEditorWidgets)
        self.actionTextEditorWidget.triggered.connect(callback)
        callback = partial(self._addWidget_, "DocumentationWidget", self.menuDocumentationWidgets)
        self.actionDocumentationWidget.triggered.connect(callback)
        callback = partial(self._addWidget_, "HierarchyWidget", self.menuHierarchyWidgets)
        self.actionHierarchyWidget.triggered.connect(callback)
        callback = partial(self._addWidget_, "GraphWidget", self.menuGraphWidgets)
        self.actionGraphWidget.triggered.connect(callback)
        self.newOntologyAction.triggered.connect(self._newOntology_)
        self.openLocalOntologyAction.triggered.connect(self._openLocalOntology_)
        self.openRemoteOntologyAction.triggered.connect(self._openRemoteOntology_)
        self.createStatusBar()
        self.ontologyAdded.connect(self.notifyOntologyAdded)
        self.clearHistoryAction.triggered.connect(self._ClearRecentOntologiesHistory_)
        self.widgets = list()
        # unique instances.
        self.fileChooser = QFileDialog(self)  
        self.dialog = QPrintDialog()
        self.userLayout = LayoutManager(self)
        filepath = pysumo.CONFIG_PATH + "/settings.ini"
        exist = False
        try :
            with open(filepath) as f :
                f.close()
                exist = True
        except IOError :
            pass
        self.settings = PySumoSettings(self, filepath)
        if not exist :
            self.settings.loadDefaults()
        self.optionDialog = OptionDialog(self, self.settings)
        self.actionSettings.triggered.connect(self._showOptionDialog_)
        # restore and show the view.
        self.userLayout.restoreLayout()
        self.show()
        
    def _showOptionDialog_(self):
        self.optionDialog.initialize()
        self.optionDialog.show()

    def _addWidget_(self, widgetType, widgetMenu):
        '''Add a widget into the layout with the given widget type as string.'''
        widget = self.createPySumoWidget(widgetType, widgetMenu)
        self.addOrRestoreWidget(widget, widgetMenu, True)
        
    def createPySumoWidget(self, widgetType, widgetMenu):
        '''Create a widget wrapper containing the given widget type.'''
        widget = PySUMOWidget(self)
        wrappedWidget = None
        if widgetType == "TextEditorWidget" :
            wrappedWidget = TextEditor(widget, settings=self.settings)
            widget.setPrefixName("Text Editor")
            wrappedWidget.ontologySelector.currentIndexChanged[str].connect(widget._setSuffixName_)
            wrappedWidget.plainTextEdit.installEventFilter(widget)
            wrappedWidget.ontologyChanged.connect(self.synchronize)
            self.ontologyAdded.connect(wrappedWidget._updateOntologySelector)
            self.ontologyRemoved.connect(wrappedWidget._updateOntologySelector)
        elif widgetType == "DocumentationWidget" :
            wrappedWidget = DocumentationWidget(widget)
            widget.setPrefixName("Documentation Widget")
        elif widgetType == "HierarchyWidget" :
            wrappedWidget = HierarchyWidget(widget)
            widget.setPrefixName("Hierarchy Widget")
            wrappedWidget.treeWidget.installEventFilter(widget)
        elif widgetType == "GraphWidget":
            wrappedWidget = GraphWidget(widget)
            widget.setPrefixName("Graph Widget")
            wrappedWidget.activeOntology.currentIndexChanged[str].connect(widget._setSuffixName_)
            wrappedWidget.graphicsView.installEventFilter(widget)
            wrappedWidget.ontologyChanged.connect(self.synchronize)
            self.ontologyAdded.connect(wrappedWidget._updateActiveOntology)
            self.ontologyRemoved.connect(wrappedWidget._updateActiveOntology)
        if wrappedWidget is None :
            self.log.error("can not create widget with type " + widgetType)
            return
        wrappedWidget.setSettings(self.settings)
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
        callback = partial(self._deleteWidget_, widget)
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
        data = socket.read(4).data()
        slen = unpack(">L", data)[0]
        data = socket.read(slen).data()
        while len(data) < slen:
            data = data + socket.read(slen - len(data))
        assert len(data) == slen, "%d data read does not equal %d data expected." % (len(data), slen)
        logrecord = logging.makeLogRecord(loads(data))
        self.statusBar.showMessage(logrecord.getMessage())

    def _updateStatusbar_(self, wrappedWidget = None):
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
        self.log.info("synchronizing")
        self.synchronizeRequested.emit()

    def _deleteWidget_(self, widget):
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
        self.actionExpand.triggered.connect(widget._expandAll_)
        self.actionCollapse.triggered.connect(widget._collapseAll_)
        self.actionUndo.triggered.connect(widget._undo_)
        self.actionRedo.triggered.connect(widget._redo_)
        if widgetType == TextEditor :
            callback = partial(self._updateStatusbar_, widget)
            widget.getWidget().cursorPositionChanged.connect(callback)
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
        self.actionExpand.triggered.disconnect(widget._expandAll_)
        self.actionCollapse.triggered.disconnect(widget._collapseAll_)
        self.actionUndo.triggered.disconnect(widget._undo_)
        self.actionRedo.triggered.disconnect(widget._redo_)
        if widgetType == TextEditor :
            self._updateStatusbar_()
            widget.getWidget().cursorPositionChanged.disconnect(callback)
            self.actionCut.triggered.disconnect(widget.plainTextEdit.cut)
            self.actionCopy.triggered.disconnect(widget.plainTextEdit.copy)
            self.actionPaste.triggered.disconnect(widget.plainTextEdit.paste)
            self.actionDelete.triggered.disconnect(widget.plainTextEdit.clear)
            self.actionSelectAll.triggered.disconnect(widget.plainTextEdit.selectAll)

    def getDefaultOutputPath(self):
        return self.settings.value("configPath")

    def _newOntology_(self):
        '''Handles the new ontology action when it is triggered.'''
        defPath = self.getDefaultOutputPath()
        dialog = NewOntologyDialog(self, defPath)
        dialog.show()

    def _openLocalOntology_(self):
        '''Handles the open local ontology action when it is triggered.'''
        defPath = self.getDefaultOutputPath()
        x, y = QFileDialog.getOpenFileName(self, "Open Ontology File",
                                                defPath, "SUO KIF Files (*.kif)")
        if x == '' and y == '':
            return
        filepath = x
        filename = os.path.split(filepath)[1]
        filename = os.path.splitext(filename)[0]
        ontology = Ontology(filepath, filename)
        self.addOntology(ontology)

    def _openRemoteOntology_(self):
        '''Handles the open remote ontology action when it is triggered.'''
        defPath = self.getDefaultOutputPath()
        dialog = OpenRemoteOntologyDialog(self, defPath)
        dialog.show()

    def addOntology(self, ontology, newversion=None):
        '''Adds an ontology to index and notify all components required.'''
        RWWidget.SyntaxController.add_ontology(ontology, newversion)
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
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/update-product.png"), QIcon.Normal, QIcon.Off)
        actionUpdate = ontologyMenu.addAction("Update")
        actionUpdate.setData(ontology)
        actionUpdate.setIcon(icon)
        actionUpdate.setIconVisibleInMenu(True)
        actionUpdate.triggered.connect(partial(self._updateOntology_, ontology))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-revert.png"), QIcon.Normal, QIcon.Off)
        actionRevert = ontologyMenu.addAction("Revert")
        actionRevert.setData(ontology)
        actionRevert.setIcon(icon)
        actionRevert.setIconVisibleInMenu(True)
        actionRevert.triggered.connect(partial(self._revertOntology_, ontology))
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-properties.png"), QIcon.Normal, QIcon.Off)
        actionProperties = ontologyMenu.addAction("Properties")
        actionProperties.setData(ontology)
        actionProperties.setIconVisibleInMenu(True)
        actionProperties.setIcon(icon)
        actionProperties.triggered.connect(partial(self._showOntologyProperties_, ontology))
        ontologyMenu.addSeparator()
        # Close action
        icon = QIcon()
        icon.addPixmap(QPixmap(":/actions/gfx/actions/document-close.png"), QIcon.Normal, QIcon.Off)
        actionClose = ontologyMenu.addAction("Close")
        actionClose.setIcon(icon)
        actionClose.setIconVisibleInMenu(True)
        actionClose.setData(ontology)
        actionClose.triggered.connect(partial(self._closeOntology_, ontology, ontologyMenu))
        ontologyMenu.addSeparator()
        # Add ontology menu to menu bar
        self.menuOntology.addMenu(ontologyMenu)

    def _ClearRecentOntologiesHistory_(self):
        '''Handles the clear recent ontologies action when it is triggered.'''
        self.menuRecent_Ontologies.clear()
        self.menuRecent_Ontologies.addSeparator()
        self.menuRecent_Ontologies.addAction(self.clearHistoryAction)

    def _deleteOntology_(self, ontology):
        ''' TODO: '''
        pass

    def _updateOntology_(self, ontology):
        update(ontology, lambda x: RWWidget.SyntaxController.add_ontology(ontology, newversion=x.getvalue().decode('utf8')))
        self.synchronize()

    def _revertOntology_(self, ontology):
        ''' TODO: '''
        pass

    def _showOntologyProperties_(self, ontology):
        ''' TODO: '''
        pass

    def _closeOntology_(self, ontology, ontologyMenu):
        RWWidget.SyntaxController.remove_ontology(ontology)
        self.ontologyRemoved.emit(ontology)
        # remove ontology in active ones.
        ontologyMenu.deleteLater()

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
