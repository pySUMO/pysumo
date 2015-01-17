""" HierarchyWidget modul from pySUMO
"""

from ui.Widget.Widget import RWWidget as RWWidget

class HierarchyWidget(RWWidget):
    """ The hierarchy widget displays the ontology in a tree form conformly to
    the SUMO hierarchy model. The user can edit the ontology from this widget.
    It can show and hide nodes in it's display.

    Methods:

    - hide: hides the node's content that the user selected in the widget view.
    - show: shows the node's content that the user selected in the widget view.

    """

    def __init__(self):
        """ Initializes the hierarchy widget. """
        super(HierarchyWidget, self).__init__()
        self.abstractGraph = None

    def hide(self, entry):
        """ Hides the part the user selected of the Ontology. This function is called as a slot.

        Args:

        - entry: The user-selected entry.

        """
        pass

    def show(self, entry):
        """ Shows the part the user selected of the ontolgy. This function is called as a slot.

        Args:

        - entry: The user-selected entry.

        """
        pass

