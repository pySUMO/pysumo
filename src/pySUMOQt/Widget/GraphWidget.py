""" Displays a graph-based representation of the Ontology and allows the
Ontology to be modified graphically.

This module contains:

GraphWidget: Displays and allows modification of a graph of the Ontology.

"""

from PySide.QtCore import QLineF, Slot, Qt
from PySide.QtGui import QColor, QPen, QMenu, QInputDialog, QMessageBox, QCompleter
from PySide.QtGui import QGraphicsEllipseItem, QGraphicsSimpleTextItem, QGraphicsScene, QGraphicsItem
from PySide.QtGui import QPrintPreviewDialog, QPainter
import pygraphviz
import random
import logging


from pySUMOQt.Designer.GraphWidget import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget
import weakref
from pysumo.syntaxcontroller import Ontology

def insert_newlines(string, every=64):
    """ Insert a newline after ’every‘ characters
    
        Arguments:
        
            - every : The amount of characters before a newline is inserted 
            
    """
    return '\n'.join(string[i:i + every] for i in range(0, len(string), every))


class QtNode(QGraphicsEllipseItem):
    """ A Node representation in Qt"""
    callback = None
    def setCallback(self, f):
        """ Sets a callback function to call after the position has changed"""
        self.callback = f
    
    def setNode(self, node):
        """ Save the graphviz node"""
        self.node = node
        
    def itemChange(self, itemChange, val):
        """ Override Qt
        
        Renew the arrows
        """
        if (itemChange == QGraphicsItem.ItemPositionHasChanged):
            if self.callback is not None:
                self.callback().renewplot()
        return super().itemChange(itemChange, val)
    
    def mouseDoubleClickEvent(self, event):
        """ Override Qt
        
        Add a relation or save start relation point when double clicking
        """
        if self.callback is not None:
            self.callback().addRelation(self)
        
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
        self.gv = pygraphviz.AGraph(strict = False)
        self.widget = self.layoutWidget
        self.log = logging.getLogger('.' + __name__)
        self.nodesToQNodes = {}
        self.qLines = []
        self.qpens = {}
        self.completer = QCompleter(list(""))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWidget(self.lineEdit)

        self.lastScale = 1
        self.initMenu()
        self.roots = set()
        self.doubleSpinBox.valueChanged[float].connect(self.changeScale)
        self.lineEdit.textChanged.connect(self.searchNode)
        self.rootSelector.insertItem(0, "---")
        self.rootSelector.currentIndexChanged[str].connect(self.newRoot)
        self.relations.currentIndexChanged[str].connect(self.newVariant)
        self.depth.valueChanged.connect(self.newRoot)
        self._updateActiveOntology()
        self.graphicsView.setScene(QGraphicsScene())
