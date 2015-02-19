from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox
from pySUMOQt.Designer.NewOntologyDialog import Ui_NewOntologyDialog
import os
from pysumo.syntaxcontroller import Ontology
from pySUMOQt.Designer.OpenRemoteOntologyDialog import Ui_OpenRemoteOntologyDialog
from pysumo import updater
from pySUMOQt.Designer.OptionDialog import Ui_Dialog


class NewOntologyDialog(QDialog, Ui_NewOntologyDialog):

    def __init__(self, parent):
        super(NewOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = '/'.join([os.environ['HOME'], '.pysumo'])
        self.ontologyPath.setText(self.defPath)
        self.browseFolderBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        path = self.ontologyPath.text()
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.ontologyPath.setText(path)

    def restoreDefaults(self):
        self.ontologyPath.setText(self.defPath)

    def accept(self):
        path = self.ontologyPath.text()
        if not os.path.exists(path):
            os.makedirs(path)
        path = ''.join([path, '/', self.ontologyName.text(), '.kif'])
        path = os.path.normpath(path)

        # create the ontology file.
        try:
            with open(path, 'x') as f:
                f.close()
        except FileExistsError:
            pass

        ontology = Ontology(path, self.ontologyName.text())
        self.parent().addOntology(ontology)
        super(NewOntologyDialog, self).accept()

class OpenRemoteOntologyDialog(QDialog, Ui_OpenRemoteOntologyDialog):

    def __init__(self, parent):
        super(OpenRemoteOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = '/'.join([os.environ['HOME'], '.pysumo'])
        self.path.setText(self.defPath)
        self.browseBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        path = self.path.text()
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.path.setText(path)

    def restoreDefaults(self):
        self.path.setText(self.defPath)

    def accept(self):
        path = self.path.text()
        if not os.path.exists(path) :
            os.makedirs(path)
        path += "/"
        path += self.name.text()
        path += ".kif"
        path = os.path.normpath(path)

        # create the ontology file.
        ontology = Ontology(path, self.name.text(), self.url.text())
        with open(path, 'wb+') as f:
            # download the ontology and fill the file,
            updater.update(ontology)
            f.close()

        self.parent().addOntology(ontology)
        super(OpenRemoteOntologyDialog, self).accept()
        
class HelpDialog(QDialog):

    """ The help dialog for the pySUMO main window. It contains information
    about Ontologies, SUMO and pySUMO such as the pySUMO API reference and the
    homepage for SUMO.  It can display both locally stored documentation as
    well as documentation retrieved from the internet.  An about box displays
    general information about pySUMO's authors and the license. """

    def __init__(self):
        """ Initializes the help dialog. """
        pass

    def initView(self):
        """ Initializes the view of the help dialog. """
        pass

class OptionDialog(QDialog, Ui_Dialog):
    """ The option dialog is the displays and allows modification of settings
    for pySUMO. It displays options for the GUI, Widgets and library. The
    settings are organized by type and owner for ease of use. It also
    contains a plugin manager which enables loading and unloading of
    plugins.  The class also provides settings persistence by writing
    storing them in a file and reading from it on init.

    Attributes:

    - options: The options dictionary to manage in the option's dialog.

    Methods:

    - createView: Creates the view of the options dialog.
    - save: Saves the options.
    - load: Loads the options.

    """

    def __init__(self, parent):
        """ Initializes the OptionDialog. """
        super(OptionDialog, self).__init__(parent)
        self.setupUi(self)
        
    def setSelectedPage(self, pageIndex):
        self.listWidget.setCurrentRow(pageIndex)
        
    def changePage(self, current, previous):
        if not current is None :
            self.stackedWidget.setCurrentIndex(self.listWidget.row(current))

    def createView(self):
        """ Initializes the view of the OptionDialog. """
        pass

    def save(self, path):
        """ Saves the settings to the given path.

        Arguments:

        - path: The path to which the settings will be written.

        Raises:

        - IOError

        """
        pass

    def load(self, path):
        """ Reads the settingns from the given path.

        Arguments:

        - path: The path from which the settings will be read.

        Raises:

        - IOError

        """
        pass
