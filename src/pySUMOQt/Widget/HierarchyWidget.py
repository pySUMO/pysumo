""" HierarchyWidget modul from pySUMO
"""

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QMainWindow, QTreeWidgetItem, QAbstractItemView
from PySide.QtGui import QStringListModel
import sys

from pySUMOQt.Designer.HierarchyWidget import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget


class OntologyHierarchyNode(QTreeWidgetItem):

    def __init__(self, data=None):
        super(OntologyHierarchyNode, self).__init__()
        if data is not None :
            self.setText(0, data)
        self.dataObj = data
        
    def __str__(self, *args, **kwargs):
        return self.dataObj
        
def buildRootNode(relations, treeview):
    """ Build the Qtreeitem from the abstract graph and it's children."""
    items = []
    createdNodes = []
    for i in relations.keys() :
        node = None
        foundNode = False
        for k in createdNodes :
            if k.dataObj == i :
                node = k
                foundNode = True
                break
        if node is None :
            node = OntologyHierarchyNode(data=i)
            createdNodes.append(node)
        for j in relations[i] :
            subNode = None
            for k in createdNodes :
                if k.dataObj == j :
                    subNode = k
                    break
            if subNode is None :
                subNode = OntologyHierarchyNode(data=j)
                createdNodes.append(subNode)
            node.addChild(subNode)
        if not foundNode :
            items.append(node)
    treeview.addTopLevelItems(items)
    return createdNodes
        
class HierarchyWidget(RWWidget, Ui_Form):

    """ The hierarchy widget displays the ontology in a tree form conformly to
    the SUMO hierarchy model. The user can edit the ontology from this widget.
    It can show and hide nodes in it's display.

    Methods:

    - hide: hides the node's content that the user selected in the widget view.
    - show: shows the node's content that the user selected in the widget view.

    """

    def __init__(self, mainwindow):
        """ Initializes the hierarchy widget. """
        super(HierarchyWidget, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.relationSelector.setCurrentIndex(-1)
        self.relationSelector.currentIndexChanged.connect(self.refresh)
        self.rootSelector.setCurrentIndex(-1)
        self.rootSelector.currentIndexChanged[int].connect(self._relationChanged_)
        self.createdNodes = None
        
    def refresh(self):
        RWWidget.refresh(self)
        idx = self.relationSelector.currentIndex()
        self.treeWidget.clear()
        variant = None
        if idx != -1 :
            variant = self.relationSelector.currentText()
        if variant is None :
            return
        abstractGraph = self.IA.get_graph([(0, variant)])
        if abstractGraph is None or len(abstractGraph.relations) == 0:
            return
        createdNodes = buildRootNode(abstractGraph.relations, treeview=self.treeWidget)
        self.rootSelector.clear()
        model = QStringListModel()
        nodeList = list()
        for i in createdNodes :
            nodeList.append(i.text(0))
        nodeList.sort()
        model.setStringList(nodeList)
        self.createdNodes = createdNodes
        self.rootSelector.setModel(model)
        self.rootSelector.setCurrentIndex(-1)
        
    def findNodeByText(self, val):
        if not self.createdNodes is None :
            for i in self.createdNodes :
                if i.text(0) == val :
                    return i
        return None
        
    def _relationChanged_(self, val):
        self.treeWidget.clearSelection()
        if val == -1 :
            self.treeWidget.collapseAll()
            return
        else :
            textVal = self.rootSelector.itemText(val)
            node = self.findNodeByText(textVal)
            if node is not None :
                idx = self.treeWidget.indexFromItem(node, 0)
                node = self.treeWidget.itemFromIndex(idx)
                self.treeWidget.setItemExpanded(node, True)
                self.treeWidget.setItemSelected(node, True)
                self.treeWidget.scrollToItem(node, QAbstractItemView.PositionAtCenter)
                self.rootSelector.clearFocus()
                self.treeWidget.setFocus()

    def _expandAll_(self):
        self.treeWidget.expandAll()

    def _collapseAll_(self):
        self.treeWidget.collapseAll()

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

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = HierarchyWidget(mainwindow)
    mainwindow.show()
    sys.exit(application.exec_())
