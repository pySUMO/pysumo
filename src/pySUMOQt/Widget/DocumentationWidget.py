""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

from PySide.QtCore import Slot
from PySide.QtGui import QApplication, QMainWindow
import sys

from pySUMOQt.Designer.DocumentationWidget import Ui_Form
from .Widget import RWidget


class DocumentationWidget(RWidget, Ui_Form):

    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """

    def __init__(self, mainwindow):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.lineEdit.editingFinished.connect(self.search)

    @Slot()
    def search(self):
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
        searchOntology = self.getIndexAbstractor().search(
            self.lineEdit.text())

        self.OntologyText.setPlainText(k + v for (k, v) in searchOntology)
        searchWordnet = self.getIndexAbstractor().wordnet_locate(
            self.lineEdit.text())
        self.WordNetText.setPlainText(k + v for (k, v) in searchWordnet)

        # print(self.lineEdit.text())

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = DocumentationWidget(mainwindow)
    mainwindow.show()
    sys.exit(application.exec_())
