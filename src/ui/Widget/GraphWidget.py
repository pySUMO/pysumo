""" Displays a graph-based representation of the Ontology and allows the
Ontology to be modified graphically.

This module contains:

GraphWidget: Displays and allows modification of a graph of the Ontology.

"""

from ui.Widget.Widget import RWWidget as RWWidget

#from pysumo.ui.qt.widget.rwwidget import RWWidget as RWWidget

class GraphWidget(RWWidget):
    """ Displays a graph of the Ontology and passes all modifications to the
    SyntaxController.

    Variables:

    - abstractGraph: The currently displayed AbstractGraph.
    - dotGraph: The DotGraph for the current AbstractGraph.
    - layout: The layouted version of the current DotGraph.

    """

    def __init__(self):
        """ Initializes the GraphWidget. """
        super(GraphWidget, self).__init__()
        self.abstractGraph = None
        self.dotGraph = None
        self.layout = None
