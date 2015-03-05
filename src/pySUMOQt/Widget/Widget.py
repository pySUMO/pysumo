""" Abstracts all Widgets of the pySUMO GUI.

This module contains:

- Widget: The main widget representation in the GUI.
- RWidget: The class of widgets which only have access to the IndexAbstractor and therefore cannot modify the Ontologies.
- RWWidget: The class of widgets which have access to the SyntaxController and the IndexAbstractor.

"""
from PySide.QtCore import QObject, Signal
from pysumo.indexabstractor import IndexAbstractor
from pysumo.syntaxcontroller import SyntaxController
from pysumo.syntaxcontroller import Ontology

import logging

class Widget(QObject):
    """ The main class representing a widget in the pySUMO GUI.

    Methods:

    - refresh: Refreshes the view of the current widget according to the IndexAbstractor.

    """
    IA = IndexAbstractor()

    def __init__(self, mainwindow):
        super(Widget, self).__init__(mainwindow)
        self.mw = mainwindow
        """ Initializes the Widget object. """

    @classmethod
    def getIndexAbstractor(cls):
        return cls.IA

    def refresh(self):
        """ Uses the IndexAbstractor to refresh the widget. """
        logging.info("refreshing " + self.parent().windowTitle())

    def getWidget(self):
        pass

    def _print_(self):
        pass
    
    def _quickPrint_(self):
        pass
    
    def _printPreview_(self):
        pass
    
    def _save_(self):
        pass
    
    def _zoomIn_(self):
        pass
    
    def _zoomOut_(self):
        pass
    
    def _expandAll_(self):
        pass
    
    def _collapseAll_(self):
        pass
    
    def _undo_(self):
        pass
    
    def _redo_(self):
        pass
    
    def setSettings(self, settings):
        self.settings = settings

class RWidget(Widget):

    """ Class for Widgets which only has read-access to the Ontologies. This
    class should not be used directly, but extended.
    """

    def __init__(self, mainwindow):
        """ Initializes the RWidget. """
        super(RWidget, self).__init__(mainwindow)


class RWWidget(Widget):

    """ Class for Widgets which have modify-access to the Ontologies. This
    class should not be used directly, but extended.

    Methods:

    - commit: Commits the modifications on the ontology and notifies the others widgets of changes.

    """
    SyntaxController = SyntaxController(Widget.getIndexAbstractor())
    ontologyChanged = Signal()

    def __init__(self, mainwindow):
        """ Initializes the read/write widget """
        super(RWWidget, self).__init__(mainwindow)

    def commit(self):
        """ Commits modifications to the ontology to the SyntaxController, and
        if successful updates the IndexAbstractor and notifies all other
        widgets that the Ontology has been modified. """
        self.ontologyChanged.emit()
        
    def getActiveOntology(self):
        pass
    
    def setActiveOntology(self, ontology):
        pass
        
    def _save_(self):
        ontology = self.getActiveOntology()
        if ontology is None :
            return 
        if type(ontology) is Ontology :
            ontology.save()
            
    def _redo_(self):
        ontology = self.getActiveOntology()
        if not ontology is None and type(ontology) == Ontology :
            action_log = ontology.action_log
            action_log.redo()
            self.commit()
            
    def _undo_(self):
        ontology = self.getActiveOntology()
        if not ontology is None and type(ontology) == Ontology :
            action_log = ontology.action_log
            action_log.undo()
            self.commit()