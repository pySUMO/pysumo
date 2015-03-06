Changes
======================


pysumo
======
* Rename lib to pysumo.

IndexAbstractor
---------------
* Delete DotGraph.
* Make root and depth keyword arguments defaulting to None
* Turn index into a simple dict. Makes index access easier and faster.
* Add init_wordnet() to initialize the WordNet mapping
* Add update_index() to build the index
* wordnet_locate() returns a list of strings
* IA now also stores the root AST node and a list of ontologies
* Change get_graph arguments to allow for more complex matching.
* Add normalize method for normalizing string arguments.
* Add function to return list of possible completions.

AbstractGraph
^^^^^^^^^^^^^
* Change init to reflect new get_graph API.
* Change variant to String from Enum and root to String from AbstractGraphNode
* Add info argument to __init__. Allows passing the Index/List of Ontologies

WordNet
-------
* change argument of wparse() from a mapping file to a directory containing the mapping files and the rest of the wordnet database - avoid merging mapping files
* completely get rid of all dependencies on NLToolkit - extending upon it is a nightmare
* locate_term() returns a tuple of String, SSType, String

SyntaxControler
---------------
* Add an optional argument newversion to add_ontology()
* Remove parse_graph(), the user now has to edit the file self
* Remove parse_add(), we can use add_ontology() now
* Moved Ontology to syntaxcontroler module

Logger
======

ActionLog
---------
* Add name argument to init.
* undo/redo now return self.current.
* Make ActionLog work with objects that provide a buffer interface via the getbuffer() function.
* Add functions for pop and clear.

LogIO
^^^^^
* Add default_path variable.

InfoLog
-------
* Add socket interface for StatusBar
* Add default_{log_path,socket_path} variables.
* init now receives a string detailing the loglevel instead of an int.

pySUMOQt
========
* Rename ui to pySUMOQt.

TextEditor
----------
* remove show autocomplete – Qt does this on its own
* Added
	* setTextChanged()
	* _initNumberBar()
	* _updateOntologySelector()
	* _hideLines(lines)
	* _showLines(lines)
	* _zoomOut_()
	* _zoomIn_()
	* showOtherOntology(ontologyname)
	* expandIfBracketRemoved()
	* increaseSize()
	* decreaseSize()
	* expandAll()
	* hideAll()
	* getLayoutWidget()
	* numberbarPaint(number_bar, event)
	* initAutocomplete()
	* searchCompletion()
	* toggleVisibility(line)
	* hideFrom(line)
	* insertCompletion(completion)
	* commit()

Introduce SyntaxHighlightSetting to handle user defined Syntax Highlight Rules

class SyntaxHighlightSetting()
__init__( expression, font_weight, font_color, expression_end='')
createFormat()
get_format()
getValues()
serialize()
deserialize( string)


Introduce class SyntaxHighlighter
class SyntaxHighlighter
__init__( document)
highlightBlock( text)

Introduce Numberbar because Qt does not do this on his own
class NumberBar(QWidget)
__init__( edit)
paintEvent( event)
adjustWidth( count)
updateContents( rect, scroll)
mouseDoubleClickEvent( event)

GraphWidget
-----------
Komplette Änderung der API, um an pygraphviz anzupassen

MainWindow
----------

* Added 
	* _showOptionDialog_()
	* _addWidget_(widgetType, widgetMenu)
	* createPySumoWidget(widgetType, widgetMenu)
	* addDeleteWidgetAction(widget)
	* addOrRestoreWidget(widget, menu, directAdd=False)
	* closeEvent(event)
	* createStatusBar()
	* setupStatusConnection()
	* displayLog(socket)
	* _updateStatusbar_(wrappedWidget=None)
	* _deleteWidget_(widget)
	* connectWidget(widget)
	* disconnectWidget(widget, callback=None)
	* getDefaultOutputPath()
	* _newOntology_()
	* _openLocalOntology_()
	* _openRemoteOntology_()
	* addOntology(ontology, newversion=None)
	* notifyOntologyAdded(ontology)
	* _ClearRecentOntologiesHistory_()
	* _deleteOntology_(ontology)
	* _updateOntology_(ontology)
	* _revertOntology_(ontology)
	* _showOntologyProperties_(ontology)
	* _closeOntology(ontology)
	
* Added quit_handler(signum, frame) to capture SIGINT signal.

* Introduced class PySUMOWidget which wrappes the application widgets.

* Removed class Statusbar, it became useless towards createStatusBar in MainWindow.

* Removed class Menubar, because the menu bar is already created by the designer.

* Removed class Toolbar, because the tool bar is already created by the designer.

* Moved class HelpDialog to module Dialog

Settings
--------

* Introduced class LayoutManager.

* Introduced class PySumoSettings.

* Removed class PluginManager.

* Removed class WSettings.

* Moved class OptionDialog to module Dialog.

OptionDialog
------------

* Remove createView() and load(path) methods.

* Added other methods to the OptionDialog.

