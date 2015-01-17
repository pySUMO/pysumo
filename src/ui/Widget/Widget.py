""" Abstracts all Widgets of the pySUMO GUI.

This module contains:

- Widget: The main widget representation in the GUI.
- RWidget: The class of widgets which only have access to the IndexAbstractor and therefore cannot modify the Ontologies.
- RWWidget: The class of widgets which have access to the SyntaxController and the IndexAbstractor.

"""

class Widget():
    """ The main class representing a widget in the pySUMO GUI.

    Methods:

    - refresh: Refreshes the view of the current widget according to the IndexAbstractor.

    """

    def __init__(self):
        """ Initializes the Widget object. """
        self.IndexAbstractor = IndexAbstractor()

    def refresh(self):
        """ Uses the IndexAbstractor to refresh the widget. """

class RWidget(Widget):
    """ Class for Widgets which only has read-access to the Ontologies. This
    class should not be used directly, but extended.
    """

    def __init__(self):
        """ Initializes the RWidget. """
        super(RWidget, self).__init__()

class RWWidget(Widget):
    """ Class for Widgets which have modify-access to the Ontologies. This
    class should not be used directly, but extended.

    Methods:

    - commit: Commits the modifications on the ontology and notifies the others widgets of changes.

    """

    def __init__(self):
        """ Initializes the read/write widget """
        super(RWWidget, self).__init__()
        self.SyntaxController = SyntaxController()

    def commit(self):
        """ Commits modifications to the ontology to the SyntaxController, and
        if successful updates the IndexAbstractor and notifies all other
        widgets that the Ontology has been modified. """
