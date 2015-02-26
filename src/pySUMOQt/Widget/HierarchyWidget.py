""" HierarchyWidget modul from pySUMO
"""

from PySide.QtCore import Qt
from PySide.QtGui import QApplication, QMainWindow, QTreeWidgetItem, QAbstractItemView
import sys

from pySUMOQt.Designer.HierarchyWidget import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget


class OntologyHierarchyNode(QTreeWidgetItem):

    def __init__(self, data=None):
        super(OntologyHierarchyNode, self).__init__()
        if data is not None :
            self.setText(0, data)
        self.dataObj = data
        
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
                createdNodes.append(node)
            node.addChild(subNode)
        if not foundNode :
            items.append(node)
    treeview.addTopLevelItems(items)
        
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
        self.refresh()
        self.relationSelector.setCurrentIndex(-1)
        self.relationSelector.currentIndexChanged[int].connect(self._selectionChanged_)
#         node = QTreeWidgetItem()
#         node.setText(0, "Ontology")
#         self.treeWidget.addTopLevelItem(node)
        
    def refresh(self):
        RWWidget.refresh(self)
        abstractGraph= self.IA.get_graph([(0, "instance")])
        if abstractGraph is None or len(abstractGraph.relations) == 0:
            return
        self.treeWidget.clear()
        buildRootNode(abstractGraph.relations, treeview=self.treeWidget)
        self.relationSelector.setModel(self.treeWidget.model())
        
    def _selectionChanged_(self, val):
        self.treeWidget.clearSelection()
        if val == -1 :
            return
        else :
            textVal = self.relationSelector.itemText(val)
            objs = self.treeWidget.findItems(textVal, Qt.MatchCaseSensitive)
            if objs is not None and len(objs) == 1 :
                node = objs[0]
                self.treeWidget.setItemExpanded(node, True)
                self.treeWidget.setItemSelected(node, True)
                self.treeWidget.scrollToItem(node, QAbstractItemView.PositionAtCenter)
                self.relationSelector.clearFocus()
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
