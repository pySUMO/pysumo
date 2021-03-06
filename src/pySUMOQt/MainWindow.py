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
from PySide.QtGui import QAction, QMenu, QMessageBox
from PySide.QtNetwork import QLocalServer

from pySUMOQt.Designer.MainWindow import Ui_mainwindow
from pySUMOQt.Widget.DocumentationWidget import DocumentationWidget
from pySUMOQt.Widget.HierarchyWidget import HierarchyWidget
from pySUMOQt.Widget.TextEditor import TextEditor
from pySUMOQt.Widget.Widget import RWWidget, PySUMOWidget

from pySUMOQt.Settings import LayoutManager, PySumoSettings
from pySUMOQt.Dialog import NewOntologyDialog, OpenRemoteOntologyDialog, OptionDialog,\
    OntologyPropertyDialog
from pySUMOQt.Widget.GraphWidget import GraphWidget
from pysumo.syntaxcontroller import Ontology
from pysumo import logger
from pysumo.logger.infolog import InfoLog
from pysumo.updater import update
from _io import BytesIO
from builtins import dict

QCoreApplication.setApplicationName("pySUMO")
QCoreApplication.setApplicationVersion("1.0")
QCoreApplication.setOrganizationName("PSE Team")


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
    jumpRequested = Signal(int, str)
    def __init__(self):
        """ Constructs the main window.  """
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.actionAboutpySUMO.triggered.connect(self._showAboutBox_)
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
        """ 
        QT Slot to open the option dialog.
        """
        self.optionDialog.initialize()
        self.optionDialog.show()

    def _addWidget_(self, widgetType, widgetMenu):
        """ 
        Add a widget into the layout with the given widget type as string.
        
        Parameter:
        
        - widgetType : The widget type as a string. Can be TextEditorWidget, DocumentationWidget, HierarchyWidget or GraphWidget.
        - widgetMenu : The QMenu from where the widget can be hidden.
        """
        widget = self.createPySumoWidget(widgetType, widgetMenu)
        self.addOrRestoreWidget(widget, widgetMenu, True)
        
    def createPySumoWidget(self, widgetType, widgetMenu):
        """
        Create a widget wrapper containing the given widget type.
        
        Parameter:
        
        - widgetType : The widget type as a string. Can be TextEditorWidget, DocumentationWidget, HierarchyWidget or GraphWidget.
        - widgetMenu : The QMenu from where the widget can be hidden.
        """
        widget = None
        if widgetType == "TextEditorWidget" :
            widget = TextEditor(self, settings=self.settings)
            widget.ontologySelector.currentIndexChanged[str].connect(widget._setSuffixName_)
            widget.ontologyChanged.connect(self.synchronize)
            self.ontologyAdded.connect(widget._updateOntologySelector)
            self.ontologyRemoved.connect(widget._updateOntologySelector)
            self.jumpRequested.connect(widget.jumpToLocation)
        elif widgetType == "DocumentationWidget" :
            widget = DocumentationWidget(self)
            widget.OntologyText.anchorClicked.connect(self.jumpToLocation)
        elif widgetType == "HierarchyWidget" :
            widget = HierarchyWidget(self)
        elif widgetType == "GraphWidget":
            widget = GraphWidget(self)
            widget.activeOntology.currentIndexChanged[str].connect(widget._setSuffixName_)
            widget.ontologyChanged.connect(self.synchronize)
            self.ontologyAdded.connect(widget._updateActiveOntology)
            self.ontologyRemoved.connect(widget._updateActiveOntology)
        if widget is None :
            self.log.error("can not create widget with type " + widgetType)
            return
        
        widget.installEventFilter(widget)
        widget.setPrefixName(widgetType)
        widget.setSettings(self.settings)
        self.synchronizeRequested.connect(widget.refresh)
        objName = widgetType
        objName += str(len(widgetMenu.actions()))
        widget.setObjectName(objName)
        widget.setWidget(widget.widget)
        widget.wrappedWidget = widget
        return widget

    def addDeleteWidgetAction(self, widget):
        """
        Add the delete action for the given widget in the delete widget menu.
        
        Parameter:
        
        - widget: The pysumo widget which will be deleted on action triggered.
        """
        action = QAction(widget)
        action.setText(widget.windowTitle())
        callback = partial(self._deleteWidget_, widget)
        action.triggered.connect(callback)
        if not self.menuDelete.isEnabled():
            self.menuDelete.setEnabled(True)
        self.menuDelete.addAction(action)

    def addOrRestoreWidget(self, widget, menu, directAdd=False):
        """
        Restore a widget on the layout or place it, if restore failed.
        
        Parameter:
        
        - widget : The pysumo widget to add in the window layout.
        - menu : The QMenu from where the widget can be hidden.
        - directAdd : If true, force add without restoring the pysumo widget.
        """
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
        """ 
        Called when the main window is closing, and meaning that the application is exiting.
        The application then saves the layout, and then check for unsaved documents.
        
        Override from QWidget.
        """
        self.userLayout.saveLayout()
        # check for unsaved files.
        for o in PySUMOWidget.IA.ontologies :
            changed , diff = self.ontologyChanged(o)
            if changed :
                msgBox = QMessageBox(self)
                msgBox.setText("The ontology file \"" + o.name + "\" has been modified.")
                msgBox.setInformativeText("Do you want to save your changes?")
                msgBox.setDetailedText(diff)
                msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
                msgBox.setDefaultButton(QMessageBox.Save)
                ret = msgBox.exec_()
                if ret == QMessageBox.Save :
                    o.save()
        super(MainWindow, self).closeEvent(event)
        
    def ontologyChanged(self, ontology):
        """
        Check if an ontology is different from the on disk file representation of this ontology.
        
        Parameter :
        
        - ontology : The ontology to check whether it changed or not.
        
        Return changed, diff. changed is whether true or false accordingly to the change state. If 
        the ontology has been changed, return diff which is the string diff of the old with the new version 
        of the ontology. If the ontology wasn't changed, return an empty string as diff.
        """
        with open(ontology.path) as f:
            b = BytesIO(f.read().encode('utf8', errors='replace'))
        diff = ontology.action_log.log_io.diff(ontology.action_log.current, b).getvalue()
        return diff != b'', diff.decode(encoding="utf-8", errors="replace")

    def createStatusBar(self):
        """
        Create the status bar.
        """
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
        """
        Qt slot which sets up a status connection in the status bar.
        """
        socket = self.statusBar.socketServer.nextPendingConnection()
        socket.readyRead.connect(partial(self.displayLog, socket))

    @Slot()
    def displayLog(self, socket):
        """
        Qt slot which displays a log message.
        
        Parameter:
        
        - socket : The socket on which the log message must be read.
        """
        data = socket.read(4).data()
        slen = unpack(">L", data)[0]
        data = socket.read(slen).data()
        while len(data) < slen:
            data = data + socket.read(slen - len(data))
        assert len(data) == slen, "%d data read does not equal %d data expected." % (len(data), slen)
        logrecord = logging.makeLogRecord(loads(data))
        self.statusBar.showMessage(logrecord.getMessage(), 5000)

    def _updateStatusbar_(self, wrappedWidget=None):
        """
        Update the status bar.
        
        Parameter:
        
        - widget: a wrapped widget which will provide some information. Here we just use the TextEditor widget.
        """
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

    def jumpToLocation(self, var):
        l = var.path().split(' ')
        loc = l.pop(0)
        ont = ' '.join(l)
        self.jumpRequested.emit(int(loc), ont)

    def synchronize(self):
        """ Performs synchronization of the main window by reporting changes in
        all the others widgets. """
        self.synchronizeRequested.emit()

    def _deleteWidget_(self, widget):
        """
        QT Slot to delete a widget from the layout.
        
        Parameter :
        
        - widget : The pysumo widget to delete.
        """
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
        """
        Connects a pysumo widget to mainwindow global actions, like expand, undo, ...
        
        Parameter :
        
        - widget : The widget to connect in the maindow.
        
        Returns a callback for TextEditor widgets with the status bar to disconnect them later.
        """
        widgetType = type(widget)
        self.actionPrint.triggered.connect(widget._print_)
        self.actionPrintPreview.triggered.connect(widget._printPreview_)
        self.actionQuickPrint.triggered.connect(widget._quickPrint_)
        self.actionSave.triggered.connect(widget.saveOntology)
        self.actionZoomIn.triggered.connect(widget.zoomIn)
        self.actionZoomOut.triggered.connect(widget.zoomOut)
        self.actionExpand.triggered.connect(widget.expandAll)
        self.actionCollapse.triggered.connect(widget.collapseAll)
        self.actionUndo.triggered.connect(widget.undo)
        self.actionRedo.triggered.connect(widget.redo)
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
        """
        Disconnects a widget from the main window global actions.
        
        Parameter :
        
        - widget : The pysumo widget to disconnect form the main window.
        - callback: The callback with the statusbar if the widget is a TextEditor widget.
        """
        widgetType = type(widget)
        self.actionPrint.triggered.disconnect(widget._print_)
        self.actionQuickPrint.triggered.disconnect(widget._quickPrint_)
        self.actionPrintPreview.triggered.disconnect(widget._printPreview_)
        self.actionSave.triggered.disconnect(widget.saveOntology)
        self.actionZoomIn.triggered.disconnect(widget.zoomIn)
        self.actionZoomOut.triggered.disconnect(widget.zoomOut)
        self.actionExpand.triggered.disconnect(widget.expandAll)
        self.actionCollapse.triggered.disconnect(widget.collapseAll)
        self.actionUndo.triggered.disconnect(widget.undo)
        self.actionRedo.triggered.disconnect(widget.redo)
        if widgetType == TextEditor :
            self._updateStatusbar_()
            widget.getWidget().cursorPositionChanged.disconnect(callback)
            self.actionCut.triggered.disconnect(widget.plainTextEdit.cut)
            self.actionCopy.triggered.disconnect(widget.plainTextEdit.copy)
            self.actionPaste.triggered.disconnect(widget.plainTextEdit.paste)
            self.actionDelete.triggered.disconnect(widget.plainTextEdit.clear)
            self.actionSelectAll.triggered.disconnect(widget.plainTextEdit.selectAll)

    def getDefaultOutputPath(self):
        """
        Returns the default output path as a string.
        """
        return self.settings.value("configPath")

    def _newOntology_(self):
        """
        QT Slot which handles the new ontology action when it is triggered.
        """
        defPath = self.getDefaultOutputPath()
        dialog = NewOntologyDialog(self, defPath)
        dialog.show()

    def _openLocalOntology_(self):
        """
        QT Slot which handles the open local ontology action when it is triggered.
        """
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
        """
        QT Slot which handles the open remote ontology action when it is triggered.
        """
        defPath = self.getDefaultOutputPath()
        dialog = OpenRemoteOntologyDialog(self, defPath)
        dialog.show()

    def addOntology(self, ontology, newversion=None):
        """
        Adds an ontology to index and notify all components required.
        
        Parameter :
        
        - ontology : The ontology to add.
        - newversion : The new version of the ontology.
        """
        RWWidget.SyntaxController.add_ontology(ontology, newversion)
        self.ontologyAdded.emit(ontology)
        
    def addRecentOntology(self, ontology):
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

    def notifyOntologyAdded(self, ontology):
        """
        Notify that an ontology was added to the index.
        
        Parameter :
        
        - ontology : The added ontology.
        """
        if ontology is None:
            return
        self.addRecentOntology(ontology)
        i = len(self.menuOntology.actions()) - 3
        ontologyMenu = None
        for x in range(i, len(self.menuOntology.actions())) :
            a = self.menuOntology.actions()[x]
            if a.text() == ontology.name :
                # Don't need to add menu.
                ontologyMenu = a.menu()
                break
            
        if ontologyMenu is None :
            ontologyMenu = QMenu(self)
            ontologyMenu.setTitle(ontology.name)
        ontologyMenu.clear()
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
        actionRevert.triggered.connect(partial(self._revertOntology_, ontology, ontologyMenu))
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
        """
        QT Slot which handles the clear recent ontologies action when it is triggered.
        """
        self.menuRecent_Ontologies.clear()
        self.menuRecent_Ontologies.addSeparator()
        self.menuRecent_Ontologies.addAction(self.clearHistoryAction)

    def _deleteOntology_(self, ontology, ontologyMenu=None):
        """
        QT Slot which handles the delete ontology action when it is triggered.
        
        Parameter :
        
        - ontology : The ontology to delete.
        - ontologyMenu : The QMenu where the ontology could be managed. It should be remove too.
        """
        self._closeOntology_(ontology, ontologyMenu)
        os.remove(ontology.path)

    def _updateOntology_(self, ontology):
        """
        QT Slot which handles the update ontology action when it is triggered.
        
        Parameter :
        
        - ontology : The ontology to update.
        """
        if not ontology is None and ontology.url is None :
            QMessageBox.warning(self, "Can not perform an update.", "The ontology " + ontology.name + " has no url specified in it's configuration to perform an update.", QMessageBox.Ok, QMessageBox.Ok)
            return 
        update(ontology, lambda x: RWWidget.SyntaxController.add_ontology(ontology, newversion=x.getvalue().decode('utf8')))
        self.synchronize()

    def _revertOntology_(self, ontology, ontologyMenu=None):
        """
        QT Slot which handles the revert ontology action when it is triggered.
        
        Parameter :
        
        - ontology : the ontology to revert.
        - ontologyMenu : The QMenu where the ontology could be managed.
        """
        # save the state of the active ontologies.
        state = dict()
        for widget in self.widgets :
            if isinstance(widget, RWWidget) and widget.getActiveOntology() is not None and widget.getActiveOntology() == ontology :
                state[widget] = ontology
        self._closeOntology_(ontology, ontologyMenu)
        self.addOntology(ontology)
        # restore the state of the active ontologies.
        for widget in state.keys() :
            if widget.getActiveOntology() is None :
                widget.setActiveOntology(ontology) 

    def _showOntologyProperties_(self, ontology):
        """
        QT Slot which handles the show ontology property action when it is triggered.
        
        Parameter :
        
        - ontology : The ontology which properties should be displayed.
        """
        OntologyPropertyDialog(self, ontology).show()
    
    def removeOntology(self, ontology):
        """ Removes an ontology form the index and notifies the required components.
        
        Parameter :
        
        - ontology : The ontology to remove.
        """
        RWWidget.SyntaxController.remove_ontology(ontology)
        self.ontologyRemoved.emit(ontology)

    def _closeOntology_(self, ontology, ontologyMenu):
        """ 
        QT Slot which handles the close ontology action when it is triggered.
        
        Parameter :
        
        - ontology : The ontology to delete.
        - ontologyMenu : The QMenu where the ontology could be managed. It should be remove too.
        """
        changed , diff = self.ontologyChanged(ontology)
        if changed :
            msgBox = QMessageBox(self)
            msgBox.setText("The ontology file \"" + ontology.name + "\" has been modified.")
            msgBox.setInformativeText("Do you want to save your changes?")
            msgBox.setDetailedText(diff)
            msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard)
            msgBox.setDefaultButton(QMessageBox.Save)
            ret = msgBox.exec_()
            if ret == QMessageBox.Save :
                ontology.save()
        self.removeOntology(ontology)
        # remove ontology in active ones.
        ontologyMenu.deleteLater()
        
    def _showAboutBox_(self):
        """
        QT Slot which handles the show about pysumo action when it is triggered.
        """
        QMessageBox.about(self, "About PySumo", "PSE TEAM Project")

def main():
    app = QApplication(sys.argv)
    signal(SIGINT, quit_handler)
    mainwindow = MainWindow()
    app.setActiveWindow(mainwindow)
    sys.exit(app.exec_())

def quit_handler(signum, frame):
    """
    Handler for the SIGINT signal.
    """
    QApplication.closeAllWindows()
    sys.exit()

if __name__ == '__main__':
    main()
