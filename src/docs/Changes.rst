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
