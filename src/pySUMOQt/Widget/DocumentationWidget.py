""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

import logging

from PySide.QtCore import Slot, QTimer
from PySide.QtGui import QApplication, QMainWindow
from multiprocessing import Process, Pipe
from atexit import register, unregister

from pySUMOQt.Designer.DocumentationWidget import Ui_Form
from .Widget import RWidget

class DocumentationWidget(RWidget, Ui_Form):
    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """

    _WN_TROOL = list()
    _WN_PROCESS = None
    _WN_RECV = None
    _WN_SEND = None
    _TIMER = QTimer()
    _TIMER.setSingleShot(True)

    def __init__(self, mainwindow):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.lineEdit.returnPressed.connect(self.search)
        if len(DocumentationWidget._WN_TROOL) == 0:
            DocumentationWidget._WN_TROOL.append(1)
            (DocumentationWidget._WN_RECV, DocumentationWidget._WN_SEND) = Pipe(False)
            DocumentationWidget._WN_PROCESS = Process(target=DocumentationWidget._initialize, args=(DocumentationWidget._WN_SEND,))
            DocumentationWidget._WN_PROCESS.start()
            register(DocumentationWidget._WN_PROCESS.terminate)
            register(DocumentationWidget._WN_SEND.close)
            register(DocumentationWidget._WN_RECV.close)

    @classmethod
    def _initialize(cls, pipe):
        cls.IA.init_wordnet()
        pipe.send(cls.IA.wordnet)

    @Slot()
    def search(self):
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
        if len(DocumentationWidget._WN_TROOL) == 1:
            if not DocumentationWidget._WN_RECV.poll():
                self.log.info('Searching')
                self._TIMER.timeout.connect(self.search)
                self._TIMER.start(3000)
                return
            DocumentationWidget._WN_TROOL.append(2)
            RWidget.IA.wordnet = DocumentationWidget._WN_RECV.recv()
            DocumentationWidget._WN_PROCESS.join()
            unregister(DocumentationWidget._WN_PROCESS.terminate)
            unregister(DocumentationWidget._WN_SEND.close)
            unregister(DocumentationWidget._WN_RECV.close)
        try:
            searchOntology = self.getIndexAbstractor().search(
            self.lineEdit.text())
            self.OntologyText.setPlainText(_searchToText(searchOntology))
        except KeyError:
            self.OntologyText.setPlainText('')
        try:
            searchWordnet = self.getIndexAbstractor().wordnet_locate(
                self.lineEdit.text())
            self.WordNetText.setPlainText(_locateToText(searchWordnet))
        except KeyError:
            self.WordNetText.setPlainText('')

def _searchToText(search_results):
    string = ''
    for ontology in search_results.keys():
        string = ''.join([string, str(ontology), ':\n', '\n'.join(search_results[ontology]), '\n'])
    return string

def _locateToText(locate_results):
    return '\n'.join(locate_results)
