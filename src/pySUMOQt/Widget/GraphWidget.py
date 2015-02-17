""" Displays a graph-based representation of the Ontology and allows the
Ontology to be modified graphically.

This module contains:

GraphWidget: Displays and allows modification of a graph of the Ontology.

"""

from PySide.QtGui import QApplication, QMainWindow
from PySide.QtGui import QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsScene, QGraphicsItem
import pygraphviz
import sys

from pySUMOQt.Designer.GraphWidget import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget

import pysumo.parser as parser
from pysumo.syntaxcontroller import Ontology


class GraphWidget(RWWidget, Ui_Form):

    """ Displays a graph of the Ontology and passes all modifications to the
    SyntaxController.

    Variables:

    - abstractGraph: The currently displayed AbstractGraph.
    - dotGraph: The DotGraph for the current AbstractGraph.
    - layout: The layouted version of the current DotGraph.

    """

    def __init__(self, mainwindow):
        """ Initializes the GraphWidget. """
        super(GraphWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)

        self.abstractGraph = None
        self.dotGraph = None
        self.layout = None

    def plot(self, layoutedgraph):
        scene = QGraphicsScene()
        for node in gv.nodes_iter():
            (x, y) = node.attr['pos'].split(',')
            qnode = QGraphicsEllipseItem(float(x), float(y), 30, 30)
            qnode.setFlag(QGraphicsItem.ItemIsMovable)
            txt = QGraphicsSimpleTextItem(qnode)
            txt.setPos(float(x), float(y))
            font = txt.font()
            font.setPointSize(12)
            txt.setFont(font)
            txt.setText(node)

            scene.addItem(qnode)
        self.graphicsView.setScene(scene)

if __name__ == "__main__":
    gv = pygraphviz.AGraph()

    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = GraphWidget(mainwindow)
    sumo = Ontology('../data/Merge.kif', name='SUMO')
    with open(sumo.path) as f:
        kif = parser.kifparse(f, sumo)

    x.getIndexAbstractor().update_index(kif)
    y = x.getIndexAbstractor().get_graph('instance')

    gv.add_nodes_from(y.nodes)
    l = list()
    for k in y.relations.keys():
        l.extend([(k, v) for v in y.relations[k]])
    gv.add_edges_from(l)
    gv.layout("dot")

    x.plot(gv)
    mainwindow.show()

    sys.exit(application.exec_())
