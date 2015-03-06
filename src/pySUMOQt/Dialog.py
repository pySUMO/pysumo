from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox, QColorDialog
from PySide.QtGui import QColor, QFont, QMessageBox
from pySUMOQt.Designer.NewOntologyDialog import Ui_NewOntologyDialog
import os
from pysumo.syntaxcontroller import Ontology
from pySUMOQt.Designer.OpenRemoteOntologyDialog import Ui_OpenRemoteOntologyDialog
from pysumo import updater
from pySUMOQt.Designer.OptionDialog import Ui_Dialog
from functools import partial
from pySUMOQt.Designer import OntologyPropertyDialog


class NewOntologyDialog(QDialog, Ui_NewOntologyDialog):
    """ Dialog to create a new ontology. """

    def __init__(self, parent, defPath):
        """ 
        Initializes the new ontology dialog. 
        
        Parameter :
        
        - parent : The main window.
        - defPath : The default output path as a string.
        """
        super(NewOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = defPath
        self.ontologyPath.setText(self.defPath)
        self.browseFolderBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        """
        Chooses a path in from the QFileDialog.
        """
        path = self.ontologyPath.text()
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.ontologyPath.setText(path)

    def restoreDefaults(self):
        """
        Restore default values in fields.
        """
        self.ontologyPath.setText(self.defPath)

    def accept(self):
        """ 
        Commit the input and dispose the dialog.
        """
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
            ret = QMessageBox.warning(self, "The ontology file already exists.", "Do you want to override the existing ontology file?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ret == QMessageBox.Yes :
                with open(path, 'w') as f:
                    f.close()
            elif ret == QMessageBox.No :
                return
            else :
                raise RuntimeError
        ontology = Ontology(path, name=self.ontologyName.text())
        self.parent().addOntology(ontology)
        super(NewOntologyDialog, self).accept()

class OpenRemoteOntologyDialog(QDialog, Ui_OpenRemoteOntologyDialog):
    """ The dialog to open a remote ontology. """

    def __init__(self, parent, defPath):
        """ 
        Initializes the open remote ontology dialog.
        
        Parameter :
        
        - parent : The main window.
        - defPath : The default output path.
        """
        super(OpenRemoteOntologyDialog, self).__init__(parent)
        self.setupUi(self)
        self.defPath = defPath
        self.path.setText(self.defPath)
        self.browseBtn.clicked.connect(self.chooseOntologyPath)
        restoreDefsBtn = self.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        restoreDefsBtn.clicked.connect(self.restoreDefaults)

    def chooseOntologyPath(self):
        """
        Choose a path from the QFileDialog.
        """
        path = self.path.text()
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory', path)
        self.path.setText(path)

    def restoreDefaults(self):
        """
        Restore default values in fields.
        """
        self.path.setText(self.defPath)

    def accept(self):
        """
        Commit the input and dispose the dialog.
        """
        path = self.path.text()
        if not os.path.exists(path) :
            os.makedirs(path)
        path += "/"
        path += self.name.text()
        path += ".kif"
        path = os.path.normpath(path)

        # create the ontology file.
        try:
            with open(path, 'x') as f:
                f.close()
        except FileExistsError:
            ret = QMessageBox.warning(self, "The ontology file already exists.", "Do you want to override the existing ontology file?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if ret == QMessageBox.Yes :
                with open(path, 'w') as f:
                    f.close()
            elif ret == QMessageBox.No :
                return
            else :
                raise RuntimeError
        ontology = Ontology(path, name=self.name.text(), url=self.url.text())
        # download the ontology (user must save to store ontology on disk)
        updater.update(ontology, lambda x: self.parent().addOntology(ontology, newversion=x.getvalue().decode('utf8')))
        super(OpenRemoteOntologyDialog, self).accept()
        
class OntologyPropertyDialog(QDialog, OntologyPropertyDialog.Ui_Dialog):
    """
    The ontology property dialog.
    """
    
    def __init__(self, parent, ontology):
        """
        Initializes an ontology property dialog.
        
        Parameter :
        
        - parent : The main window.
        - ontology : The ontology.
        """
        
        super(OntologyPropertyDialog, self).__init__(parent)
        self.setupUi(self)
        self.ontologyName.setText(ontology.name)
        self.ontologyPath.setText(ontology.path)
        self.ontologyUrl.setText(ontology.url)
        self.ontologyLogPath.setText(ontology.action_log.log_io.path)
        
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
    """ Convert a string value of a boolean in boolean.
    
    Parameter : 
    
    - s : A boolean as String.
    """
    s = str(s)
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
        self.defaultFontFamily.currentFontChanged.connect(partial(self.onOptionChanged, self.defaultFontFamily))
        self.defaultFontSize.valueChanged.connect(partial(self.onOptionChanged, self.defaultFontSize))
        self.defaultFontColor.textChanged.connect(partial(self.onOptionChanged, self.defaultFontColor))
        self.defaultFontColorChooser.clicked.connect(partial(self.colorChooserClicked, self.defaultFontColor))
        self.useHighlightingFontSize.toggled.connect(partial(self.onOptionChanged, self.useHighlightingFontSize))
        button = self.buttonBox.button(QDialogButtonBox.Apply)
        button.clicked.connect(self.onApplyClicked)
        button = self.buttonBox.button(QDialogButtonBox.Reset)
        button.clicked.connect(self.onResetClicked)
        button = self.buttonBox.button(QDialogButtonBox.RestoreDefaults)
        button.clicked.connect(self.onRestoreDefaultsClicked)
        
    def initialize(self):
        """
        Fill the dialog fields with the value from the setting file.
        """
        self.loadTextSetting(self.configPath)
        self.loadIntSetting(self.maxQueueSize)
        self.loadIntSetting(self.maxUndoRedoQueueSize)
        self.loadIntSetting(self.flushWriteQueuesTimeout)
        self.loadTextSetting(self.logOutputPath)
        self.loadTextSetting(self.socketOutputPath)
        self.loadIntSetting(self.logLevel)
        self.loadIntSetting(self.maxTextEditorWidgets)
        self.loadIntSetting(self.defaultFontSize)
        self.loadComboBoxSetting(self.defaultFontFamily)
        self.loadColorSetting(self.defaultFontColor)
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
        self.loadBoolSetting(self.useHighlightingFontSize)
        
    def onApplyClicked(self):
        """
        QT Slot to handle the click on apply button.
        """
        self.save()
        
    def onResetClicked(self):
        """
        QT Slot to handle the click on reset button.
        """
        self.changes.clear()
        self.initialize()
        
    def onRestoreDefaultsClicked(self):
        """
        QT Slot to handle click on restore defaults button.
        """
        self.changes.clear()
        self.settings.loadDefaults()
        self.initialize()
    
    def loadBoolSetting(self, checkbox):
        """ 
        Load setting in the checkbox.
        
        Parameter :
        
        - checkbox : The QCheckBox where to load the setting with the object name as property key.
        """
        checkbox.setChecked(str_to_bool(self.settings.value(checkbox.objectName())))
    
    def loadComboBoxSetting(self, combobox):
        """
        Load setting in the combo box.
        
        Parameter :
        
        - combobox : The QComboBox where to load the setting with the object name as property key.
        """ 
        idx = combobox.findText(self.settings.value(combobox.objectName()))
        combobox.setCurrentIndex(idx)
        
    def loadColorSetting(self, textfield):
        """
        Load color setting in the text field.
        
        Parameter :
        
        - textfield : The QLineEdit where to load the setting with the object name as property key.
        """
        self.updateColorField(textfield, self.settings.value(textfield.objectName()))

    def loadIntSetting(self, spinbox):
        """
        Load integer setting in the spinbox.
        
        Parameter :
        
        - spinbox : The QSpinBox where to load the setting with the object name as property.
        """
        spinbox.setValue(int(self.settings.value(spinbox.objectName())))
        
    def loadTextSetting(self, textField):
        """
        Load text setting in the textfield.
        
        Parameter :
        
        - textfield : The QLineEdit where to load the setting with the object name as property.
        """
        textField.setText(self.settings.value(textField.objectName()))
        
    def colorChooserClicked(self, textfield):
        """
        QT Slot handles when a color chooser is clicked.
        
        Parameter :
        
        - textfield : The QLineEdit where to output the name of the choosen color.
        """
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
        """
        Update the color field by seting it's text color with the given color.
        
        Parameter :
        
        - textfield : The QLineEdit to output the choosen color.
        - color :  The color name.
        """
        stylesheet = "QLineEdit { color: ";
        stylesheet += color
        stylesheet += "}"
        textfield.setText(color)
        textfield.setStyleSheet(stylesheet)
        
    def directoryPathChooserClicked(self, textfield):
        """ 
        QT Slot handles when the directory chooser is clicked.
        
        Parameter : 
        
        - textfield : The QLineEdit where to output the choosen path.
        """
        path = textfield.text()
        path = QFileDialog.getExistingDirectory(self, "Select Folder", path)
        textfield.setText(path)
        
    def onOptionChanged(self, qItem, newValue):
        """
        QT Slot handles when an option field changed.
        
        Parameter :
        
        - qItem : The QWidget which changed, which the object name as property key.
        - newValue : The new value of the changed option.
        """
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
        
    def accept(self, *args, **kwargs):
        """
        Commit changes and disposes the dialog.
        """
        # Save the options.
        self.save()
        return QDialog.accept(self, *args, **kwargs)
        
    def setSelectedPage(self, pageIndex):
        """
        QT Slot handles when a page is selected.
        
        Parameter :
        
        - pageIndex : The index of the page selected.
        """
        self.listWidget.setCurrentRow(pageIndex)
        
    def changePage(self, current, previous):
        """
        QT Slot handles when a page is selected.
        
        Parameter :
        
        - current : The index of the page selected.
        - previous : The index of the old selected page.
        """
        if not current is None :
            self.stackedWidget.setCurrentIndex(self.listWidget.row(current))

    def save(self):
        """ Saves the settings to the given path.

        Arguments:

        - path: The path to which the settings will be written.

        Raises:

        - IOError

        """
        for key in self.changes.keys() :
            self.settings.setValue(key, self.changes.get(key))
        self.changes.clear()
