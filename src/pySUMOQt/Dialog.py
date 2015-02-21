from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox, QColorDialog
from PySide.QtGui import QColor, QFont
from pySUMOQt.Designer.NewOntologyDialog import Ui_NewOntologyDialog
import os
from pysumo.syntaxcontroller import Ontology
from pySUMOQt.Designer.OpenRemoteOntologyDialog import Ui_OpenRemoteOntologyDialog
from pysumo import updater
from pySUMOQt.Designer.OptionDialog import Ui_Dialog
from functools import partial


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
    
def str_to_bool(s):
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError

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

    def __init__(self, parent, settings):
        """ Initializes the OptionDialog. """
        super(OptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.settings = settings
        self.changes = dict()
        self.initialize()
        self.configPath.textChanged.connect(partial(self.onOptionChanged, self.configPath))
        self.configPathChooser.clicked.connect(partial(self.directoryPathChooserClicked, self.configPath))
        self.maxQueueSize.valueChanged.connect(partial(self.onOptionChanged, self.maxQueueSize))
        self.maxUndoRedoQueueSize.valueChanged.connect(partial(self.onOptionChanged, self.maxUndoRedoQueueSize))
        self.flushWriteQueuesTimeout.valueChanged.connect(partial(self.onOptionChanged, self.flushWriteQueuesTimeout))
        self.logOutputPath.textChanged.connect(partial(self.onOptionChanged, self.logOutputPath))
        self.socketOutputPath.textChanged.connect(partial(self.onOptionChanged, self.socketOutputPath))
        self.logLevel.valueChanged.connect(partial(self.onOptionChanged, self.logLevel))
        self.keywordsFontFamily.currentFontChanged.connect(partial(self.onOptionChanged, self.keywordsFontFamily))
        self.keywordsFontSize.valueChanged.connect(partial(self.onOptionChanged, self.keywordsFontSize))
        self.keywordsFontColor.textChanged.connect(partial(self.onOptionChanged, self.keywordsFontColor))
        self.keywordsFontColorChooser.clicked.connect(partial(self.colorChooserClicked, self.keywordsFontColor))
        self.keywordsBoldStyle.toggled.connect(partial(self.onOptionChanged, self.keywordsBoldStyle))
        self.keywordsItalicStyle.toggled.connect(partial(self.onOptionChanged, self.keywordsItalicStyle))
        self.keywordsUnderlinedStyle.toggled.connect(partial(self.onOptionChanged, self.keywordsUnderlinedStyle))
        self.logicExprFontFamily.currentFontChanged.connect(partial(self.onOptionChanged, self.logicExprFontFamily))
        self.logicExprFontSize.valueChanged.connect(partial(self.onOptionChanged, self.logicExprFontSize))
        self.logicExprFontColor.textChanged.connect(partial(self.onOptionChanged, self.logicExprFontColor))
        self.logicExprFontColorChooser.clicked.connect(partial(self.colorChooserClicked, self.logicExprFontColor))
        self.logicExprBoldStyle.toggled.connect(partial(self.onOptionChanged, self.logicExprBoldStyle))
        self.logicExprItalicStyle.toggled.connect(partial(self.onOptionChanged, self.logicExprItalicStyle))
        self.logicExprUnderlinedStyle.toggled.connect(partial(self.onOptionChanged, self.logicExprUnderlinedStyle))
        self.commentFontFamily.currentFontChanged.connect(partial(self.onOptionChanged, self.commentFontFamily))
        self.commentFontSize.valueChanged.connect(partial(self.onOptionChanged, self.commentFontSize))
        self.commentFontColor.textChanged.connect(partial(self.onOptionChanged, self.commentFontColor))
        self.commentFontColorChooser.clicked.connect(partial(self.colorChooserClicked, self.commentFontColor))
        self.commentBoldStyle.toggled.connect(partial(self.onOptionChanged, self.commentBoldStyle))
        self.commentItalicStyle.toggled.connect(partial(self.onOptionChanged, self.commentItalicStyle))
        self.commentUnderlinedStyle.toggled.connect(partial(self.onOptionChanged, self.commentUnderlinedStyle))
        self.stringsFontFamily.currentFontChanged.connect(partial(self.onOptionChanged, self.stringsFontFamily))
        self.stringsFontSize.valueChanged.connect(partial(self.onOptionChanged, self.stringsFontSize))
        self.stringsFontColor.textChanged.connect(partial(self.onOptionChanged, self.stringsFontColor))
        self.stringsFontColorChooser.clicked.connect(partial(self.colorChooserClicked, self.stringsFontColor))
        self.stringsBoldStyle.toggled.connect(partial(self.onOptionChanged, self.stringsBoldStyle))
        self.stringsItalicStyle.toggled.connect(partial(self.onOptionChanged, self.stringsItalicStyle))
        self.stringsUnderlinedStyle.toggled.connect(partial(self.onOptionChanged, self.stringsUnderlinedStyle))
        self.maxTextEditorWidgets.valueChanged.connect(partial(self.onOptionChanged, self.maxTextEditorWidgets))
        self.maxDocumentationWidgets.valueChanged.connect(partial(self.onOptionChanged, self.maxDocumentationWidgets))
        self.maxHierarchyWidgets.valueChanged.connect(partial(self.onOptionChanged, self.maxHierarchyWidgets))
        self.maxGraphWidgets.valueChanged.connect(partial(self.onOptionChanged, self.maxGraphWidgets))
        
    def initialize(self):
        self.loadTextSetting(self.configPath)
        self.loadIntSetting(self.maxQueueSize)
        self.loadIntSetting(self.maxUndoRedoQueueSize)
        self.loadIntSetting(self.flushWriteQueuesTimeout)
        self.loadTextSetting(self.logOutputPath)
        self.loadTextSetting(self.socketOutputPath)
        self.loadIntSetting(self.logLevel)
        self.loadIntSetting(self.maxTextEditorWidgets)
        self.loadComboBoxSetting(self.keywordsFontFamily)
        self.loadIntSetting(self.keywordsFontSize)
        self.loadColorSetting(self.keywordsFontColor)
        self.loadBoolSetting(self.keywordsBoldStyle)
        self.loadBoolSetting(self.keywordsItalicStyle)
        self.loadBoolSetting(self.keywordsUnderlinedStyle)
        self.loadComboBoxSetting(self.logicExprFontFamily)
        self.loadIntSetting(self.logicExprFontSize)
        self.loadColorSetting(self.logicExprFontColor)
        self.loadBoolSetting(self.logicExprBoldStyle)
        self.loadBoolSetting(self.logicExprItalicStyle)
        self.loadBoolSetting(self.logicExprUnderlinedStyle)
        self.loadComboBoxSetting(self.commentFontFamily)
        self.loadIntSetting(self.commentFontSize)
        self.loadColorSetting(self.commentFontColor)
        self.loadBoolSetting(self.commentBoldStyle)
        self.loadBoolSetting(self.commentItalicStyle)
        self.loadBoolSetting(self.commentUnderlinedStyle)
        self.loadComboBoxSetting(self.stringsFontFamily)
        self.loadIntSetting(self.stringsFontSize)
        self.loadColorSetting(self.stringsFontColor)
        self.loadBoolSetting(self.stringsBoldStyle)
        self.loadBoolSetting(self.stringsItalicStyle)
        self.loadBoolSetting(self.stringsUnderlinedStyle)
        self.loadIntSetting(self.maxDocumentationWidgets)
        self.loadIntSetting(self.maxHierarchyWidgets)
        self.loadIntSetting(self.maxGraphWidgets)
        
    def actiontriggered(self, action):
        pass
    
    def loadBoolSetting(self, checkbox):
        checkbox.setChecked(str_to_bool(self.settings.value(checkbox.objectName())))
    
    def loadComboBoxSetting(self, combobox):
        idx = combobox.findText(self.settings.value(combobox.objectName()))
        combobox.setCurrentIndex(idx)
        
    def loadColorSetting(self, textfield):
        self.updateColorField(textfield, self.settings.value(textfield.objectName()))

    def loadIntSetting(self, spinbox):
        spinbox.setValue(int(self.settings.value(spinbox.objectName())))
        
    def loadTextSetting(self, textField):
        textField.setText(self.settings.value(textField.objectName()))
        
    def colorChooserClicked(self, textfield):
        color = textfield.text()
        colorChooser = QColorDialog(self)
        if color :
            colorChooser.setCurrentColor(QColor(color))
        if colorChooser.exec_() :
            ret = colorChooser.currentColor()
            if ret is not None and ret.isValid() :
                color = ret.name()
        self.updateColorField(textfield, color)
        
    def updateColorField(self, textfield, color):
        stylesheet = "QLineEdit { color: ";
        stylesheet += color
        stylesheet += "}"
        textfield.setText(color)
        textfield.setStyleSheet(stylesheet)
        
    def directoryPathChooserClicked(self, textfield):
        path = textfield.text()
        path = QFileDialog.getExistingDirectory(self, "Select Folder", path)
        textfield.setText(path)
        
    def onOptionChanged(self, qItem, newValue):
        optionName = qItem.objectName()
        if type(newValue) is QFont :
            newValue = newValue.family()
        oldValue = None
        try :
            oldValue = self.changes.pop(optionName)
        except KeyError :
            pass
        if newValue == oldValue :
            return
        self.changes[optionName] = newValue
        print(self.changes)
        
    def accept(self, *args, **kwargs):
        # Save the options.
        for key in self.changes.keys() :
            self.settings.setValue(key, self.changes.get(key))
        self.changes.clear()
        return QDialog.accept(self, *args, **kwargs)
        
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
        """ Reads the settings from the given path.

        Arguments:

        - path: The path from which the settings will be read.

        Raises:

        - IOError

        """
        pass
