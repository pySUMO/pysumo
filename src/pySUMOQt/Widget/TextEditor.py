""" The text editor module for pySUMO. The TextEditor widget is the main pySUMO
widget. It contains the textual representation of the currently loaded
Ontologies allowing conventional kif editing with features such as syntax
highlighting and autocompletion.
"""
from PySide.QtCore import Qt, QRegExp, QObject, SIGNAL, Slot, QRect, QPoint, QSize, QTimer
from PySide.QtGui import QApplication, QMainWindow, QCompleter, QTextCursor, QWidget, QPainter
from PySide.QtGui import QFont, QSyntaxHighlighter, QShortcut, QKeySequence, QPrintDialog, QColor
from PySide.QtGui import QTextCharFormat, QDialog, QPrinter, QPrinterInfo, QPrintPreviewDialog
from collections import OrderedDict
import re
import string
import sys

from pySUMOQt.Designer.TextEditor import Ui_Form
from pySUMOQt.Widget.Widget import RWWidget
import pysumo.parser as parser
from pysumo.syntaxcontroller import Ontology
from pySUMOQt.Dialog import str_to_bool
import logging


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
    
    - __init__: Initalizes the Object and the QPlainTextEdit
    - commit: Notifies other Widgets of changes.
    - show_autocomplete: Returns autocompletion choices.
    - getWidget: returns the QPlainTextEdit
    - numberbarPaint: Paints the numberbar
    - searchCompletion: Asks QCompleter if a whole word exists starting with user input
    - hideFrom: Starts hides all lines from the ()-block started by line
    - insertCompletion: Puts the selected Completion into the TextEditor
    """

    def __init__(self, mainwindow, settings=None):
        """ Initializes the text editor widget. """
        super(TextEditor, self).__init__(mainwindow)
        self.setupUi(self.mw)
        self.plainTextEdit.clear()
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.show()
        self.highlighter = SyntaxHighlighter(self.plainTextEdit.document(), settings)
        self.initAutocomplete()
        

        self._initNumberBar()
        self.hidden = {}
        self.printer = QPrinter(QPrinterInfo.defaultPrinter())
        self.plainTextEdit.setTextCursor(
            self.plainTextEdit.cursorForPosition(QPoint(0, 0)))


        self.canUndo = False
        self.canRedo = False


        self.ontologySelector.setCurrentIndex(-1)
        

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.commit)


        #Connects
        self.getWidget().textChanged.connect(self.searchCompletion)
        self.plainTextEdit.undoAvailable.connect(self.setCanUndo)
        self.plainTextEdit.redoAvailable.connect(self.setCanRedo)

        self.ontologySelector.currentIndexChanged[int].connect(
            self.showOtherOntology)
        self.plainTextEdit.textChanged.connect(self.expandIfBracketRemoved)

        self.plainTextEdit.textChanged.connect(self.setTextChanged)

        self._updateOntologySelector() #must be after connects

    
    @Slot()
    def setTextChanged(self):
        """Is called if the text changed signal is thrown and 
        sets a timer of 3 seconds to reparse the ontology. """
        self.timer.stop()
        self.timer.start(3000)
    
             

    def setCanUndo(self, b):
        self.canUndo = b
        
    def setCanRedo(self, b):
        self.canRedo = b
        

    def _print_(self):
        """ Creates a print dialog with the latest text"""
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted :
            doc = self.plainTextEdit.document()
            doc.print_(dialog.printer())
            
    def _quickPrint_(self):
        """ No dialog, just print"""
        if self.printer is None :
            return
        doc = self.plainTextEdit.document()
        doc.print_(self.printer)
        
    def _printPreview_(self):
        """ Create a print preview"""
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.plainTextEdit.print_)
        dialog.exec_()
        
    def _save_(self):
        """ Save the ontology to disk"""
        idx = self.ontologySelector.currentIndex()
        ontology = self.ontologySelector.itemData(idx)
        if ontology is None :
            return 
        if type(ontology) is Ontology :
            ontology.save()

    def getActiveOntology(self):
        idx = self.ontologySelector.currentIndex()
        return self.ontologySelector.itemData(idx)
    
    def _undo_(self):
        if self.canUndo :
            self.plainTextEdit.undo()
            self.SyntaxController.add_ontology(self.getActiveOntology(), self.plainTextEdit.toPlainText())
            self.commit()
            return 
        # RWWidget._undo_(self)
        
    def _redo_(self):
        if self.canRedo :
            self.plainTextEdit.redo()
            self.SyntaxController.add_ontology(self.getActiveOntology(), self.plainTextEdit.toPlainText())
            self.commit()
            return
        # RWWidget._redo_(self)
        
    def _initNumberBar(self):
        """ Init the number bar"""
        self.number_bar = NumberBar(self)
        self.number_bar.setMinimumSize(QSize(30, 0))
        self.number_bar.setObjectName("number_bar")
        self.gridLayout.addWidget(self.number_bar, 1, 0, 1, 1)
        self.plainTextEdit.blockCountChanged.connect(
            self.number_bar.adjustWidth)
        self.plainTextEdit.updateRequest.connect(
            self.number_bar.updateContents)

    def _updateOntologySelector(self):
        """ Update the ontology selector where you can select which Ontology to show in the editor"""
        current = self.ontologySelector.currentText()
        self.ontologySelector.currentIndexChanged[int].disconnect(self.showOtherOntology)
        self.ontologySelector.clear()
        index = -1
        count = 0
        for i in self.getIndexAbstractor().ontologies :
            if current == i.name :
                index = count
            self.ontologySelector.addItem(i.name, i)
            count = count + 1
        self.ontologySelector.setCurrentIndex(index)
        # if index == -1 :
            # the ontology was removed.
        #    self.showOtherOntology(index)
        if index == -1 :
            self.plainTextEdit.setEnabled(False)
            self.plainTextEdit.clear()
        self.ontologySelector.currentIndexChanged[int].connect(self.showOtherOntology)

    def setActiveOntology(self, ontology):
        index = -1
        count = 0
        for i in self.getIndexAbstractor().ontologies :
            if ontology.name == i.name :
                index = count
                break
            count = count + 1
        self.ontologySelector.setCurrentIndex(index)

    @Slot(int)
    def showOtherOntology(self, idx):

        """ Show other ontology in the plaintextedit
            
            Arguments:
            
            - idx: The id of the current Ontologyselector
        """
        dced = False
        try:
            self.plainTextEdit.textChanged.disconnect(self.setTextChanged)
        except RuntimeError:
            dced = True

        idx = self.ontologySelector.currentIndex()


        if idx == -1 :
            self.plainTextEdit.setEnabled(False)
            self.plainTextEdit.clear()
            return
        ontologyname = self.ontologySelector.currentText()
        for i in self.getIndexAbstractor().ontologies:
            if i.name == ontologyname:
                self.plainTextEdit.setEnabled(True)
                self.getWidget().setPlainText(
                    self.getIndexAbstractor().get_ontology_file(i).getvalue())

                if not dced:
                    self.plainTextEdit.textChanged.connect(self.setTextChanged)

                return
        self.plainTextEdit.textChanged.connect(self.commit)
        assert False

    @Slot()
    def expandIfBracketRemoved(self):
        """ Check if a line with ( or ) was changed and expand the possible hidden lines   
        """
        current_line = self.getWidget().document().findBlock(
            self.getWidget().textCursor().position()).blockNumber() + 1
        if current_line in self.hidden:
            self.toggleVisibility(current_line)

    @Slot()
    def increaseSize(self):
        """ Increase the size of the font in the TextEditor
        
        """
        doc = self.getWidget().document()
        font = doc.defaultFont()
        font.setPointSize(font.pointSize() + 1)
        font = QFont(font)
        doc.setDefaultFont(font)
        
    def _zoomIn_(self):
        """ API of Widget - see increaseSize
        This function is deprecated since pysumo 1.0 and will be merged with increaseSize
        """
        self.increaseSize()

    @Slot()
    def decreaseSize(self):
        """ Decrease the size of the font in the TextEditor"""
        doc = self.getWidget().document()
        font = doc.defaultFont()
        font.setPointSize(font.pointSize() - 1)
        font = QFont(font)
        doc.setDefaultFont(font)
        
    def _zoomOut_(self):
        """ API of Widget - see decreaseSize
            This function is deprecated since pysumo 1.0 and will be merged with decreaseSize
        """
        self.decreaseSize()

    @Slot()
    def expandAll(self):
        """ Expands all hidden code blocks"""
        for see in list(self.hidden.keys()):
            self.toggleVisibility(see)

    def _expandAll_(self):
        """ Stupid work of Kent"""
        self.expandAll()

    @Slot()
    def hideAll(self):
        """ Collapse all code blocks (where possible)"""
        block = self.getWidget().document().firstBlock()
        while block.isValid():
            if block.isVisible():
                if block.text().count("(") > block.text().count(")"):
                    self.toggleVisibility(block.blockNumber() + 1)
            block = block.next()
            
    def _collapseAll_(self):
        """ Stupid work of Kent"""
        self.hideAll()

    def _hideLines(self, lines):
        for line in lines:
            block = self.getWidget().document().findBlockByNumber(line - 1)
            assert block.isVisible()
            block.setVisible(False)
            assert not block.isVisible()

    def _showLines(self, lines):
        """ Show the lines not visible starting by lines
        
        Arguments:
        
        - lines: The first line followed by an unvisible block
        
        """
        for line in lines:
            block = self.getWidget().document().findBlockByNumber(line - 1)
            assert not block.isVisible(), "%r %r %r %r %r" % (
                line, lines, block.text(), block.isValid(), self.hidden)
            block.setVisible(True)
            assert block.isVisible(
            ), "there was an error hide/unhide line %r %r" % (line, block.text())

    def getLayoutWidget(self):
        """ Returns the layout widget"""
        return self.widget

    def numberbarPaint(self, number_bar, event):
        """Paints the line numbers of the code file"""
        self.number_bar.link = []
        font_metrics = self.getWidget().fontMetrics()
        current_line = self.getWidget().document().findBlock(
            self.getWidget().textCursor().position()).blockNumber() + 1

        block = self.getWidget().firstVisibleBlock()
        line_count = block.blockNumber()
        painter = QPainter(self.number_bar)
        # TODO: second argument is color -> to settings
        painter.fillRect(
            self.number_bar.rect(), self.getWidget().palette().base())

        # Iterate over all visible text blocks in the document.
        while block.isValid():
            line_count += 1
            text = str(line_count)
            block_top = self.getWidget().blockBoundingGeometry(
                block).translated(self.getWidget().contentOffset()).top()
            if not block.isVisible():
                block = block.next()
                while not block.isVisible():
                    line_count += 1
                    block = block.next()
                continue
            self.number_bar.link.append((block_top, line_count))
            # Check if the position of the block is out side of the visible
            # area.
            if block_top >= event.rect().bottom():
                break

            # We want the line number for the selected line to be bold.
            if line_count == current_line:
                font = painter.font()
                font.setBold(True)

            else:
                font = painter.font()
                font.setBold(False)
            # line opens a block
            if line_count in self.hidden:
                text += "+"
                font.setUnderline(True)
            elif block.text().count("(") > block.text().count(")"):
                text += "-"
                font.setUnderline(True)
            else:
                font.setUnderline(False)
            painter.setFont(font)
            # Draw the line number right justified at the position of the
            # line.
            paint_rect = QRect(
                0, block_top, self.number_bar.width(), font_metrics.height())
            painter.drawText(paint_rect, Qt.AlignLeft, text)
            block = block.next()

        painter.end()

    def initAutocomplete(self):
        """Inits the QCompleter and gives him a list of words"""
        self.completer = QCompleter(
            list(OrderedDict.fromkeys(re.split("\\W", self.plainTextEdit.toPlainText()))))
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setWidget(self.getWidget())
        self.completer.activated.connect(self.insertCompletion)

    def searchCompletion(self):
        """Searches for possible completion from QCompleter to the current text position"""
        tc = self.getWidget().textCursor()
        tc.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
        if tc.selectedText() in string.whitespace:
            self.completer.popup().hide()
            return
        tc.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)

        beginning = tc.selectedText()
        if len(beginning) >= 3:
            self.completer.setCompletionPrefix(beginning)
            self.completer.complete()
        shortcut = QShortcut(
            QKeySequence("Ctrl+Enter"), self.getWidget(), self.insertCompletion)

    def toggleVisibility(self, line):
        """ Shows or hides a line """
        if line in self.hidden:
            self._showLines(self.hidden[line])
            del self.hidden[line]
        else:
            self.hideFrom(line)

        # update views
        self.getWidget().hide()
        self.getWidget().show()
        self.number_bar.update()

    def hideFrom(self, line):
        """ Hides a block starting by line. Do nothing if not hidable"""
        block = self.getWidget().document().findBlockByNumber(
            line - 1)

        openB = block.text().count("(")
        closeB = block.text().count(")")
        startline = line
        # go to line >= line: block starts counting by 0
        block = self.getWidget().document().findBlockByNumber(line - 1)
        hidden = []
        assert block.isValid()
        while openB > closeB and block.isValid():
            assert block.isValid()
            block = block.next()
            line = block.blockNumber() + 1
            if block.isVisible():
                hidden.append(line)
            openB += block.text().count("(")
            closeB += block.text().count(")")

        if hidden == []:
            return
        self._hideLines(hidden)
        self.hidden[startline] = hidden

        # set current line in viewable area
        current_line = self.getWidget().document().findBlock(
            self.getWidget().textCursor().position()).blockNumber() + 1
        if (startline < current_line and current_line <= line):
            block = block.next()
            cursor = QTextCursor(block)
            self.getWidget().setTextCursor(cursor)

    @Slot(str)
    def insertCompletion(self, completion):
        """ Adds the completion to current text"""
        tc = self.getWidget().textCursor()
        tc.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        tc.removeSelectedText()
        tc.insertText(completion)

    def getWidget(self):
        """ Return the QPlainTextEdit Widget"""
        return self.plainTextEdit

    def commit(self):
        """ Overrides commit from RWWidget. """

        idx = self.ontologySelector.currentIndex()
        if idx == -1 :
            return
        ontology = self.ontologySelector.itemData(idx)
        if ontology is None :
            return
        self.SyntaxController.add_ontology(ontology, self.plainTextEdit.toPlainText())
        RWWidget.commit(self)
        
    @Slot()    
    def refresh(self):
        """ Refreshes the content of the TextEditor (syncing with other widgets)"""
        textCursor = self.plainTextEdit.textCursor()
        super(TextEditor, self).refresh(self)
        self.plainTextEdit.textChanged.disconnect(self.setTextChanged)
        idx = self.ontologySelector.currentIndex()
        ontology = self.ontologySelector.itemData(idx)
        if not ontology is None and type(ontology) == Ontology :
            f = self.IA.get_ontology_file(ontology)
            self.plainTextEdit.setPlainText(f.getvalue())
        self.plainTextEdit.textChanged.connect(self.setTextChanged)
        self.plainTextEdit.setTextCursor(textCursor)

class SyntaxHighlightSetting():
    """ This class contains a single Setting for a code block in the SyntaxHighlighter. 
    
    Variables:
        
        - expression: The regular expression of the syntax block
        - expression_end: If the expression has a start and an end expression
        - font_size
        - font_color
        - font_weight
        - font_style
        - font_underline
        - use_font_size
        
    
    """
    def __init__(self, expression, font_family, font_size, font_color, font_weight, font_style, font_underline, use_font_size, expression_end=''):
        self.expression = expression
        if expression_end != '':
            self.expression_end = expression_end
        self.font_family = font_family
        self.font_size = font_size
        self.font_color = font_color
        self.font_weight = font_weight
        self.font_style = font_style
        self.font_underline = font_underline
        self.use_font_size = use_font_size
        self.createFormat()

    def createFormat(self):
        """ Create a QTextCharformat and saves it in self.class_format"""
        self.class_format = QTextCharFormat()
        self.class_format.setFontFamily(self.font_family)
        if self.use_font_size :
            self.class_format.setFontPointSize(self.font_size)
        self.class_format.setForeground(self.font_color)
        self.class_format.setFontWeight(self.font_weight)
        self.class_format.setFontItalic(self.font_style)
        self.class_format.setFontUnderline(self.font_underline)

    def get_format(self):
        return self.class_format

    def getValues(self):
        return [self.expression, self.font_color, self.font_weight]

    def serialize(self):
        str1 = ""
        str1 += self.expression + "//"
        str1 += str(self.font_color) + "//"
        str1 += str(self.font_weight) + "//"
        return str1

    def deserialize(self, string):
        splitted = string.split("//")
        self.expression = splitted[0]
        self.font_color = splitted[1]
        self.font_weight = splitted[2]


class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, document, settings):
        super(SyntaxHighlighter, self).__init__(document)
        self.settings = settings
        use_font_size = self.settings.value("useHighlightingFontSize")
        use_font_size = str_to_bool(use_font_size)
        self.singleline = []
        # logical expressions highlighting
        regex = "(and|=>|not|or)(?!\w)"
        fFamily = self._getFontFamily("logicExprFontFamily")
        fSize = self._getFontSize("logicExprFontSize")
        fColor = self._getFontColor("logicExprFontColor")
        fWeight = self._getFontWeight("logicExprBoldStyle")
        fItalic = self._getFontItalic("logicExprItalicStyle")
        fUnderline = self._getFontUnderline("logicExprUnderlinedStyle")
        shSettings = SyntaxHighlightSetting(regex, fFamily, fSize, fColor, fWeight, fItalic, fUnderline, use_font_size)
        self.singleline.append(shSettings)

        # keywords highlighting
        regex = "(member|patient|agent|instance|subclass|exists|documentation|part|domain|equal|hasPurpose)[\W'\n']"
        fFamily = self._getFontFamily("keywordsFontFamily")
        fSize = self._getFontSize("keywordsFontSize")
        fColor = self._getFontColor("keywordsFontColor")
        fWeight = self._getFontWeight("keywordsBoldStyle")
        fItalic = self._getFontItalic("keywordsItalicStyle")
        fUnderline = self._getFontUnderline("keywordsUnderlinedStyle")
        shSettings = SyntaxHighlightSetting(regex, fFamily, fSize, fColor, fWeight, fItalic, fUnderline, use_font_size)
        self.singleline.append(shSettings)
        
        # comment highlighting
        regex = ";.*$"
        fFamily = self._getFontFamily("commentFontFamily")
        fSize = self._getFontSize("commentFontSize")
        fColor = self._getFontColor("commentFontColor")
        fWeight = self._getFontWeight("commentBoldStyle")
        fItalic = self._getFontItalic("commentItalicStyle")
        fUnderline = self._getFontUnderline("commentUnderlinedStyle")
        shSettings = SyntaxHighlightSetting(regex, fFamily, fSize, fColor, fWeight, fItalic, fUnderline, use_font_size)
        self.singleline.append(shSettings)

        self.multiline = []
        
        # strings highlighting
        fFamily = self._getFontFamily("stringsFontFamily")
        fSize = self._getFontSize("stringsFontSize")
        fColor = self._getFontColor("stringsFontColor")
        fWeight = self._getFontWeight("stringsBoldStyle")
        fItalic = self._getFontItalic("stringsItalicStyle")
        fUnderline = self._getFontUnderline("stringsUnderlinedStyle")
        shSettings = SyntaxHighlightSetting('"', fFamily, fSize, fColor, fWeight, fItalic, fUnderline, use_font_size, expression_end='"')
        self.multiline.append(shSettings)
        
    def _getFontFamily(self, propKey):
        fFamily = self.settings.value(propKey)
        return fFamily
    
    def _getFontSize(self, propKey):
        fSize = self.settings.value(propKey)
        return int(fSize)
    
    def _getFontColor(self, propKey):
        fColor = self.settings.value(propKey)
        return QColor(fColor)
    
    def _getFontItalic(self, propKey):
        fStyle = self.settings.value(propKey)
        return str_to_bool(fStyle)
    
    def _getFontUnderline(self, propKey):
        fUnderlined = self.settings.value(propKey)
        return str_to_bool(fUnderlined)
        
    def _getFontWeight(self, propKey):
        fWeight = self.settings.value(propKey)
        fWeight = str_to_bool(fWeight)
        if fWeight :
            fWeight = QFont.Bold
        else :
            fWeight = QFont.Normal
        return fWeight

    def highlightBlock(self, text):
        for h in self.singleline:
            expression = QRegExp(h.expression)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, h.get_format())
                index = expression.indexIn(text, index + length)

        for h in self.multiline:
            startIndex = 0
            self.setCurrentBlockState(0)
            expression = QRegExp(h.expression)
            expression_end = QRegExp(h.expression_end)

            if(self.previousBlockState() != 1):
                startIndex = expression.indexIn(text)

            while startIndex >= 0:
                endIndex = expression_end.indexIn(text, startIndex + 1)
                if endIndex == -1:
                    self.setCurrentBlockState(1)
                    commentLength = len(text) - startIndex
                else:
                    commentLength = endIndex - startIndex + \
                        expression_end.matchedLength()
                self.setFormat(startIndex, commentLength, h.get_format())
                startIndex = expression.indexIn(
                    text, startIndex + commentLength)


class NumberBar(QWidget):
    """ 
    A widget for the numberbar on the left of QPlainTextEdit
    """
    def __init__(self, edit):
        QWidget.__init__(self, edit.getWidget())
        self.edit = edit
        self.adjustWidth(100)
        self.link = []

    def paintEvent(self, event):
        self.edit.numberbarPaint(self, event)
        QWidget.paintEvent(self, event)

    def adjustWidth(self, count):
        width = self.fontMetrics().width(str(count) + "+")
        if self.width() != width:
            self.setFixedWidth(width)

    def updateContents(self, rect, scroll):
        if scroll:
            self.scroll(0, scroll)
        else:
            # It would be nice to do
            # self.update(0, rect.y(), self.width(), rect.height())
            # But we can't because it will not remove the bold on the
            # current line if word wrap is enabled and a new block is
            # selected.
            self.update()

    def mouseDoubleClickEvent(self, event):
        """Hides the lines from the line clicked on. """
        for (height, line) in self.link:
            if height >= event.y():
                break
            last = line
        assert self.edit.getWidget().document().findBlockByNumber(
            last - 1).isVisible()
        self.edit.toggleVisibility(last)
