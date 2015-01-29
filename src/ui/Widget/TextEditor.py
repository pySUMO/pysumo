""" The text editor module for pySUMO. The TextEditor widget is the main pySUMO
widget. It contains the textual representation of the currently loaded
Ontologies allowing conventional kif editing with features such as syntax
highlighting and autocompletion.
"""
import sys
from PySide.QtGui import QApplication, QMainWindow
from PySide.QtGui import QTextCharFormat
from PySide.QtGui import QFont
from PySide.QtCore import Qt, QRegExp

from ui.Widget.Widget import RWWidget as RWWidget
from ui.Designer.TextEditor import Ui_Form as Ui_Form
class TextEditor(RWWidget, Ui_Form):
    """ Contains many features of popular text editors adapted for use with
    Ontologies such as syntax highlighting, and autocompletion. One column on
    the left of the text editor contains line numbers and another contains
    other contextual information such as whether a block of code has been
    hidden/collapsed and can be displayed/expanded later.  It also contains an
    incremental search and an interface to pySUMO's settings so font size and
    family can be changed at will.

    Variables:

    - syntax_highlighter: The syntax highlighter object for the text editor.

    Methods:

    - commit: Notifies other Widgets of changes.
    - show_autocomplete: Returns autocompletion choices.

    """

    def __init__(self,mainwindow):
        """ Initializes the text editor widget. """
        super(TextEditor, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.plainTextEdit.show()

    def commit(self):
        """ Overrides commit from RWWidget. """

    def show_autocomplete(self, string):
        """ Returns a list of possible words which can be created from string.
        When the user triggers autocompletion, the text editor uses the
        IndexAbstractor to process the terms which can complete the given
        string. string has to be greater than or equal to 3 characters. """

if __name__ == "__main__":
    application = QApplication(sys.argv)
    mainwindow = QMainWindow()
    x = TextEditor(mainwindow)
    mainwindow.show()
    sys.exit(application.exec_())
    #x.
    
