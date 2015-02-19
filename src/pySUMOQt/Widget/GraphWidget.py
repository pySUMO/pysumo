""" Displays a graph-based representation of the Ontology and allows the
Ontology to be modified graphically.

This module contains:

GraphWidget: Displays and allows modification of a graph of the Ontology.

"""

from PySide.QtCore import QLineF, Slot
from PySide.QtGui import QApplication, QMainWindow, QColor, QPen, QStandardItem
from PySide.QtGui import QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsScene, QGraphicsItem
import pygraphviz
import random
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
        self.layoutedGraph = None

        self.nodesToQNodes = None
        self.qLines = []
        self.qpens = {}
        self.lastScale = 1
        #self.graphicsView.scale(0.33, 0.33)
        self.doubleSpinBox.valueChanged[float].connect(self.changeScale)

    def initRelationBox(self):
        m = self.relations.model()
        for i in self.getIndexAbstractor().get_graph('instance').relations.keys():
            m.appendRow(QStandardItem(i))

    @Slot(float)
    def changeScale(self, val):
        toScale = val / self.lastScale
        self.lastScale = val
        self.graphicsView.scale(toScale, toScale)

    @Slot()
    def renewplot(self):
        scene = self.graphicsView.scene()
        scene.changed.disconnect(self.renewplot)
        for i in self.qLines:
            scene.removeItem(i)

        self.qLines = []

        for edge in gv.edges_iter():

            qnode1 = self.nodesToQNodes[edge[0]]
            qnode2 = self.nodesToQNodes[edge[1]]
            line = QLineF(qnode1.pos(), qnode2.pos())
            item = scene.addLine(line, self.qpens[edge.attr['color']])
            self.qLines.append(item)

    def plot(self, layoutedgraph):
        if layoutedgraph is None:
            return
        self.layoutedGraph = layoutedgraph
        scene = QGraphicsScene()
        self.nodesToQNodes = {}
        for node in gv.nodes_iter():
            (x, y) = node.attr['pos'].split(',')
            qnode = QGraphicsEllipseItem(-25, -25, 50, 50)
            qnode.setPos(float(x) * 4, float(y) * 4)
            qnode.setFlag(QGraphicsItem.ItemIsMovable)
            qnode.setBrush(QColor(255, 150, 150))
            txt = QGraphicsSimpleTextItem(qnode)
            txt.setPos(-25, 0)
            font = txt.font()
            font.setPointSize(7)
            txt.setFont(font)
            txt.setText(node)
            scene.addItem(qnode)

            self.nodesToQNodes[node] = qnode

        for edge in gv.edges_iter():

            qnode1 = self.nodesToQNodes[edge[0]]
            qnode2 = self.nodesToQNodes[edge[1]]
            line = QLineF(
                qnode1.pos(), qnode2.pos())
            if edge.attr['color'] not in self.qpens:
                self.qpens[edge.attr['color']] = QPen(
                    QColor(edge.attr['color']))
            item = scene.addLine(line, self.qpens[edge.attr['color']])

            self.qLines.append(item)
            # break
        scene.changed.connect(self.renewplot)
        self.graphicsView.setScene(scene)

    def createGV(self):
        gv = pygraphviz.AGraph(strict=False)
        y = self.getIndexAbstractor().get_graph('instance')
        colors = ["black", "red", "blue", "green", "darkorchid", "gold2",
                  "yellow", "turquoise", "sienna", "darkgreen"]
        for k in y.relations.keys():
            l = [(k, v) for v in y.relations[k]]
            gv.add_edges_from(l, color=random.choice(colors))
        gv.layout("sfdp")

if __name__ == "__main__":
    gv = pygraphviz.AGraph(strict=False)

    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = GraphWidget(mainwindow)
    sumo = Ontology('../data/Merge.kif', name='SUMO')
    with open(sumo.path) as f:
        kif = parser.kifparse(f, sumo)

    x.getIndexAbstractor().update_index(kif)

    x.createGV()
    x.plot()
    x.initRelationBox()
    mainwindow.show()

    sys.exit(application.exec_())
