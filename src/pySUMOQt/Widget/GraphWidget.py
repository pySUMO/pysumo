""" Displays a graph-based representation of the Ontology and allows the
Ontology to be modified graphically.

This module contains:

GraphWidget: Displays and allows modification of a graph of the Ontology.

"""

from PySide.QtCore import QLineF, Slot, Qt
from PySide.QtGui import QColor, QPen, QStandardItem, QMenu, QInputDialog
from PySide.QtGui import QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsScene, QGraphicsItem
import pygraphviz
import random
import logging


from pySUMOQt.Designer.GraphWidget import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget

def insert_newlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))


class QtNode(QGraphicsEllipseItem):
    """ A Node representation in Qt"""
    callback = None
    def setCallBackItemChange(self, f):
        """ Sets a callback function to call after the position has changed"""
        self.callback = f
        
    def setCallBackAddRelation(self, f):
        self.callbackR = f
    
    def setNode(self,node):
        self.node = node
        
    def itemChange(self, itemChange, val):
        if (itemChange == QGraphicsItem.ItemPositionHasChanged):
            if self.callback is not None:
                self.callback()
        return super().itemChange(itemChange, val)
    
    def mouseDoubleClickEvent(self, event):
        if self.callbackR is not None:
            self.callbackR(self)
        #super(QtNode, self).mouseDoubleClickEvent(event)

