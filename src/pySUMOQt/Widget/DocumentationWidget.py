""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

from PySide.QtCore import Slot
from PySide.QtGui import QApplication, QMainWindow
from multiprocessing import Process, Pipe

from pySUMOQt.Designer.DocumentationWidget import Ui_Form
from .Widget import RWidget

class DocumentationWidget(RWidget, Ui_Form):
    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """

    WN_TROOL = list()
    WN_PROCESS = None
    WN_RECV = None
    WN_SEND = None

    def __init__(self, mainwindow):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.lineEdit.returnPressed.connect(self.search)
        if len(DocumentationWidget.WN_TROOL) == 0:
            DocumentationWidget.WN_TROOL.append(1)
            (DocumentationWidget.WN_RECV, DocumentationWidget.WN_SEND) = Pipe(False)
            DocumentationWidget.WN_PROCESS = Process(target=DocumentationWidget._initialize, args=(DocumentationWidget.WN_SEND,))
            DocumentationWidget.WN_PROCESS.start()

    @classmethod
    def _initialize(cls, pipe):
        cls.IA.init_wordnet()
        pipe.send(cls.IA.wordnet)

    @Slot()
    def search(self):
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
        if len(DocumentationWidget.WN_TROOL) == 1:
            DocumentationWidget.WN_TROOL.append(2)
            RWidget.IA.wordnet = DocumentationWidget.WN_RECV.recv()
            DocumentationWidget.WN_PROCESS.join()
        try:
            searchOntology = self.getIndexAbstractor().search(
            self.lineEdit.text())
            self.OntologyText.setPlainText(searchToText(searchOntology))
        except KeyError:
            self.OntologyText.setPlainText('')
        try:
            searchWordnet = self.getIndexAbstractor().wordnet_locate(
                self.lineEdit.text())
            self.WordNetText.setPlainText(locateToText(searchWordnet))
        except KeyError:
            self.WordNetText.setPlainText('')

def searchToText(search_results):
    string = ''
    for ontology in search_results.keys():
        string = ''.join([string, str(ontology), ':\n', '\n'.join(search_results[ontology]), '\n'])
    return string

def locateToText(locate_results):
    return '\n'.join(locate_results)
