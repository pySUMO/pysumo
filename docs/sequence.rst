Sequence diagram
================

Adding graph node
------------------
.. uml::
   !include ./UML/graph_node_add.iuml

This diagram displays how the GraphWidget responds to user input and adds new
nodes to the Ontology. Note that all operations that might change the Ontology
pass through the SyntaxController and all operations that read from the loaded
Ontologies pass through the IndexAbstractor.

Searching in the index
----------------------
.. uml::
   !include ./UML/search.iuml

This diagram displays a simple abstraction of how the DocumentationWidget
responds to a user search request. Note that it does not include any
IndexAbstractor internal operations such as building and maintaining the Index.

Activity diagram
================
Graph widget input loop
-----------------------
.. uml::
   :scale: 80%

   !include ./UML/graphactivity.iuml

This diagram displays the activity diagram used by the GraphWidget when a user
adds a node to the graph. Of special note is that the parsing of the new graph
is done in the background so that the user can still interact with the
GraphWidget while it is updating the Ontology.

Text editor input loop
----------------------
.. uml::
   !include ./UML/textactivity.iuml

This diagram displays the activity diagram used by the TextWidget while the
user is typing. Once the user pauses typing, the text editor checks whether the
parenthetical syntax is correct, and if it passes a simple syntax check, the
text is passed to the parser. The parser then checks syntax and semantics and
returns accordingly. If errors occur during parsing, they are displayed in the
editor.

Common workflow
------------------
.. uml::
   :scale: 90%

   !include ./UML/activity_1.iuml

This diagram displays an abstract view of a common User-interaction with the
program. The user starts the program adds a .kif-File, searches in WordNet
and finally adds a relation through the GraphWidget. PySUMO automatically
converts the relation to kif and appends it to the ontology source.

Exit process
------------
.. uml::
   !include ./UML/activity_2.iuml

This diagram displays an abstract view of the activity diagram when a user
wants to exit the program. This is done when the user clicks on the close icon
in the title bar of the main window of pySUMO or on 'Exit' in the menu 'File'.
The program makes sure that there are no unsaved changes in open ontologies and
if there are changes, prompts if they should be saved. If the user doesn't save
them, the modifications will be lost. Note that the program also saves session
layouting preferences of the GUI so they can be restored in the next pySUMO
session.  These preferences include, for example, the position of widgets in
the main window.
