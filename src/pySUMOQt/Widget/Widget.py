""" Abstracts all Widgets of the pySUMO GUI.

This module contains:

- Widget: The main widget representation in the GUI.
- RWidget: The class of widgets which only have access to the IndexAbstractor and therefore cannot modify the Ontologies.
- RWWidget: The class of widgets which have access to the SyntaxController and the IndexAbstractor.

"""
from PySide.QtCore import Signal, Slot, QEvent, Qt
from PySide.QtGui import QDockWidget
from pysumo.indexabstractor import IndexAbstractor
from pysumo.syntaxcontroller import SyntaxController

import logging

class PySUMOWidget(QDockWidget):
    """ The main class representing a widget in the pySUMO GUI.
    It catches the focus event on components in widget to 
    connect them the application actions like cut, copy, 
    paste, or undo, ...

    Methods:

    - refresh: Refreshes the view of the current widget according to the IndexAbstractor.

    
    """
    def __init__(self, mainwindow):
        """ Initializes the Widget object.  
        Initializes a pysumo widget with the parent which is the main window.
        
        Parameter: 
        
        - mainwindow : The main window.
        """
        super(PySUMOWidget, self).__init__()
        
        self.mw = mainwindow
        self.mainWindow = mainwindow
        self.isPopedOut = False
        self.topLevelChanged.connect(self.setPopedOut)
        self.widget = None
        self.callback = None
        self.prefixName = None
        self.suffixName = None

    def _setSuffixName_(self, s):
        """ QT Slot which sets a suffix name to the title of the dock widget, 
        like the name of the active ontology in the widget.
        
        Parameter:
        
        - s : The suffix name as a string.
        """
        if s is None :
            return
        s = s.strip()
        if "" == s :
            s = None
        self.suffixName = s
        self.updateTitle()

    def setPrefixName(self, s):
        """ 
        Sets the prefix name which is the default title of a pysumo widget.
        
        Parameter:
        
        - s : The prefix or default name as a string.
        """
        if s is None :
            return
        s = s.strip()
        if "" == s :
            return
        self.prefixName = s
        self.updateTitle()

    def updateTitle(self):
        """ 
        Updates the title of the pysumo widget according to it'S prefix and suffix name.
        """
        assert self.prefixName is not None
        title = self.prefixName
        if self.suffixName is not None :
            title = title + " | " + self.suffixName
        self.setWindowTitle(title)

    @Slot()
    def setPopedOut(self):
        """ 
        Qt Slot which customizes the pop out of a pysumo widget.
        """
        if not self.isPopedOut :
            self.setWindowFlags(Qt.Window)
            self.show()
            self.isPopedOut = True
        else :
            self.isPopedOut = False

    def eventFilter(self, source, event):
        """
        Filters event on a component where the pysumo was installed as event filter.
        
        Override from QObject.
        """
        if event.type() == QEvent.FocusIn:
            self.callback = self.mainWindow.connectWidget(self)
        elif event.type() == QEvent.FocusOut:
            self.mainWindow.disconnectWidget(self, self.callback)
        return super(PySUMOWidget, self).eventFilter(source, event)


    IA = IndexAbstractor()


    @classmethod
    def getIndexAbstractor(cls):
        return cls.IA

    def refresh(self):
        """ Uses the IndexAbstractor to refresh the widget. """

    def getWidget(self):
        pass

    def _print_(self):
        pass
    
    def _quickPrint_(self):
        pass
    
    def _printPreview_(self):
        pass
    
    def zoomIn(self):
        pass
    
    def zoomOut(self):
        pass
    
    def expandAll(self):
        pass
    
    def collapseAll(self):
        pass
    
    def setSettings(self, settings):
        self.settings = settings

class RWidget(PySUMOWidget):

    """ Class for Widgets which only has read-access to the Ontologies. This
    class should not be used directly, but extended.
    """

    def __init__(self, mainwindow):
        """ Initializes the RWidget. """
        super(RWidget, self).__init__(mainwindow)


class RWWidget(PySUMOWidget):

    """ Class for Widgets which have modify-access to the Ontologies. This
    class should not be used directly, but extended.

    Methods:

    - commit: Commits the modifications on the ontology and notifies the others widgets of changes.

    """
    SyntaxController = SyntaxController(PySUMOWidget.getIndexAbstractor())
    ontologyChanged = Signal()

    def __init__(self, mainwindow):
        """ Initializes the read/write widget """
        super(RWWidget, self).__init__(mainwindow)
        self.log = logging.getLogger('.' + __name__)
    
    def commit(self):
        """ Commits modifications to the ontology to the SyntaxController, and
        if successful updates the IndexAbstractor and notifies all other
        widgets that the Ontology has been modified. """
        self.ontologyChanged.emit()
        
    def getActiveOntology(self):
        pass
    
    def setActiveOntology(self, ontology):
        pass
        
    def saveOntology(self):
        ontology = self.getActiveOntology()
        if ontology in self.IA.ontologies:
            self.log.info('Saving Ontology: %s' % str(ontology))
            ontology.save()
            
    def redo(self):
        ontology = self.getActiveOntology()
        if ontology in self.IA.ontologies:
            self.SyntaxController.redo(ontology)
            self.ontologyChanged.emit()
                        
    def undo(self):
        ontology = self.getActiveOntology()
        if ontology in self.IA.ontologies:
            self.SyntaxController.undo(ontology)
            self.ontologyChanged.emit()
