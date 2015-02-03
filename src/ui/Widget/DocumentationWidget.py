""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

from PySide.QtCore import Slot
from PySide.QtGui import QApplication, QMainWindow
import sys

from ui.Designer.DocumentationWidget import Ui_Form
from ui.Widget.Widget import RWidget as RWidget


class DocumentationWidget(RWidget, Ui_Form):

    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """

    def __init__(self, mainwindow):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.lineEdit.editingFinished.connect(self.search)

    def search_wordnet(self, string):
        """ Search the given string in the WordNet mapping database and
        displays the results the widgets content view.

        Arguments:

        - string: The given string to search for.

        """
        pass

    @Slot()
    def search(self):
        display = self.getIndexAbstractor().search(self.lineEdit.text())
        self.OntologyText.setPlainText(display)
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
        # print(self.lineEdit.text())

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = DocumentationWidget(mainwindow)
    mainwindow.show()
    sys.exit(application.exec_())
