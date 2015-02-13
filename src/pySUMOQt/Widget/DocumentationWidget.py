""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

from PySide.QtCore import Slot
from PySide.QtGui import QApplication, QMainWindow

from pySUMOQt.Designer.DocumentationWidget import Ui_Form
from .Widget import RWidget


class DocumentationWidget(RWidget, Ui_Form):
    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """


    def __init__(self, mainwindow):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.lineEdit.returnPressed.connect(self.search)

    @Slot()
    def search(self):
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
        searchOntology = self.getIndexAbstractor().search(
            self.lineEdit.text())

        self.OntologyText.setPlainText(searchToText(searchOntology))
        searchWordnet = self.getIndexAbstractor().wordnet_locate(
            self.lineEdit.text())
        self.WordNetText.setPlainText(locateToText(searchWordnet))

def searchToText(search_results):
    string = ''
    for ontology in search_results.keys():
        string = ''.join([string, str(ontology), ':\n', '\n'.join(search_results[ontology]), '\n'])
    return string

def locateToText(locate_results):
    return '\n'.join(locate_results)