#     def initRelationBox(self):
#         m = self.relations.model()
#         for i in self.getIndexAbstractor().get_graph('instance').relations.keys():
#             m.appendRow(QStandardItem(i))
    
    def refresh(self):
        """ Override Widget
        Updates the GraphWidget regarding to latest indexabstractor changes
        """
        self.newVariant()
        super(GraphWidget, self).refresh()

        
    def _redo_(self):
        self.log.info("redoing from graph widget")
        idx = self.activeOntology.currentIndex()
        ontology = self.activeOntology.itemData(idx)
        if not ontology is None and type(ontology) == Ontology :
            action_log = ontology.action_log
            action_log.redo()
            self.commit()
            
    def _undo_(self):
        self.log.info("undoing from graph widget")
        idx = self.activeOntology.currentIndex()
        ontology = self.activeOntology.itemData(idx)
        if not ontology is None and type(ontology) == Ontology :
            action_log = ontology.action_log
            action_log.undo()
            self.commit()

    def getActiveOntology(self):
        idx = self.activeOntology.currentIndex()
        return self.activeOntology.itemData(idx)
    
    def _updateActiveOntology(self):
        currentText = self.activeOntology.currentText()
        self.activeOntology.clear()
        idx = -1
        count = 0
        for i in self.getIndexAbstractor().ontologies :
            if currentText == i.name :
                idx = count
            self.activeOntology.addItem(i.name, i)
            count = count + 1
        self.activeOntology.setCurrentIndex(idx)

    def searchNode(self, search):
        """Search the node and focus the GraphicView to the node """
        try:
            #self.completer.setCompletionPrefix(search)
            #self.completer.complete()
            node = self.nodesToQNodes[search]
            self.graphicsView.centerOn(node)
        except KeyError:
            pass # TODO: Mach hier einen Log
        
    def addRelation(self, qnode):
        """ Adds a relation or save a starting point
        
        """
        if self.startRelation != None: # yeah a new relation
            self.log.info("Add relation from " + self.startRelation.node + " to " + qnode.node )
            if self.relations.currentText() == "---":
                msg = QMessageBox()
                msg.setText("Please choose a valid variant.")
                msg.exec_()
                return
            addstr = "\n(" + self.relations.currentText() + " " + self.startRelation.node + " " + qnode.node + ")\n"
            self.startRelation = None
            ontology = None
            for i in self.getIndexAbstractor().ontologies:
                if i.name == self.activeOntology.currentText():
                    ontology = i
                    
            if ontology is None:
                msg = QMessageBox()
                msg.setText("Please choose a valid Ontology to write to.")
                msg.exec_()
                return
            
            x = self.getIndexAbstractor().get_ontology_file(ontology)
            x.seek(0, 2)
            x.write(addstr)
            self.SyntaxController.add_ontology(ontology, newversion=x.getvalue())
            self.commit()
        else:
            self.log.info("Starting node is " + qnode.node)
            self.startRelation = qnode

    def _printPreview_(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.print_)
        dialog.exec_()
        
    def print_(self, printer):
        painter = QPainter(printer)
        painter.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.render(painter)
        
    def _zoomIn_(self):
        val = self.doubleSpinBox.value() + 0.10
        self.doubleSpinBox.setValue(val)
        
    def _zoomOut_(self):
        val = self.doubleSpinBox.value() - 0.10
        self.doubleSpinBox.setValue(val)
        
    @Slot(float)
    def changeScale(self, val):
        """ Scale the GraphicView to val
        
        Arguments:
        
            - val: The value to scale to. In Designer: 0.01 <= val <= 5
        
        """
        toScale = val / self.lastScale
        self.lastScale = val
        self.graphicsView.scale(toScale, toScale)

    @Slot()
    def renewplot(self):
        """ Do not layout anything, but redraw all lines"""
        scene = self.graphicsView.scene()
        self.roots = set()
        # scene.changed.disconnect(self.renewplot)
        for i in self.qLines:
            scene.removeItem(i)

        self.qLines = []

        for edge in self.gv.edges_iter():

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
            item.setFlag(QGraphicsItem.ItemIsSelectable, True)
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
        #scene = QGraphicsScene()
        #self.graphicsView.setScene(scene)
        scene = self.graphicsView.scene()
        scene.clear()
        self.nodesToQNodes = {}
        self.qLines = []
        for node in self.gv.nodes_iter():
            (x, y) = node.attr['pos'].split(',')
            qnode = self.createQtNode(node, float(x) * 4, float(y) * 4)
            scene.addItem(qnode)

            self.nodesToQNodes[node] = qnode
            
        
        
        self.completer = QCompleter(list(self.nodesToQNodes.keys()))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWidget(self.lineEdit)
        self.lineEdit.setCompleter(self.completer)
        self.renewplot()

    def createQtNode(self, node, posx, posy, color = QColor(255,150,150)):
        """ Create a QtNode with given position, color for given node
        
        Arguments:
            
            - node: The graphviz node
            - posx: The x position from graphviz layout
            - posy: The y position from graphviz layout
            - color: The color of circle (red by default)
        
        """
        qnode = QtNode(-40, -40, 80, 80)
        qnode.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        qnode.setPos(posx, posy)
        qnode.setFlag(QGraphicsItem.ItemIsMovable)
        qnode.setCallback(weakref.ref(self))
        qnode.setNode(node)
        qnode.setBrush(color)
        txt = QGraphicsSimpleTextItem(qnode)
        txt.setPos(-35, -25)
        font = txt.font()
        font.setPointSize(14)
        txt.setFont(font)
        txt.setText(insert_newlines(node, 8))
        
        return qnode

    def initMenu(self):
        """
        Configure the Widget to provide a handmade CustomContextMenu 
        """
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
            (text, ok) = QInputDialog.getText(self.graphicsView, "Insert Node Name", "Please insert a name for the node")
            if ok:
                if text not in self.nodesToQNodes:
                    #User clicked on ok. Otherwise do nothing
                    self.gv.add_node(text)
                    node = self.gv.get_node(text)
                    qnode = self.createQtNode(node, 0, 0, QColor(204, 255, 255))

                    self.graphicsView.scene().addItem(qnode)
                    qnode.setPos(self.graphicsView.mapToScene(gpos))
                    qnode.setPos(qnode.x(), qnode.y() - 200)
                    self.nodesToQNodes[node] = qnode
                else:
                    msg = QMessageBox()
                    msg.setText("The node already exists.")
                    msg.exec_()
                self.searchNode(text)
    @Slot()
    def newRoot(self):
        """ Change to new root set in the widget and redraw"""
        root = self.rootSelector.currentText()
        variant = [(0, self.relations.currentText())]
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
        """ Change to new variant set in the widget and redraw"""
        self.rootSelector.currentIndexChanged[str].disconnect(self.newRoot)
        self.rootSelector.clear()
        self.rootSelector.insertItem(0, "---")
        self.newRoot()
        self.rootSelector.insertItems(1, list(self.roots))
        self.rootSelector.currentIndexChanged[str].connect(self.newRoot)
    
    def createGV(self, variant='instance', r=None, d=None):
        """ Create a pygraphviz graph from pysumo abstract graph and layout it.
        
        Arguments: 
            
            - variant: The variant to use (e.g. instance)
            - r: The root
            - d: The depth (none for infinite depth
        
        """
        gv = pygraphviz.AGraph(strict=False)
        y = self.getIndexAbstractor().get_graph(variant, root=r, depth=d)
        colors = ["black", "red", "blue", "green", "darkorchid", "gold2",
                  "yellow", "turquoise", "sienna", "darkgreen"]
        for k in y.relations.keys():
            l = [(k, v) for v in y.relations[k]]
            gv.add_edges_from(l, color=random.choice(colors))
        gv.layout("sfdp")

        self.gv = gv