class GraphWidget(RWWidget, Ui_Form):

    """ Displays a graph of the Ontology and passes all modifications to the
    SyntaxController.

    Variables:

    - abstractGraph: The currently displayed AbstractGraph.
    - gv: The layouted version of the current DotGraph.

    """

    def __init__(self, mainwindow):
        """ Initializes the GraphWidget. """
        super(GraphWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.startRelation = None
        self.abstractGraph = None
        self.gv = None
        self.widget = self.layoutWidget
        self.nodesToQNodes = None
        self.qLines = []
        self.qpens = {}
        self.lastScale = 1
        self.initMenu()
        self.roots = set()
        self.doubleSpinBox.valueChanged[float].connect(self.changeScale)
        self.lineEdit.textChanged.connect(self.searchNode)
        self.rootSelector.insertItem(0,"---")
        self.rootSelector.currentIndexChanged[str].connect(self.newRoot)
        self.relations.currentIndexChanged[str].connect(self.newVariant)
        self.depth.valueChanged.connect(self.newRoot)
        self._updateActiveOntology()
        
#     def initRelationBox(self):
#         m = self.relations.model()
#         for i in self.getIndexAbstractor().get_graph('instance').relations.keys():
#             m.appendRow(QStandardItem(i))
    
    def _updateActiveOntology(self):
        self.activeOntology.clear()
        self.activeOntology.addItems(
            [i.name for i in self.getIndexAbstractor().ontologies])

    def searchNode(self,search):
        try:
            node = self.nodesToQNodes[search]
            self.graphicsView.centerOn(node)
        except KeyError:
            pass # TODO: Mach hier einen Log
        
    def addRelation(self, qnode):
        if self.startRelation != None: # yeah a new relation
            logging.info("Add relation from " + self.startRelation.node + " to " + qnode.node )
            addstr = "\n(" + self.relations.currentText() + " " + self.startRelation.node + " " + qnode.node + ")\n"
            self.startRelation = None
            ontology = None
            for i in self.getIndexAbstractor().ontologies:
                if i.name == self.activeOntology.currentText():
                    ontology = i
                    
            assert ontology is not None
            print("here")
            x = self.getIndexAbstractor().get_ontology_file(ontology)
            x.write(addstr)
            self.SyntaxController.add_ontology(ontology, newversion=x.getvalue())
            print("here1")
            self.commit()
            print("here2")
            #TODO: please delete next line if commit is implemented
            self.newRoot()
            print("here3")
        else:
            logging.info("Starting node is " + qnode.node)
            self.startRelation = qnode
        
    @Slot(float)
    def changeScale(self, val):
        toScale = val / self.lastScale
        self.lastScale = val
        self.graphicsView.scale(toScale, toScale)

    @Slot()
    def renewplot(self):
        scene = self.graphicsView.scene()
        self.roots = set()
        # scene.changed.disconnect(self.renewplot)
        for i in self.qLines:
            scene.removeItem(i)

        self.qLines = []

        for edge in gv.edges_iter():

            qnode1 = self.nodesToQNodes[edge[0]]
            qnode2 = self.nodesToQNodes[edge[1]]
            line = QLineF(qnode1.pos(), qnode2.pos())
            line.setLength(line.length() - 40)
            end = line.p2()

            arrowLine1 = QLineF()
            arrowLine1.setP1(end)
            arrowLine1.setLength(10)
            arrowLine1.setAngle(line.angle() + 210)

            arrowLine2 = QLineF()
            arrowLine2.setP1(end)
            arrowLine2.setLength(10)
            arrowLine2.setAngle(line.angle() - 210)
            if edge.attr['color'] not in self.qpens:
                self.qpens[edge.attr['color']] = QPen(
                    QColor(edge.attr['color']))

            item = scene.addLine(line, self.qpens[edge.attr['color']])
            item.setZValue(-1)
            item.setFlag(QGraphicsItem.ItemIsSelectable,True)
            self.qLines.append(item)
            item = scene.addLine(arrowLine1, self.qpens[edge.attr['color']])
            self.qLines.append(item)
            item = scene.addLine(arrowLine2, self.qpens[edge.attr['color']])
            self.qLines.append(item)
            
            self.roots.add(edge[0])
        # scene.changed.connect(self.renewplot)

    def plot(self):
        """
        Creates a QGraphicScene for the layouted graph in self.gv
        This function has to be called every time, a node change happened.
        """
        scene = QGraphicsScene()
        self.graphicsView.setScene(scene)
        self.nodesToQNodes = {}
        self.qLines = []
        for node in self.gv.nodes_iter():
            (x, y) = node.attr['pos'].split(',')
            qnode = QtNode(-40, -40, 80, 80)
            qnode.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
            qnode.setPos(float(x) * 4, float(y) * 4)
            qnode.setFlag(QGraphicsItem.ItemIsMovable)
            qnode.setCallBackItemChange(self.renewplot)
            qnode.setCallBackAddRelation(self.addRelation)
            qnode.setNode(node)
            qnode.setBrush(QColor(255, 150, 150))
            txt = QGraphicsSimpleTextItem(qnode)
            txt.setPos(-35, -25)
            font = txt.font()
            font.setPointSize(14)
            txt.setFont(font)
            txt.setText(insert_newlines(node, 8))
            scene.addItem(qnode)

            self.nodesToQNodes[node] = qnode

        self.renewplot()

    def initMenu(self):
        self.graphicsView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.graphicsView.customContextMenuRequested.connect(self.showContextMenu)
    
    def showContextMenu(self, pos):
        """
        Shows a context menu to add a node in the graph widget
        """
        gpos = self.graphicsView.mapToGlobal(pos)
        menu = QMenu()
        actionAddNode = menu.addAction("Add Node") 
        QAction = menu.exec_(gpos)
        
        if (actionAddNode == QAction):
            (text,ok) = QInputDialog.getText(self.graphicsView, "Insert Node Name", "Please insert a name for the node")
            if ok:
                #User clicked on ok. Otherwise do nothing
                self.gv.add_node(text)
                node = self.gv.get_node(text)
                qnode = QtNode(-40, -40, 80, 80)
                qnode.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
                qnode.setPos(pos)
                qnode.setFlag(QGraphicsItem.ItemIsMovable)
                qnode.setCallBack(self.renewplot)
                qnode.setBrush(QColor(204, 255, 255))
                txt = QGraphicsSimpleTextItem(qnode)
                txt.setPos(-35, -25)
                font = txt.font()
                font.setPointSize(14)
                txt.setFont(font)
                txt.setText(insert_newlines(node, 8))
                self.graphicsView.scene().addItem(qnode)

            self.nodesToQNodes[node] = qnode
            self.searchNode(node)
    @Slot()
    def newRoot(self):
        root = self.rootSelector.currentText()
        variant = self.relations.currentText()
        if root == "---":
            root = None

        depth = None
        if self.depth.value() != -1:
            depth = self.depth.value()
        if variant == "---":
            variant = ''
        
        self.createGV(variant, root, depth)
        self.plot()
        
    def newVariant(self):
        self.rootSelector.currentIndexChanged[str].disconnect(self.newRoot)
        self.rootSelector.clear()
        self.rootSelector.insertItem(0, "---")
        self.newRoot()
        self.rootSelector.insertItems(1,list(self.roots))
        self.rootSelector.currentIndexChanged[str].connect(self.newRoot)
    
    def createGV(self,variant='instance',r=None,d=None):
        gv = pygraphviz.AGraph(strict=False)
        y = self.getIndexAbstractor().get_graph(variant,root=r, depth=d)
        colors = ["black", "red", "blue", "green", "darkorchid", "gold2",
                  "yellow", "turquoise", "sienna", "darkgreen"]
        for k in y.relations.keys():
            l = [(k, v) for v in y.relations[k]]
            gv.add_edges_from(l, color=random.choice(colors))
        gv.layout("sfdp")

        self.gv = gv
