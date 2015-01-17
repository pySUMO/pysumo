""" This widget displays useful information related to the current
Ontology. For example you can search WordNet for synonyms or
print the definition for a selected term
"""

from ui.Widget.Widget import RWidget as RWidget

class DocumentationWidget(RWidget):
    """ The DocumentationWidget displays relevant information about the
    current Ontology, and offers a search interface to WordNet. """

    def __init__(self):
        """ Initializes the DocumentationWidget. """
        super(DocumentationWidget, self).__init__()

    def search_wordnet(self, string):
        """ Search the given string in the WordNet mapping database and
        displays the results the widgets content view.

        Arguments:

        - string: The given string to search for.

        """
        pass

    def search(self, string):
        """ Uses the IndexAbstractor to search for all occurrences of
        string in the Ontology and displays them.  """
