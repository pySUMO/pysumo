""" HierarchyWidget modul from pySUMO
"""

from PySide.QtCore import Slot, SIGNAL, Qt
from PySide.QtGui import QApplication, QMainWindow, QFileSystemModel
import os
import sys

from pySUMOQt.Designer.HierarchyWidget import Ui_Form
from .Widget import RWWidget


class CheckableDirModel(QFileSystemModel):

    def __init__(self, parent=None):
        QFileSystemModel.__init__(self, None)
        self.checks = {}

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.CheckStateRole:
            return QFileSystemModel.data(self, index, role)
        else:
            if index.column() == 0:
                return self.checkState(index)

    def flags(self, index):
        return QFileSystemModel.flags(self, index) | Qt.ItemIsUserCheckable

    def checkState(self, index):
        if index in self.checks:
            return self.checks[index]
        else:
            return Qt.Unchecked

    def setData(self, index, value, role):
        if (role == Qt.CheckStateRole and index.column() == 0):
            self.checks[index] = value
            self.emit(
                SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
            return True

        return QFileSystemModel.setData(self, index, value, role)


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

        self.model = CheckableDirModel()
        self.treeView.setModel(self.model)
        # self.treeView.setRootIndex(os.getcwd())
        # self.treeView.setRootIndex(self.model.index(os.getcwd()))
        self.model.index(os.getcwd())
        # self.treeView.setRootIndex(self.model.index(os.getcwd()))

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
